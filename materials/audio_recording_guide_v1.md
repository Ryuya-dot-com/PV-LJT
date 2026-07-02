# PV-LJT Audio Recording Guide v1

## Files To Record

- Main LJT sentences: `audio_recording_script_ljt_v4_pre_audio.tsv`
- Audio PV decision stimuli: `audio_recording_script_audio_decision_v2.tsv`
- Practice stimuli: `audio_recording_script_practice_v1.tsv`

Use the `audio_file_name` column as the required output file name.

## Technical Settings

- Format: WAV
- Channel: mono
- Sampling rate: 44.1 kHz or 48 kHz
- Bit depth: 16-bit or 24-bit
- Normalize only after all recordings are complete.
- Avoid clipping, room echo, background noise, and inconsistent microphone distance.

## LJT Sentence Recording

- Use one speaker for all LJT sentences if possible.
- Record at a natural but controlled pace.
- Do not place special emphasis on the phrasal verb.
- Do not pause between the verb and the particle.
- Keep prosody neutral unless the item-specific note says otherwise.
- Trim leading and trailing silence consistently, leaving roughly 100-300 ms.

Special LJT item:

- `ljt_038a` / `come on`: record with natural disbelief or disagreement intonation.
- `ljt_038b` / `come on`: record the final clause with sincere agreement intonation; avoid sarcasm.

## Audio Decision Recording

- Record only the two-word stimulus.
- Do not use a carrier phrase.
- Use neutral stress and normal connected pronunciation.
- Do not make foil items sound artificially odd.
- The same guidance applies to audio decision practice stimuli in `audio_recording_script_practice_v1.tsv`.

## Quality Check

Before piloting, check every file for:

- correct file name
- complete stimulus
- no repeated takes inside the file
- no clipping
- comparable loudness across items
- no prosodic cue that reveals the expected response
