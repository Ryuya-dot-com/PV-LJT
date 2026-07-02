# IRTree Plan for the Three-Stage PV Test

## Short Answer

Yes, the three-stage PV design can be examined as an IRTree-style model, but it should be framed as a multi-process response tree rather than as three ordinary tests placed in a fixed order.

The administration order can remain:

1. Aural PV-LJT
2. Audio phrasal verb decision
3. Orthographic PV meaning recognition

This order is defensible because it minimizes priming from easier or more explicit tasks.

However, the psychometric tree should be interpreted in construct order:

1. Orthographic explicit meaning knowledge
2. Aural PV form familiarity
3. Automatized contextual aural use

The administration order and the latent-process order do not need to be identical.

## Construct Interpretation

For each learner and each target PV, the three tasks provide a response profile:

- `LJT`: Can the learner judge whether the PV is semantically appropriate in an aural sentence context?
- `Audio decision`: Does the learner recognize the heard verb-particle sequence as a common English PV?
- `Orthographic recognition`: Can the learner select the correct English meaning in print?

The most theoretically important profiles are:

- `111`: robust/automatized PV knowledge
- `011`: explicit meaning plus aural form familiarity, but not automatized contextual use
- `001`: orthographic meaning only
- `000`: no observed knowledge

Other profiles are not useless. They are informative hierarchy violations and should be retained at first:

- `010`: aural form familiarity without explicit meaning
- `101`, `110`, `100`: likely slips, guesses, context effects, or task-specific noise

See `irtree_response_coding_v1.tsv` for the coding scheme.

## Candidate Model 1: Descriptive Latent-State Scoring

This is the safest first analysis.

For each PV and learner, code the observed profile as one of eight binary patterns. Then report:

- percentage of learners in each state
- percentage of items producing hierarchy-violating patterns
- relationship between state membership and PV item predictors:
  - sense frequency
  - opacity
  - register
  - source set
  - semantic category

This does not require strong IRTree assumptions and is ideal for the first pilot.

## Candidate Model 2: Multi-Process Explanatory IRT

Reshape the data to long format with one row per learner-item-node:

- node = `orthographic_recognition`
- node = `audio_decision`
- node = `aural_ljt`

Then fit a logistic mixed model or explanatory IRT model:

```text
correct ~ 0 + node
        + node:sense_frequency
        + node:opacity
        + node:register
        + (0 + node | learner)
        + (0 + node | item)
```

This estimates separate learner abilities and item difficulties for each process while allowing the same PV item to be linked across tasks.

This is not a strict IRTree yet, but it is likely the most stable first model.

## Candidate Model 3: Strict IRTree / Sequential Tree

A stricter IRTree can define a prerequisite-like tree:

```text
Node 1: Orthographic meaning recognized?
  no  -> no explicit PV meaning evidence
  yes -> Node 2

Node 2: Aural PV form recognized?
  no  -> orthographic-only knowledge
  yes -> Node 3

Node 3: Contextual aural LJT correct?
  no  -> declarative + aural form, not automatized
  yes -> automatized contextual PV knowledge
```

This model is elegant, but it assumes a hierarchy that may not always hold. The first pilot should therefore examine how often hierarchy violations occur before treating this as the main model.

## Practical Recommendation

Use the three-stage design, but analyze it in two steps:

1. First pilot:
   - descriptive response-pattern analysis
   - multi-process explanatory IRT / GLMM
   - inspect hierarchy violations

2. Main study:
   - fit an IRTree if the observed response profiles are sufficiently hierarchical
   - compare against the less restrictive multi-process model

If many learners show `010`, `101`, `110`, or `100` profiles, the data are telling us that PV knowledge is not a single linear hierarchy. In that case, a multidimensional explanatory IRT model is more appropriate than a strict IRTree.

## Design Implications

Keep all three tasks for the same 48 target PVs.

Avoid giving explicit feedback between tasks.

Keep the current administration order:

1. LJT first, because it is most vulnerable to priming.
2. Audio decision second, because it exposes the PV form but not its meaning.
3. Orthographic recognition last, because it gives the clearest semantic cue.

Record both accuracy and response time for LJT and audio decision. The IRTree-style accuracy model can be supplemented by reaction-time analyses for automatization.
