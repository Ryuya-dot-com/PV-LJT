# Subagent Expert Review Summary

Reviewer: Godel

Scope:

- `aural_pv_ljt_items_v1.tsv`
- 96 candidate LJT sentences
- focus on semantic appropriateness, target sense control, alternative-sense risk, audio suitability, and whether unacceptable items can be solved without processing the PV.

## Main Finding

The acceptable items were generally aligned with the intended PV senses.

The main weakness was in the unacceptable items. Many v1 unacceptable sentences used obviously anomalous nouns such as `weather`, `cloud`, `silence`, `soup`, `chair`, `rain`, and `thunderstorm`. These items risked being rejected because the whole sentence was odd, not because the learner processed the target phrasal verb meaning.

## Action Taken

Created a reviewed v2 LJT set:

- `aural_pv_ljt_items_v2_reviewed.tsv`
- `aural_pv_ljt_list_assignment_v2_reviewed.tsv`
- `aural_pv_ljt_list_A_v2_reviewed.tsv`
- `aural_pv_ljt_list_B_v2_reviewed.tsv`
- `aural_pv_ljt_expert_review_form_v2_reviewed.tsv`
- `three_stage_pv_master_v2_reviewed.tsv`

In v2, unacceptable items were rewritten as near-miss semantic contradictions or controlled semantic mismatches.

Examples:

- v1: `The guard handed over the weather to the manager.`
- v2: `The guard handed over the keys but kept them in his pocket.`

- v1: `The researchers carried out the thunderstorm in three schools.`
- v2: `The researchers carried out the hypothesis in three schools.`

- v1: `The doctor followed up the test with a cloud.`
- v2: `The doctor followed up the test with no further action.`

## Remaining Review Priorities

See `aural_pv_ljt_review_flags_v2_reviewed.tsv`.

The most important remaining issue is `come on`, because discourse-marker interpretation depends on recording prosody.
