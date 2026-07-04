# C-level PV-LJT design specification v1

Status: design specification, not a production item set

Purpose: Develop a 48-target, multiple-list aural lexicosemantic judgment
task (LJT) for CEFR C1-centered English learners, targeting automatized
phonological and lexicosemantic knowledge of English phrasal verbs (PVs).

## 1. Construct

The test should measure whether a C-level learner can hear a PV in a short
sentence and rapidly judge whether the PV is semantically and collocationally
appropriate in that context.

The target construct is not:

- written PV meaning recognition
- isolated audio PV familiarity
- explicit translation knowledge
- grammaticality judgment in a broad syntactic sense
- detection of absurd nouns, impossible events, or world-knowledge violations

The target construct is:

- aural recognition of the PV form
- retrieval of the intended PV sense
- use-in-context knowledge: semantic fit, collocational restrictions,
  argument structure, register, and local discourse compatibility
- sufficiently rapid and stable access to that knowledge under listening
  conditions

This follows Uchihara et al. (2025), where the LJT is treated as an index of
automatized phonological vocabulary knowledge distinct from meaning
recognition and meaning recall. For PVs, the construct must be narrowed more
carefully than for single words because many PVs are polysemous and many
unacceptable contexts can become rejectable from broad noun-category oddness.

## 2. Literature basis

### Uchihara et al. (2025)

Uchihara, Saito, Kurokawa, Takizawa, and Suzukida developed an aural LJT for
single words. Participants heard short sentences once and judged whether the
target word was semantically appropriate in context. Their LJT predicted TOEIC
listening better than aural meaning recognition and recall, and was modeled as
automatized rather than declarative phonological vocabulary knowledge.

Design implications for the PV-LJT:

- Use audio presentation, not written sentence presentation.
- Present short sentences.
- Do not place the target at the beginning of the sentence.
- Keep non-target vocabulary easy enough that the target PV is the construct.
- Keep syntax simple enough that the task is not a grammar test.
- Use both appropriate and inappropriate contexts.
- Require native/expert review until items are unambiguous.
- Score accuracy as the primary indicator; response time and replay behavior
  are secondary process indicators.

### Saito et al. (2023/2024) and Saito et al. (2026)

The broader LJT line treats use-in-context vocabulary knowledge as a dimension
of phonological vocabulary knowledge that is closer to listening performance
than decontextualized form-meaning tests. The 2026 timed/untimed LJT work
suggests that time pressure should be handled carefully: timing can support an
automatization interpretation, but validity depends more on the quality of the
items and the aural/contextual task than on aggressive time limits alone.

Design implications:

- Use one-play audio and discourage deliberative reanalysis.
- A short response window may be used, but should be piloted rather than
  imposed arbitrarily.
- Report whether the test is timed or untimed and how RT is measured.

### Judgment-task methodology

Plonsky, Marsden, Crowther, Gass, and Spinner (2020) and Ionin and Zyzik
(2014) show that judgment-task scores vary with modality, timing, context,
scale, and reporting practices. A PV-LJT must therefore document modality,
timing, randomization, practice, response options, scoring, reliability, and
item validation.

Design implications:

- Treat this as a judgment task with explicit construct validation needs.
- Report item counts, condition balance, response timing, modality, and
  randomization constraints.
- Use pilot reliability and item statistics before releasing a production
  version.

### Aural phrasal verb knowledge

Cheng, Matthews, Lange, and McLean (2022) showed that aural PV knowledge is
related to L2 listening comprehension and contributes beyond single-word
knowledge. Their PV selection emphasized frequent PVs, opacity, sense
selection, and aural presentation.

Design implications:

- Select PV senses, not only PV forms.
- Prefer opaque or semi-opaque senses where learners cannot solve the item by
  composing verb + particle literally.
- Keep target PV forms contiguous for standardization unless a separable form
  is essential and can be controlled.
- Use a clear rater reference document for acceptable meanings.

### PV frequency, senses, and polysemy

