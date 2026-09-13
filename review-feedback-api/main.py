"""Small shared feedback API for ATA public audio review pages."""

from __future__ import annotations

import base64
import hmac
import json
import os
import re
from datetime import datetime, timezone

from flask import Flask, jsonify, make_response, request
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
ITEM_RE = re.compile(r"^A\d{2}/[^/\s]{1,180}$")


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
    bucket = storage_client.bucket(BUCKET_NAME)
    for blob in storage_client.list_blobs(BUCKET_NAME, prefix=prefix):
        try:
            record = json.loads(blob.download_as_text(encoding="utf-8"))
        except (ValueError, TypeError):
            continue
        item_key = str(record.get("itemKey", ""))
        if item_key:
            records[item_key] = record
    return jsonify({"ok": True, "review": review, "items": records})


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

    reason = str(payload.get("reason", "")).strip()
    reviewer = str(payload.get("reviewer", "Merna")).strip()[:80] or "Merna"
    if len(reason) > 2000:
        return error("reason too long", 400)

    record = {
        "review": review,
        "itemKey": item_key,
        "needed": bool(payload.get("needed")),
        "reason": reason,
        "checked": bool(payload.get("checked")),
        "reviewer": reviewer,
        "updatedAt": utc_now(),
    }
    bucket = storage_client.bucket(BUCKET_NAME)
    blob = bucket.blob(object_name(review, item_key))
    if not record["needed"] and not record["reason"] and not record["checked"]:
        try:
            blob.delete()
        except Exception as exc:
            if getattr(exc, "code", None) != 404:
                raise
        return jsonify({"ok": True, "deleted": True, "itemKey": item_key})
    blob.cache_control = "no-store"
    blob.upload_from_string(
        json.dumps(record, ensure_ascii=False, separators=(",", ":")),
        content_type="application/json; charset=utf-8",
    )
    return jsonify({"ok": True, "item": record})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "8080")))
