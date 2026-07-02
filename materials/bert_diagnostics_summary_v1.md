# BERT/SBERT Diagnostics Summary v1

Input: `aural_pv_ljt_items_v2_reviewed.tsv`

Models:

- Sentence embeddings: `sentence-transformers/all-MiniLM-L6-v2`
- Masked LM diagnostics: `bert-base-uncased`

Interpretation:

- These metrics are item diagnostics, not automatic item decisions.
- `target_fit_not_higher_for_acceptable` is noisy and should not drive revision by itself.
- The most useful flags are low context similarity, extreme target-fit gaps, and large naturalness differences.

Flag counts:

- `low_context_similarity`: 3
- `low_full_sentence_similarity`: 10
- `none`: 18
- `target_fit_gap_extreme`: 2
- `target_fit_not_higher_for_acceptable`: 25

Priority counts:

- `high`: 3
- `low`: 15
- `medium`: 14

High-priority items:

- `come in` (ljt_039b): acceptable/unacceptable contexts are relatively dissimilar; masked-LM target-fit direction is not as expected; interpret cautiously
- `rule out` (ljt_043b): acceptable/unacceptable contexts are relatively dissimilar
- `come out` (ljt_040b): acceptable/unacceptable contexts are relatively dissimilar; masked-LM target-fit direction is not as expected; interpret cautiously

Medium-priority items:

- `hold back` (ljt_007b): full-sentence SBERT similarity is relatively low
- `put in` (ljt_004b): full-sentence SBERT similarity is relatively low; masked-LM target-fit direction is not as expected; interpret cautiously
- `carry out` (ljt_042b): expert-review flag: academic_near_miss
- `take out` (ljt_034b): full-sentence SBERT similarity is relatively low; masked-LM target-fit direction is not as expected; interpret cautiously
- `bring in` (ljt_023b): full-sentence SBERT similarity is relatively low; masked-LM target-fit direction is not as expected; interpret cautiously
- `sit back` (ljt_006b): BERT target-fit gap is unusually large
- `put on` (ljt_015b): full-sentence SBERT similarity is relatively low; masked-LM target-fit direction is not as expected; interpret cautiously
- `cut off` (ljt_022b): expert-review flag: temporal_mismatch; masked-LM target-fit direction is not as expected; interpret cautiously
- `come along` (ljt_010b): expert-review flag: semantic_contradiction_strength; masked-LM target-fit direction is not as expected; interpret cautiously
- `lay out` (ljt_047b): expert-review flag: clarity_mismatch
- `give out` (ljt_003b): BERT target-fit gap is unusually large
- `work out` (ljt_048b): expert-review flag: method_mismatch
- `make out` (ljt_017b): expert-review flag: modality_mismatch; masked-LM target-fit direction is not as expected; interpret cautiously
- `come on` (ljt_038b): expert-review flag: prosody_sensitive; masked-LM target-fit direction is not as expected; interpret cautiously

Recommended next step:

Review the high-priority items first. If they are revised, rerun `scripts/compute_bert_item_diagnostics.py` and this summary script.
