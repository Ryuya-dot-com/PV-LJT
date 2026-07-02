# BERT/SBERT Diagnostics Summary

Input: `aural_pv_ljt_items_v4_pre_audio.tsv`

Models:

- Sentence embeddings: `sentence-transformers/all-MiniLM-L6-v2`
- Masked LM diagnostics: `bert-base-uncased`

Interpretation:

- These metrics are item diagnostics, not automatic item decisions.
- `target_fit_not_higher_for_acceptable` is noisy and should not drive revision by itself.
- The most useful flags are low context similarity, extreme target-fit gaps, and large naturalness differences.

Flag counts:

- `low_full_sentence_similarity`: 7
- `none`: 21
- `target_fit_gap_extreme`: 1
- `target_fit_not_higher_for_acceptable`: 25
- `unacceptable_much_less_natural`: 1

Priority counts:

- `low`: 17
- `medium`: 11

High-priority items:

- none

Medium-priority items:

- `carry out` (ljt_042b): expert-review flag: task_completion_contradiction; masked-LM target-fit direction is not as expected; interpret cautiously
- `lay out` (ljt_047b): expert-review flag: presentation_contradiction
- `take out` (ljt_034b): full-sentence SBERT similarity is relatively low; masked-LM target-fit direction is not as expected; interpret cautiously
- `bring in` (ljt_023b): full-sentence SBERT similarity is relatively low; masked-LM target-fit direction is not as expected; interpret cautiously
- `sit back` (ljt_006b): BERT target-fit gap is unusually large
- `put on` (ljt_015b): full-sentence SBERT similarity is relatively low; masked-LM target-fit direction is not as expected; interpret cautiously
- `work out` (ljt_048b): expert-review flag: solution_process_contradiction; masked-LM target-fit direction is not as expected; interpret cautiously
- `come along` (ljt_010b): expert-review flag: semantic_contradiction_strength; masked-LM target-fit direction is not as expected; interpret cautiously
- `cut off` (ljt_022b): expert-review flag: temporal_mismatch; masked-LM target-fit direction is not as expected; interpret cautiously
- `make out` (ljt_017b): expert-review flag: clarity_contradiction
- `come on` (ljt_038b): expert-review flag: prosody_sensitive; masked-LM target-fit direction is not as expected; interpret cautiously

Recommended next step:

No high-priority items remain. Review the medium-priority items before audio recording, especially those with expert-review flags.
