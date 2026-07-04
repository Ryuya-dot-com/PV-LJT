# Current C-Level PV-LJT Working Set

Date organized: 2026-07-04

This directory is an index for the current C-level phrasal-verb LJT working set. The actual TSV, manifest, and audio files remain in their original locations so existing relative paths in manifests and scripts continue to work.

## Current Item Set

- `../c_level_pv_ljt_48_target_master_v4_multi_agent.tsv`
- `../c_level_pv_ljt_list_A_v4_multi_agent.tsv`
- `../c_level_pv_ljt_list_B_v4_multi_agent.tsv`
- `../c_level_pv_ljt_list_assignment_v4_multi_agent.tsv`
- `../pilot_trial_file_ljt_list_A_v4_multi_agent.tsv`
- `../pilot_trial_file_ljt_list_B_v4_multi_agent.tsv`
- `../c_level_pv_ljt_48_target_balance_audit_v4_multi_agent_ja.md`
- `../c_level_pv_ljt_multi_agent_candidate_synthesis_v3_ja.md`

## Design Basis

- `../c_level_pv_ljt_design_spec_v1.md`
- `../c_level_pv_ljt_design_spec_v1_ja.md`
- `../c_level_pv_ljt_item_review_rubric_v1.tsv`

## Recording And ElevenLabs Output

- `../audio_recording_script_ljt_v4_multi_agent.tsv`
- `../elevenlabs_generation_manifest_male_ljt_v4_multi_agent.tsv`
- `../elevenlabs_generation_manifest_female_ljt_v4_multi_agent.tsv`
- `../elevenlabs_generation_summary_ljt_v4_multi_agent.md`
- `../../audio/raw/elevenlabs/male/ljt_v4_multi_agent/`
- `../../audio/raw/elevenlabs/female/ljt_v4_multi_agent/`

## Archived Development Work

Earlier C-level drafts and replacement-work files were moved to:

- `../archive/c_level_ljt_development/rounds/`
- `../archive/c_level_ljt_development/replacement_work/`

## Current Status

The v4 multi-agent set is the current pre-audio expert-review candidate:

- 48 targets / 96 LJT sentences
- List A and List B each contain 48 trials
- Each list has 24 acceptable and 24 unacceptable trials
- App-ready List A and List B files each contain 6 fixed practice trials plus 48 main trials
- Male and female ElevenLabs audio have been generated for all 96 sentences
- All generated mp3 files passed existence, zero-byte, and duration checks