Gardner and Davies (2007), Liu (2011), Garnier and Schmitt (2015), and Sonbul,
El-Dakhs, and Al-Otaibi (2020) all support the same core point: PVs must be
handled at the sense level. Frequency of the PV form is not enough because
common PVs can have multiple senses with very different frequency,
transparency, and learnability.

Design implications:

- Every target row must specify the tested sense.
- Sense-based frequency should be preferred over raw PV frequency where
  available.
- Polysemy risk must be treated as an item-validity threat, not as an
  interesting afterthought.
- A high-frequency PV may still be rejected if the intended sense cannot be
  isolated in a short aural sentence.

## 3. Target population and difficulty

Primary target population: CEFR C1-centered English learners.

Assumed profile:

- high general English proficiency
- substantial declarative vocabulary knowledge
- likely familiarity with many common PV forms
- remaining difficulty in rapid sense selection, collocation, register, and
  use-in-context under listening conditions

C1 implications:

- Avoid items solvable by basic physical/literal particle meanings alone.
- Avoid items where the correct response is obvious from an absurd noun.
- Prefer academic, professional, institutional, interpersonal, and abstract
  contexts that C1 learners plausibly encounter.
- Keep non-target words easy; difficulty should reside in the PV sense and its
  contextual fit.
- Do not make sentences long or syntactically complex merely to make the task
  harder.

## 4. Target selection rules

The production set must contain 48 scored PV targets. Existing targets may be
kept, revised, or replaced. Maintaining the number 48 is more important than
preserving the exact original 48 PV forms.

### 4.1 Required metadata per target

Each target PV must have:

- `pv_id`
- `pv`
- `target_sense`
- `source`
- `raw_frequency_source`
- `sense_frequency_source`
- `opacity_or_transparency_rating`
- `register_focus`
- `polysemy_risk`
- `construct_fit`
- `replacement_status`
- `rationale`

### 4.2 Preferred sources

Use these in priority order:

1. Existing project master lists and audits.
2. Sonbul/El-Dakhs sense-level PV data already in `materials/`.
3. PHaVE sense data and user manual.
4. Gardner & Davies and Liu frequency/register evidence.
5. Additional corpus checks if a target sense remains uncertain.

### 4.3 Keep criteria

A PV sense can remain in the production pool if all are true:

- The intended sense is identifiable without a long discourse.
- A same-domain inappropriate context can be created.
- The inappropriate sentence cannot be accepted under a common alternate sense.
- The item does not rely on special intonation.
- The target is suitable for C1 learners: neither trivially literal nor
  extremely rare/technical.
- Non-target vocabulary can be kept high-frequency and unambiguous.

### 4.4 Replace criteria

Replace the target PV or target sense if any are true:

- Discourse-marker meaning is central and prosody determines the key.
- The PV is too polysemous for stable keying in one short sentence.
- The only available inappropriate item uses an impossible noun or implausible
  world event.
- The target sense is transparent enough that C1 learners can solve it from
  particle directionality alone.
- The acceptable sentence sounds dictionary-like rather than natural.
- Native/expert raters disagree about the intended key.

### 4.5 Current targets requiring replacement priority

Based on the existing v6 audit, these should not be carried into the C-level
production pool without replacement or a new target sense:

- replace/rewrite: `give out`, `put in`, `take in`, `sit back`, `hold back`,
  `come along`, `get down`, `put out`, `clean up`, `keep up`, `look out`,
  `look back`, `go up`, `go down`, `come in`
- drop unless a completely new design is justified: `make out`, `come on`

These are not banned as English PVs. They are weak for this LJT format because
the intended sense is difficult to isolate without broad semantic or prosodic
cues.

## 5. Sentence design rules

Each retained target PV requires one acceptable sentence and one unacceptable
sentence. The production pool therefore contains 96 sentence candidates for 48
targets, but each learner should see only one sentence per target in a given
list.

### 5.1 Sentence length

Default range: 5-9 words.

