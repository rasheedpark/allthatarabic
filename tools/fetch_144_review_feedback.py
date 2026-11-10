#!/usr/bin/env python3
"""ATA 1.4.4 신고를 받아 본다.

두 묶음이 있다.
  --review a21-a35  오디오 점검(음원 재제작 요청)
  --review class144 수업 중 수정 신고 — 교재 화면의 신고 버튼이 보내는 것
본문 수정은 ATA-1.4.4 시트에서 한다. 이 스크립트는 읽기만 한다.
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import urlopen


ROOT = Path(__file__).resolve().parents[1]
LOCAL_ENV = ROOT / ".review-feedback-144.env"


def load_local_env() -> None:
    if not LOCAL_ENV.exists():
        return
    for raw_line in LOCAL_ENV.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip())


def main() -> int:
    load_local_env()
    parser = argparse.ArgumentParser()
    parser.add_argument("--review", default="class144", help="신고 묶음 (class144 | a21-a35)")
    parser.add_argument("--all", action="store_true", help="처리된 것까지 전부")
    parser.add_argument("--target", choices=["content", "audio", "both"], help="대상으로 거르기")
    parser.add_argument("--unit", help="과로 거르기 (예: A05)")
    parser.add_argument("--json", action="store_true", help="원본 JSON 그대로")
    args = parser.parse_args()

    api = os.environ.get("ATA144_REVIEW_API", "").rstrip("/")
    key = os.environ.get("ATA144_REVIEW_KEY", "")
    if not api or not key:
        raise SystemExit(f"Missing ATA144_REVIEW_API/ATA144_REVIEW_KEY in {LOCAL_ENV}")

    query = urlencode({"review": args.review, "key": key})
    with urlopen(f"{api}/feedback?{query}", timeout=20) as response:
        payload = json.load(response)
    records = list(payload.get("items", {}).values())
    records.sort(key=lambda item: item.get("itemKey", ""))
    if not args.all:
        # 신고가 있고 아직 시트에 반영하지 않은 것만
        records = [
            item
            for item in records
            if (item.get("needed") or item.get("target") or (item.get("reason") or "").strip())
            and not item.get("done")
        ]
    if args.target:
        wanted = {args.target, "both"} if args.target != "both" else {"both"}
        records = [item for item in records if (item.get("target") or "content") in wanted]
    if args.unit:
        records = [item for item in records if str(item.get("itemKey", "")).startswith(args.unit + "/")]

    if args.json:
        print(json.dumps(records, ensure_ascii=False, indent=2))
        return 0

    if not records:
        print("신고 없음")
        return 0

    target_ko = {"content": "내용", "audio": "음원", "both": "내용+음원", "": "내용"}
    # 종류 → 시트 탭. 어느 탭에서 고치면 되는지 바로 보이게 한다.
    type_tab = {
        "unit": "units", "ptn": "pattern", "repertory": "repertory",
        "drilla": "drill", "drillb": "drill", "drillc": "drill", "writing": "drill",
        "exp": "expression", "kalimat": "kalimat", "nass": "nass", "jadwal": "appendix",
    }
    for index, item in enumerate(records, 1):
        item_key = str(item.get("itemKey", ""))
        unit, _, rest = item_key.partition("/")
        kind, _, row_id = rest.partition(":")
        mark = " [처리됨]" if item.get("done") else ""
        who = item.get("reportedBy") or item.get("reviewer", "")
        print(f"{index}. {unit} · {target_ko.get(item.get('target') or '', '내용')}{mark} — {who}")
        print(f"   사유: {item.get('reason') or '사유 미입력'}")
        print(f"   시트: {type_tab.get(kind, kind)} 탭 · {row_id or item_key}")
        snapshot = item.get("snapshot") or {}
        if snapshot.get("arabic"):
            print("   당시: " + " / ".join(snapshot["arabic"].split())[:80])
        confirms = [
            label for slot, label in (("confirm1", "확인1"), ("confirm2", "확인2"))
            if (item.get(slot) or {}).get("active")
        ]
        print(f"   시각: {item.get('reportedAt') or item.get('updatedAt', '')}"
              + (f" · {' '.join(confirms)}" if confirms else ""))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
