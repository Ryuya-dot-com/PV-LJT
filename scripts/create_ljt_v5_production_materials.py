#!/usr/bin/env python3
"""Create PV-LJT v5 production materials.

The v5 design removes the main flaws in v4:
- no overt contrast markers that only appear in unacceptable items
- no explicit contradiction templates
- matched word counts within each PV pair
- short, parallel sentences suitable for audio presentation
"""

from __future__ import annotations

import csv
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MATERIALS = ROOT / "materials"

ITEMS_V4 = MATERIALS / "aural_pv_ljt_items_v4_pre_audio.tsv"
ASSIGNMENT_V4 = MATERIALS / "aural_pv_ljt_list_assignment_v4_pre_audio.tsv"
LIST_A_V4 = MATERIALS / "aural_pv_ljt_list_A_v4_pre_audio.tsv"
LIST_B_V4 = MATERIALS / "aural_pv_ljt_list_B_v4_pre_audio.tsv"
MASTER_V4 = MATERIALS / "three_stage_pv_master_v4_pre_audio.tsv"

ITEMS_V5 = MATERIALS / "aural_pv_ljt_items_v5_production.tsv"
ASSIGNMENT_V5 = MATERIALS / "aural_pv_ljt_list_assignment_v5_production.tsv"
LIST_A_V5 = MATERIALS / "aural_pv_ljt_list_A_v5_production.tsv"
LIST_B_V5 = MATERIALS / "aural_pv_ljt_list_B_v5_production.tsv"
FORM_V5 = MATERIALS / "aural_pv_ljt_expert_review_form_v5_production.tsv"
FLAGS_V5 = MATERIALS / "aural_pv_ljt_review_flags_v5_production.tsv"
MASTER_V5 = MATERIALS / "three_stage_pv_master_v5_production.tsv"
AUDIT_V5 = MATERIALS / "stimulus_audit_ljt_v5_production.tsv"

LJT_PRACTICE_V5 = MATERIALS / "ljt_practice_items_v5_production.tsv"
LJT_RECORDING_V5 = MATERIALS / "audio_recording_script_ljt_v5_production.tsv"
PRACTICE_RECORDING_V5 = MATERIALS / "audio_recording_script_ljt_practice_v5_production.tsv"
PILOT_A_V5 = MATERIALS / "pilot_trial_file_ljt_list_A_v5_production.tsv"
PILOT_B_V5 = MATERIALS / "pilot_trial_file_ljt_list_B_v5_production.tsv"


Pair = tuple[str, str, str, str]