Allowed exception: 4 or 10 words if the sentence is substantially more natural
and does not increase working-memory load.

Rationale: Uchihara et al. used short sentences to avoid turning the LJT into a
memory or syntax task. PV items sometimes need one extra complement compared
with single-word items, but should remain short.

### 5.2 Target position

The target PV must not be sentence-initial.

Preferred structures:

- subject + PV + object/complement
- subject + auxiliary + PV + object/complement
- short prepositional complement after the PV when needed

Avoid:

- target in the first two words unless unavoidable
- target at the very end if the final word alone reveals the answer
- long lead-ins before the target

### 5.3 Syntax

Use simple syntax:

- one finite clause
- no relative clauses
- no subordination unless unavoidable
- no idiom nested inside another idiom
- no passive voice unless passive use is central to the target sense

### 5.4 Non-target vocabulary

Non-target words should be common and easy for C1 learners. The item should not
require knowledge of a rare noun, technical term, or culture-specific event.

Recommended:

- mostly high-frequency words
- common academic/workplace nouns where appropriate
- familiar proper names only when they do not carry content knowledge

Avoid:

- rare nouns introduced only to create a mismatch
- technical vocabulary outside general academic/professional English
- culturally specific institutions or events

### 5.5 Acceptable sentence

An acceptable sentence must:

- use the intended PV sense naturally
- be plausible in ordinary English
- avoid overexplaining the sense
- avoid giving a synonym or paraphrase nearby
- be acceptable across major standard varieties unless a register is specified

### 5.6 Unacceptable sentence

An unacceptable sentence must:

- be semantically inappropriate because the target PV sense does not fit
- preserve the same broad domain as the acceptable sentence
- preserve similar syntax and length
- use a plausible noun or complement, not an absurd one
- avoid an alternate PV sense that makes the sentence acceptable

The unacceptable item should be a near-miss, not nonsense.

Good near-miss types:

- task vs proposition in the same research domain
- evidence vs outcome in the same legal/academic domain
- role vs event in the same institutional domain
- process vs document component in the same discourse domain

Bad near-miss types:

- person vs furniture
- event vs pencil
- deadline used repeatedly as a generic wrong object
- subject animacy mismatch
- impossible physical action
- number reversal that can be solved without knowing the PV

### 5.7 Cue bans

Do not use:

- `but`, `although`, `however`, or overt contrast markers
- `never`, `no`, `nothing`, or negation as the source of unacceptability
- obvious antonymic pairs
- transparent quantity changes for increase/decrease senses
- sarcasm, irony, or special intonation
- topic shifts where discourse coherence reveals the answer

## 6. Multiple-list design

Use two main LJT lists, with optional future expansion to four forms if item
calibration requires it.

### 6.1 Two-list core

For 48 targets:

- List A: 48 trials, 24 acceptable and 24 unacceptable
- List B: 48 trials, opposite condition for each target
- Each learner sees each PV once.
- Across List A and List B, both acceptable and unacceptable sentences are
  observed for every PV.

This differs from Uchihara et al.'s paired scoring, where both appropriate and
inappropriate uses were available per target. The adaptation is justified to
avoid repeated PV exposure and reduce fatigue, but it must be reported as a
counterbalanced PV-LJT rather than a literal replication of the original
single-word LJT scoring format.

### 6.2 Assignment constraints

Within each list:

- 24 acceptable, 24 unacceptable
- equal or near-equal source distribution
- equal or near-equal register distribution
- no more than two same responses in a row
- same base verb gap: at least 8 trials where possible
- same particle gap: at least 4 trials where possible
- high-risk items not clustered

### 6.3 Participant assignment

The participant-facing app should auto-assign:

- list A/B
- voice male/female
- F/J response mapping

Assignment should be deterministic from normalized participant ID but balanced
across participants as much as possible. Participants should not self-select
list or voice in the production version.

## 7. Audio and timing

ElevenLabs TTS will continue to be used, but TTS output must be treated as a
recording candidate, not as automatically production-ready audio.

