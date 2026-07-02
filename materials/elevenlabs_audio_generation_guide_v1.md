# ElevenLabs Audio Generation Guide v1

## Secret Handling

- Put the API key only in `.env`.
- Do not paste the API key into scripts, TSV files, manuscripts, or experiment code.
- `.gitignore` excludes `.env` and generated audio directories.
- Generated manifests record voice/model/settings/seed, but never the API key.

Required `.env` keys:

```text
ELEVENLABS_API_KEY=...
ELEVENLABS_MALE_VOICE_ID=...
ELEVENLABS_FEMALE_VOICE_ID=...
```

Optional `.env` defaults:

```text
ELEVENLABS_MODEL_ID=eleven_multilingual_v2
ELEVENLABS_OUTPUT_FORMAT=mp3_44100_128
```

## Choose A Voice

Save available voices to a TSV:

```bash
python3 scripts/elevenlabs_list_voices.py
```

For the two-voice design, choose one male and one female voice and save both in `.env`:

```text
ELEVENLABS_MALE_VOICE_ID=...
ELEVENLABS_FEMALE_VOICE_ID=...
```

For this study, prefer one clear adult English voice with neutral delivery. Avoid voices with strong theatrical, conversational, or emotional style.

## Recommended Settings

- `model_id`: `eleven_multilingual_v2`
- `output_format`: `mp3_44100_128` for broad account compatibility
- `stability`: `0.75`
- `similarity_boost`: `0.75`
- `style`: `0.0`
- `speed`: `1.0`
- `use_speaker_boost`: `true`

If the account supports WAV output, use `--output-format wav_44100_16` and update the manifest accordingly.

## Dry Run

Dry runs create only manifests and do not call the API.

Dry-run all male/female audio sets:

```bash
python3 scripts/elevenlabs_generate_all_voice_versions.py --limit 5
```

This creates planned manifests for:

- male LJT, audio decision, and practice stimuli
- female LJT, audio decision, and practice stimuli

Dry-run one voice and one task:

```bash
python3 scripts/elevenlabs_generate_audio.py \
  --recording-script materials/audio_recording_script_ljt_v4_pre_audio.tsv \
  --out-dir audio/raw/elevenlabs/male/ljt_v4 \
  --manifest materials/elevenlabs_generation_manifest_male_ljt_v4.tsv \
  --voice-id-env ELEVENLABS_MALE_VOICE_ID \
  --voice-label male \
  --limit 5
```

## Generate All Male/Female Audio Sets

Generate all LJT, audio decision, and practice stimuli for both voices:

```bash
python3 scripts/elevenlabs_generate_all_voice_versions.py --generate
```

The expected output structure is:

```text
audio/raw/elevenlabs/male/ljt_v4/
audio/raw/elevenlabs/male/audio_decision_v2/
audio/raw/elevenlabs/male/practice_v1/
audio/raw/elevenlabs/female/ljt_v4/
audio/raw/elevenlabs/female/audio_decision_v2/
audio/raw/elevenlabs/female/practice_v1/
```

The expected manifests are:

```text
materials/elevenlabs_generation_manifest_male_ljt_v4.tsv
materials/elevenlabs_generation_manifest_male_audio_decision_v2.tsv
materials/elevenlabs_generation_manifest_male_practice_v1.tsv
materials/elevenlabs_generation_manifest_female_ljt_v4.tsv
materials/elevenlabs_generation_manifest_female_audio_decision_v2.tsv
materials/elevenlabs_generation_manifest_female_practice_v1.tsv
```

## Generate One Voice And Task

Male LJT sentences:

```bash
python3 scripts/elevenlabs_generate_audio.py \
  --recording-script materials/audio_recording_script_ljt_v4_pre_audio.tsv \
  --out-dir audio/raw/elevenlabs/male/ljt_v4 \
  --manifest materials/elevenlabs_generation_manifest_male_ljt_v4.tsv \
  --voice-id-env ELEVENLABS_MALE_VOICE_ID \
  --voice-label male \
  --generate
```

Female audio decision stimuli:

```bash
python3 scripts/elevenlabs_generate_audio.py \
  --recording-script materials/audio_recording_script_audio_decision_v2.tsv \
  --out-dir audio/raw/elevenlabs/female/audio_decision_v2 \
  --manifest materials/elevenlabs_generation_manifest_female_audio_decision_v2.tsv \
  --voice-id-env ELEVENLABS_FEMALE_VOICE_ID \
  --voice-label female \
  --generate
```

Female practice stimuli:

```bash
python3 scripts/elevenlabs_generate_audio.py \
  --recording-script materials/audio_recording_script_practice_v1.tsv \
  --out-dir audio/raw/elevenlabs/female/practice_v1 \
  --manifest materials/elevenlabs_generation_manifest_female_practice_v1.tsv \
  --voice-id-env ELEVENLABS_FEMALE_VOICE_ID \
  --voice-label female \
  --generate
```

## Pilot Review

After generation, review every audio file for:

- correct file name and complete stimulus
- no clipping or background noise
- no unusual pauses between verb and particle
- no prosodic cue that reveals expected response
- controlled intonation for `come on`
- comparable pacing and loudness across male and female versions

The most important review files remain:

- `ljt_medium_priority_expert_review_packet_v2_for_ljt_v4.tsv`
- `audio_recording_guide_v1.md`
- generated `elevenlabs_generation_manifest_*.tsv`