PAIR_SENTENCES: dict[str, Pair] = {
    "pv_001": (
        "The committee broke off the negotiations.",
        "The committee broke off the agenda.",
        "none",
        "selectional_semantic_mismatch",
    ),
    "pv_002": (
        "The officer handed over the documents.",
        "The officer handed over the deadline.",
        "none",
        "selectional_semantic_mismatch",
    ),
    "pv_003": (
        "The old engine gave out suddenly.",
        "The old answer gave out suddenly.",
        "none",
        "subject_selection_mismatch",
    ),
    "pv_004": (
        "She put in steady effort yesterday.",
        "She put in steady evidence yesterday.",
        "none",
        "object_selection_mismatch",
    ),
    "pv_005": (
        "The lecture was hard to take in.",
        "The doorway was hard to take in.",
        "none",
        "object_selection_mismatch",
    ),
    "pv_006": (
        "The mayor sat back during the crisis.",
        "The mayor sat back during the sprint.",
        "none",
        "context_selection_mismatch",
    ),
    "pv_007": (
        "Poor training held back the players.",
        "Extra support held back the players.",
        "none",
        "cause_selection_mismatch",
    ),
    "pv_008": (
        "She moved up to senior manager.",
        "She moved up to junior assistant.",
        "none",
        "hierarchy_semantic_mismatch",
    ),
    "pv_009": (
        "The tourists got on the bus.",
        "The tourists got on the lecture.",
        "none",
        "object_selection_mismatch",
    ),
    "pv_010": (
        "A rare chance came along today.",
        "A rare schedule came along today.",
        "none",
        "subject_selection_mismatch",
    ),
    "pv_011": (
        "Her analysis stood out among reports.",
        "Her analysis stood out among deadlines.",
        "none",
        "comparison_set_mismatch",
    ),
    "pv_012": (
        "The company pulled back from investment.",
        "The company pulled back from approval.",
        "none",
        "object_selection_mismatch",
    ),
    "pv_013": (
        "The office ran out of paper.",
        "The office ran out of agenda.",
        "none",
        "object_selection_mismatch",
    ),
    "pv_014": (
        "The officer turned over the files.",
        "The officer turned over the deadline.",
        "none",
        "object_selection_mismatch",
    ),
    "pv_015": (
        "The school put on a concert.",
        "The school put on a textbook.",
        "none",
        "event_selection_mismatch",
    ),
    "pv_016": (
        "The party took back the council.",
        "The party took back the outcome.",
        "none",
        "object_selection_mismatch",
    ),
    "pv_017": (
        "I could barely make out the sign outside.",
        "I could barely make out the flavor outside.",
        "none",
        "object_selection_mismatch",
    ),
    "pv_018": (
        "The hard work paid off eventually.",
        "The hard weather paid off eventually.",
        "none",
        "subject_selection_mismatch",
    ),
    "pv_019": (
        "The children got off the train.",
        "The children got off the deadline.",
        "none",
        "object_selection_mismatch",
    ),
    "pv_020": (
        "He turned up at the meeting.",
        "He turned up at the method.",
        "none",
        "location_selection_mismatch",
    ),
    "pv_021": (
        "The soldiers got down behind the wall.",
        "The soldiers got down behind the idea.",
        "none",
        "location_selection_mismatch",
    ),
    "pv_022": (
        "The host cut off the speaker.",
        "The host cut off the policy.",
        "none",
        "object_selection_mismatch",
    ),
    "pv_023": (
        "The firm brought in an expert.",
        "The firm brought in a deadline.",
        "none",
        "object_selection_mismatch",
    ),
    "pv_024": (
        "Police put out a warning.",
        "Police put out a wallet.",
        "none",
        "object_selection_mismatch",
    ),
    "pv_025": (
        "The editor cleaned up the insults.",
        "The editor cleaned up the deadline.",
        "none",
        "object_selection_mismatch",
    ),
    "pv_026": (
        "The report set out the rules.",
        "The report set out the pencils.",
        "none",
        "object_selection_mismatch",
    ),
    "pv_027": (
        "The teacher broke down the problem.",
        "The teacher broke down the applause.",
        "none",
        "object_selection_mismatch",
    ),
    "pv_028": (
        "The manager reached out to clients.",
        "The manager reached out to deadlines.",
        "none",
        "recipient_selection_mismatch",
    ),
    "pv_029": (
        "She kept up the good work.",
        "She kept up the heavy claim.",
        "none",
        "object_selection_mismatch",
    ),
    "pv_030": (
        "They put up posters downtown.",
        "They put up music downtown.",
        "none",
        "object_selection_mismatch",
    ),
    "pv_031": (
        "The coach turned around the team.",
        "The coach turned around the deadline.",
        "none",
        "object_selection_mismatch",
    ),
    "pv_032": (
        "The data backed up the claim.",
        "The data backed up the deadline.",
        "none",
        "object_selection_mismatch",
    ),
    "pv_033": (
        "She looked out at the garden.",
        "She looked out at the deadline.",
        "none",
        "object_selection_mismatch",
    ),
    "pv_034": (
        "He took out a loan yesterday.",
        "He took out a deadline yesterday.",
        "none",
        "object_selection_mismatch",
    ),
    "pv_035": (
        "They looked back on the decision.",
        "They looked back on the ceiling.",
        "none",
        "object_selection_mismatch",
    ),
    "pv_036": (
        "The rent went up sharply.",
        "The advice went up sharply.",
        "none",
        "subject_selection_mismatch",
    ),
    "pv_037": (
        "The rent went down sharply.",
        "The advice went down sharply.",
        "none",
        "subject_selection_mismatch",
    ),
    "pv_038": (
        "Oh, come on, that sounds impossible.",
        "Oh, come on, that sounds accurate.",
        "none",
        "discourse_semantic_mismatch",
    ),
    "pv_039": (
        "Experts came in during planning.",
        "Experts came in during deadline.",
        "none",
        "context_selection_mismatch",
    ),
    "pv_040": (
        "The truth came out during interviews.",
        "The furniture came out during interviews.",
        "none",
        "context_selection_mismatch",
    ),
    "pv_041": (
        "The reforms brought about major change.",
        "The reforms brought about major furniture.",
        "none",
        "object_selection_mismatch",
    ),
    "pv_042": (
        "The researchers carried out the survey.",
        "The researchers carried out the deadline.",
        "none",
        "object_selection_mismatch",
    ),
    "pv_043": (
        "The evidence ruled out that explanation.",
        "The evidence ruled out that deadline.",
        "none",
        "object_selection_mismatch",
    ),
    "pv_044": (
        "The teacher pointed out the error.",
        "The pencil pointed out the error.",
        "none",
        "subject_selection_mismatch",
    ),
    "pv_045": (
        "The paragraph summed up the argument.",
        "The paragraph summed up the deadline.",
        "none",
        "object_selection_mismatch",
    ),
    "pv_046": (
        "The nurse followed up after surgery.",
        "The nurse followed up after furniture.",
        "none",
        "context_selection_mismatch",
    ),
    "pv_047": (
        "The chart laid out the plan.",
        "The chart laid out the spoon.",
        "none",
        "object_selection_mismatch",
    ),
    "pv_048": (
        "The students worked out the answer.",
        "The students worked out the carpet.",
        "none",
        "object_selection_mismatch",
    ),
}


