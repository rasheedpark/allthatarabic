#!/usr/bin/env python3
"""Fetch shared ATA 1.4.4 audio-review feedback for regeneration work."""

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
    parser.add_argument("--review", default="a21-a35")
    parser.add_argument("--all", action="store_true", help="include non-remake records")
    parser.add_argument("--json", action="store_true", help="print raw JSON")
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
        records = [item for item in records if item.get("needed")]

    if args.json:
        print(json.dumps(records, ensure_ascii=False, indent=2))
        return 0

    if not records:
        print("재제작 요청 없음")
        return 0
    for index, item in enumerate(records, 1):
        print(f"{index}. {item.get('itemKey')} · {item.get('reviewer', '')}")
        print(f"   사유: {item.get('reason') or '사유 미입력'}")
        print(f"   수정: {item.get('updatedAt', '')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