### 7.1 Audio generation

Use fixed generation settings across all files:

- one male and one female voice
- same model and output format across voices
- stable generation manifest
- no API keys in manifests or materials
- consistent audio paths and file names

### 7.2 Audio quality gate

Every generated file must pass native/expert listening review:

- complete sentence
- no clipping or noise
- comparable loudness
- no unnatural pause between verb and particle
- no exaggerated stress on the particle
- no prosodic cue to acceptability
- no pronunciation that makes the PV ambiguous
- no voice acting that changes the intended meaning

### 7.3 Playback

Production LJT:

- main trials should play once
- replay should be disabled by default
- if replay is allowed for accessibility, replay count must be modeled and
  replay trials must be flagged
- response buttons should become available after the audio has started; the
  precise timing policy must be fixed before piloting

Recommended for first C1 pilot:

- one mandatory play
- no replay on main trials
- RT measured from audio offset
- soft response warning after 6 seconds
- timeout after 10 seconds only if piloting shows it does not add noise

## 8. Practice trials

Practice trials should train the task procedure, not the target strategy.

Requirements:

- 6-8 practice trials
- balanced acceptable/unacceptable
- PVs not used in the main target set
- no paired acceptable/unacceptable examples of the same PV in immediate
  succession
- no real-real-real-foil-foil patterning
- feedback in practice only
- no feedback in main trials

## 9. Item review rubric

Each candidate PV pair receives a 100-point validity score. A production item
must score at least 90 and must not fail any critical gate.

Weights:

- PV-sense dependency: 25
- near-miss quality: 20
- cue control: 15
- polysemy and alternate-sense control: 15
- acceptable sentence naturalness: 10
- audio robustness: 10
- C1 suitability: 5

Critical gates:

- If the unacceptable sentence is acceptable under a common sense, reject.
- If the item can be answered from an absurd noun or impossible event, reject.
- If native/expert raters disagree on the key, revise or reject.
- If TTS prosody can flip the key, reject or re-record.

Interpretation:

- 90-100: production candidate
- 80-89: minor revision candidate; not recordable yet
- 70-79: major revision candidate
- below 70: replace target or rebuild pair

The machine audit is necessary but insufficient. Passing word-count and overt
cue checks does not imply construct validity.

## 10. Native/expert validation protocol

Minimum before production freeze:

1. Two native speakers of English independently rate each sentence.
2. One applied linguist or vocabulary/PV researcher reviews pair rationale.
3. Disagreements are resolved by revision, not majority vote alone.
4. Revised items are re-rated.

Sentence-level ratings:

- acceptable item naturalness
- unacceptable item unambiguity
- PV-sense dependency
- general cue risk
- alternate-sense risk
- audio suitability

Pair-level decision:

- keep
- revise minor
- revise major
- replace target/sense
- drop

## 11. Participant scoring

### 11.1 Trial score

Each trial is scored binary:

- 1 = participant response matches the keyed expected response
- 0 = incorrect, timeout, or missing response

### 11.2 Person score

Primary score:

- total correct out of 48
- percent correct

Report separately:

- acceptable accuracy
- unacceptable accuracy
- response bias
- median RT for correct no-replay trials
- timeout rate
- flagged/replay rate if replay is enabled

### 11.3 Item analysis

At pilot stage, estimate:

- item facility
- discrimination
- condition-specific accuracy
- RT distribution
- list effect
- voice effect
- response-key effect
- local dependence by shared verb or particle

Production freeze requires:

- acceptable internal consistency for the intended use
- no item with extreme facility unless theoretically justified
- no item with negative discrimination
- no systematic voice/list/key bias

## 12. Production-freeze requirements

Do not call any new set `production` until all are true:

- 48 targets have final keep decisions.
- All 96 sentence candidates have expert ratings.
- All 96 audio files per voice pass audio review.
- Two counterbalanced lists are generated from the frozen item pool.
- Practice trials are finalized and separate from target PVs.
- A production manifest identifies the exact files used.
- README states one current production version and one analysis join table.
- Deprecated files are clearly labeled as historical.