PRACTICE_ROWS = [
    {
        "practice_id": "practice_ljt_v5_001",
        "pv": "wake up",
        "condition": "acceptable",
        "expected_response": "acceptable",
        "target_form": "woke up",
        "sentence_text": "Mina woke up before the alarm.",
        "intended_sense": "stop sleeping",
        "mismatch_type": "none",
        "notes": "v5 practice only; no overt contrast cue",
    },
    {
        "practice_id": "practice_ljt_v5_002",
        "pv": "wake up",
        "condition": "unacceptable",
        "expected_response": "unacceptable",
        "target_form": "woke up",
        "sentence_text": "Mina woke up before the pencil.",
        "intended_sense": "stop sleeping",
        "mismatch_type": "context_selection_mismatch",
        "notes": "v5 practice only; no overt contrast cue",
    },
    {
        "practice_id": "practice_ljt_v5_003",
        "pv": "turn off",
        "condition": "acceptable",
        "expected_response": "acceptable",
        "target_form": "turn off",
        "sentence_text": "Please turn off the lamp.",
        "intended_sense": "stop a device operating",
        "mismatch_type": "none",
        "notes": "v5 practice only; no overt contrast cue",
    },
    {
        "practice_id": "practice_ljt_v5_004",
        "pv": "turn off",
        "condition": "unacceptable",
        "expected_response": "unacceptable",
        "target_form": "turn off",
        "sentence_text": "Please turn off the sandwich.",
        "intended_sense": "stop a device operating",
        "mismatch_type": "object_selection_mismatch",
        "notes": "v5 practice only; no overt contrast cue",
    },
    {
        "practice_id": "practice_ljt_v5_005",
        "pv": "give up",
        "condition": "acceptable",
        "expected_response": "acceptable",
        "target_form": "gave up",
        "sentence_text": "He gave up smoking last year.",
        "intended_sense": "stop doing something",
        "mismatch_type": "none",
        "notes": "v5 practice only; no overt contrast cue",
    },
    {
        "practice_id": "practice_ljt_v5_006",
        "pv": "give up",
        "condition": "unacceptable",
        "expected_response": "unacceptable",
        "target_form": "gave up",
        "sentence_text": "He gave up rainfall last year.",
        "intended_sense": "stop doing something",
        "mismatch_type": "object_selection_mismatch",
        "notes": "v5 practice only; no overt contrast cue",
    },
]


CUE_PATTERN = re.compile(
    r"\b(but|although|however|yet|nevertheless|never|no|none|nothing|without|despite)\b",
    re.IGNORECASE,
)
WORD_PATTERN = re.compile(r"[A-Za-z]+(?:'[A-Za-z]+)?")


def read_tsv(path: Path) -> tuple[list[dict[str, str]], list[str]]:
    with path.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f, delimiter="\t")
        return list(reader), list(reader.fieldnames or [])


def write_tsv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, delimiter="\t", extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def word_count(text: str) -> int:
    return len(WORD_PATTERN.findall(text))


def has_cue(text: str) -> bool:
    return bool(CUE_PATTERN.search(text))


def v5_note(condition: str) -> str:
    if condition == "acceptable":
        return "v5 production: short matched acceptable sentence; no overt contrast cue"
    return "v5 production: selectional mismatch; no overt contrast cue or explicit contradiction"


