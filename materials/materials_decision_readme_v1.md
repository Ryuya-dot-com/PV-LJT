# PV-LJT Pilot Materials Decision v1

## Core Decision

Use 48 two-word phrasal verbs as the shared target set for:

1. Aural PV-LJT
2. Audio phrasal verb decision task
3. Orthographic PV meaning recognition

The first pilot excludes three-word phrasal-prepositional frames such as `put up with`, `get down to`, `get on with`, and `look out for`. This keeps the construct focused on two-word verb-particle combinations.

## Main Files

- `pv_materials_decision_v2_strict_two_word.csv`
  - master target list
  - 40 core items from the Sonbul & El-Dakhs supplement
  - 8 academic/general extension items from S&AW PHaVE

- `three_stage_pv_master_v4_pre_audio.tsv`
  - one row per target PV
  - links the LJT item IDs, audio decision real trial ID, orthographic recognition item ID, frequency, opacity, register, and semantic category
  - use this as the analysis join table for IRTree or multi-process IRT

- `orthographic_pv_meaning_recognition_v2_balanced.tsv`
  - recommended version for expert review
  - 48 prompted four-choice meaning recognition items
  - one correct English definition and three English distractors
  - correct options are balanced: A/B/C/D = 12 items each
  - use after audio tasks to avoid orthographic priming

- `audio_pv_decision_items_v2_mixed_foils.tsv`
  - recommended version for foil screening
  - 48 real PVs and 48 foil candidates
  - foil candidates are split into 24 pseudo verb-particle combinations and 24 natural free combinations
  - present isolated two-word audio stimuli
  - response: `yes` = common English phrasal verb, `no` = not a common English phrasal verb

- `audio_foil_screening_v1.tsv`
  - screening/diagnostic file for the earlier same-verb foil set
  - retains the v1 foil candidates for comparison but does not supersede the mixed-foil v2 file

- `audio_pv_decision_screening_form_for_raters_v1.tsv`
  - blind rater form for checking the v2 audio decision stimuli
  - contains only screen order, stimulus text, and rater response columns

- `audio_pv_decision_screening_form_v1.tsv`
  - internal keyed version of the same screening form
  - includes hidden item type, foil type, and expected response columns

- `aural_pv_ljt_items_v4_pre_audio.tsv`
  - recommended LJT candidate set after subagent expert review, BERT/SBERT diagnostics, and pre-audio internal review
  - 96 candidate LJT sentences
  - one acceptable and one unacceptable sentence per target PV
  - intended for expert review before audio recording

- `aural_pv_ljt_list_assignment_v4_pre_audio.tsv`
  - assigns one LJT sentence per PV to List A and the opposite condition to List B
  - each list has 48 PVs, 24 acceptable and 24 unacceptable sentences

- `aural_pv_ljt_list_A_v4_pre_audio.tsv` and `aural_pv_ljt_list_B_v4_pre_audio.tsv`
  - randomized 48-trial implementation files for the two LJT lists

- `aural_pv_ljt_expert_review_form_v4_pre_audio.tsv`
  - review form for checking sentence naturalness, intended sense, semantic fit/mismatch, and audio suitability

- `aural_pv_ljt_review_flags_v4_pre_audio.tsv`
  - priority list of reviewed v4 LJT candidate sentences that still need special attention
  - use this file to focus expert review

- `subagent_expert_review_summary_v1.md`
  - summary of the subagent review and the changes made from LJT v1 to v2

- `bert_item_diagnostics_v3_for_ljt_v4.tsv`
  - BERT/SBERT diagnostics for each of the 96 v4 LJT sentences
  - includes pseudo-log-likelihood, target PV fit, pairwise sentence similarity, and pairwise context similarity

- `bert_pair_diagnostics_v3_for_ljt_v4.tsv`
  - one row per target PV pair
  - compares acceptable and unacceptable LJT sentences for the same PV

- `bert_review_priorities_v3_for_ljt_v4.tsv`
  - prioritized review list combining BERT/SBERT diagnostics with the expert-review flags

- `bert_diagnostics_summary_v3_for_ljt_v4.md`
  - short summary of the BERT/SBERT diagnostic run

- `ljt_medium_priority_expert_review_packet_v2_for_ljt_v4.tsv`
  - focused 11-item review packet for the remaining medium-priority LJT pairs
  - use this before audio recording to confirm semantic near-miss quality, naturalness, and audio suitability