Recommended name:

- `aural_pv_ljt_items_v7_c_level_freeze.tsv`
- `aural_pv_ljt_list_A_v7_c_level_freeze.tsv`
- `aural_pv_ljt_list_B_v7_c_level_freeze.tsv`
- `pilot_trial_file_ljt_list_A_v7_c_level_freeze.tsv`
- `pilot_trial_file_ljt_list_B_v7_c_level_freeze.tsv`

Avoid using `production` before the freeze is actually complete.

## 13. Immediate next work

1. Build a replacement-candidate pool for the 17 weak/drop targets.
2. Select 48 target senses using frequency, opacity, register, and
   C1-suitability criteria.
3. Draft two sentence candidates per target.
4. Run automated checks for length, target position, repeated nouns, overt
   cues, same-domain labels, and list balance.
5. Create an expert review form using the rubric in
   `c_level_pv_ljt_item_review_rubric_v1.tsv`.
6. Only after review, generate ElevenLabs audio for the frozen candidate set.

## References used

- Cheng, J., Matthews, J., Lange, K., & McLean, S. (2022). Aural single-word
  and aural phrasal verb knowledge and their relationships to L2 listening
  comprehension. TESOL Quarterly. https://doi.org/10.1002/tesq.3137
- Gardner, D., & Davies, M. (2007). Pointing out frequent phrasal verbs: A
  corpus-based analysis. TESOL Quarterly, 41(2), 339-359.
  https://doi.org/10.1002/j.1545-7249.2007.tb00062.x
- Garnier, M., & Schmitt, N. (2015). The PHaVE list: A pedagogical list of
  phrasal verbs and their most frequent meaning senses. Language Teaching
  Research, 19(6), 645-666. https://doi.org/10.1177/1362168814559798
- Ionin, T., & Zyzik, E. (2014). Judgment and interpretation tasks in second
  language research. Annual Review of Applied Linguistics, 34, 37-64.
  https://doi.org/10.1017/S0267190514000026
- Liu, D. (2011). The most frequently used English phrasal verbs in American
  and British English: A multicorpus examination. TESOL Quarterly, 45(4),
  661-688.
- Plonsky, L., Marsden, E., Crowther, D., Gass, S. M., & Spinner, P. (2020).
  A methodological synthesis and meta-analysis of judgment tasks in second
  language research. Second Language Research, 36(4), 583-621.
  https://doi.org/10.1177/0267658319828413
- Read, J. (2023). Towards a new sophistication in vocabulary assessment.
  Language Testing, 40(1), 40-46. https://doi.org/10.1177/02655322221125698
- Saito, K., Hosaka, I., Suzukida, Y., Takizawa, K., & Uchihara, T. (2026).
  Timed vs. untimed lexicosemantic judgement task for measuring automatized
  phonological vocabulary knowledge. Second Language Research.
  https://doi.org/10.1177/02676583261420616
- Saito, K., Uchihara, T., Takizawa, K., & Suzukida, Y. (2024). Declarative and
  automatized phonological vocabulary knowledge in L2 listening proficiency:
  A training study. Applied Psycholinguistics, 45(6), 1187-1218.
  https://doi.org/10.1017/S0142716424000468
- Sonbul, S., Salam El-Dakhs, D. A., & Al-Otaibi, H. (2020). Productive versus
  receptive L2 knowledge of polysemous phrasal verbs: A comparison of
  determining factors. System, 95, 102361.
  https://doi.org/10.1016/j.system.2020.102361
- Uchihara, T., Saito, K., Kurokawa, S., Takizawa, K., & Suzukida, Y. (2025).
  Declarative and automatized phonological vocabulary knowledge:
  Recognition, recall, lexicosemantic judgment, and listening-focused
  employability of second language words. Language Learning, 75(2), 458-492.
  https://doi.org/10.1111/lang.12668