def make_items() -> tuple[list[dict[str, str]], list[str]]:
    rows, fields = read_tsv(ITEMS_V4)
    by_pv_condition = {(row["pv_id"], row["condition"]): row for row in rows}
    v5_rows: list[dict[str, str]] = []

    for pv_id in sorted(PAIR_SENTENCES):
        acceptable, unacceptable, ok_type, bad_type = PAIR_SENTENCES[pv_id]
        for condition, sentence, mismatch in [
            ("acceptable", acceptable, ok_type),
            ("unacceptable", unacceptable, bad_type),
        ]:
            row = dict(by_pv_condition[(pv_id, condition)])
            row["sentence_text"] = sentence
            row["mismatch_type"] = mismatch
            row["expected_response"] = condition
            row["notes"] = v5_note(condition)
            v5_rows.append(row)

    write_tsv(ITEMS_V5, v5_rows, fields)
    return v5_rows, fields


def refresh_rows(rows: list[dict[str, str]], item_by_id: dict[str, dict[str, str]]) -> list[dict[str, str]]:
    out_rows = []
    for row in rows:
        out = dict(row)
        item = item_by_id[out["ljt_item_id"]]
        for key, value in item.items():
            if key in out:
                out[key] = value
        out_rows.append(out)
    return out_rows


def make_assignment_and_lists(item_by_id: dict[str, dict[str, str]]) -> None:
    for src, dst in [
        (ASSIGNMENT_V4, ASSIGNMENT_V5),
        (LIST_A_V4, LIST_A_V5),
        (LIST_B_V4, LIST_B_V5),
    ]:
        rows, fields = read_tsv(src)
        refreshed = refresh_rows(rows, item_by_id)
        write_tsv(dst, refreshed, fields)


def make_review_form(items: list[dict[str, str]]) -> None:
    fields = [
        "ljt_item_id",
        "pv_id",
        "pv",
        "condition",
        "expected_response",
        "sentence_text",
        "target_form",
        "intended_sense",
        "mismatch_type",
        "word_count",
        "has_overt_cue",
        "naturalness_1_4",
        "sense_fit_or_mismatch_1_4",
        "target_sense_clear_1_4",
        "audio_suitability_1_4",
        "reviewer_comments",
        "decision_keep_revise_drop",
    ]
    rows = []
    for row in items:
        rows.append(
            {
                **row,
                "word_count": str(word_count(row["sentence_text"])),
                "has_overt_cue": str(has_cue(row["sentence_text"])).lower(),
            }
        )
    write_tsv(FORM_V5, rows, fields)


def make_master() -> None:
    rows, fields = read_tsv(MASTER_V4)
    for row in rows:
        row["notes"] = row["notes"] + "; LJT v5 production sentence pair created"
    write_tsv(MASTER_V5, rows, fields)


def recording_note(row: dict[str, str]) -> str:
    if row["pv_id"] == "pv_038":
        return "Use natural disbelief intonation on 'come on'; avoid sarcasm or added contrastive stress."
    return "Record with natural sentence prosody; avoid pausing between verb and particle."


def make_recording_script(items: list[dict[str, str]]) -> None:
    fields = [
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
    rows = []
    for row in items:
        recording_id = f"rec_ljt_v5_{row['ljt_item_id']}"
        rows.append(
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
                "recording_notes": recording_note(row),
            }
        )
    write_tsv(LJT_RECORDING_V5, rows, fields)


def make_practice() -> None:
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
    write_tsv(LJT_PRACTICE_V5, PRACTICE_ROWS, practice_fields)

    recording_fields = [
        "recording_id",
        "audio_file_name",
        "task",
        "practice_id",
        "item_type",
        "text_to_record",
        "correct_response",
        "recording_notes",
    ]
    recording_rows = []
    for row in PRACTICE_ROWS:
        recording_id = f"rec_{row['practice_id']}"
        recording_rows.append(
            {
                "recording_id": recording_id,
                "audio_file_name": f"{recording_id}.wav",
                "task": "aural_pv_ljt_practice",
                "practice_id": row["practice_id"],
                "item_type": row["condition"],
                "text_to_record": row["sentence_text"],
                "correct_response": row["expected_response"],
                "recording_notes": "Practice item; record with the same voice and pacing as v5 LJT items.",
            }
        )
    write_tsv(PRACTICE_RECORDING_V5, recording_rows, recording_fields)


