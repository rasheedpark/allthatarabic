#!/usr/bin/env python3
"""Build a local ATA 1.4.4 nass review manifest from the live sheet."""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
GENERATOR_PATH = PROJECT_ROOT / "archive/ata-audio-pipeline/generate_144_nass_elevenlabs.py"


def load_generator():
    spec = importlib.util.spec_from_file_location("ata144_nass_generator", GENERATOR_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load {GENERATOR_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def dialect_rank(value: str) -> int:
    dialect = value.strip().upper()
    if dialect == "MSA":
        return 0
    if dialect in {"GLF", "GULF", "UAE", "KSA"}:
        return 1
    return 2


def unit_number(value: str) -> int:
    digits = "".join(character for character in value if character.isdigit())
    return int(digits or 0)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--unit", action="append", required=True)
    parser.add_argument("--audio-root", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--title", default="ATA 1.4.4 지문 듣기 통합 검수")
    parser.add_argument(
        "--audio-url-base",
        default="",
        help="optional public URL prefix; unit and filename are appended",
    )
    args = parser.parse_args()

    generator = load_generator()
    units = {generator.normalize_unit(unit) for unit in args.unit}
    rows = generator.collect_rows(units, set())
    rows.sort(
        key=lambda row: (
            unit_number(row["_unit"]),
            dialect_rank(generator.row_value(row, "lahja")),
            int(row.get("_row_number") or 0),
        )
    )

    audio_root = Path(args.audio_root)
    output_path = Path(args.output)
    if not output_path.is_absolute():
        output_path = PROJECT_ROOT / output_path

    items = []
    missing = []
    for row in rows:
        unit = row["_unit"]
        item_id = row["_id"]
        audio_path = audio_root / unit / f"{item_id}.mp3"
        absolute_audio_path = audio_path if audio_path.is_absolute() else PROJECT_ROOT / audio_path
        generated = absolute_audio_path.exists()
        if not generated:
            missing.append(f"{unit}/{item_id}")
        version = absolute_audio_path.stat().st_mtime_ns if generated else 0
        if args.audio_url_base:
            audio_url = f"{args.audio_url_base.rstrip('/')}/{unit}/{item_id}.mp3?v={version}"
        else:
            audio_url = f"{audio_path.as_posix()}?v={version}"
        items.append(
            {
                "id": item_id,
                "unit": unit,
                "pattern": generator.row_value(row, "ref_unit", "id_pattern"),
                "status": "confirmed",
                "lahja": generator.row_value(row, "lahja"),
                "speakers": [
                    generator.row_value(row, "speaker1"),
                    generator.row_value(row, "speaker2"),
                ],
                "arabic": generator.row_value(row, "arabic"),
                "tss": generator.select_tts_text(row),
                "korean": generator.row_value(row, "korean"),
                "note": generator.row_value(row, "note"),
                "audio": audio_url,
                "voices": [],
                "generated": generated,
            }
        )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps({"title": args.title, "items": items}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"output={output_path}")
    print(f"items={len(items)} missing={len(missing)}")
    for item in missing:
        print(f"MISSING {item}")
    return 1 if missing else 0


if __name__ == "__main__":
    raise SystemExit(main())
