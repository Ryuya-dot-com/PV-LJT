#!/usr/bin/env python3
"""Compute BERT/SBERT diagnostics for PV-LJT candidate sentences.

Outputs:
- materials/bert_item_diagnostics_v1.tsv
- materials/bert_pair_diagnostics_v1.tsv

The metrics are diagnostics for expert review, not automatic item decisions.
"""

from __future__ import annotations

import csv
import argparse
import math
import re
from collections import defaultdict
from pathlib import Path
from statistics import median

import numpy as np
import torch
from sentence_transformers import SentenceTransformer
from transformers import AutoModelForMaskedLM, AutoTokenizer


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "materials" / "aural_pv_ljt_items_v2_reviewed.tsv"
DEFAULT_ITEM_OUT = ROOT / "materials" / "bert_item_diagnostics_v1.tsv"
DEFAULT_PAIR_OUT = ROOT / "materials" / "bert_pair_diagnostics_v1.tsv"

SBERT_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
MLM_MODEL = "bert-base-uncased"


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def write_tsv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)


def cosine(a: np.ndarray, b: np.ndarray) -> float:
    denom = np.linalg.norm(a) * np.linalg.norm(b)
    if denom == 0:
        return float("nan")
    return float(np.dot(a, b) / denom)


def replace_target(sentence: str, target_form: str, replacement: str = "[PV]") -> str:
    pattern = re.compile(re.escape(target_form), flags=re.IGNORECASE)
    return pattern.sub(replacement, sentence, count=1)


def split_target(sentence: str, target_form: str) -> tuple[str, str, str] | None:
    match = re.search(re.escape(target_form), sentence, flags=re.IGNORECASE)
    if not match:
        return None
    return sentence[: match.start()], sentence[match.start() : match.end()], sentence[match.end() :]


class MaskedLmScorer:
    def __init__(self, model_name: str) -> None:
        self.device = torch.device("cpu")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForMaskedLM.from_pretrained(model_name).to(self.device)
        self.model.eval()

    @torch.no_grad()
    def pseudo_log_likelihood(self, sentence: str) -> tuple[float, float, int]:
        enc = self.tokenizer(sentence, return_tensors="pt")
        input_ids = enc["input_ids"].to(self.device)
        attention_mask = enc.get("attention_mask")
        if attention_mask is not None:
            attention_mask = attention_mask.to(self.device)
        special_ids = set(self.tokenizer.all_special_ids)
        positions = [
            i
            for i, token_id in enumerate(input_ids[0].tolist())
            if token_id not in special_ids
        ]
        log_probs: list[float] = []
        for pos in positions:
            masked = input_ids.clone()
            target_id = int(masked[0, pos].item())
            masked[0, pos] = self.tokenizer.mask_token_id
            kwargs = {"input_ids": masked}
            if attention_mask is not None:
                kwargs["attention_mask"] = attention_mask
            logits = self.model(**kwargs).logits[0, pos]
            log_prob = torch.log_softmax(logits, dim=-1)[target_id].item()
            log_probs.append(float(log_prob))
        if not log_probs:
            return float("nan"), float("nan"), 0
        return float(sum(log_probs)), float(sum(log_probs) / len(log_probs)), len(log_probs)

    @torch.no_grad()
    def target_fit_logprob(self, sentence: str, target_form: str) -> tuple[float, float, int]:
        split = split_target(sentence, target_form)
        if split is None:
            return float("nan"), float("nan"), 0
        before, target, after = split
        before_ids = self.tokenizer(before, add_special_tokens=False)["input_ids"]
        target_ids = self.tokenizer(target.strip(), add_special_tokens=False)["input_ids"]
        after_ids = self.tokenizer(after, add_special_tokens=False)["input_ids"]
        if not target_ids:
            return float("nan"), float("nan"), 0
        input_ids = (
            [self.tokenizer.cls_token_id]
            + before_ids
            + [self.tokenizer.mask_token_id] * len(target_ids)
            + after_ids
            + [self.tokenizer.sep_token_id]
        )
        mask_start = 1 + len(before_ids)
        tensor = torch.tensor([input_ids], dtype=torch.long, device=self.device)
        logits = self.model(input_ids=tensor).logits[0]
        log_probs: list[float] = []
        for offset, target_id in enumerate(target_ids):
            pos = mask_start + offset
            lp = torch.log_softmax(logits[pos], dim=-1)[target_id].item()
            log_probs.append(float(lp))
        return float(sum(log_probs)), float(sum(log_probs) / len(log_probs)), len(log_probs)


