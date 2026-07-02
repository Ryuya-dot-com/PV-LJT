#!/usr/bin/env python3
"""Create PV-LJT v4 pre-audio materials from the v3 BERT-reviewed files."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MATERIALS = ROOT / "materials"

ITEMS_V3 = MATERIALS / "aural_pv_ljt_items_v3_bert_reviewed.tsv"
ASSIGNMENT_V3 = MATERIALS / "aural_pv_ljt_list_assignment_v3_bert_reviewed.tsv"
LIST_A_V3 = MATERIALS / "aural_pv_ljt_list_A_v3_bert_reviewed.tsv"
LIST_B_V3 = MATERIALS / "aural_pv_ljt_list_B_v3_bert_reviewed.tsv"
FORM_V3 = MATERIALS / "aural_pv_ljt_expert_review_form_v3_bert_reviewed.tsv"
MASTER_V3 = MATERIALS / "three_stage_pv_master_v3_bert_reviewed.tsv"

ITEMS_V4 = MATERIALS / "aural_pv_ljt_items_v4_pre_audio.tsv"
ASSIGNMENT_V4 = MATERIALS / "aural_pv_ljt_list_assignment_v4_pre_audio.tsv"
LIST_A_V4 = MATERIALS / "aural_pv_ljt_list_A_v4_pre_audio.tsv"
LIST_B_V4 = MATERIALS / "aural_pv_ljt_list_B_v4_pre_audio.tsv"
FORM_V4 = MATERIALS / "aural_pv_ljt_expert_review_form_v4_pre_audio.tsv"
MASTER_V4 = MATERIALS / "three_stage_pv_master_v4_pre_audio.tsv"
FLAGS_V4 = MATERIALS / "aural_pv_ljt_review_flags_v4_pre_audio.tsv"
INTERNAL_REVIEW = MATERIALS / "ljt_pre_audio_internal_review_v1.tsv"


REVISIONS: dict[str, dict[str, str]] = {
    "ljt_003b": {
        "sentence_text": "After the long climb, his knees gave out, but he kept walking easily.",
        "notes": "v4 pre-audio review: reduced extreme outcome while preserving contradiction",
    },
    "ljt_004a": {
        "sentence_text": "She put in three hours on the report before the meeting.",
        "notes": "v4 pre-audio review: made effort object explicit",
    },
    "ljt_004b": {
        "sentence_text": "She put in three hours on the report but spent no time on it.",
        "notes": "v4 pre-audio review: made effort object explicit and context parallel",
    },
    "ljt_007a": {
        "sentence_text": "Poor training held back the young players, so they improved slowly.",
        "notes": "v4 pre-audio review: added outcome cue for target meaning",
    },
    "ljt_007b": {
        "sentence_text": "Poor training held back the young players, so they improved quickly.",
        "notes": "v4 pre-audio review: made acceptable and unacceptable contexts more parallel",
    },
    "ljt_017b": {
        "sentence_text": "I could barely make out the sign, although it was clear and easy to read.",
        "mismatch_type": "semantic_contradiction",
        "notes": "v4 pre-audio review: replaced modality mismatch with semantic contradiction",
    },
    "ljt_022b": {
        "sentence_text": "The host cut off the speaker after the answer was complete.",
        "notes": "v4 pre-audio review: made speaker reference parallel and reduced guest ambiguity",
    },
    "ljt_042b": {
        "sentence_text": "The researchers carried out the survey in three schools but never collected any data.",
        "mismatch_type": "semantic_contradiction",
        "notes": "v4 pre-audio review: replaced collocational near-miss with task-completion contradiction",
    },
    "ljt_047b": {
        "sentence_text": "The introduction laid out the plan for the paper but never described the plan.",
        "notes": "v4 pre-audio review: replaced clarity mismatch with clearer presentation contradiction",
    },
    "ljt_048b": {
        "sentence_text": "The students worked out the answer but never tried to solve it.",
        "mismatch_type": "semantic_contradiction",
        "notes": "v4 pre-audio review: replaced copying method with solution-process contradiction",
    },
}


INTERNAL_DECISIONS = [
    ("pv_003", "give out", "revise", "The original outcome was very extreme; revised to a milder contradiction."),
    ("pv_004", "put in", "revise", "Made the time/effort object explicit and parallel across conditions."),
    ("pv_007", "hold back", "revise", "Made the consequence cue parallel across conditions."),
    ("pv_010", "come along", "keep_with_review", "Retain; still worth expert check for contradiction strength in audio."),
    ("pv_017", "make out", "revise", "Removed phone/sign modality mismatch; now targets difficulty/clarity contradiction."),
    ("pv_022", "cut off", "revise", "Made speaker reference parallel and reduced alternative segment-ending interpretation."),
    ("pv_023", "bring in", "keep", "BERT-only issue; LJT contrast is semantically clear."),
    ("pv_034", "take out", "keep", "BERT-only issue; loan/borrow contrast is semantically clear."),
    ("pv_006", "sit back", "keep", "Target-fit gap likely reflects strong diagnostic contrast rather than a defect."),
    ("pv_015", "put on", "keep", "BERT-only issue; event-staging contrast is semantically clear."),
    ("pv_038", "come on", "keep_with_review", "Retain but mark as prosody-sensitive for recording."),
    ("pv_042", "carry out", "revise", "Changed from collocational academic near-miss to completed-task contradiction."),
    ("pv_047", "lay out", "revise", "Changed from unclear-order mismatch to explicit no-description contradiction."),
    ("pv_048", "work out", "revise", "Changed from copying-method mismatch to no-solution-process contradiction."),
]


REVIEW_FLAGS_V4 = [
    {
        "ljt_item_id": "ljt_010b",
        "pv": "come along",
        "issue_type": "semantic_contradiction_strength",
        "why_to_review": "The sentence relies on contradiction between a chance coming along and nothing new appearing.",
        "suggested_review_focus": "Check whether the mismatch is clear in audio without making the item trivial.",
    },
    {
        "ljt_item_id": "ljt_017b",
        "pv": "make out",
        "issue_type": "clarity_contradiction",
        "why_to_review": "The v4 sentence rejects barely making out a sign because the sign is clear and easy to read.",
        "suggested_review_focus": "Check whether listeners reject the sentence for the intended perceptual-difficulty meaning.",
    },
    {
        "ljt_item_id": "ljt_022b",
        "pv": "cut off",
        "issue_type": "temporal_mismatch",
        "why_to_review": "The v4 sentence says the answer was complete, so interruption is not appropriate.",
        "suggested_review_focus": "Check whether listeners interpret cut off as interrupting, not ending a segment.",
    },
    {
        "ljt_item_id": "ljt_038b",
        "pv": "come on",
        "issue_type": "prosody_sensitive",
        "why_to_review": "The discourse marker depends heavily on intonation; sincere agreement prosody is needed.",
        "suggested_review_focus": "Check whether this item should be recorded with controlled prosody or dropped.",
    },
    {
        "ljt_item_id": "ljt_042b",
        "pv": "carry out",
        "issue_type": "task_completion_contradiction",
        "why_to_review": "The v4 sentence says the survey was carried out but no data were collected.",
        "suggested_review_focus": "Check whether this is a clear semantic mismatch for an academic task.",
    },
    {
        "ljt_item_id": "ljt_047b",
        "pv": "lay out",
        "issue_type": "presentation_contradiction",
        "why_to_review": "The v4 sentence says the introduction laid out the plan for the paper but never described it.",
        "suggested_review_focus": "Check whether the contradiction targets the present/explain sense clearly.",
    },
    {
        "ljt_item_id": "ljt_048b",
        "pv": "work out",
        "issue_type": "solution_process_contradiction",
        "why_to_review": "The v4 sentence says the students worked out the answer but never tried to solve it.",
        "suggested_review_focus": "Check whether learners might still accept the item from answer availability alone.",
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


def revised_item(row: dict[str, str]) -> dict[str, str]:
    out = dict(row)
    revision = REVISIONS.get(out["ljt_item_id"])
    if not revision:
        return out
    for key, value in revision.items():
        if key == "notes":
            out["notes"] = value
        else:
            out[key] = value
    return out


def refresh_rows_from_items(
    rows: list[dict[str, str]], item_by_id: dict[str, dict[str, str]]
) -> list[dict[str, str]]:
    refreshed = []
    for row in rows:
        out = dict(row)
        item = item_by_id[out["ljt_item_id"]]
        for key, value in item.items():
            if key in out:
                out[key] = value
        refreshed.append(out)
    return refreshed


def main() -> None:
    item_rows, item_fields = read_tsv(ITEMS_V3)
    v4_items = [revised_item(row) for row in item_rows]
    item_by_id = {row["ljt_item_id"]: row for row in v4_items}
    write_tsv(ITEMS_V4, v4_items, item_fields)

    for src, dst in [
        (ASSIGNMENT_V3, ASSIGNMENT_V4),
        (LIST_A_V3, LIST_A_V4),
        (LIST_B_V3, LIST_B_V4),
    ]:
        rows, fields = read_tsv(src)
        write_tsv(dst, refresh_rows_from_items(rows, item_by_id), fields)

    form_rows, form_fields = read_tsv(FORM_V3)
    write_tsv(FORM_V4, refresh_rows_from_items(form_rows, item_by_id), form_fields)

    master_rows, master_fields = read_tsv(MASTER_V3)
    changed_pv_ids = {item_by_id[item_id]["pv_id"] for item_id in REVISIONS}
    for row in master_rows:
        if row["pv_id"] in changed_pv_ids:
            row["notes"] = row["notes"] + "; LJT v4 pre-audio sentence revised"
    write_tsv(MASTER_V4, master_rows, master_fields)

    flag_fields = [
        "ljt_item_id",
        "pv",
        "issue_type",
        "why_to_review",
        "suggested_review_focus",
    ]
    write_tsv(FLAGS_V4, REVIEW_FLAGS_V4, flag_fields)

    decision_fields = ["pv_id", "pv", "decision", "rationale"]
    write_tsv(
        INTERNAL_REVIEW,
        [
            {
                "pv_id": pv_id,
                "pv": pv,
                "decision": decision,
                "rationale": rationale,
            }
            for pv_id, pv, decision, rationale in INTERNAL_DECISIONS
        ],
        decision_fields,
    )

    for path in [
        ITEMS_V4,
        ASSIGNMENT_V4,
        LIST_A_V4,
        LIST_B_V4,
        FORM_V4,
        MASTER_V4,
        FLAGS_V4,
        INTERNAL_REVIEW,
    ]:
        print(f"Wrote {path}")


if __name__ == "__main__":
    main()
