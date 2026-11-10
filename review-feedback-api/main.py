"""Small shared feedback API for ATA 1.4.4 public review pages.

두 창구가 같은 저장소를 쓴다.
  - 오디오 점검(`audio-review144.html`) — needed/reason/checked
  - 수업 중 수정 신고(`ata144_teacher.html`) — target/reason/confirm1/confirm2/done

기록은 항목 하나당 JSON 하나이고, 신고·확인·처리는 history에 덧붙여 쌓는다.
1.5 어드민 피드백(대상·작성자·시간·당시 본문·이력)과 같은 모양으로 받아 두어,
나중에 어드민으로 옮길 때 그대로 들어가게 한다.
"""

from __future__ import annotations

import base64
import hmac
import json
import os
import re
from datetime import datetime, timezone

from flask import Flask, jsonify, make_response, request
from google.api_core.exceptions import NotFound, PreconditionFailed
from google.cloud import storage


app = Flask(__name__)
storage_client = storage.Client()

BUCKET_NAME = os.environ.get("FEEDBACK_BUCKET", "all-that-arabic-14")
REVIEW_TOKEN = os.environ.get("REVIEW_TOKEN", "")
ALLOWED_ORIGINS = {
    origin.strip()
    for origin in os.environ.get(
        "ALLOWED_ORIGINS",
        "https://rasheedpark.github.io,http://localhost:7744",
    ).split(",")
    if origin.strip()
}
REVIEW_RE = re.compile(r"^[a-z0-9][a-z0-9-]{0,63}$")
# `A05/ptn:ptn060_...` 처럼 과/종류:행id 꼴. 공백만 막고 나머지는 열어 둔다
# (행 id에 `/`가 들어가는 탭이 있다).
ITEM_RE = re.compile(r"^A\d{2}/[^\s]{1,220}$")
TARGETS = {"", "content", "audio", "both"}
HISTORY_MAX = 40
SNAPSHOT_FIELDS = ("unit", "type", "arabic", "korean", "note", "id")


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def authorized() -> bool:
    supplied = request.args.get("key", "") or request.headers.get("X-Review-Key", "")
    return bool(REVIEW_TOKEN) and hmac.compare_digest(supplied, REVIEW_TOKEN)


def error(message: str, status: int):
    return jsonify({"ok": False, "error": message}), status


def validate_review(value: object) -> str | None:
    review = str(value or "").strip().lower()
    return review if REVIEW_RE.fullmatch(review) else None


def object_name(review: str, item_key: str) -> str:
    encoded = base64.urlsafe_b64encode(item_key.encode("utf-8")).decode("ascii").rstrip("=")
    return f"review-feedback/1.4.4/{review}/items/{encoded}.json"


def add_cors(response):
    origin = request.headers.get("Origin", "")
    if origin in ALLOWED_ORIGINS:
        response.headers["Access-Control-Allow-Origin"] = origin
        response.headers["Vary"] = "Origin"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, X-Review-Key"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    response.headers["Cache-Control"] = "no-store"
    return response


@app.after_request
def after_request(response):
    return add_cors(response)


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"ok": True, "service": "ata144-review-feedback"})


@app.route("/feedback", methods=["OPTIONS"])
def feedback_options():
    return make_response("", 204)


@app.route("/feedback", methods=["GET"])
def feedback_list():
    if not authorized():
        return error("unauthorized", 401)
    review = validate_review(request.args.get("review"))
    if not review:
        return error("invalid review", 400)

    prefix = f"review-feedback/1.4.4/{review}/items/"
    records: dict[str, dict] = {}
    for blob in storage_client.list_blobs(BUCKET_NAME, prefix=prefix):
        try:
            record = json.loads(blob.download_as_text(encoding="utf-8"))
        except (ValueError, TypeError):
            continue
        item_key = str(record.get("itemKey", ""))
        if item_key:
            records[item_key] = record
    return jsonify({"ok": True, "review": review, "items": records})


def read_existing(blob) -> tuple[dict, int]:
    """현재 기록과 generation을 함께 돌려준다 (덮어쓰기 충돌 방지용).

    generation 0은 "아직 없음"이고, if_generation_match=0은 새로 만들 때만 통과한다.
    """
    try:
        blob.reload()
    except NotFound:
        return {}, 0
    generation = int(blob.generation or 0)
    try:
        return json.loads(blob.download_as_text(encoding="utf-8")) or {}, generation
    except (ValueError, TypeError, NotFound):
        return {}, generation


def confirmation(payload_value: object, previous: object, reviewer: str) -> dict:
    """확인1·확인2 칸. payload에 값이 없으면 이전 상태를 그대로 둔다."""
    if payload_value is None:
        return previous if isinstance(previous, dict) else {"active": False}
    if not bool(payload_value):
        return {"active": False}
    return {"active": True, "reviewer": reviewer, "at": utc_now()}


def is_empty(record: dict) -> bool:
    """아무 흔적도 없으면 기록을 지운다."""
    return not (
        record.get("needed")
        or str(record.get("reason", "")).strip()
        or record.get("checked")
        or record.get("target")
        or record.get("done")
        or (record.get("confirm1") or {}).get("active")
        or (record.get("confirm2") or {}).get("active")
    )


