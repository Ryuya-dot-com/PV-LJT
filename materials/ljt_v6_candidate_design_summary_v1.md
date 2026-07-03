# LJT v6 candidate design summary v1

## Status

This is a pre-audio candidate set. It is not production-cleared and should not be recorded until native/expert review confirms semantic naturalness and PV dependency.

## Design decisions

- Use only targets rated `keep_revise_lightly` or `revise` in the v6 feasibility audit.
- Do not force `replace_or_rewrite` or `drop` targets into the LJT.
- Keep one additional weak candidate as a reserve rather than placing it in the balanced active lists.
- Use same-domain near-misses to reduce broad noun-category cues.
- Require native/expert review before audio generation.

## Counts

- candidate PV pool: 31
- active balanced-list PVs: 30
- reserve candidates: 1
- excluded or replacement-needed PVs: 17

Candidate pool status:
- active_candidate: 30
- reserve_needs_native_review: 1

Preliminary gate status:
- prelim_pass_native_review_required: 28
- prelim_review_required: 2
- reserve_not_listed: 1

Red-team residual risk:
- high: 3
- low: 5
- moderate: 23

Excluded target status:
- drop: 2
- replace_or_rewrite: 15

## List balance

The active set has 30 PVs. List A receives 15 acceptable and 15 unacceptable items; List B receives the opposite conditions. Each PV appears once per list.

## Files

- `aural_pv_ljt_items_v6_candidate.tsv`: full 31-PV candidate pool, two rows per PV
- `aural_pv_ljt_list_assignment_v6_candidate.tsv`: 30-PV active balanced assignment
- `aural_pv_ljt_list_A_v6_candidate.tsv` and `aural_pv_ljt_list_B_v6_candidate.tsv`: pseudo-randomized active lists
- `ljt_v6_candidate_expert_review_form_v1.tsv`: expert-review form for all candidate items
- `ljt_v6_candidate_pre_audio_audit_v1.tsv`: item-level pre-audio gate audit
- `ljt_v6_candidate_red_team_review_v1.tsv`: residual-risk review after the mechanical gate
- `ljt_v6_excluded_targets_v1.tsv`: targets requiring replacement, major rewrite, or drop
