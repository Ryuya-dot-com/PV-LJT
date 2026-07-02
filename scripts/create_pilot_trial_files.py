#!/usr/bin/env python3
"""Create practice-plus-main trial files for the PV-LJT pilot."""

from __future__ import annotations

import csv
import random
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MATERIALS = ROOT / "materials"

LJT_LISTS = {
    "A": MATERIALS / "aural_pv_ljt_list_A_v4_pre_audio.tsv",
    "B": MATERIALS / "aural_pv_ljt_list_B_v4_pre_audio.tsv",
}
LJT_PRACTICE = MATERIALS / "ljt_practice_items_v1.tsv"
GENERAL_PRACTICE = MATERIALS / "practice_items_v1.tsv"
AUDIO_DECISION = MATERIALS / "audio_pv_decision_items_v2_mixed_foils.tsv"
ORTHOGRAPHIC = MATERIALS / "orthographic_pv_meaning_recognition_v2_balanced.tsv"
LJT_RECORDING = MATERIALS / "audio_recording_script_ljt_v4_pre_audio.tsv"
AUDIO_DECISION_RECORDING = MATERIALS / "audio_recording_script_audio_decision_v2.tsv"
PRACTICE_RECORDING = MATERIALS / "audio_recording_script_practice_v1.tsv"

OUT_LJT_A = MATERIALS / "pilot_trial_file_ljt_list_A_v1.tsv"
OUT_LJT_B = MATERIALS / "pilot_trial_file_ljt_list_B_v1.tsv"
OUT_AUDIO_DECISION = MATERIALS / "pilot_trial_file_audio_decision_v1.tsv"
OUT_ORTHOGRAPHIC = MATERIALS / "pilot_trial_file_orthographic_recognition_v1.tsv"

SEED_AUDIO_DECISION = 20260628
SEED_ORTHOGRAPHIC = 20260629


def read_tsv(path: Path) -> tuple[list[dict[str, str]], list[str]]:
    with path.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f, delimiter="\t")
        return list(reader), list(reader.fieldnames or [])


def write_tsv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, delimiter="\t", extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def recording_map(path: Path, key_field: str) -> dict[str, str]:
    rows, _ = read_tsv(path)
    return {row[key_field]: row["audio_file_name"] for row in rows}


def make_ljt_trial_file(list_id: str, out_path: Path) -> None:
    practice_rows, _ = read_tsv(LJT_PRACTICE)
    main_rows, _ = read_tsv(LJT_LISTS[list_id])
    main_audio = recording_map(LJT_RECORDING, "item_id")
    practice_audio = recording_map(PRACTICE_RECORDING, "practice_id")

    fields = [
        "trial_order",
        "phase",
        "task",
        "list_id",
        "item_id",
        "pv_id",
        "pv",
        "condition",
        "expected_response",
        "stimulus_text",
        "target_form",
        "audio_file_name",
        "notes",
    ]
    out_rows = []
    order = 1
    for row in practice_rows:
        out_rows.append(
            {
                "trial_order": str(order),
                "phase": "practice",
                "task": "aural_pv_ljt",
                "list_id": list_id,
                "item_id": row["practice_id"],
                "pv_id": "",
                "pv": row["pv"],
                "condition": row["condition"],
                "expected_response": row["expected_response"],
                "stimulus_text": row["sentence_text"],
                "target_form": row["target_form"],
                "audio_file_name": practice_audio.get(row["practice_id"], ""),
                "notes": row["notes"],
            }
        )
        order += 1
    for row in main_rows:
        out_rows.append(
            {
                "trial_order": str(order),
                "phase": "main",
                "task": "aural_pv_ljt",
                "list_id": list_id,
                "item_id": row["ljt_item_id"],
                "pv_id": row["pv_id"],
                "pv": row["pv"],
                "condition": row["condition"],
                "expected_response": row["expected_response"],
                "stimulus_text": row["sentence_text"],
                "target_form": row["target_form"],
                "audio_file_name": main_audio[row["ljt_item_id"]],
                "notes": row["notes"],
            }
        )
        order += 1
    write_tsv(out_path, out_rows, fields)


