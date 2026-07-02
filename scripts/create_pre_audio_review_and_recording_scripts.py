#!/usr/bin/env python3
"""Create focused review packets and recording scripts for the PV-LJT pilot."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MATERIALS = ROOT / "materials"

LJT_ITEMS = MATERIALS / "aural_pv_ljt_items_v4_pre_audio.tsv"
AUDIO_DECISION_ITEMS = MATERIALS / "audio_pv_decision_items_v2_mixed_foils.tsv"
BERT_PRIORITIES = MATERIALS / "bert_review_priorities_v3_for_ljt_v4.tsv"
GENERAL_PRACTICE = MATERIALS / "practice_items_v1.tsv"

MEDIUM_PACKET = MATERIALS / "ljt_medium_priority_expert_review_packet_v2_for_ljt_v4.tsv"
LJT_RECORDING = MATERIALS / "audio_recording_script_ljt_v4_pre_audio.tsv"
AUDIO_DECISION_RECORDING = MATERIALS / "audio_recording_script_audio_decision_v2.tsv"
LJT_PRACTICE = MATERIALS / "ljt_practice_items_v1.tsv"
PRACTICE_RECORDING = MATERIALS / "audio_recording_script_practice_v1.tsv"


LJT_PRACTICE_ROWS = [
    {
        "practice_id": "practice_ljt_001",
        "pv": "wake up",
        "condition": "acceptable",
        "expected_response": "acceptable",
        "target_form": "woke up",
        "sentence_text": "Mina woke up before the alarm.",
        "intended_sense": "stop sleeping",
        "mismatch_type": "none",
        "notes": "practice only; not in target set",
    },
    {
        "practice_id": "practice_ljt_002",
        "pv": "wake up",
        "condition": "unacceptable",
        "expected_response": "unacceptable",
        "target_form": "woke up",
        "sentence_text": "Mina woke up before the alarm but stayed asleep until noon.",
        "intended_sense": "stop sleeping",
        "mismatch_type": "semantic_contradiction",
        "notes": "practice only; not in target set",
    },
    {
        "practice_id": "practice_ljt_003",
        "pv": "write down",
        "condition": "acceptable",
        "expected_response": "acceptable",
        "target_form": "write down",
        "sentence_text": "Please write down the number before you forget it.",
        "intended_sense": "record in writing",
        "mismatch_type": "none",
        "notes": "practice only; not in target set",
    },
    {
        "practice_id": "practice_ljt_004",
        "pv": "write down",
        "condition": "unacceptable",
        "expected_response": "unacceptable",
        "target_form": "write down",
        "sentence_text": "Please write down the number but do not write anything.",
        "intended_sense": "record in writing",
        "mismatch_type": "semantic_contradiction",
        "notes": "practice only; not in target set",
    },
    {
        "practice_id": "practice_ljt_005",
        "pv": "give up",
        "condition": "acceptable",
        "expected_response": "acceptable",
        "target_form": "gave up",
        "sentence_text": "He gave up smoking last year.",
        "intended_sense": "stop doing something",
        "mismatch_type": "none",
        "notes": "practice only; not in target set",
    },
    {
        "practice_id": "practice_ljt_006",
        "pv": "give up",
        "condition": "unacceptable",
        "expected_response": "unacceptable",
        "target_form": "gave up",
        "sentence_text": "He gave up smoking last year but continued to smoke every day.",
        "intended_sense": "stop doing something",
        "mismatch_type": "semantic_contradiction",
        "notes": "practice only; not in target set",
    },
]


def read_tsv(path: Path) -> tuple[list[dict[str, str]], list[str]]:
    with path.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f, delimiter="\t")
        return list(reader), list(reader.fieldnames or [])


def write_tsv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, delimiter="\t", extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def ljt_recording_note(row: dict[str, str]) -> str:
    if row["ljt_item_id"] == "ljt_038a":
        return "Use natural disbelief/disagreement intonation; do not over-emphasize the PV."
    if row["ljt_item_id"] == "ljt_038b":
        return "Use sincere agreement intonation on the final clause; avoid sarcastic delivery."
    return "Record with natural sentence prosody; avoid pausing between verb and particle."


def main() -> None:
    priorities, _ = read_tsv(BERT_PRIORITIES)
    medium_rows = [row for row in priorities if row["priority"] == "medium"]
    medium_fields = [
        "review_order",
        "pv_id",
        "pv",
        "acceptable_item_id",
        "acceptable_sentence",
        "unacceptable_item_id",
        "unacceptable_sentence",
        "bert_flags",
        "expert_flag",
        "diagnostic_reason",
        "current_recommendation",
        "intended_sense_clear_1_5",
        "acceptable_sentence_natural_1_5",
        "unacceptable_sentence_near_miss_1_5",
        "unacceptable_sentence_rejectable_for_intended_reason_1_5",
        "audio_suitable_1_5",
        "decision_keep_revise_drop",
        "suggested_revision",
        "reviewer_comments",
    ]
    medium_packet = []
    for i, row in enumerate(medium_rows, start=1):
        medium_packet.append(
            {
                "review_order": str(i),
                "pv_id": row["pv_id"],
                "pv": row["pv"],
                "acceptable_item_id": row["acceptable_item_id"],
                "acceptable_sentence": row["acceptable_sentence"],
                "unacceptable_item_id": row["unacceptable_item_id"],
                "unacceptable_sentence": row["unacceptable_sentence"],
                "bert_flags": row["bert_flags"],
                "expert_flag": row["expert_flag"],
                "diagnostic_reason": row["reason"],
                "current_recommendation": row["recommendation"],
            }
        )
    write_tsv(MEDIUM_PACKET, medium_packet, medium_fields)

    ljt_rows, _ = read_tsv(LJT_ITEMS)
    ljt_recording_fields = [
        "recording_id",
        "audio_file_name",
        "task",
        "item_id",
        "pv_id",
        "pv",
        "condition",
        "expected_response",
        "text_to_record",
        "target_form",
        "recording_notes",
    ]
    ljt_recording_rows = []
    for row in ljt_rows:
        recording_id = f"rec_ljt_v4_{row['ljt_item_id']}"
        ljt_recording_rows.append(
            {
                "recording_id": recording_id,
                "audio_file_name": f"{recording_id}.wav",
                "task": "aural_pv_ljt",
                "item_id": row["ljt_item_id"],
                "pv_id": row["pv_id"],
                "pv": row["pv"],
                "condition": row["condition"],
                "expected_response": row["expected_response"],
                "text_to_record": row["sentence_text"],
                "target_form": row["target_form"],
                "recording_notes": ljt_recording_note(row),
            }
        )
    write_tsv(LJT_RECORDING, ljt_recording_rows, ljt_recording_fields)

    audio_rows, _ = read_tsv(AUDIO_DECISION_ITEMS)
    audio_recording_fields = [
        "recording_id",
        "audio_file_name",
        "task",
        "trial_id",
        "item_type",
        "stimulus_text",
        "correct_response",
        "foil_type",
        "recording_notes",
    ]
    audio_recording_rows = []
    for row in audio_rows:
        recording_id = f"rec_audio_decision_{row['trial_id']}"
        audio_recording_rows.append(
            {
                "recording_id": recording_id,
                "audio_file_name": f"{recording_id}.wav",
                "task": "audio_pv_decision",
                "trial_id": row["trial_id"],
                "item_type": row["item_type"],
                "stimulus_text": row["stimulus_text"],
                "correct_response": row["correct_response"],
                "foil_type": row["foil_type"],
                "recording_notes": "Record as an isolated two-word stimulus; no carrier phrase; neutral stress.",
            }
        )
    write_tsv(AUDIO_DECISION_RECORDING, audio_recording_rows, audio_recording_fields)

    practice_fields = [
        "practice_id",
        "pv",
        "condition",
        "expected_response",
        "target_form",
        "sentence_text",
        "intended_sense",
        "mismatch_type",
        "notes",
    ]
    write_tsv(LJT_PRACTICE, LJT_PRACTICE_ROWS, practice_fields)

    practice_recording_fields = [
        "recording_id",
        "audio_file_name",
        "task",
        "practice_id",
        "item_type",
        "text_to_record",
        "correct_response",
        "recording_notes",
    ]
    practice_recording_rows = []
    for row in LJT_PRACTICE_ROWS:
        recording_id = f"rec_{row['practice_id']}"
        practice_recording_rows.append(
            {
                "recording_id": recording_id,
                "audio_file_name": f"{recording_id}.wav",
                "task": "aural_pv_ljt_practice",
                "practice_id": row["practice_id"],
                "item_type": row["condition"],
                "text_to_record": row["sentence_text"],
                "correct_response": row["expected_response"],
                "recording_notes": "Practice item; record with the same voice and pacing as main LJT items.",
            }
        )
    general_practice_rows, _ = read_tsv(GENERAL_PRACTICE)
    for row in general_practice_rows:
        if row["task"] != "audio_decision":
            continue
        recording_id = f"rec_{row['practice_id']}"
        practice_recording_rows.append(
            {
                "recording_id": recording_id,
                "audio_file_name": f"{recording_id}.wav",
                "task": "audio_pv_decision_practice",
                "practice_id": row["practice_id"],
                "item_type": row["item_type"],
                "text_to_record": row["stimulus_or_sentence"],
                "correct_response": row["correct_response"],
                "recording_notes": "Practice item; record as an isolated two-word stimulus with neutral stress.",
            }
        )
    write_tsv(PRACTICE_RECORDING, practice_recording_rows, practice_recording_fields)

    for path in [
        MEDIUM_PACKET,
        LJT_RECORDING,
        AUDIO_DECISION_RECORDING,
        LJT_PRACTICE,
        PRACTICE_RECORDING,
    ]:
        print(f"Wrote {path}")


if __name__ == "__main__":
    main()
