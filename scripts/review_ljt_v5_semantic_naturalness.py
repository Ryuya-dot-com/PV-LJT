#!/usr/bin/env python3
"""Write an expert-style semantic/naturalness review for PV-LJT v5."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MATERIALS = ROOT / "materials"

ITEMS = MATERIALS / "aural_pv_ljt_items_v5_production.tsv"
OUT_REVIEW = MATERIALS / "ljt_v5_semantic_naturalness_expert_review_v1.tsv"
OUT_SUMMARY = MATERIALS / "ljt_v5_semantic_naturalness_expert_review_summary_v1.md"


# Ratings:
# 4 = strong/pass, 3 = acceptable with caution, 2 = weak, 1 = fail.
# general_cue_risk_1_4 is reversed: 1 = low risk, 4 = high risk.
REVIEWS: dict[str, dict[str, str]] = {
    "pv_001": {
        "acceptable_natural_1_4": "4",
        "unacceptable_framing_1_4": "2",
        "pv_dependency_1_4": "3",
        "general_cue_risk_1_4": "2",
        "decision": "revise_minor",
        "comment": "Agenda is a plausible committee noun, but broke off the agenda is mainly a collocational anomaly.",
    },
    "pv_002": {
        "acceptable_natural_1_4": "4",
        "unacceptable_framing_1_4": "2",
        "pv_dependency_1_4": "3",
        "general_cue_risk_1_4": "2",
        "decision": "revise_minor",
        "comment": "Deadline is not transferable; mismatch is local, but a more task-plausible object is needed.",
    },
    "pv_003": {
        "acceptable_natural_1_4": "4",
        "unacceptable_framing_1_4": "1",
        "pv_dependency_1_4": "2",
        "general_cue_risk_1_4": "4",
        "decision": "revise_major",
        "comment": "The old answer gave out is rejected from subject oddness, not specifically PV knowledge.",
    },
    "pv_004": {
        "acceptable_natural_1_4": "3",
        "unacceptable_framing_1_4": "2",
        "pv_dependency_1_4": "2",
        "general_cue_risk_1_4": "3",
        "decision": "revise_major",
        "comment": "Put in evidence can be acceptable in legal/register contexts, so the mismatch is not controlled.",
    },
    "pv_005": {
        "acceptable_natural_1_4": "4",
        "unacceptable_framing_1_4": "1",
        "pv_dependency_1_4": "2",
        "general_cue_risk_1_4": "4",
        "decision": "revise_major",
        "comment": "Doorway is rejected by broad object semantics; take in is also polysemous.",
    },
    "pv_006": {
        "acceptable_natural_1_4": "4",
        "unacceptable_framing_1_4": "2",
        "pv_dependency_1_4": "2",
        "general_cue_risk_1_4": "3",
        "decision": "revise_major",
        "comment": "Runner/sprint creates a world-knowledge mismatch; sit back is also posture/polysemy sensitive.",
    },
    "pv_007": {
        "acceptable_natural_1_4": "4",
        "unacceptable_framing_1_4": "2",
        "pv_dependency_1_4": "2",
        "general_cue_risk_1_4": "3",
        "decision": "revise_major",
        "comment": "Extra support can sometimes hold players back, so the intended mismatch is unstable.",
    },
    "pv_008": {
        "acceptable_natural_1_4": "4",
        "unacceptable_framing_1_4": "3",
        "pv_dependency_1_4": "4",
        "general_cue_risk_1_4": "1",
        "decision": "keep_with_caution",
        "comment": "The contrast is hierarchy-based and locally tied to move up; this is one of the stronger items.",
    },
    "pv_009": {
        "acceptable_natural_1_4": "4",
        "unacceptable_framing_1_4": "1",
        "pv_dependency_1_4": "2",
        "general_cue_risk_1_4": "4",
        "decision": "revise_major",
        "comment": "Lecture is not a vehicle; the item is too easily solved from object category.",
    },
    "pv_010": {
        "acceptable_natural_1_4": "4",
        "unacceptable_framing_1_4": "2",
        "pv_dependency_1_4": "2",
        "general_cue_risk_1_4": "3",
        "decision": "revise_major",
        "comment": "A schedule can come along in informal usage; the mismatch is weak and unstable.",
    },
    "pv_011": {
        "acceptable_natural_1_4": "3",
        "unacceptable_framing_1_4": "2",
        "pv_dependency_1_4": "3",
        "general_cue_risk_1_4": "2",
        "decision": "revise_minor",
        "comment": "Among deadlines is an odd comparison set; use a more parallel competing-item set.",
    },
    "pv_012": {
        "acceptable_natural_1_4": "3",
        "unacceptable_framing_1_4": "2",
        "pv_dependency_1_4": "3",
        "general_cue_risk_1_4": "2",
        "decision": "revise_minor",
        "comment": "Pulled back from approval is locally wrong, but approval is not a clean activity/involvement noun.",
    },
    "pv_013": {
        "acceptable_natural_1_4": "4",
        "unacceptable_framing_1_4": "1",
        "pv_dependency_1_4": "2",
        "general_cue_risk_1_4": "4",
        "decision": "revise_major",
        "comment": "Agenda makes the depletion mismatch too obvious from noun semantics alone.",
    },
    "pv_014": {
        "acceptable_natural_1_4": "4",
        "unacceptable_framing_1_4": "2",
        "pv_dependency_1_4": "3",
        "general_cue_risk_1_4": "2",
        "decision": "revise_minor",
        "comment": "Deadline is too generic; use a better legal/authority near-miss.",
    },
    "pv_015": {
        "acceptable_natural_1_4": "4",
        "unacceptable_framing_1_4": "2",
        "pv_dependency_1_4": "3",
        "general_cue_risk_1_4": "2",
        "decision": "revise_minor",
        "comment": "Textbook is not an event; mismatch is clear but solved by noun type.",
    },
    "pv_016": {
        "acceptable_natural_1_4": "2",
        "unacceptable_framing_1_4": "1",
        "pv_dependency_1_4": "2",
        "general_cue_risk_1_4": "4",
        "decision": "revise_major",
        "comment": "Took back the council is less natural than took back control; outcome is a poor near-miss.",
    },
    "pv_017": {
        "acceptable_natural_1_4": "4",
        "unacceptable_framing_1_4": "3",
        "pv_dependency_1_4": "1",
        "general_cue_risk_1_4": "4",
        "decision": "drop_candidate",
        "comment": "Make out the flavor is actually acceptable as discern a flavor; item cannot be used as keyed.",
    },
    "pv_018": {
        "acceptable_natural_1_4": "4",
        "unacceptable_framing_1_4": "1",
        "pv_dependency_1_4": "2",
        "general_cue_risk_1_4": "4",
        "decision": "revise_major",
        "comment": "Weather subject makes the item solvable without PV knowledge.",
    },
    "pv_019": {
        "acceptable_natural_1_4": "4",
        "unacceptable_framing_1_4": "1",
        "pv_dependency_1_4": "2",
        "general_cue_risk_1_4": "4",
        "decision": "revise_major",
        "comment": "Deadline is not a vehicle/location; use a travel-context near-miss.",
    },
    "pv_020": {
        "acceptable_natural_1_4": "4",
        "unacceptable_framing_1_4": "1",
        "pv_dependency_1_4": "2",
        "general_cue_risk_1_4": "4",
        "decision": "revise_major",
        "comment": "Method is not a place/event; mismatch is broad object semantics.",
    },
    "pv_021": {
        "acceptable_natural_1_4": "4",
        "unacceptable_framing_1_4": "1",
        "pv_dependency_1_4": "2",
        "general_cue_risk_1_4": "4",
        "decision": "revise_major",
        "comment": "Idea is not a physical location; this is a general concreteness cue.",
    },
    "pv_022": {
        "acceptable_natural_1_4": "4",
        "unacceptable_framing_1_4": "2",
        "pv_dependency_1_4": "2",
        "general_cue_risk_1_4": "3",
        "decision": "revise_major",
        "comment": "Cut off the policy targets object type rather than the interrupt-someone sense.",
    },
    "pv_023": {
        "acceptable_natural_1_4": "4",
        "unacceptable_framing_1_4": "2",
        "pv_dependency_1_4": "1",
        "general_cue_risk_1_4": "4",
        "decision": "revise_major",
        "comment": "Bring in a deadline can mean introduce a deadline, so the keyed response is unsafe.",
    },
    "pv_024": {
        "acceptable_natural_1_4": "4",
        "unacceptable_framing_1_4": "2",
        "pv_dependency_1_4": "2",
        "general_cue_risk_1_4": "3",
        "decision": "revise_major",
        "comment": "Wallet is too object-like; put out also has literal object-placement senses.",
    },
    "pv_025": {
        "acceptable_natural_1_4": "4",
        "unacceptable_framing_1_4": "1",
        "pv_dependency_1_4": "2",
        "general_cue_risk_1_4": "4",
        "decision": "revise_major",
        "comment": "Deadline is simply not cleanable; broad noun semantics solves the item.",
    },
    "pv_026": {
        "acceptable_natural_1_4": "4",
        "unacceptable_framing_1_4": "1",
        "pv_dependency_1_4": "2",
        "general_cue_risk_1_4": "4",
        "decision": "revise_major",
        "comment": "Report plus pencils is a subject-object mismatch; set out has literal arrangement senses.",
    },
    "pv_027": {
        "acceptable_natural_1_4": "4",
        "unacceptable_framing_1_4": "2",
        "pv_dependency_1_4": "3",
        "general_cue_risk_1_4": "2",
        "decision": "revise_minor",
        "comment": "Applause is odd but the mismatch is fairly local to the decompose-an-object sense.",
    },
    "pv_028": {
        "acceptable_natural_1_4": "4",
        "unacceptable_framing_1_4": "2",
        "pv_dependency_1_4": "3",
        "general_cue_risk_1_4": "2",
        "decision": "revise_minor",
        "comment": "Deadlines are not recipients; a human/institutional near-miss would be better.",
    },
    "pv_029": {
        "acceptable_natural_1_4": "4",
        "unacceptable_framing_1_4": "1",
        "pv_dependency_1_4": "2",
        "general_cue_risk_1_4": "4",
        "decision": "revise_major",
        "comment": "Heavy claim is unnatural independent of keep up.",
    },
    "pv_030": {
        "acceptable_natural_1_4": "4",
        "unacceptable_framing_1_4": "2",
        "pv_dependency_1_4": "3",
        "general_cue_risk_1_4": "2",
        "decision": "revise_minor",
        "comment": "Music is less attachable/displayable than posters, but the item may be too noun-category based.",
    },
    "pv_031": {
        "acceptable_natural_1_4": "4",
        "unacceptable_framing_1_4": "2",
        "pv_dependency_1_4": "3",
        "general_cue_risk_1_4": "2",
        "decision": "revise_minor",
        "comment": "Deadline is a weak object for business improvement; use a more plausible but wrong object.",
    },
    "pv_032": {
        "acceptable_natural_1_4": "4",
        "unacceptable_framing_1_4": "2",
        "pv_dependency_1_4": "3",
        "general_cue_risk_1_4": "2",
        "decision": "revise_minor",
        "comment": "Deadline is not a proposition; mismatch is local but still object-type based.",
    },
    "pv_033": {
        "acceptable_natural_1_4": "4",
        "unacceptable_framing_1_4": "1",
        "pv_dependency_1_4": "2",
        "general_cue_risk_1_4": "4",
        "decision": "revise_major",
        "comment": "Deadline is not visually look-out-at material; broad noun semantics solves it.",
    },
    "pv_034": {
        "acceptable_natural_1_4": "4",
        "unacceptable_framing_1_4": "2",
        "pv_dependency_1_4": "3",
        "general_cue_risk_1_4": "2",
        "decision": "revise_minor",
        "comment": "Deadline is not an official service/document; object-type cue remains strong.",
    },
    "pv_035": {
        "acceptable_natural_1_4": "4",
        "unacceptable_framing_1_4": "1",
        "pv_dependency_1_4": "2",
        "general_cue_risk_1_4": "4",
        "decision": "revise_major",
        "comment": "Ceiling creates a broad object mismatch; not a good past-event near-miss.",
    },
    "pv_036": {
        "acceptable_natural_1_4": "4",
        "unacceptable_framing_1_4": "2",
        "pv_dependency_1_4": "2",
        "general_cue_risk_1_4": "3",
        "decision": "revise_major",
        "comment": "Advice can change in quality/amount metaphorically; the key is ambiguous.",
    },
    "pv_037": {
        "acceptable_natural_1_4": "4",
        "unacceptable_framing_1_4": "2",
        "pv_dependency_1_4": "2",
        "general_cue_risk_1_4": "3",
        "decision": "revise_major",
        "comment": "Advice went down has competing idioms and is not a stable unacceptable item.",
    },
    "pv_038": {
        "acceptable_natural_1_4": "3",
        "unacceptable_framing_1_4": "2",
        "pv_dependency_1_4": "1",
        "general_cue_risk_1_4": "4",
        "decision": "drop_candidate",
        "comment": "Come on is discourse/prosody sensitive; audio intonation can flip the interpretation.",
    },
    "pv_039": {
        "acceptable_natural_1_4": "3",
        "unacceptable_framing_1_4": "1",
        "pv_dependency_1_4": "1",
        "general_cue_risk_1_4": "4",
        "decision": "revise_major",
        "comment": "During deadline is ungrammatical; item fails surface naturalness.",
    },
    "pv_040": {
        "acceptable_natural_1_4": "4",
        "unacceptable_framing_1_4": "1",
        "pv_dependency_1_4": "2",
        "general_cue_risk_1_4": "4",
        "decision": "revise_major",
        "comment": "Furniture as subject makes the item trivially odd for the reveal sense.",
    },
    "pv_041": {
        "acceptable_natural_1_4": "4",
        "unacceptable_framing_1_4": "1",
        "pv_dependency_1_4": "2",
        "general_cue_risk_1_4": "4",
        "decision": "revise_major",
        "comment": "Furniture is not an event/result; broad noun semantics solves the item.",
    },
    "pv_042": {
        "acceptable_natural_1_4": "4",
        "unacceptable_framing_1_4": "2",
        "pv_dependency_1_4": "3",
        "general_cue_risk_1_4": "2",
        "decision": "revise_minor",
        "comment": "Deadline is not a task/study; mismatch is local but object-type based.",
    },
    "pv_043": {
        "acceptable_natural_1_4": "4",
        "unacceptable_framing_1_4": "2",
        "pv_dependency_1_4": "3",
        "general_cue_risk_1_4": "2",
        "decision": "revise_minor",
        "comment": "Deadline is not an explanation/possibility; acceptable but could be a better near-miss.",
    },
    "pv_044": {
        "acceptable_natural_1_4": "4",
        "unacceptable_framing_1_4": "1",
        "pv_dependency_1_4": "2",
        "general_cue_risk_1_4": "4",
        "decision": "revise_major",
        "comment": "Pencil subject is trivially non-agentive; not enough PV-meaning dependency.",
    },
    "pv_045": {
        "acceptable_natural_1_4": "4",
        "unacceptable_framing_1_4": "2",
        "pv_dependency_1_4": "2",
        "general_cue_risk_1_4": "3",
        "decision": "revise_major",
        "comment": "Deadline object is a broad object-type cue; use a text/content near-miss.",
    },
    "pv_046": {
        "acceptable_natural_1_4": "4",
        "unacceptable_framing_1_4": "1",
        "pv_dependency_1_4": "2",
        "general_cue_risk_1_4": "4",
        "decision": "revise_major",
        "comment": "After furniture is surface-odd and does not test the follow-up sense cleanly.",
    },
    "pv_047": {
        "acceptable_natural_1_4": "4",
        "unacceptable_framing_1_4": "1",
        "pv_dependency_1_4": "2",
        "general_cue_risk_1_4": "4",
        "decision": "revise_major",
        "comment": "Chart plus spoon creates a broad object mismatch; lay out is also literal/polysemous.",
    },
    "pv_048": {
        "acceptable_natural_1_4": "4",
        "unacceptable_framing_1_4": "1",
        "pv_dependency_1_4": "2",
        "general_cue_risk_1_4": "4",
        "decision": "revise_major",
        "comment": "Carpet is a broad object mismatch and does not test solution calculation cleanly.",
    },
}


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def write_tsv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, delimiter="\t", extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    items = read_tsv(ITEMS)
    pairs: dict[str, dict[str, dict[str, str]]] = {}
    for row in items:
        pairs.setdefault(row["pv_id"], {})[row["condition"]] = row

    fields = [
        "pv_id",
        "pv",
        "acceptable_item_id",
        "acceptable_sentence",
        "unacceptable_item_id",
        "unacceptable_sentence",
        "acceptable_natural_1_4",
        "unacceptable_framing_1_4",
        "pv_dependency_1_4",
        "general_cue_risk_1_4",
        "decision",
        "expert_comment",
    ]

    rows = []
    counts: dict[str, int] = {}
    for pv_id in sorted(pairs):
        pair = pairs[pv_id]
        review = REVIEWS[pv_id]
        counts[review["decision"]] = counts.get(review["decision"], 0) + 1
        rows.append(
            {
                "pv_id": pv_id,
                "pv": pair["acceptable"]["pv"],
                "acceptable_item_id": pair["acceptable"]["ljt_item_id"],
                "acceptable_sentence": pair["acceptable"]["sentence_text"],
                "unacceptable_item_id": pair["unacceptable"]["ljt_item_id"],
                "unacceptable_sentence": pair["unacceptable"]["sentence_text"],
                "acceptable_natural_1_4": review["acceptable_natural_1_4"],
                "unacceptable_framing_1_4": review["unacceptable_framing_1_4"],
                "pv_dependency_1_4": review["pv_dependency_1_4"],
                "general_cue_risk_1_4": review["general_cue_risk_1_4"],
                "decision": review["decision"],
                "expert_comment": review["comment"],
            }
        )
    write_tsv(OUT_REVIEW, rows, fields)

    total = len(rows)
    revise_or_drop = sum(
        count for decision, count in counts.items() if decision not in {"keep", "keep_with_caution"}
    )
    summary = [
        "# LJT v5 semantic/naturalness expert review v1",
        "",
        "Conclusion: v5 passes the mechanical cue/word-count audit but does not pass semantic-naturalness review for production learner data.",
        "",
        "Decision counts:",
    ]
    for decision in sorted(counts):
        summary.append(f"- {decision}: {counts[decision]}")
    summary.extend(
        [
            "",
            f"Items requiring revision or dropping: {revise_or_drop} / {total}.",
            "",
            "Main failure mode: unacceptable sentences often become rejectable from broad noun/category oddness rather than from the target phrasal-verb meaning.",
            "",
            "Recommendation: do not treat v5 as production-ready. Build a v6 set from expert-reviewed near-miss contexts before using learner response data.",
        ]
    )
    OUT_SUMMARY.write_text("\n".join(summary) + "\n", encoding="utf-8")

    print(f"Wrote {OUT_REVIEW}")
    print(f"Wrote {OUT_SUMMARY}")


if __name__ == "__main__":
    main()