def make_audio_decision_trial_file() -> None:
    practice_rows, _ = read_tsv(GENERAL_PRACTICE)
    practice_rows = [row for row in practice_rows if row["task"] == "audio_decision"]
    main_rows, _ = read_tsv(AUDIO_DECISION)
    random.Random(SEED_AUDIO_DECISION).shuffle(main_rows)
    main_audio = recording_map(AUDIO_DECISION_RECORDING, "trial_id")
    practice_audio = recording_map(PRACTICE_RECORDING, "practice_id")

    fields = [
        "trial_order",
        "phase",
        "task",
        "trial_id",
        "item_type",
        "stimulus_text",
        "correct_response",
        "foil_type",
        "audio_file_name",
        "notes",
    ]
    out_rows = []
    order = 1
    for row in practice_rows:
        out_rows.append(
            {
                "trial_order": str(order),
                "phase": "practice",
                "task": "audio_pv_decision",
                "trial_id": row["practice_id"],
                "item_type": row["item_type"],
                "stimulus_text": row["stimulus_or_sentence"],
                "correct_response": row["correct_response"],
                "foil_type": "",
                "audio_file_name": practice_audio.get(row["practice_id"], ""),
                "notes": row["notes"],
            }
        )
        order += 1
    for row in main_rows:
        out_rows.append(
            {
                "trial_order": str(order),
                "phase": "main",
                "task": "audio_pv_decision",
                "trial_id": row["trial_id"],
                "item_type": row["item_type"],
                "stimulus_text": row["stimulus_text"],
                "correct_response": row["correct_response"],
                "foil_type": row["foil_type"],
                "audio_file_name": main_audio[row["trial_id"]],
                "notes": row["notes"],
            }
        )
        order += 1
    write_tsv(OUT_AUDIO_DECISION, out_rows, fields)


def make_orthographic_trial_file() -> None:
    practice_rows, _ = read_tsv(GENERAL_PRACTICE)
    practice_rows = [row for row in practice_rows if row["task"] == "orthographic"]
    main_rows, _ = read_tsv(ORTHOGRAPHIC)
    random.Random(SEED_ORTHOGRAPHIC).shuffle(main_rows)

    fields = [
        "trial_order",
        "phase",
        "task",
        "item_id",
        "pv",
        "prompt_sentence",
        "option_a",
        "option_b",
        "option_c",
        "option_d",
        "correct_response",
        "source_material",
        "notes",
    ]
    out_rows = []
    order = 1
    for row in practice_rows:
        out_rows.append(
            {
                "trial_order": str(order),
                "phase": "practice",
                "task": "orthographic_pv_meaning_recognition",
                "item_id": row["practice_id"],
                "pv": "",
                "prompt_sentence": row["stimulus_or_sentence"],
                "option_a": row["option_a"],
                "option_b": row["option_b"],
                "option_c": row["option_c"],
                "option_d": row["option_d"],
                "correct_response": row["correct_response"],
                "source_material": "practice",
                "notes": row["notes"],
            }
        )
        order += 1
    for row in main_rows:
        out_rows.append(
            {
                "trial_order": str(order),
                "phase": "main",
                "task": "orthographic_pv_meaning_recognition",
                "item_id": row["item_id"],
                "pv": row["pv"],
                "prompt_sentence": row["prompt_sentence"],
                "option_a": row["option_a"],
                "option_b": row["option_b"],
                "option_c": row["option_c"],
                "option_d": row["option_d"],
                "correct_response": row["correct_option"],
                "source_material": row["source_material"],
                "notes": row["notes"],
            }
        )
        order += 1
    write_tsv(OUT_ORTHOGRAPHIC, out_rows, fields)


def main() -> None:
    make_ljt_trial_file("A", OUT_LJT_A)
    make_ljt_trial_file("B", OUT_LJT_B)
    make_audio_decision_trial_file()
    make_orthographic_trial_file()
    for path in [OUT_LJT_A, OUT_LJT_B, OUT_AUDIO_DECISION, OUT_ORTHOGRAPHIC]:
        print(f"Wrote {path}")


if __name__ == "__main__":
    main()