def recording_map(path: Path, key_field: str) -> dict[str, str]:
    rows, _ = read_tsv(path)
    return {row[key_field]: row["audio_file_name"] for row in rows}


def make_trial_file(list_path: Path, out_path: Path, list_id: str) -> None:
    practice_audio = recording_map(PRACTICE_RECORDING_V5, "practice_id")
    main_audio = recording_map(LJT_RECORDING_V5, "item_id")
    practice_rows, _ = read_tsv(LJT_PRACTICE_V5)
    main_rows, _ = read_tsv(list_path)

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
    rows = []
    order = 1
    for row in practice_rows:
        rows.append(
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
        rows.append(
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
    write_tsv(out_path, rows, fields)


def make_audit(items: list[dict[str, str]]) -> None:
    by_pv: dict[str, dict[str, dict[str, str]]] = {}
    for row in items:
        by_pv.setdefault(row["pv_id"], {})[row["condition"]] = row

    fields = [
        "pv_id",
        "pv",
        "acceptable_item_id",
        "acceptable_word_count",
        "acceptable_has_overt_cue",
        "unacceptable_item_id",
        "unacceptable_word_count",
        "unacceptable_has_overt_cue",
        "word_count_delta_unacceptable_minus_acceptable",
        "target_form_in_both",
        "audit_status",
    ]
    rows = []
    flags = []
    for pv_id, pair in sorted(by_pv.items()):
        acceptable = pair["acceptable"]
        unacceptable = pair["unacceptable"]
        a_count = word_count(acceptable["sentence_text"])
        u_count = word_count(unacceptable["sentence_text"])
        target = acceptable["target_form"].lower()
        target_ok = (
            target in acceptable["sentence_text"].lower()
            and target in unacceptable["sentence_text"].lower()
        )
        status = "pass"
        if a_count != u_count or has_cue(acceptable["sentence_text"]) or has_cue(unacceptable["sentence_text"]) or not target_ok:
            status = "review"
        rows.append(
            {
                "pv_id": pv_id,
                "pv": acceptable["pv"],
                "acceptable_item_id": acceptable["ljt_item_id"],
                "acceptable_word_count": str(a_count),
                "acceptable_has_overt_cue": str(has_cue(acceptable["sentence_text"])).lower(),
                "unacceptable_item_id": unacceptable["ljt_item_id"],
                "unacceptable_word_count": str(u_count),
                "unacceptable_has_overt_cue": str(has_cue(unacceptable["sentence_text"])).lower(),
                "word_count_delta_unacceptable_minus_acceptable": str(u_count - a_count),
                "target_form_in_both": str(target_ok).lower(),
                "audit_status": status,
            }
        )
        if pv_id in {"pv_006", "pv_007", "pv_038"}:
            flags.append(
                {
                    "ljt_item_id": unacceptable["ljt_item_id"],
                    "pv": unacceptable["pv"],
                    "issue_type": "production_expert_review",
                    "why_to_review": "This PV remains comparatively context/prosody sensitive even after v5 rewriting.",
                    "suggested_review_focus": "Check whether the item is rejected for PV meaning rather than broad plausibility.",
                }
            )
    write_tsv(AUDIT_V5, rows, fields)

    flag_fields = [
        "ljt_item_id",
        "pv",
        "issue_type",
        "why_to_review",
        "suggested_review_focus",
    ]
    write_tsv(FLAGS_V5, flags, flag_fields)


def main() -> None:
    items, _ = make_items()
    item_by_id = {row["ljt_item_id"]: row for row in items}
    make_assignment_and_lists(item_by_id)
    make_review_form(items)
    make_master()
    make_recording_script(items)
    make_practice()
    make_trial_file(LIST_A_V5, PILOT_A_V5, "A")
    make_trial_file(LIST_B_V5, PILOT_B_V5, "B")
    make_audit(items)

    for path in [
        ITEMS_V5,
        ASSIGNMENT_V5,
        LIST_A_V5,
        LIST_B_V5,
        FORM_V5,
        FLAGS_V5,
        MASTER_V5,
        LJT_PRACTICE_V5,
        LJT_RECORDING_V5,
        PRACTICE_RECORDING_V5,
        PILOT_A_V5,
        PILOT_B_V5,
        AUDIT_V5,
    ]:
        print(f"Wrote {path}")


if __name__ == "__main__":
    main()
