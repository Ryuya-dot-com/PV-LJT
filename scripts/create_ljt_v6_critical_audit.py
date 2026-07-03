#!/usr/bin/env python3
"""Create a critical, multi-perspective audit for the next PV-LJT revision."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MATERIALS = ROOT / "materials"

MASTER = MATERIALS / "three_stage_pv_master_v5_production.tsv"
V5_REVIEW = MATERIALS / "ljt_v5_semantic_naturalness_expert_review_v1.tsv"

OUT_ITEM = MATERIALS / "ljt_v6_item_feasibility_audit_v1.tsv"
OUT_REPORT = MATERIALS / "ljt_v6_critical_design_audit_v1.md"


# Ratings:
# construct_fit_1_4: 4 = strong candidate for LJT, 1 = poor candidate.
# polysemy_risk_1_4 / audio_risk_1_4: 1 = low risk, 4 = high risk.
# near_miss_feasibility_1_4: 4 = near-miss contexts are feasible.
ITEM_AUDIT: dict[str, dict[str, str]] = {
    "pv_001": {
        "construct_fit_1_4": "3",
        "near_miss_feasibility_1_4": "3",
        "polysemy_risk_1_4": "2",
        "audio_risk_1_4": "1",
        "v6_action": "revise",
        "critical_note": "Use negotiation/relationship contexts; avoid object-category anomalies such as agenda.",
    },
    "pv_002": {
        "construct_fit_1_4": "3",
        "near_miss_feasibility_1_4": "3",
        "polysemy_risk_1_4": "2",
        "audio_risk_1_4": "1",
        "v6_action": "revise",
        "critical_note": "Use possession/control-transfer contexts with plausible entities; avoid non-transferable abstractions.",
    },
    "pv_003": {
        "construct_fit_1_4": "2",
        "near_miss_feasibility_1_4": "2",
        "polysemy_risk_1_4": "3",
        "audio_risk_1_4": "2",
        "v6_action": "replace_or_rewrite",
        "critical_note": "Collapse/fail sense is difficult without obvious world-knowledge cues; may require dropping.",
    },
    "pv_004": {
        "construct_fit_1_4": "2",
        "near_miss_feasibility_1_4": "2",
        "polysemy_risk_1_4": "4",
        "audio_risk_1_4": "1",
        "v6_action": "replace_or_rewrite",
        "critical_note": "Put in has many literal/legal/work senses; near-miss control is unstable.",
    },
    "pv_005": {
        "construct_fit_1_4": "2",
        "near_miss_feasibility_1_4": "2",
        "polysemy_risk_1_4": "4",
        "audio_risk_1_4": "1",
        "v6_action": "replace_or_rewrite",
        "critical_note": "Comprehension sense overlaps with physical taking-in and intake senses; hard to isolate in one sentence.",
    },
    "pv_006": {
        "construct_fit_1_4": "2",
        "near_miss_feasibility_1_4": "2",
        "polysemy_risk_1_4": "4",
        "audio_risk_1_4": "3",
        "v6_action": "replace_or_rewrite",
        "critical_note": "Posture and passive-inaction senses compete; intonation/context may decide the interpretation.",
    },
    "pv_007": {
        "construct_fit_1_4": "2",
        "near_miss_feasibility_1_4": "2",
        "polysemy_risk_1_4": "3",
        "audio_risk_1_4": "1",
        "v6_action": "replace_or_rewrite",
        "critical_note": "Prevent-progress meaning is causal and world-knowledge heavy; near-miss contexts are fragile.",
    },
    "pv_008": {
        "construct_fit_1_4": "4",
        "near_miss_feasibility_1_4": "4",
        "polysemy_risk_1_4": "2",
        "audio_risk_1_4": "1",
        "v6_action": "keep_revise_lightly",
        "critical_note": "Hierarchy/status contrast is locally tied to the PV and comparatively robust.",
    },
    "pv_009": {
        "construct_fit_1_4": "3",
        "near_miss_feasibility_1_4": "3",
        "polysemy_risk_1_4": "3",
        "audio_risk_1_4": "1",
        "v6_action": "revise",
        "critical_note": "Transport sense is clear, but unacceptable item must remain in transport context rather than object category.",
    },
    "pv_010": {
        "construct_fit_1_4": "2",
        "near_miss_feasibility_1_4": "2",
        "polysemy_risk_1_4": "4",
        "audio_risk_1_4": "2",
        "v6_action": "replace_or_rewrite",
        "critical_note": "Appear/arrive sense is too broad; many nouns can naturally come along.",
    },
    "pv_011": {
        "construct_fit_1_4": "3",
        "near_miss_feasibility_1_4": "3",
        "polysemy_risk_1_4": "2",
        "audio_risk_1_4": "1",
        "v6_action": "revise",
        "critical_note": "Use comparison among same-class candidates; avoid odd comparison sets.",
    },
    "pv_012": {
        "construct_fit_1_4": "3",
        "near_miss_feasibility_1_4": "3",
        "polysemy_risk_1_4": "2",
        "audio_risk_1_4": "1",
        "v6_action": "revise",
        "critical_note": "Withdrawal sense can work if both conditions describe activities or commitments.",
    },
    "pv_013": {
        "construct_fit_1_4": "3",
        "near_miss_feasibility_1_4": "3",
        "polysemy_risk_1_4": "2",
        "audio_risk_1_4": "1",
        "v6_action": "revise",
        "critical_note": "Depletion can be tested with countable resources; avoid impossible object categories.",
    },
    "pv_014": {
        "construct_fit_1_4": "3",
        "near_miss_feasibility_1_4": "3",
        "polysemy_risk_1_4": "3",
        "audio_risk_1_4": "1",
        "v6_action": "revise",
        "critical_note": "Authority-transfer sense can work, but literal turning-over sense must be suppressed.",
    },
    "pv_015": {
        "construct_fit_1_4": "3",
        "near_miss_feasibility_1_4": "3",
        "polysemy_risk_1_4": "3",
        "audio_risk_1_4": "1",
        "v6_action": "revise",
        "critical_note": "Event-staging sense can work, but clothing/application senses are strong competitors.",
    },
    "pv_016": {
        "construct_fit_1_4": "3",
        "near_miss_feasibility_1_4": "3",
        "polysemy_risk_1_4": "2",
        "audio_risk_1_4": "1",
        "v6_action": "revise",
        "critical_note": "Use regain-control contexts; current acceptable sentence also needs rewriting.",
    },
    "pv_017": {
        "construct_fit_1_4": "1",
        "near_miss_feasibility_1_4": "1",
        "polysemy_risk_1_4": "4",
        "audio_risk_1_4": "2",
        "v6_action": "drop",
        "critical_note": "Make out is too flexible across visual, auditory, and inferential senses; keyed unacceptable was unsafe.",
    },
    "pv_018": {
        "construct_fit_1_4": "3",
        "near_miss_feasibility_1_4": "3",
        "polysemy_risk_1_4": "2",
        "audio_risk_1_4": "1",
        "v6_action": "revise",
        "critical_note": "Outcome-benefit sense can work if effort/investment and result are controlled.",
    },
    "pv_019": {
        "construct_fit_1_4": "3",
        "near_miss_feasibility_1_4": "3",
        "polysemy_risk_1_4": "4",
        "audio_risk_1_4": "1",
        "v6_action": "revise",
        "critical_note": "Vehicle-leaving sense can work in travel contexts; avoid broad non-vehicle objects.",
    },
    "pv_020": {
        "construct_fit_1_4": "3",
        "near_miss_feasibility_1_4": "3",
        "polysemy_risk_1_4": "4",
        "audio_risk_1_4": "1",
        "v6_action": "revise",
        "critical_note": "Arrival sense can work, but turn up also means increase volume and be found.",
    },
    "pv_021": {
        "construct_fit_1_4": "2",
        "near_miss_feasibility_1_4": "2",
        "polysemy_risk_1_4": "4",
        "audio_risk_1_4": "1",
        "v6_action": "replace_or_rewrite",
        "critical_note": "Body-position sense is transparent and heavily physical; near-miss likely becomes world-knowledge cue.",
    },
    "pv_022": {
        "construct_fit_1_4": "3",
        "near_miss_feasibility_1_4": "3",
        "polysemy_risk_1_4": "4",
        "audio_risk_1_4": "1",
        "v6_action": "revise",
        "critical_note": "Interruption sense can work with speaking contexts; avoid object-cutting/service-stop senses.",
    },
    "pv_023": {
        "construct_fit_1_4": "3",
        "near_miss_feasibility_1_4": "3",
        "polysemy_risk_1_4": "4",
        "audio_risk_1_4": "1",
        "v6_action": "revise",
        "critical_note": "Recruit/ask-someone sense requires human role contexts; many abstractions can be brought in.",
    },
    "pv_024": {
        "construct_fit_1_4": "2",
        "near_miss_feasibility_1_4": "2",
        "polysemy_risk_1_4": "4",
        "audio_risk_1_4": "1",
        "v6_action": "replace_or_rewrite",
        "critical_note": "Put out has too many senses; public-release sense is difficult to isolate in one sentence.",
    },
    "pv_025": {
        "construct_fit_1_4": "2",
        "near_miss_feasibility_1_4": "2",
        "polysemy_risk_1_4": "3",
        "audio_risk_1_4": "1",
        "v6_action": "replace_or_rewrite",
        "critical_note": "Remove-unacceptable-content sense is abstract and often solved from object cleanability.",
    },
    "pv_026": {
        "construct_fit_1_4": "3",
        "near_miss_feasibility_1_4": "3",
        "polysemy_risk_1_4": "4",
        "audio_risk_1_4": "1",
        "v6_action": "revise",
        "critical_note": "Explain/present-clearly sense can work in report/policy contexts; literal laying-out/travel senses compete.",
    },
    "pv_027": {
        "construct_fit_1_4": "3",
        "near_miss_feasibility_1_4": "3",
        "polysemy_risk_1_4": "4",
        "audio_risk_1_4": "1",
        "v6_action": "revise",
        "critical_note": "Analysis/decomposition sense can work with problem/task contexts; avoid physical failure sense.",
    },
    "pv_028": {
        "construct_fit_1_4": "3",
        "near_miss_feasibility_1_4": "3",
        "polysemy_risk_1_4": "3",
        "audio_risk_1_4": "1",
        "v6_action": "revise",
        "critical_note": "Communication/help sense can work with human/institutional recipients.",
    },
    "pv_029": {
        "construct_fit_1_4": "2",
        "near_miss_feasibility_1_4": "2",
        "polysemy_risk_1_4": "4",
        "audio_risk_1_4": "1",
        "v6_action": "replace_or_rewrite",
        "critical_note": "Continuation sense is broad and formulaic; current item invites object-category anomalies.",
    },
    "pv_030": {
        "construct_fit_1_4": "3",
        "near_miss_feasibility_1_4": "3",
        "polysemy_risk_1_4": "4",
        "audio_risk_1_4": "1",
        "v6_action": "revise",
        "critical_note": "Display/attach sense can work but must avoid build/tolerate/price-increase senses.",
    },
    "pv_031": {
        "construct_fit_1_4": "3",
        "near_miss_feasibility_1_4": "3",
        "polysemy_risk_1_4": "3",
        "audio_risk_1_4": "1",
        "v6_action": "revise",
        "critical_note": "Improvement-after-problems sense can work with teams/companies if outcome words are controlled.",
    },
    "pv_032": {
        "construct_fit_1_4": "3",
        "near_miss_feasibility_1_4": "3",
        "polysemy_risk_1_4": "4",
        "audio_risk_1_4": "1",
        "v6_action": "revise",
        "critical_note": "Evidence-support sense can work; computer copy/reverse senses must be suppressed.",
    },
    "pv_033": {
        "construct_fit_1_4": "2",
        "near_miss_feasibility_1_4": "2",
        "polysemy_risk_1_4": "4",
        "audio_risk_1_4": "1",
        "v6_action": "replace_or_rewrite",
        "critical_note": "Look outside sense is transparent and physical; near-miss tends to be object-category based.",
    },
    "pv_034": {
        "construct_fit_1_4": "3",
        "near_miss_feasibility_1_4": "3",
        "polysemy_risk_1_4": "4",
        "audio_risk_1_4": "1",
        "v6_action": "revise",
        "critical_note": "Official-service sense can work with loans/policies; remove-from-container and social-date senses compete.",
    },
    "pv_035": {
        "construct_fit_1_4": "2",
        "near_miss_feasibility_1_4": "2",
        "polysemy_risk_1_4": "4",
        "audio_risk_1_4": "1",
        "v6_action": "replace_or_rewrite",
        "critical_note": "Past-event recollection sense is hard to mismatch without temporal/common-sense cues.",
    },
    "pv_036": {
        "construct_fit_1_4": "2",
        "near_miss_feasibility_1_4": "2",
        "polysemy_risk_1_4": "3",
        "audio_risk_1_4": "1",
        "v6_action": "replace_or_rewrite",
        "critical_note": "Increase sense is transparent and likely solved by numbers/world knowledge.",
    },
    "pv_037": {
        "construct_fit_1_4": "2",
        "near_miss_feasibility_1_4": "2",
        "polysemy_risk_1_4": "3",
        "audio_risk_1_4": "1",
        "v6_action": "replace_or_rewrite",
        "critical_note": "Decrease sense is transparent and likely solved by numbers/world knowledge.",
    },
    "pv_038": {
        "construct_fit_1_4": "1",
        "near_miss_feasibility_1_4": "1",
        "polysemy_risk_1_4": "4",
        "audio_risk_1_4": "4",
        "v6_action": "drop",
        "critical_note": "Discourse marker is prosody-dependent and unsuitable for stable audio LJT keying.",
    },
    "pv_039": {
        "construct_fit_1_4": "2",
        "near_miss_feasibility_1_4": "2",
        "polysemy_risk_1_4": "4",
        "audio_risk_1_4": "1",
        "v6_action": "replace_or_rewrite",
        "critical_note": "Become-involved sense competes with literal enter-place sense; near-miss contexts are difficult.",
    },
    "pv_040": {
        "construct_fit_1_4": "3",
        "near_miss_feasibility_1_4": "3",
        "polysemy_risk_1_4": "3",
        "audio_risk_1_4": "1",
        "v6_action": "revise",
        "critical_note": "Reveal sense can work with information/truth/news contexts; avoid subject-category anomalies.",
    },
    "pv_041": {
        "construct_fit_1_4": "3",
        "near_miss_feasibility_1_4": "3",
        "polysemy_risk_1_4": "2",
        "audio_risk_1_4": "1",
        "v6_action": "revise",
        "critical_note": "Causation sense can work in academic contexts if result nouns are controlled.",
    },
    "pv_042": {
        "construct_fit_1_4": "4",
        "near_miss_feasibility_1_4": "4",
        "polysemy_risk_1_4": "2",
        "audio_risk_1_4": "1",
        "v6_action": "keep_revise_lightly",
        "critical_note": "Conduct/perform task sense is strong for academic LJT; use plausible wrong task objects.",
    },
    "pv_043": {
        "construct_fit_1_4": "4",
        "near_miss_feasibility_1_4": "4",
        "polysemy_risk_1_4": "2",
        "audio_risk_1_4": "1",
        "v6_action": "keep_revise_lightly",
        "critical_note": "Exclude-possibility sense is a strong academic candidate with manageable near-misses.",
    },
    "pv_044": {
        "construct_fit_1_4": "4",
        "near_miss_feasibility_1_4": "4",
        "polysemy_risk_1_4": "2",
        "audio_risk_1_4": "1",
        "v6_action": "keep_revise_lightly",
        "critical_note": "Draw-attention sense is strong if both sentences keep human/author subjects.",
    },
    "pv_045": {
        "construct_fit_1_4": "4",
        "near_miss_feasibility_1_4": "4",
        "polysemy_risk_1_4": "2",
        "audio_risk_1_4": "1",
        "v6_action": "keep_revise_lightly",
        "critical_note": "Summarize-content sense is strong if both conditions use text/content objects.",
    },
    "pv_046": {
        "construct_fit_1_4": "3",
        "near_miss_feasibility_1_4": "3",
        "polysemy_risk_1_4": "3",
        "audio_risk_1_4": "1",
        "v6_action": "revise",
        "critical_note": "Further-action sense can work with medical/research follow-up contexts.",
    },
    "pv_047": {
        "construct_fit_1_4": "4",
        "near_miss_feasibility_1_4": "4",
        "polysemy_risk_1_4": "3",
        "audio_risk_1_4": "1",
        "v6_action": "keep_revise_lightly",
        "critical_note": "Present/organize-information sense is strong, but literal arrangement sense must be avoided.",
    },
    "pv_048": {
        "construct_fit_1_4": "4",
        "near_miss_feasibility_1_4": "4",
        "polysemy_risk_1_4": "3",
        "audio_risk_1_4": "1",
        "v6_action": "keep_revise_lightly",
        "critical_note": "Solution/calculation sense is strong if both conditions involve problems or quantities.",
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
    master = {row["pv_id"]: row for row in read_tsv(MASTER)}
    v5 = {row["pv_id"]: row for row in read_tsv(V5_REVIEW)}

    fields = [
        "pv_id",
        "pv",
        "source",
        "meaning",
        "register_focus",
        "v5_decision",
        "v5_general_cue_risk_1_4",
        "v5_pv_dependency_1_4",
        "construct_fit_1_4",
        "near_miss_feasibility_1_4",
        "polysemy_risk_1_4",
        "audio_risk_1_4",
        "v6_action",
        "critical_note",
    ]

    rows = []
    for pv_id in sorted(master):
        m = master[pv_id]
        review = v5[pv_id]
        audit = ITEM_AUDIT[pv_id]
        rows.append(
            {
                "pv_id": pv_id,
                "pv": m["pv"],
                "source": m["source"],
                "meaning": m["meaning"],
                "register_focus": m["register_focus"],
                "v5_decision": review["decision"],
                "v5_general_cue_risk_1_4": review["general_cue_risk_1_4"],
                "v5_pv_dependency_1_4": review["pv_dependency_1_4"],
                **audit,
            }
        )
    write_tsv(OUT_ITEM, rows, fields)

    action_counts: dict[str, int] = {}
    construct_counts: dict[str, int] = {}
    high_polysemy = 0
    for row in rows:
        action_counts[row["v6_action"]] = action_counts.get(row["v6_action"], 0) + 1
        construct_counts[row["construct_fit_1_4"]] = (
            construct_counts.get(row["construct_fit_1_4"], 0) + 1
        )
        if int(row["polysemy_risk_1_4"]) >= 4:
            high_polysemy += 1

    report = [
        "# LJT v6 critical design audit v1",
        "",
        "## Bottom line",
        "",
        "The v5 revision solved surface-level mechanical problems, but it did not solve construct validity. The next version should not start from the assumption that all 48 PVs are equally usable in an audio LJT. Several targets are too polysemous, too transparent, too prosody-dependent, or too reliant on world knowledge for stable acceptability judgment.",
        "",
        "## Audit lenses",
        "",
        "1. Construct validity: Does the item require access to the intended PV meaning?",
        "2. Linguistic naturalness: Is the acceptable sentence natural and is the unacceptable sentence a controlled near-miss rather than nonsense?",
        "3. Cue control: Can participants solve the item from discourse markers, negation, animacy, noun category, numbers, or world knowledge?",
        "4. Polysemy control: Are competing literal or idiomatic senses suppressed by context?",
        "5. Audio stability: Is the key robust to intonation, pauses, TTS prosody, and short-term memory load?",
        "6. Analysis readiness: Can item-level exclusions and list balancing be justified before learner data collection?",
        "",
        "## v6 action counts",
        "",
    ]
    for key in sorted(action_counts):
        report.append(f"- {key}: {action_counts[key]}")
    report.extend(
        [
            "",
            "## Construct-fit counts",
            "",
        ]
    )
    for key in sorted(construct_counts):
        report.append(f"- rating {key}: {construct_counts[key]}")
    report.extend(
        [
            "",
            f"High polysemy risk items: {high_polysemy} / {len(rows)}.",
            "",
            "## Critical decisions",
            "",
            "- Drop immediately: `make out`, `come on`.",
            "- Strongest candidates for v6: `move up`, `carry out`, `rule out`, `point out`, `sum up`, `lay out`, `work out`.",
            "- Do not record v6 until item-level semantic-naturalness review passes; mechanical audit alone is insufficient.",
            "- For each unacceptable item, require a written rationale showing why rejection depends on the target PV sense rather than a broad category mismatch.",
            "- Prefer same-domain near-misses: human vs human, task vs task, document vs document, event vs event, quantity vs quantity.",
            "- Avoid impossible nouns, non-agentive subjects, overt negation, adversative conjunctions, and transparent number reversals.",
            "",
            "## Required gate before audio generation",
            "",
            "A v6 item may be recorded only if it passes all of the following:",
            "",
            "- acceptable naturalness >= 3/4",
            "- unacceptable framing >= 3/4",
            "- PV dependency >= 3/4",
            "- general cue risk <= 2/4",
            "- no overt contrast or negation cue",
            "- matched or near-matched word count",
            "- no plausible alternate PV sense that makes the keyed unacceptable item acceptable",
            "",
            "See `ljt_v6_item_feasibility_audit_v1.tsv` for item-level decisions.",
        ]
    )
    OUT_REPORT.write_text("\n".join(report) + "\n", encoding="utf-8")

    print(f"Wrote {OUT_ITEM}")
    print(f"Wrote {OUT_REPORT}")


if __name__ == "__main__":
    main()
