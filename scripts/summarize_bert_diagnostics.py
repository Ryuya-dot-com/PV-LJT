#!/usr/bin/env python3
"""Summarize BERT/SBERT diagnostics into a review-priority file."""

from __future__ import annotations

import csv
import argparse
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PAIR_IN = ROOT / "materials" / "bert_pair_diagnostics_v1.tsv"
DEFAULT_EXPERT_FLAGS = ROOT / "materials" / "aural_pv_ljt_review_flags_v2_reviewed.tsv"
DEFAULT_PRIORITY_OUT = ROOT / "materials" / "bert_review_priorities_v1.tsv"
DEFAULT_SUMMARY_OUT = ROOT / "materials" / "bert_diagnostics_summary_v1.md"


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def write_tsv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pair-in", default=str(DEFAULT_PAIR_IN))
    parser.add_argument("--expert-flags", default=str(DEFAULT_EXPERT_FLAGS))
    parser.add_argument("--priority-out", default=str(DEFAULT_PRIORITY_OUT))
    parser.add_argument("--summary-out", default=str(DEFAULT_SUMMARY_OUT))
    parser.add_argument("--input-label", default="aural_pv_ljt_items_v2_reviewed.tsv")
    args = parser.parse_args()

    pair_in = Path(args.pair_in)
    expert_flags = Path(args.expert_flags)
    priority_out = Path(args.priority_out)
    summary_out = Path(args.summary_out)

    pairs = read_tsv(pair_in)
    expert = read_tsv(expert_flags)
    expert_by_pv = {r["pv"]: r for r in expert}

    rows: list[dict[str, object]] = []
    for r in pairs:
        flags = set(r["diagnostic_flags"].split(";")) if r["diagnostic_flags"] else set()
        expert_flag = r["pv"] in expert_by_pv
        reasons: list[str] = []
        priority = "low"

        if "low_context_similarity" in flags:
            priority = "high"
            reasons.append("acceptable/unacceptable contexts are relatively dissimilar")
        if expert_flag:
            if priority != "high":
                priority = "medium"
            reasons.append(f"expert-review flag: {expert_by_pv[r['pv']]['issue_type']}")
        if "target_fit_gap_extreme" in flags:
            if priority == "low":
                priority = "medium"
            reasons.append("BERT target-fit gap is unusually large")
        if "low_full_sentence_similarity" in flags and priority == "low":
            priority = "medium"
            reasons.append("full-sentence SBERT similarity is relatively low")

        # This flag is useful to inspect but too noisy to drive priority alone.
        if "target_fit_not_higher_for_acceptable" in flags:
            reasons.append("masked-LM target-fit direction is not as expected; interpret cautiously")

        if reasons:
            if "low_context_similarity" in flags:
                recommendation = "revise pair to keep non-target context more parallel, then rerun diagnostics"
            elif expert_flag:
                recommendation = "send to expert review before audio recording"
            elif "target_fit_gap_extreme" in flags:
                recommendation = "check whether the unacceptable sentence is too easy"
            else:
                recommendation = "inspect manually; BERT-only issue may not require revision"

            rows.append(
                {
                    "priority": priority,
                    "pv_id": r["pv_id"],
                    "pv": r["pv"],
                    "acceptable_item_id": r["acceptable_item_id"],
                    "unacceptable_item_id": r["unacceptable_item_id"],
                    "full_sentence_sbert_cosine": r["full_sentence_sbert_cosine"],
                    "context_without_pv_sbert_cosine": r[
                        "context_without_pv_sbert_cosine"
                    ],
                    "pll_mean_delta_acc_minus_unacc": r[
                        "pll_mean_delta_acc_minus_unacc"
                    ],
                    "target_fit_mean_delta_acc_minus_unacc": r[
                        "target_fit_mean_delta_acc_minus_unacc"
                    ],
                    "bert_flags": r["diagnostic_flags"],
                    "expert_flag": "yes" if expert_flag else "no",
                    "reason": "; ".join(reasons),
                    "recommendation": recommendation,
                    "acceptable_sentence": r["acceptable_sentence"],
                    "unacceptable_sentence": r["unacceptable_sentence"],
                }
            )

    order = {"high": 0, "medium": 1, "low": 2}
    rows.sort(
        key=lambda x: (
            order[str(x["priority"])],
            float(x["context_without_pv_sbert_cosine"]),
            str(x["pv"]),
        )
    )
    fields = list(rows[0].keys()) if rows else []
    write_tsv(priority_out, rows, fields)

    flag_counts = Counter()
    for r in pairs:
        for flag in r["diagnostic_flags"].split(";"):
            flag_counts[flag] += 1
    priority_counts = Counter(str(r["priority"]) for r in rows)

    high_rows = [r for r in rows if r["priority"] == "high"]
    medium_rows = [r for r in rows if r["priority"] == "medium"]

    summary = [
        "# BERT/SBERT Diagnostics Summary",
        "",
        f"Input: `{args.input_label}`",
        "",
        "Models:",
        "",
        "- Sentence embeddings: `sentence-transformers/all-MiniLM-L6-v2`",
        "- Masked LM diagnostics: `bert-base-uncased`",
        "",
        "Interpretation:",
        "",
        "- These metrics are item diagnostics, not automatic item decisions.",
        "- `target_fit_not_higher_for_acceptable` is noisy and should not drive revision by itself.",
        "- The most useful flags are low context similarity, extreme target-fit gaps, and large naturalness differences.",
        "",
        "Flag counts:",
        "",
    ]
    for flag, count in sorted(flag_counts.items()):
        summary.append(f"- `{flag}`: {count}")
    summary.extend(
        [
            "",
            "Priority counts:",
            "",
        ]
    )
    for priority, count in sorted(priority_counts.items()):
        summary.append(f"- `{priority}`: {count}")
    summary.extend(["", "High-priority items:", ""])
    if high_rows:
        for r in high_rows:
            summary.append(
                f"- `{r['pv']}` ({r['unacceptable_item_id']}): {r['reason']}"
            )
    else:
        summary.append("- none")
    summary.extend(["", "Medium-priority items:", ""])
    if medium_rows:
        for r in medium_rows:
            summary.append(
                f"- `{r['pv']}` ({r['unacceptable_item_id']}): {r['reason']}"
            )
    else:
        summary.append("- none")
    summary.extend(["", "Recommended next step:", ""])
    if high_rows:
        summary.append(
            "Review the high-priority items first. If they are revised, rerun `scripts/compute_bert_item_diagnostics.py` and this summary script."
        )
    elif medium_rows:
        summary.append(
            "No high-priority items remain. Review the medium-priority items before audio recording, especially those with expert-review flags."
        )
    else:
        summary.append(
            "No high- or medium-priority diagnostic items remain. Proceed to expert confirmation and audio recording preparation."
        )
    summary.append("")
    summary_out.write_text("\n".join(summary), encoding="utf-8")
    print(f"Wrote {priority_out}")
    print(f"Wrote {summary_out}")


if __name__ == "__main__":
    main()