@app.route("/feedback", methods=["POST"])
def feedback_save():
    if not authorized():
        return error("unauthorized", 401)
    payload = request.get_json(silent=True) or {}
    review = validate_review(payload.get("review"))
    item_key = str(payload.get("itemKey", "")).strip()
    if not review:
        return error("invalid review", 400)
    if not ITEM_RE.fullmatch(item_key):
        return error("invalid itemKey", 400)

    target = str(payload.get("target", "") or "").strip().lower()
    if target not in TARGETS:
        return error("invalid target", 400)
    reason = str(payload.get("reason", "")).strip()
    reviewer = str(payload.get("reviewer", "") or "").strip()[:80] or "Merna"
    if len(reason) > 2000:
        return error("reason too long", 400)

    bucket = storage_client.bucket(BUCKET_NAME)
    blob = bucket.blob(object_name(review, item_key))

    for attempt in (0, 1):
        previous, generation = read_existing(blob)
        now = utc_now()

        # 신고 본문 — payload에 그 칸이 들어 있으면 그 값으로 갈아 끼우고(오디오 점검
        # 페이지는 needed·reason을 항상 보내므로 끄는 것도 그대로 전달된다), 확인·처리만
        # 누른 요청처럼 칸이 아예 없으면 이전 값을 지킨다.
        sent_report = any(field in payload for field in ("target", "reason", "needed"))
        if sent_report:
            new_target, new_reason = target, reason
            new_needed = bool(payload.get("needed", bool(target) or bool(reason)))
        else:
            new_target = str(previous.get("target", "") or "")
            new_reason = str(previous.get("reason", "") or "")
            new_needed = bool(previous.get("needed"))
        reported = sent_report and (bool(new_target) or bool(new_reason) or new_needed)

        record = {
            "review": review,
            "itemKey": item_key,
            "target": new_target,
            "reason": new_reason,
            "needed": new_needed,
            "checked": bool(payload.get("checked"))
            if payload.get("checked") is not None
            else bool(previous.get("checked")),
            # reviewer는 「마지막으로 손댄 사람」, reportedBy는 「신고한 사람」이다.
            # 내가 처리됨을 눌러도 신고자가 바뀌면 안 된다.
            "reviewer": reviewer,
            "reportedBy": reviewer
            if reported
            else (str(previous.get("reportedBy", "") or "") if not sent_report else ""),
            "firstReportedAt": (previous.get("firstReportedAt") or (now if reported else ""))
            if (reported or not sent_report)
            else "",
            "updatedAt": now,
            "reportedAt": now
            if reported
            else (str(previous.get("reportedAt", "") or "") if not sent_report else ""),
        }

        # 당시 본문 — 신고가 새로 들어올 때만 새로 찍는다.
        snapshot = payload.get("snapshot")
        if reported and isinstance(snapshot, dict):
            record["snapshot"] = {
                field: str(snapshot.get(field, "") or "")[:600] for field in SNAPSHOT_FIELDS
            }
        elif previous.get("snapshot"):
            record["snapshot"] = previous["snapshot"]

        record["confirm1"] = confirmation(
            payload.get("confirm1"), previous.get("confirm1"), reviewer
        )
        record["confirm2"] = confirmation(
            payload.get("confirm2"), previous.get("confirm2"), reviewer
        )

        # 처리 완료 — 내가 시트에 반영했다는 표시.
        if payload.get("done") is None:
            record["done"] = bool(previous.get("done"))
            record["doneAt"] = str(previous.get("doneAt", "") or "")
        elif bool(payload.get("done")):
            record["done"] = True
            record["doneAt"] = now
        else:
            record["done"] = False
            record["doneAt"] = ""

        # 이력 — 덧붙여 쌓는다.
        history = previous.get("history")
        history = list(history) if isinstance(history, list) else []
        entries = []
        was_reported = bool(previous.get("needed")) or bool(previous.get("target")) or bool(
            str(previous.get("reason", "") or "").strip()
        )
        if reported:
            entries.append(
                {"action": "report", "target": record["target"], "reason": record["reason"]}
            )
        elif sent_report and was_reported:
            entries.append({"action": "clear"})
        for slot in ("confirm1", "confirm2"):
            was = bool((previous.get(slot) or {}).get("active"))
            now_active = bool(record[slot].get("active"))
            if was != now_active:
                entries.append({"action": slot if now_active else slot + "_off"})
        if bool(previous.get("done")) != record["done"]:
            entries.append({"action": "done" if record["done"] else "done_off"})
        if payload.get("checked") is not None and bool(previous.get("checked")) != record["checked"]:
            entries.append({"action": "checked" if record["checked"] else "checked_off"})
        for entry in entries:
            entry.update({"at": now, "reviewer": reviewer})
            history.append(entry)
        record["history"] = history[-HISTORY_MAX:]

        if is_empty(record):
            try:
                blob.delete()
            except Exception as exc:
                if getattr(exc, "code", None) != 404:
                    raise
            return jsonify({"ok": True, "deleted": True, "itemKey": item_key})

        blob.cache_control = "no-store"
        try:
            blob.upload_from_string(
                json.dumps(record, ensure_ascii=False, separators=(",", ":")),
                content_type="application/json; charset=utf-8",
                if_generation_match=generation,
            )
        except PreconditionFailed:
            if attempt == 0:
                continue  # 다른 사람이 먼저 썼다 — 다시 읽어 합친다
            return error("conflict", 409)
        return jsonify({"ok": True, "item": record})

    return error("conflict", 409)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "8080")))
