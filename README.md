# PV-LJT Audio Review

Static review materials for the pilot phrasal-verb listening tasks.

The GitHub Pages site lets reviewers complete the listening tasks with either
the male or female ElevenLabs voice and export their responses as CSV.

## Review Tasks

- Aural PV-LJT List A
- Aural PV-LJT List B
- Audio phrasal verb decision

The public site is intended for collaborator audio review, not for learner data
collection. The repository includes keyed materials for review and audit.

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
