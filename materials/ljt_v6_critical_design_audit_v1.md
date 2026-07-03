# LJT v6 critical design audit v1

## Bottom line

The v5 revision solved surface-level mechanical problems, but it did not solve construct validity. The next version should not start from the assumption that all 48 PVs are equally usable in an audio LJT. Several targets are too polysemous, too transparent, too prosody-dependent, or too reliant on world knowledge for stable acceptability judgment.

## Audit lenses

1. Construct validity: Does the item require access to the intended PV meaning?
2. Linguistic naturalness: Is the acceptable sentence natural and is the unacceptable sentence a controlled near-miss rather than nonsense?
3. Cue control: Can participants solve the item from discourse markers, negation, animacy, noun category, numbers, or world knowledge?
4. Polysemy control: Are competing literal or idiomatic senses suppressed by context?
5. Audio stability: Is the key robust to intonation, pauses, TTS prosody, and short-term memory load?
6. Analysis readiness: Can item-level exclusions and list balancing be justified before learner data collection?

## v6 action counts

- drop: 2
- keep_revise_lightly: 7
- replace_or_rewrite: 15
- revise: 24

## Construct-fit counts

- rating 1: 2
- rating 2: 15
- rating 3: 24
- rating 4: 7

High polysemy risk items: 21 / 48.

## Critical decisions

- Drop immediately: `make out`, `come on`.
- Strongest candidates for v6: `move up`, `carry out`, `rule out`, `point out`, `sum up`, `lay out`, `work out`.
- Do not record v6 until item-level semantic-naturalness review passes; mechanical audit alone is insufficient.
- For each unacceptable item, require a written rationale showing why rejection depends on the target PV sense rather than a broad category mismatch.
- Prefer same-domain near-misses: human vs human, task vs task, document vs document, event vs event, quantity vs quantity.
- Avoid impossible nouns, non-agentive subjects, overt negation, adversative conjunctions, and transparent number reversals.

## Required gate before audio generation

A v6 item may be recorded only if it passes all of the following:

- acceptable naturalness >= 3/4
- unacceptable framing >= 3/4
- PV dependency >= 3/4
- general cue risk <= 2/4
- no overt contrast or negation cue
- matched or near-matched word count
- no plausible alternate PV sense that makes the keyed unacceptable item acceptable

See `ljt_v6_item_feasibility_audit_v1.tsv` for item-level decisions.
