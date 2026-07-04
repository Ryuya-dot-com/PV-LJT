# ElevenLabs Generation Summary: C-Level PV-LJT v4 Multi-Agent

Date: 2026-07-04

## Input

- Recording script: `materials/audio_recording_script_ljt_v4_multi_agent.tsv`
- Source item master: `materials/c_level_pv_ljt_48_target_master_v4_multi_agent.tsv`
- Rows generated: 96 LJT sentence files per voice
- Task label: `aural_pv_ljt_c_level_v4_multi_agent`

## Output

Male voice:

- Audio directory: `audio/raw/elevenlabs/male/ljt_v4_multi_agent/`
- Manifest: `materials/elevenlabs_generation_manifest_male_ljt_v4_multi_agent.tsv`
- Generated files: 96/96
- Manifest status: 96 generated, 0 failed
- File-size check: 0 missing, 0 zero-byte files
- Duration range: 1.802 to 3.474 seconds
- Mean duration: 2.329 seconds

Female voice:

- Audio directory: `audio/raw/elevenlabs/female/ljt_v4_multi_agent/`
- Manifest: `materials/elevenlabs_generation_manifest_female_ljt_v4_multi_agent.tsv`
- Generated files: 96/96
- Manifest status: 96 generated, 0 failed
- File-size check: 0 missing, 0 zero-byte files
- Duration range: 1.802 to 3.527 seconds
- Mean duration: 2.400 seconds

## Generation Settings

The generation used the existing ElevenLabs environment configuration from `.env` without exposing the API key.

- Model: `eleven_multilingual_v2`
- Output format: `mp3_44100_128`
- Stability: `0.75`
- Similarity boost: `0.75`
- Style: `0.0`
- Speed: `1.0`
- Speaker boost: `true`
- Seed base: `20260701`

Generation required setting `SSL_CERT_FILE` to the local `certifi` CA bundle because the default Python SSL certificate path failed certificate verification.

## Verification

Completed checks:

- Manifest row count matches recording script row count.
- All manifest rows have `status=generated`.
- All referenced audio paths exist.
- No generated mp3 file is zero bytes.
- All files are readable by `ffprobe`.
- No duration is shorter than 1.0 second or longer than 8.0 seconds.

Remaining human review:

- Listen for unnatural phrasing or prosodic cues.
- Check that verb and particle are not separated by an unusual pause.
- Check that unacceptable items are not signaled by intonation.
- Confirm comparable pacing and loudness across male and female versions.