def robust_high_flags(values: list[float], multiplier: float = 1.5) -> float:
    clean = [v for v in values if not math.isnan(v)]
    if len(clean) < 4:
        return float("inf")
    q1, q3 = np.percentile(clean, [25, 75])
    return float(q3 + multiplier * (q3 - q1))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default=str(DEFAULT_INPUT))
    parser.add_argument("--item-out", default=str(DEFAULT_ITEM_OUT))
    parser.add_argument("--pair-out", default=str(DEFAULT_PAIR_OUT))
    args = parser.parse_args()

    input_path = Path(args.input)
    item_out = Path(args.item_out)
    pair_out = Path(args.pair_out)

    rows = read_tsv(input_path)
    if not rows:
        raise SystemExit(f"No rows found: {input_path}")

    print(f"Loading SBERT model: {SBERT_MODEL}")
    sbert = SentenceTransformer(SBERT_MODEL, device="cpu")
    print(f"Loading masked LM model: {MLM_MODEL}")
    scorer = MaskedLmScorer(MLM_MODEL)

    sentences = [r["sentence_text"] for r in rows]
    contexts = [replace_target(r["sentence_text"], r["target_form"]) for r in rows]
    print(f"Encoding {len(sentences)} sentences and contexts")
    sent_emb = sbert.encode(sentences, normalize_embeddings=True, show_progress_bar=False)
    context_emb = sbert.encode(contexts, normalize_embeddings=True, show_progress_bar=False)

    by_id = {r["ljt_item_id"]: r for r in rows}
    by_pv_id: dict[str, dict[str, dict[str, str]]] = defaultdict(dict)
    for idx, r in enumerate(rows):
        r["_row_index"] = str(idx)
        by_pv_id[r["pv_id"]][r["condition"]] = r

    print("Scoring masked-LM diagnostics")
    item_metrics: dict[str, dict[str, object]] = {}
    for i, r in enumerate(rows, start=1):
        if i % 10 == 0:
            print(f"  scored {i}/{len(rows)}")
        pll_sum, pll_mean, token_n = scorer.pseudo_log_likelihood(r["sentence_text"])
        fit_sum, fit_mean, target_token_n = scorer.target_fit_logprob(
            r["sentence_text"], r["target_form"]
        )
        item_metrics[r["ljt_item_id"]] = {
            "pll_sum_logprob": pll_sum,
            "pll_mean_logprob": pll_mean,
            "pll_token_n": token_n,
            "target_fit_sum_logprob": fit_sum,
            "target_fit_mean_logprob": fit_mean,
            "target_token_n": target_token_n,
        }

    pair_rows: list[dict[str, object]] = []
    for pv_id, pair in sorted(by_pv_id.items()):
        acc = pair.get("acceptable")
        unacc = pair.get("unacceptable")
        if not acc or not unacc:
            continue
        ai = int(acc["_row_index"])
        ui = int(unacc["_row_index"])
        full_cos = cosine(sent_emb[ai], sent_emb[ui])
        context_cos = cosine(context_emb[ai], context_emb[ui])
        acc_m = item_metrics[acc["ljt_item_id"]]
        unacc_m = item_metrics[unacc["ljt_item_id"]]
        pll_delta = float(acc_m["pll_mean_logprob"]) - float(unacc_m["pll_mean_logprob"])
        fit_delta = float(acc_m["target_fit_mean_logprob"]) - float(
            unacc_m["target_fit_mean_logprob"]
        )
        pair_rows.append(
            {
                "pv_id": pv_id,
                "pv": acc["pv"],
                "acceptable_item_id": acc["ljt_item_id"],
                "unacceptable_item_id": unacc["ljt_item_id"],
                "full_sentence_sbert_cosine": full_cos,
                "context_without_pv_sbert_cosine": context_cos,
                "pll_mean_delta_acc_minus_unacc": pll_delta,
                "target_fit_mean_delta_acc_minus_unacc": fit_delta,
                "acceptable_sentence": acc["sentence_text"],
                "unacceptable_sentence": unacc["sentence_text"],
            }
        )

    pll_high = robust_high_flags(
        [float(r["pll_mean_delta_acc_minus_unacc"]) for r in pair_rows]
    )
    fit_high = robust_high_flags(
        [float(r["target_fit_mean_delta_acc_minus_unacc"]) for r in pair_rows]
    )

    pair_lookup = {}
    for p in pair_rows:
        flags: list[str] = []
        if float(p["context_without_pv_sbert_cosine"]) < 0.70:
            flags.append("low_context_similarity")
        if float(p["full_sentence_sbert_cosine"]) < 0.65:
            flags.append("low_full_sentence_similarity")
        if float(p["pll_mean_delta_acc_minus_unacc"]) > pll_high:
            flags.append("unacceptable_much_less_natural")
        if float(p["target_fit_mean_delta_acc_minus_unacc"]) <= 0:
            flags.append("target_fit_not_higher_for_acceptable")
        if float(p["target_fit_mean_delta_acc_minus_unacc"]) > fit_high:
            flags.append("target_fit_gap_extreme")
        p["diagnostic_flags"] = ";".join(flags) if flags else "none"
        pair_lookup[p["pv_id"]] = p

    item_rows: list[dict[str, object]] = []
    for r in rows:
        pair = pair_lookup[r["pv_id"]]
        m = item_metrics[r["ljt_item_id"]]
        item_rows.append(
            {
                "ljt_item_id": r["ljt_item_id"],
                "pv_id": r["pv_id"],
                "pv": r["pv"],
                "condition": r["condition"],
                "target_form": r["target_form"],
                "sentence_text": r["sentence_text"],
                "intended_sense": r["intended_sense"],
                "mismatch_type": r["mismatch_type"],
                "pll_mean_logprob": m["pll_mean_logprob"],
                "pll_sum_logprob": m["pll_sum_logprob"],
                "pll_token_n": m["pll_token_n"],
                "target_fit_mean_logprob": m["target_fit_mean_logprob"],
                "target_fit_sum_logprob": m["target_fit_sum_logprob"],
                "target_token_n": m["target_token_n"],
                "full_sentence_sbert_cosine_pair": pair["full_sentence_sbert_cosine"],
                "context_without_pv_sbert_cosine_pair": pair[
                    "context_without_pv_sbert_cosine"
                ],
                "pll_mean_delta_acc_minus_unacc_pair": pair[
                    "pll_mean_delta_acc_minus_unacc"
                ],
                "target_fit_mean_delta_acc_minus_unacc_pair": pair[
                    "target_fit_mean_delta_acc_minus_unacc"
                ],
                "diagnostic_flags_pair": pair["diagnostic_flags"],
            }
        )

    item_fields = list(item_rows[0].keys())
    pair_fields = list(pair_rows[0].keys())
    write_tsv(item_out, item_rows, item_fields)
    write_tsv(pair_out, pair_rows, pair_fields)
    print(f"Wrote {item_out}")
    print(f"Wrote {pair_out}")
    print(f"Pair PLL high threshold: {pll_high:.4f}")
    print(f"Pair target-fit high threshold: {fit_high:.4f}")
    print("Flag counts:")
    counts: dict[str, int] = defaultdict(int)
    for p in pair_rows:
        for flag in str(p["diagnostic_flags"]).split(";"):
            counts[flag] += 1
    for key in sorted(counts):
        print(f"  {key}: {counts[key]}")


if __name__ == "__main__":
    main()
