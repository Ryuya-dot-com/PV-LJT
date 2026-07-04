# PV-LJT Audio Review

Static review materials for the phrasal-verb listening tasks.

The GitHub Pages site lets reviewers complete the listening tasks with either
the male or female ElevenLabs voice and export their responses as an Excel
workbook after every trial is complete.

A simplified participant-facing page is also available at `participant.html`.
It removes listening-review ratings, comments, transcript display, and email
collection. Participants enter only an ID, voice, and task, then download CSV
or JSON results at completion. Practice trials are shown before the main task,
and each trial attempts to start audio automatically. The participant page uses
a custom audio status panel instead of browser-native audio controls. F/J
response keys are counterbalanced from the normalized participant ID, and main
trials use LJT-S-style seeded constrained randomization.

## Review Tasks

- C-Level PV-LJT v4 Review List A
- C-Level PV-LJT v4 Review List B
- Aural PV-LJT v5 Review List A
- Aural PV-LJT v5 Review List B
- Audio phrasal verb decision

The default LJT pages currently use the C-level v4 multi-agent stimuli:

- `materials/c_level_pv_ljt_48_target_master_v4_multi_agent.tsv`
- `materials/c_level_pv_ljt_list_A_v4_multi_agent.tsv`
- `materials/c_level_pv_ljt_list_B_v4_multi_agent.tsv`
- `materials/pilot_trial_file_ljt_list_A_v4_multi_agent.tsv`
- `materials/pilot_trial_file_ljt_list_B_v4_multi_agent.tsv`

The older v5 review stimuli remain selectable for comparison:

- `materials/aural_pv_ljt_items_v5_production.tsv`
- `materials/pilot_trial_file_ljt_list_A_v5_production.tsv`
- `materials/pilot_trial_file_ljt_list_B_v5_production.tsv`

The v5 LJT set replaces the earlier v4 pre-audio candidate items and passes the
mechanical cue/word-count audit. A later semantic-naturalness review found that
v5 should not be treated as production-ready for learner data because many
unacceptable items are rejectable from broad noun/category oddness rather than
from the target phrasal-verb meaning. See:

- `materials/ljt_v5_semantic_naturalness_expert_review_v1.tsv`
- `materials/ljt_v5_semantic_naturalness_expert_review_summary_v1.md`
- `materials/ljt_v6_item_feasibility_audit_v1.tsv`
- `materials/ljt_v6_critical_design_audit_v1.md`

The v6 audit is a pre-audio gate. It classifies the original 48 PV targets by
construct fit, near-miss feasibility, polysemy risk, and audio stability before
new LJT items are written or recorded.

A reduced v6 candidate set has been created for review only:

- `materials/aural_pv_ljt_items_v6_candidate.tsv`
- `materials/aural_pv_ljt_list_A_v6_candidate.tsv`
- `materials/aural_pv_ljt_list_B_v6_candidate.tsv`
- `materials/ljt_v6_candidate_expert_review_form_v1.tsv`
- `materials/ljt_v6_candidate_pre_audio_audit_v1.tsv`
- `materials/ljt_v6_candidate_red_team_review_v1.tsv`
- `materials/ljt_v6_excluded_targets_v1.tsv`
- `materials/ljt_v6_candidate_design_summary_v1.md`

The v6 candidate set is not currently served in the review app and should not
be recorded yet. It contains a 31-PV review pool, a 30-PV balanced active list,
and 17 excluded or replacement-needed targets.

## Current C-Level PV-LJT Working Set

A newer C-level, C1-centered PV-LJT candidate set has been created and is now
the default LJT task in both the listening-review page and the simplified
participant page.

Current item and list files:

- `materials/c_level_pv_ljt_48_target_master_v4_multi_agent.tsv`
- `materials/c_level_pv_ljt_list_A_v4_multi_agent.tsv`
- `materials/c_level_pv_ljt_list_B_v4_multi_agent.tsv`
- `materials/c_level_pv_ljt_list_assignment_v4_multi_agent.tsv`
- `materials/pilot_trial_file_ljt_list_A_v4_multi_agent.tsv`
- `materials/pilot_trial_file_ljt_list_B_v4_multi_agent.tsv`

Current design and audit files:

- `materials/c_level_pv_ljt_design_spec_v1_ja.md`
- `materials/c_level_pv_ljt_item_review_rubric_v1.tsv`
- `materials/c_level_pv_ljt_48_target_balance_audit_v4_multi_agent_ja.md`
- `materials/c_level_pv_ljt_multi_agent_candidate_synthesis_v3_ja.md`
- `materials/current_c_level_ljt/README.md`

Generated ElevenLabs audio for this set is available under:

- `audio/raw/elevenlabs/male/ljt_v4_multi_agent/`
- `audio/raw/elevenlabs/female/ljt_v4_multi_agent/`

Generation manifests:

- `materials/elevenlabs_generation_manifest_male_ljt_v4_multi_agent.tsv`
- `materials/elevenlabs_generation_manifest_female_ljt_v4_multi_agent.tsv`
- `materials/elevenlabs_generation_summary_ljt_v4_multi_agent.md`

Earlier C-level development rounds and replacement drafts have been archived
under `materials/archive/c_level_ljt_development/`.

Practice trials are presented first in fixed order. Main trials are
pseudo-randomized from reviewer ID, voice, and task, so the same reviewer gets
the same order when resuming.

Each trial collects both the task response and two 6-point listening-review
ratings:

- ease of listening
- naturalness of English

The written script is hidden until the reviewer has answered the trial, then it
is shown automatically for the listening-quality review.

## Result Workbook

The download is an `.xlsx` workbook with separate sheets:

- `Session`: reviewer ID, task, voice, completion count, and randomization seed
- `Responses`: one flat row per trial, including answer, correctness, response
  time, playback count, ratings, flags, comments, audio path, and stimulus text
- `Trial_Order`: display order and item metadata used for reproducibility
- `Codebook`: short descriptions of key variables

The download button remains locked until all trials in the selected task are
complete.

The public site is intended for collaborator review and pilot dry-runs before
final learner data collection. The repository includes keyed materials for
review and audit.

## Audio

Generated audio is stored under:

- `audio/raw/elevenlabs/male/`
- `audio/raw/elevenlabs/female/`

Generation manifests are stored in `materials/elevenlabs_generation_manifest_*.tsv`.

## Local Preview

```bash
python3 -m http.server 8000
```

Then open `http://localhost:8000/`.