- `ljt_pre_audio_internal_review_v1.tsv`
  - internal decision log for the 14 medium-priority v3 pairs reviewed before creating v4

- `audio_recording_script_ljt_v4_pre_audio.tsv`
  - 96 LJT sentence recordings with file names and item-level recording notes

- `audio_recording_script_audio_decision_v2.tsv`
  - 96 isolated two-word audio decision recordings with file names

- `ljt_practice_items_v1.tsv` and `audio_recording_script_practice_v1.tsv`
  - six aural LJT practice items plus LJT/audio-decision practice recording scripts

- `audio_recording_guide_v1.md`
  - recording specifications, file naming instructions, and prosody notes

- `elevenlabs_audio_generation_guide_v1.md`
  - ElevenLabs API setup, dry-run commands, generation commands, and review workflow

- `pilot_trial_file_ljt_list_A_v1.tsv` and `pilot_trial_file_ljt_list_B_v1.tsv`
  - implementation-ready LJT files with 6 practice trials and 48 main trials

- `pilot_trial_file_audio_decision_v1.tsv`
  - implementation-ready audio decision file with 8 practice trials and 96 main trials

- `pilot_trial_file_orthographic_recognition_v1.tsv`
  - implementation-ready orthographic recognition file with 4 practice trials and 48 main trials

- `scripts/compute_bert_item_diagnostics.py`
  - reproducible script for recomputing the BERT/SBERT diagnostics

- `scripts/summarize_bert_diagnostics.py`
  - reproducible script for generating the review-priority file and summary

- `scripts/create_ljt_v4_pre_audio_materials.py`
  - reproducible script for generating the LJT v4 files from v3

- `scripts/create_pre_audio_review_and_recording_scripts.py`
  - reproducible script for generating the focused v4 review packet and recording scripts

- `scripts/create_pilot_trial_files.py`
  - reproducible script for generating the practice-plus-main pilot trial files

- `scripts/elevenlabs_list_voices.py`
  - saves available ElevenLabs voices to `materials/elevenlabs_voices_available.tsv`

- `scripts/elevenlabs_generate_audio.py`
  - generates audio files from the recording-script TSVs and writes generation manifests

- `scripts/elevenlabs_generate_all_voice_versions.py`
  - generates or dry-runs male and female versions of LJT, audio decision, and practice audio

## Recommended Task Order

1. Aural PV-LJT
2. Audio phrasal verb decision task
3. Orthographic PV meaning recognition
4. Vocabulary size / listening / exposure questionnaire

For the IRTree interpretation, the latent construct order remains:

1. Orthographic explicit meaning knowledge
2. Aural PV form familiarity
3. Automatized contextual aural use

## Current Status

Orthographic v2 items are usable as a first expert-review version.

Aural PV-LJT v4 is the current recommended LJT version. It incorporates subagent expert-review revisions, BERT/SBERT diagnostics, and a pre-audio internal review. The latest diagnostic pass found no high-priority BERT/SBERT review items; 11 medium-priority items remain for expert review before audio recording.

Audio foils require screening before data collection. The recommended v2 audio file uses mixed foil types so that no-items are not limited to obviously odd pseudo-PVs. Before piloting with learners, run a short native-speaker or high-proficiency screening:

- Is this a common English phrasal verb?
- Is this a possible but uncommon expression?
- Is this clearly impossible or unnatural?

Retain foils that are clearly judged as not common English phrasal verbs. For pseudo verb-particle foils, avoid items that are so odd that the task becomes trivial. For natural free-combination foils, avoid items that raters judge as common phrasal verbs or fixed expressions.

## First Pilot Recommendation

For an initial learner pilot:

- Orthographic task: 48 trials
- Audio decision task: 96 trials
- Aural PV-LJT: 48 trials per participant via List A or List B
- Practice trials: included in the `pilot_trial_file_*` files
- Randomize trial order within task
- Keep the orthographic task untimed or mildly timed
- Record accuracy and response time for LJT and audio decision

## Analysis Notes

For the 40 Sonbul & El-Dakhs core items, item-level predictors include:

- COCA sense-based frequency
- opacity rating
- semantic category
- source sentence

For the 8 S&AW PHaVE extension items, register is the primary design motivation. Add comparable frequency/opacity estimates later if the extension items are retained after piloting.
