# C-Level Phrasal Verb LJT Replacement Sentences: Self-Audit v2

Date: 2026-07-04

This audit reviews `c_level_pv_ljt_replacement_sentence_pairs_v2.tsv`, which revises the 17 weakest replacement pairs identified in the v1 audit. The goal is not to declare final production readiness, but to move the replacement set closer to a defensible C1-centered phrasal-verb LJT item pool before native-speaker review and pilot testing.

## Mechanical Validation

The v2 TSV passes the current mechanical checks.

- Rows: 34
- Pairs: 17
- Acceptable rows: 17
- Unacceptable rows: 17
- Expected acceptable responses: 17
- Expected unacceptable responses: 17
- Target form located in every sentence
- Target form is never sentence-initial or in the first two words
- Sentence length constraint passed for all items
- Pair-internal PV, condition, response, and score consistency passed

## Score Distribution

| Self-review score | Number of pairs |
|---:|---:|
| 90 | 3 |
| 88 | 5 |
| 86 | 5 |
| 84 | 3 |
| 78 | 1 |

Summary:

- Mean score: 86.47
- Median score: 86
- Minimum score: 78
- Maximum score: 90
- Pairs scoring 90+: 3/17
- Pairs scoring 85+: 13/17
- Pairs scoring 80+: 16/17
- Pairs below 80: 1/17

This is a clear improvement over v1, where seven pairs remained below 80. The v2 set now meets the working target of having at least 12 of the 17 replacement pairs score 85 or higher.

## Strongest Current Replacement Pairs

These pairs are the best current candidates and can move forward to native-speaker review with only targeted attention to edge readings.

| Pair | PV | Score | Main reason |
|---|---|---:|---|
| v2_001 | set up | 90 | Strong created-entity contrast: `review process` vs. `review finding`. |
| v2_004 | take on | 90 | Strong responsibility-object contrast: `case` vs. `verdict`. |
| v2_017 | take over | 90 | Strong control/responsibility contrast: `project` vs. `advice`. |

These are close to the intended LJT logic: the unacceptable version is lexically plausible at the phrase level, but fails because the object does not fit the selected PV sense.

## Good But Not Yet Final Pairs

These pairs are viable C-level candidates, but need native-speaker acceptability checks and possibly one more round of lexical control.

| Pair | PV | Score | Main risk |
|---|---|---:|---|
| v2_002 | take up | 88 | `take up the outcome` may be acceptable if interpreted as discussing an outcome. |
| v2_003 | put off | 88 | `evidence` is clearly not schedulable, but the mismatch may be too easy. |
| v2_005 | give in | 86 | Good semantic fit, but may function as an easier anchor item. |
| v2_007 | sort out | 86 | Keep the target sense fixed as resolve/problem management, not understand/cause discovery. |
| v2_008 | pass on | 86 | `silence` may be too obviously non-transferable. |
| v2_009 | bring out | 86 | Must constrain the sense to release/publication, not make a quality noticeable. |
| v2_010 | throw out | 86 | `throw out the agenda` may be possible under a discard/cancel reading. |
| v2_011 | set off | 88 | `summary` is a product noun, but may be too obviously wrong. |
| v2_015 | shut down | 88 | Strong sense contrast, but `reason` may be too obvious as a wrong object. |
| v2_016 | turn down | 88 | Legal/register readings of `turn down evidence` should be checked. |

## Pairs Needing Revision Before Pilot Use

These pairs should not be treated as production candidates yet.

| Pair | PV | Score | Problem |
|---|---|---:|---|
| v2_006 | play out | 84 | `agreement played out in public` may be acceptable in some discourse contexts. |
| v2_012 | open up | 84 | `opened up objections` is probably marked, but not fully impossible. |
| v2_014 | hold up | 84 | `receipt` can sometimes be delayed, so the unacceptable sentence is not stable enough. |
| v2_013 | fill in | 78 | The unacceptable object `chair` is too concrete and cue-heavy; this is not a strong C1 LJT item. |

Priority revision order:

1. Replace or redesign `fill in`.
2. Revise `play out`.
3. Revise `hold up`.
4. Recheck `open up`.

## Reviewer-Style Verdict

The v2 replacement set is substantially stronger than v1 and is now suitable as a draft replacement pool for a C1-centered LJT. However, it is still not ready for final deployment. The strongest items show the intended LJT structure: short aural sentences, easy non-target vocabulary, delayed target placement, and a semantic judgment that depends on the selected phrasal-verb sense rather than broad grammaticality.

The remaining weakness is that several unacceptable sentences can still be rejected through overly obvious object mismatch, and a few may permit alternative interpretations. For high-stakes C-level measurement, this matters because the task should measure automatized semantic access to a specific phrasal-verb sense, not general anomaly detection.

Recommended next step:

Create a provisional 48-target master list by combining the retained high-quality existing targets with the v2 replacement pool, but mark `fill in`, `play out`, `hold up`, and `open up` as pre-pilot revision items. After that, run a full multiple-list balance audit across PV frequency, sense opacity, item difficulty, condition balance, target position, audio length, and response-key distribution.

