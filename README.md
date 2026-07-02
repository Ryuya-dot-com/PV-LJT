# PV-LJT Audio Review

Static review materials for the pilot phrasal-verb listening tasks.

The GitHub Pages site lets reviewers complete the listening tasks with either
the male or female ElevenLabs voice and export their responses as an Excel
workbook after every trial is complete.

## Review Tasks

- Aural PV-LJT List A
- Aural PV-LJT List B
- Audio phrasal verb decision

Practice trials are presented first in fixed order. Main trials are
pseudo-randomized from reviewer ID, voice, and task, so the same reviewer gets
the same order when resuming.

Each trial collects both the task response and two 6-point listening-review
ratings:

- ease of listening
- naturalness of English

## Result Workbook

The download is an `.xlsx` workbook with separate sheets:

- `Session`: reviewer ID, task, voice, completion count, and randomization seed
- `Responses`: one flat row per trial, including answer, correctness, response
  time, playback count, ratings, flags, comments, audio path, and stimulus text
- `Trial_Order`: display order and item metadata used for reproducibility
- `Codebook`: short descriptions of key variables

The download button remains locked until all trials in the selected task are
complete.

The public site is intended for collaborator review and pilot dry-runs, not for
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
