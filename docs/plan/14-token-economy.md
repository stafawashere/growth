---
title: Token economy
research_date: 2026-09-20
status: draft
purpose: Rank every method that lowers the AI layer's token cost to exam day without lowering teaching effectiveness, price each one against tools/cost_model.py, name the quality instrument that would detect the loss and the measurement that settles it, and hand the operator a line by line plan that fits a $100.00 ceiling.
---

# Token economy

`13-ai-engineering.md` prices the AI layer at $348.05 to exam day. The operator's ceiling is
$100.00. This document is the gap, closed direction by direction.

Every dollar figure here is emitted by `python3 tools/cost_model.py` and
`python3 tools/cost_model.py --check docs/plan/14-token-economy.md` exits 0. Where this document
needed a figure the calculator did not emit, the calculator gained a named constant with its tag
and `tests/tools/test_cost_model.py` stayed green. Nothing is recalled from memory and no figure is
arithmetic done in prose.

Four quality floors are not tradeable and nothing below relaxes one. The verifier never sees the
key. An unverified item is never served. The deterministic checks decide before a model does. A
disagreement routes to review and is never averaged. No key material enters a log, a URL or an
audit detail. Elaborated feedback keeps the three parts `03-diagnosis-and-feedback.md` requires.
A direction that breaks one is listed under rejected with the floor that rejects it.

A saving counts only when it names the instrument that would detect the quality loss. The
instruments are the ones `10-quality-and-evaluation.md` and `13-ai-engineering.md` already define:
golden set 1's key equivalence and calculator boundary, golden set 2's exact match and escalation
rate, golden set 3's expression level exact match, the 100 item audited key error rate, the
false mastery rate in simulation under 5 percent, and the operator's three part check on a feedback
sentence.

## What the ceiling changes [verified]

The recommended tier is $348.05, Anthropic $327.69 and Google $20.36
[measured: `python3 tools/cost_model.py`, the `tier.recommended` lines]. It is 3.48 times the
ceiling, so this is not a trimming exercise. Two lines carry the overrun: the generator at $177.62
and the evals at $76.60, which are 73.0 percent of the tier between them. The grader at $44.34 is
third. Everything else together, meaning the tutor at $5.01, the transcriber at $3.41, the
diagnostician at $20.51, the verifier at $20.36 and the Haiku 4.5 screen at $0.20, is $49.49.

That shape decides the ranking. The largest direction changes the unit of generation. The second
largest stops paying for a measurement the design already makes for free. The third stops calling a
model on points a deterministic checker already decides. None of the three is a discount on
teaching; each is a call the plan makes that its own design says it does not have to make.

The one lever the plan has already taken is worth restating so nobody counts it twice: effort
`medium` rather than the documented default of `high` on the generator is worth $126.49 on one bank
pass, and dropping `metadata` from the generator schema is worth $22.96. Both are already inside
the $348.05. Nothing below re-sells them.

## Ranked directions [verified]

Ranked by dollars saved to exam day. Effort is build effort, low meaning a configuration change,
medium meaning code that already has a home in the plan, high meaning new code and a new gate.

| Direction | Saved to exam day | Quality risk | Instrument that detects it | Settling measurement | Effort |
| --- | --- | --- | --- | --- | --- |
| 1. Generation authors one template per archetype, the backend instantiates | $160.24 | A key error becomes a template property, so one bad template poisons 40 items instead of 1 | 100 item audited key error rate, stratified to at most 1 item per template so 100 items cover about 100 templates | The per step defect rate and key error rate on a bank built from gated templates, against the hand authored P1 rate | high |
| 2. The grader's call count honours the deterministic partition 03 already specifies | $34.22 | None from the partition itself; the risk is mis-classifying a point type as mechanical when its `earns` text is not fully expressible as one of the four checks | Golden set 2 per point type exact match, reported with its count | The operator labels each of the 76 BC-PT records for whether its `earns` text is fully expressible as one of the four checks. Zero tokens, offline, today | medium |
| 3. Golden set 2's monthly run drops to one sample; three samples only on a full run | $25.92 | The adversarial set stops reporting an escalation rate monthly | Escalation rate on real gradings, which is continuous and free | Whether the canary and the full run ever disagree in direction on exact match over two full runs | low |
| 4. Grader thinking off, as an alternative to direction 2 rather than on top of it | $25.20 | A justification point whose decision flips under a thinking pass is decided without one | Golden set 2 aggregate exact match against fixed operator labels, and the escalation rate | The sweep 13 already names: escalation rate and exact match with thinking on against off, on the same golden set 2 responses | low |
| 5. Golden set 1 moves onto the free template gate | $12.69 | None. The gate asserts the same properties over 300 draws that the eval asserted over 1 | Golden set 1's own assertions, now run by `tools/template_trial.py` `run_draws` | Nothing. The gate is strictly stronger at 300 draws than the eval at 1 | medium |
| 6. The diagnostician runs on a recurring error path, not on every incorrect attempt | $12.30 | A first occurrence gets feedback with no misconception hypothesis | 11's diagnostician exit floor, two ranked hypotheses on at least 80 percent of diagnosed errors, plus the error type recurrence rate after diagnosis | The recurrence rate of a BC-ERR path with and without a first occurrence diagnosis | medium |
| 7. Grader draws a third sample only when the first two disagree | $11.02 | The strictness varied third sample stops running on agreed points, so leniency drift is visible on fewer points | Leniency calibration against the 2025 per point means, and the escalation rate | The measured disagreement share over the first month against the assumed 0.25 | low |
| 8. Verifier moves to `gemini-3.5-flash-lite` on batch | $7.49 before 2027-01-01, $27.69 after | A weaker blind re-solver raises false disagreement, which costs operator review time, or agrees for a shared reason, which is worse | The 100 item audited key error rate, and the escalation rate on the verification stage | The disagreement rate with the generator on the same 500 items, Flash-Lite against 3.8 Flash | low |
| 9. The bank pass runs before 2026-12-31 | $20.20 of avoided price doubling on the verifier line | None. It is a calendar decision | The Gemini pricing page, which prints the promotional end date | Nothing. The date is printed | low |
| 10. Tutor stays at 12 calls a session rather than 20 | $2.70 | Fewer guardrail nudges at the `example` and `completion` stages | The operator's three part check, and the distribution of tutor calls per item | The per item ceiling's bind rate over a month of real sessions | low |

Directions 2 and 4 are alternatives on the same line and are not additive. Direction 7 composes
with either.

## The $100 tier, line by line [verified]

| Line | Setting | Cost |
| --- | --- | --- |
| tutor, 12 calls a session, thinking disabled, effort low, 1h cache | unchanged from 13 | $5.01 |
| grader, 3 samples on the model judged share of 1,200 points | direction 2 | $10.11 |
| transcriber, 200 photographed pages | unchanged from 13 | $3.41 |
| diagnostician, on a recurring error path only | direction 6 | $8.21 |
| generator, 348 template authoring calls on the Batch API | direction 1 | $17.37 |
| verifier, 6,178 blind re-solves on `gemini-3.5-flash-lite` batch | direction 8 | $12.71 |
| Haiku 4.5 screen between transcriber and grader | unchanged from 13 | $0.20 |
| evals, golden set 1 on the template gate, golden set 2 mixed, golden set 3 monthly | directions 3 and 5 | $38.00 |
| **Total** | | **$95.03** |

Headroom against the ceiling is $4.97, and the saving against the recommended tier is $253.02
[measured: the `tier.hundred` lines of `python3 tools/cost_model.py`]. Against the $20.00 of credit
on hand it still needs $75.03.

**The tier's single point of failure is direction 2.** The grader line rests on a measurement that
does not exist. 17 of the 76 active BC-PT records answer yes to at least one of
`justification_required`, `interpretation_required` or `hypotheses_required`
[measured: `python3` over `data/scoring_points.json`, 2026-09-20, 76 active records, 59 answer no
to all three, 14 require justification, 3 require interpretation, 3 require hypotheses]. That is a
lower bound on the model share, not the share, because 03 adds a second condition the data does not
carry: the point's `earns` text must also be fully expressible as one of the four deterministic
checks. If every judged point turns out to need the model, the grader line returns to $44.34 and
the tier becomes $129.25, an overrun of $29.25. Directions 4 and 7 together bring that worst case
to $99.33, with $0.67 of headroom, which is too tight to plan on and is why the operator's labelling
pass is the first thing to do.

## Per role model choice [verified]

**No role moves to Haiku 4.5 and the arithmetic says so.** Haiku 4.5's prompt cache minimum is
4,096 tokens against Sonnet 5's 1,024 (https://platform.claude.com/docs/en/build-with-claude/prompt-caching
[verified, re-read in 13 on 2026-09-20]), and it is absent from the effort parameter's supported
model list (https://platform.claude.com/docs/en/build-with-claude/effort [verified, same]). The
tutor prefix of about 1,100 tokens therefore cannot cache on Haiku 4.5, so the comparison is a
cached Sonnet 5 call against an uncached Haiku 4.5 call. The tutor cycle is $5.01 on Sonnet 5 with
the prefix cached. Haiku 4.5's rates of $1 and $5 per MTok against Sonnet 5's $2 and $10 do not
recover the cache, and the difference is smaller than the $2.70 that moving from 20 calls a session
to 12 is worth. The transcriber's move off Haiku 4.5 is already decided in 13 on resolution grounds
and nothing here reopens it. Haiku 4.5 keeps the one role it has, the output screen between the
transcriber and the grader, at $0.20 for the cycle, and that call is correctly priced uncached.

**The verifier moves to a cheaper Gemini tier.** The pricing page prints Gemini 3.5 Flash-Lite at
$0.30 input, $2.50 output and $0.03 cached input, with batch at $0.15 and $1.25, and prints no
promotional end date against those figures, while Gemini 3.8 Flash carries "$0.75 through December
31, 2026. $1.50 starting January 1, 2027" on input and "$3.75 through December 31, 2026. $7.50
starting January 1, 2027" on output (https://ai.google.dev/gemini-api/docs/pricing [verified,
fetched 2026-09-20]). The model page prints Flash-Lite's capability list as "Caching (Supported),
Code execution (Supported), ... Structured outputs (Supported), Thinking (Supported)", with an
input limit of 1,048,576 tokens and an output limit of 65,536, and names Batch API among its
consumption options (https://ai.google.dev/gemini-api/docs/models/gemini-3.5-flash-lite [verified,
fetched 2026-09-20]). The verifier's schema is an answer plus a solution path, which is shallow, so
nothing the role needs is missing. A verifier call is $0.003270 on 3.8 Flash batch and $0.002058 on
Flash-Lite batch, and 6,178 calls are $20.20 against $12.71. The saving doubles to $27.69 for a
bank pass that lands after 2026-12-31.

**The generator stays on Opus 5 and the reason changes.** 13 records that the same bank pass costs
$71.05 on Sonnet 5 batch against $177.62 on Opus 5 batch, a saving of $106.57, and calls that the
largest single saving available. Under direction 1 it is not, because the generator's call count
falls from 7,784 to 348 and the whole line falls to $17.37. A Sonnet 5 template pass would save a
fraction of $17.37 while spending the model's judgement on the one artefact in the system that 40
items inherit from. Downgrading the model that authors the template is the worst dollar per risk
trade in this document.

**The grader, the diagnostician and the tutor stay on Sonnet 5.** 13's reasoning holds and nothing
found here outranks it. The roles whose errors reach a student directly are the grader, the verifier
and the transcriber, and the two that stay on a frontier tier under this plan are the grader and the
transcriber. The verifier is the exception and it is defended by the deterministic checks that
bracket it: a Flash-Lite answer is never trusted, it is compared under SymPy against a key three
other checks already agree on, and a disagreement routes to review rather than to publication.

## Thinking and effort per role [verified]

Thinking is on by default on Opus 5 and Sonnet 5 and its tokens are billed as output, and
`output_config.effort` defaults to `high` (https://platform.claude.com/docs/en/build-with-claude/thinking
and https://platform.claude.com/docs/en/build-with-claude/effort [verified, re-read in 13 on
2026-09-20]). 13 already sets thinking off on the tutor and the transcriber and effort `medium`
elsewhere, and that is worth $8.56 and $126.49 respectively. What is left is one role.

**The grader's 700 thinking tokens are 70 percent of its output and $25.20 of its $44.34.** 13
keeps them and states the tension honestly: thinking reintroduces run to run variance on the one
role whose disagreement detector was built on the premise that two identically configured samples
should agree, and temperature is no longer available to pin anything because a non-default
`temperature` is a 400 on both routed models [verified, recorded in 13]. The settling measurement is
already written in 13 and is unchanged here: escalation rate with thinking on against off, on the
same golden set 2 responses whose intended score the operator has fixed. If thinking on escalates
materially more without improving exact match, the extra escalations are noise and $25.20 is free.

**The effort sweep is still unpriced and still unmeasured.** No provider page prints a token count
by effort level for a given task shape, which 13 lists among its unsourced claims and this document
does not improve on. What has changed is how much rides on it: under direction 1 the generator emits
348 calls rather than 7,784, so the effort setting on the generation role is worth roughly a twenty
second of what it was worth, and the effort lever moves to the grader and the verifier where the
call counts now dominate. That is a reordering, not a new measurement.

**One trap the documentation prints and 13 does not carry.** Disabling thinking on Opus 5 has two
documented failure modes, a tool call written into visible text and `<thinking>` tags leaking into
the response, and the guidance is to prefer low effort over disabled thinking on that model. No role
in this plan disables thinking on Opus 5: the two disabled roles are the tutor and the transcriber,
both on Sonnet 5, where `{"type": "disabled"}` is accepted. The rule to carry forward is that the
template authoring role on Opus 5 must not be configured with thinking disabled to save tokens,
because effort `low` is the supported way to ask for the same thing.

## Prompt caching [verified]

13 settles the prefix design, the breakpoints, the TTL and the sub-minimum trap, and the rules do
not change under a $100.00 ceiling. Three things do change.

**The template authoring prefix clears every minimum with room.** `tools/template_trial.py` already
sends its instruction block as a system message with `cache_control` at a 1 hour TTL. That block is
4,420 characters [measured: `len(INSTRUCTIONS)` in `tools/template_trial.py`, 2026-09-20], which at
the 3.1 divisor is about 1,426 tokens against Opus 5's 512 minimum. The per archetype user turn is
1,582.3 characters on average over all 139 active archetypes
[measured: `build_prompt` over the 139 active records of `data/archetypes.json`, 2026-09-20], so the
cached share of a template call's input is about 53 percent. The cost model writes the prefix 139
times and reads it on the other 209 calls.

**The tutor's cross attempt sentence cache is worth less than it looks, and the reason is the draw
rule.** `03-diagnosis-and-feedback.md` selects the three parts deterministically from the violated
step, the BC-ERR record's `observed_behavior` and `scoring_consequence`, and the stored worked
solution, so the composed sentence is a pure function of the item, the chosen option and the
guardrail level. That looks like a perfect cache key. It is not, because 13 adopts a least recently
served draw precisely so the same item is not served twice, and the distinct item corroboration rule
forbids crediting the same item three times. A cache whose hit rate is high is a cache sitting on
top of a repeat exposure problem the engine exists to prevent. The honest saving is close to zero
and the direction is not ranked.

**The sub-minimum miss is still undetectable in code.** 13 records that
`app/providers/guard.py` `_reconcile` conflates a null usage field with a zero and that
`app/db/models.py` types the columns non-nullable, which disables the cache hit rate metric that is
the only way to see a silent sub-minimum miss. That defect is worth naming again here because every
cache figure in this document is a model output rather than a measurement, and it stays that way
until that field distinction exists.

## Batch API [verified]

Everything off the interactive path already batches in 13: generation, independent verification, and
golden set 1. Under direction 1 the batch shrinks from 7,784 generation requests to 348, which
removes the only workload in the plan that approached the Start tier's rate limits and makes the
whole authoring pass a single small job.

Cache behaviour inside a batch is unchanged and still best effort, with reported hit rates of 30 to
98 percent and the documentation's own advice being identical `cache_control` blocks across the
batch and a 1 hour TTL (https://platform.claude.com/docs/en/build-with-claude/batch-processing
[verified, re-read in 13 on 2026-09-20]). 13's shape was one batch per archetype so that every
request shared a prefix byte for byte. Under direction 1 that shape inverts: there is one request
per archetype, and the prefix that must be shared is the instruction block, which is identical
across all 348 requests. So the whole authoring pass is one batch with one shared prefix, which is
the configuration the documentation's advice describes rather than the one 13 had to engineer
around.

The retry ladder matters more than before. `tools/template_trial.py` sets
`MAX_GENERATION_ATTEMPTS = 3` and the gate feedback loop re-authors a failing template. A batch
cannot carry that loop, because results are matched by `custom_id` and a re-author depends on the
previous result. The pass is therefore up to three batches in sequence, each carrying only the
archetypes that failed the previous gate run, which is still one shared prefix per batch.

## Output shape [verified]

The generator's `metadata` block already left the schema in 13, worth $22.96. Three further shape
decisions follow from direction 1.

**The template schema is the output shape now.** `TEMPLATE_SCHEMA` is 2,280 characters
[measured: `len(json.dumps(TEMPLATE_SCHEMA))` in `tools/template_trial.py`, 2026-09-20]. Whether a
structured output schema is billed as input tokens is unknown from the loaded page, so the cost
model charges it as uncached input, which errs high.

**The measured template body is 778.10 tokens and the priced one is 1,100.** The 26 template
artifacts under `var/` average 2,412.1 characters of compact JSON
[measured: `json.dumps(..., separators=(",", ":"))` over the 26 files, mean 2,412.1, median 2,372.5,
min 1,910, max 3,212, 2026-09-20]. Every one of them predates the `representation`, `figure`,
parameter `role` and allowed error path fields the extended gate now requires, and 13 records that
0 of 26 pass it. The priced figure is raised to 1,100 visible tokens for those fields and is
`[inferred]`.

**`max_output_tokens` is the one setting direction 1 makes riskier.** `tools/template_trial.py`
sets 16,000, which is right for a template and would be wasteful per item. The monitoring rule is
unchanged and now matters more: any `stop_reason: "max_tokens"` on a template authoring call is a
truncated template, and a truncated template that still parses is the failure mode the gate has to
catch rather than the budget.

## Doing less with models [verified]

This is where the money is, and every item in it is the plan choosing not to make a call its own
design says it does not have to make.

**The template architecture, one model call per archetype.** 13's "Template architecture and the
migration" section already adopts the shape: "The model authors one parameterised template per
archetype, the backend instantiates it, and everything downstream sees an item." Its cost model does
not follow, and still prices 56 generation calls per archetype at $177.62. That is the single
largest inconsistency in 13 and closing it is direction 1. Priced from the measured prompt and
artifact sizes above, 139 archetypes at 2.5 authoring attempts each is 348 calls at $0.0540 a call,
so $17.37 against $177.62, a saving of $160.24 and 9.8 percent of the per item pass.

The 2.5 attempts is `[inferred]` from `MAX_GENERATION_ATTEMPTS = 3` and from 0 of 26 templates
passing the extended gate today. At 3.0 attempts the line is higher and the saving is still the
largest in the document by an order of magnitude; the direction does not turn on that number.

What the gate buys back is not a cost argument and belongs here anyway. `tools/template_trial.py`
`run_draws` checks eleven properties over 300 seeded draws: LaTeX balance, doubled signs, math mode
presence and vacuous steps under a 2 percent surface rate, key disagreement at zero, the key not a
copy of the last step, a draw space of at least 2,000, a declared representation with a figure spec
where the representation is graphical, every distractor's `error_path` an active BC-ERR id, every
`point_type_id` a BC-PT id, exactly four options, and the declared parameter roles checked by
structural invariance. Those are stronger assertions than golden set 1 makes, and they run on every
draw rather than on one frozen draw, for free, offline, with no key.

The literature 13 already collected says templating is right and says where it bites. Isomorphs do
not share a difficulty: 9 of 23 templates isomorphic on a first pass, 20 of 50 item models with a
facility spread above 0.15 across variants, and 10 to 30 percent item loss after calibration
[single-source, the four papers recorded in 13's "Radicals and incidentals"]. The mitigation is
already built, which is the radical and incidental declaration and the structural invariance check,
and the residual is a known centre-ward bias in `p_A` that 02 accepts.

**Golden set 1 moves onto the template gate.** Golden set 1 replays generation against a frozen
parameter draw and asserts four things. Under direction 1 the instantiation is deterministic code,
so replaying a frozen draw is free and produces the identical item every time. Three of the four
assertions are exactly gate checks, and the fourth, key equivalence under SymPy, is the gate's
`KEY_DISAGREEMENT_BAR = 0` over 300 draws. So golden set 1's model cost is $0.00, its assertions get
300 times the sample, and the $12.69 the eval was going to cost disappears. What survives as a paid
eval is re-authoring templates after a prompt version bump, at $7.51 for all 139, which is the same
event that triggered golden set 1 in 13's schedule.

**The grader's deterministic partition, honoured in the call count.** 03 states that a point whose
BC-PT record answers no to `justification_required`, `interpretation_required` and
`hypotheses_required`, and whose `earns` text is fully expressible as one of four deterministic
checks, is decided by the checker and never reaches a model, and calls that partition "the single
highest-leverage design choice in the grader". 13's cost model prices 1,200 judged points times 3
samples as 3,600 model calls, which prices the partition at zero. At the field bound, 17 of 76 point
types require a model, so 268 of 1,200 judged points do, 804 calls rather than 3,600, and $10.11
rather than $44.34.

**The diagnostician on recurrence rather than on every error.** All three parts of elaborated
feedback are available without the diagnostician: the rule violated comes from the BC-PT record or
the `expected_solution_path` step, the scoring consequence comes from `errors.scoring_consequence`
or the BC-PT `does_not_earn` text, and what the correct response would have shown comes from the
stored worked solution. The diagnostician adds a fourth thing, a ranked misconception hypothesis,
which 03 permits the app to surface only as a question and only through a discriminating probe. On a
first occurrence of an error path there is nothing to rank: one observation does not distinguish a
slip from a misconception. On a recurrence it does. At an `[inferred]` 0.35 recurrence share the
line is 564 calls and $8.21 rather than 1,610 calls and $20.51.

This is also the one direction with a positive learning argument rather than a neutral one. 03 is
explicit that feedback must not assert a misconception it does not know, and a hypothesis drawn from
a single observation is exactly the assertion it warns against.

**What is already free and stays free.** Micro-session MCQ and short answer grading is deterministic
through SymPy and costs nothing. The composed tutor sentence is cached on `attempts.tutor_sentence`,
so a re-read of the feedback screen is free. The Monte Carlo family pass runs once per archetype
rather than once per item. The verification pipeline runs its four free stages before the paid one.
None of that is a new direction and all of it is load bearing for the tier above.

## Call count ceilings, and when the tutor is worth calling [verified]

13 sets a per session ceiling of 20 tutor calls and a per item ceiling of 3, and prices the traffic
model at 12 calls a session. The cycle is $5.01 at 12, $2.65 at 5 and $7.71 at 20.

**The tutor is the cheapest line in the system and the only model output the student reads every
day.** At $5.01 for 230 days it is 5.3 percent of the $95.03 tier. Any direction that removes it
trades the whole of the elaborated feedback advantage for less than the price of one eval run, and
the evidence for that advantage is the strongest in the plan: Shute concludes elaborated feedback
beats verification only feedback [verified, cited in 03], Bangert-Drowns et al find feedback helps
when it supplies correct answer information the learner cannot already anticipate [single-source,
cited in 03], and Hattie and Timperley report an average feedback effect around d = 0.79 while
arguing the effect is highly variable [single-source, cited in 03]. The only tutor direction ranked
is holding the traffic model at 12 calls a session rather than 20, worth $2.70, and even that is a
guardrail question rather than a cost question.

**Where the pedagogy says the calls should sit.** 03's timing policy puts immediate step level
verification at the `example` and `completion` stages and no feedback of any kind until submission
at the `unsupported` stage and on every exam shaped item. The per item ceiling of 3 therefore binds
almost entirely at the acquisition stages, which is where the intelligent tutoring literature 03
cites favours immediate correction. A ceiling that binds often at the `unsupported` stage would mean
something is wrong with the item selection rather than with the budget, and 13 already says the two
are distinguishable from the attempt outcome.

**Retrieval practice and varied retrieval are the two mechanics that cost nothing and are already
in.** The spacing and testing effect results 03 cites, Roediger and Karpicke at 61 percent against
40 percent at a one week delay and Cepeda et al's optimal inter-study gap, are engine behaviour
rather than model behaviour. Varied retrieval beating identical repetition at 0.64 against 0.52 on
transfer [verified, cited in 13] is the argument for the least recently served draw, which is one
line of selection code and moves the metric further than 50 percent more generation spend does. The
cheapest learning per dollar in this whole document is a draw rule change with no token cost at all.

## Cheaper measurement [verified]

**`count_tokens` is free and settles the largest measurement gap in 13.** `POST
/v1/messages/count_tokens` is free to use, subject to its own limit of 5,000 requests per minute on
the Start tier (https://platform.claude.com/docs/en/build-with-claude/token-counting [verified,
re-read in 13 on 2026-09-20]). Every prefix and output figure in 13 and in this document is a
character count divided by 3.1. One session with a key converts all of them from `[inferred]` to
measured at zero cost, and `BUILD-LEDGER.md` already names the missing key as the blocker on
`test_prompt_cache_prefix_length`. This is the highest value free measurement available and it is
listed as an open question below because it needs the operator's key.

**The escalation rate is a zero cost monitor and is already scheduled as one.** It is computed from
the three grader samples disagreeing with each other, needs no operator labels, and runs
continuously on real gradings. Under direction 7 it is computed from two samples with a third drawn
on disagreement, which measures the same quantity with the third sample as its own confirmation.
Under direction 2 it is computed on fewer points, because fewer points reach the model at all, and
that is the one real loss in direction 2: a smaller denominator makes the rate noisier.

**The smallest golden set that still discriminates is already computed and it is larger, not
smaller.** 13 computes that Cohen's kappa at 5 responses on 30 point types gives an interval of
0.2652 width, which cannot separate 0.47 from 0.56, and that excluding 0.47 needs 326 point
decisions. Its decision was to drop per point type kappa from the P3 gate and report per point type
exact match with its count. That decision is unchanged and it is what makes direction 3 safe: a
canary run at one sample measures exact match, which is the metric that survived, and the metric
that did not survive is not worth three samples a month.

**Two free measurements the operator can run today, before spending anything.** Labelling the 76
BC-PT records for direction 2 is offline and costs nothing. Running
`.venv/bin/python tools/template_trial.py draw` over a template costs nothing, needs no key, and is
the gate that decides direction 1.

## Local and offline fallbacks [single-source]

13 keeps an Ollama offline fallback on DeepSeek-R1-Distill-Qwen-14B, whose official card publishes
MATH-500 pass@1 93.9 and AIME 2024 pass@1 69.7 under an MIT licence, with the Ollama 14b tag a 9.0
GB download [verified, cited in 13].

**The role a local model could take is the verifier, and the saving is the whole $12.71.** The
verifier's task is a blind re-solve compared under SymPy against a key three deterministic checks
already agree on, its output schema is shallow, it is off the interactive path entirely, and a
disagreement routes to review rather than to publication. Every property that makes a role safe to
run on a weaker model holds. There is no privacy objection either, because the verifier sees a stem
and a figure spec and never a student's work.

**What it cannot do, and why it is not ranked.** The wall clock is the cost. 6,178 blind re-solves
of BC items on a 14B model on a laptop is an operator time budget, not a dollar budget, and nothing
in this repository or on Ollama's GPU page bounds it, because per quantisation VRAM is unpublished
[verified as absent, cited in 13]. It also cannot take any role that carries a student's work or
that a student waits on, and it cannot be the transcriber, because no handwriting mathematics
accuracy figure exists for any model, cloud or local [verified as absent, cited in 13]. The
direction is real, its dollar saving is the smallest of the top eight, and its cost is denominated
in the one resource this project is shortest of, which is the operator's time.

## What the literature moves that this plan does not use [single-source]

Four things were looked for and three were already in the plan.

**Automatic item generation from item models is direction 1**, and the psychometric literature 13
collected is the reason the direction carries a gate rather than a promise. Nothing new.

**Worked example study replacing problem solving early in a skill** is the fading ladder, which 03
and 02 already implement as `example`, `completion` and `unsupported` stages. It also happens to be
the cheapest stage to serve, because a worked example needs no grader call at all.

**Self explanation at g = 0.55 across 69 effect sizes** [verified, cited in 03] is already in, as
the student's one line error note after a corrected item, and it is the one place where the student
does the generating and the model does nothing. It is worth naming as the pattern the rest of this
document is an instance of: the cheapest token is the one the student spends instead.

**The one thing found that the plan does not use, and it is not recommended.** Nothing in the
tutoring systems literature read here supports replacing the model composed feedback sentence with a
templated one, and the plan's own instrument, the operator's three part check, would pass a
templated sentence by construction while measuring nothing about whether it reads as a sentence.
That is a case where the instrument is weaker than the decision, and the right response is to leave
the $5.01 alone rather than to spend it against a check that cannot see the difference.

## Rejected directions [verified]

| Direction | Why it is rejected |
| --- | --- |
| Verify per template on a sample of draws instead of per published item, saving about $7.49 more on the verifier line | Breaks the floor "an unverified item is never served". Item 37 of a template that received no blind re-solve is an unverified item under the floor as written. Whether the unit of verification may become the template is the operator's decision, not this document's, and it is in the open questions |
| Drop the tutor and compose the feedback sentence from a template, saving $5.01 | Does not break a floor and is rejected on learning grounds. It is 5.3 percent of the tier, it is the only model output the student reads daily, and 03's evidence for elaborated feedback is the strongest in the plan |
| Fold transcription and rubric evaluation into one call | Breaks nothing and is rejected by 13's existing decision, which stands: a combined call makes the 87 percent transcription share of residual grading errors unmeasurable, because a wrong grade cannot be attributed to a misread rather than to a rubric error |
| Route the generator, meaning the template author, to Sonnet 5 | Does not break a floor. Rejected on arithmetic: under direction 1 the whole line is $17.37, so the saving is a fraction of that, while the artefact 40 items inherit from is authored by a weaker model |
| Move the transcriber back to Haiku 4.5 to save $0.008008 a page | Rejected in 13 on resolution grounds and unchanged. Halving the linear resolution of a photographed page on the one role whose dominant failure mode is misreading is the wrong trade at any price |
| Drop the Haiku 4.5 screen between the transcriber and the grader, saving $0.20 | Rejected on the prompt injection control it provides. It is the only screen between an untrusted multimodal input and a model call, it costs $0.001000 a page, and removing it to save $0.20 over 230 days is not a cost decision |
| Average two grader samples instead of escalating on disagreement | Breaks the floor "a disagreement routes to review and is never averaged" |
| Put the item's key in a cached verifier prefix so the verifier prompt clears a cache minimum | Breaks the floor "the verifier never sees the key", and 13 already names a cached prefix as exactly the place a key could be smuggled in |
| Pad the tutor prefix to clear the Sonnet 5 cache minimum | Rejected in 13 and unchanged. Growing a prompt with filler to save $1.35 makes the prompt worse; the prefix is grown with content that earns its place or the breakpoint is removed |
| Reduce the published bank below 40 per archetype to save generation dollars | Under direction 1 the bank size stops being a cost lever on the generator at all, because instantiation is free. It remains a lever on the verifier line, and it is a learning decision about repeat exposure rather than a cost decision, so it stays where 13 put it |
| Use the 5 minute cache TTL anywhere to avoid the 1 hour write premium | Rejected in 13 by the three call floor and unchanged. The tutor, the grader and the diagnostician all span more than 5 minutes inside a session, so a 5 minute entry expires between calls and is rewritten, which is the sparse caller trap |

## What landed on 2026-09-20 [verified]

Eight of the ten ranked directions were written into the plan on the operator's instruction the same
day, and the two gated ones were not. What changed, file by file:

| File | What changed |
| --- | --- |
| `tools/cost_model.py` | Additive only. `gemini-3.5-flash-lite` prices, a `template` role, the grader's model share, the diagnostician's recurrence share, the golden set 2 canary, and the `tier.hundred` lines. No existing constant moved, so both configurations stay priced side by side and `tests/tools/test_cost_model.py` stays green |
| `13-ai-engineering.md` | The verifier row moves to Flash-Lite with 3.8 Flash second; the price table gains two Flash-Lite rows; a fourth tier is added at $95.03 and named the recommendation; a second per-role table prices the cycle under these directions; the eval schedule rows for golden sets 1 and 2 are rewritten; six tunables and five decisions are added |
| `07-ai-provider-layer.md` | D8's verifier row and the paragraph above it |
| `04-item-generation.md` | The independent re-solve's routing, and a paragraph on what the unit of generation does to caching, batching and the bank's cost |
| `10-quality-and-evaluation.md` | Golden set 1 moves onto the template gate; golden set 2's sampling and cadence split; which point types reach the grader at all; the P3 and P4 gates |
| `03-diagnosis-and-feedback.md` | A new section on when the diagnostician is called, and the rule-based section renamed from "unavailable" to "does not run" |
| `11-phased-delivery.md` | The BC-PT labelling pass becomes a P3 entry criterion; the calculator boundary joins the template gate |
| `12-open-questions.md` | Ten rows in the tunables register, including the two savings deliberately not taken |
| `docs/operator/ai-operating-costs.md` | The settings table, the spend table, four tiers, the eval schedule, the credit arithmetic under templates, and the 2026-12-31 calendar note |

Directions 4 and 7, grader thinking off at $25.20 and a conditional third sample at $11.02, are
recorded as decisions not to save money yet, each with its settling measurement, and are the remedy
held in reserve if the grader line comes in at its worst case.

## Proposed edits to tools/cost_model.py, not applied [inferred]

The additive constants this document needed are in the file, because `--check` cannot pass without
them, and the directions above landed by making the documents quote the alternative lines rather
than by moving a constant. The edits below would retire the superseded configuration instead of
pricing it beside the new one, and they are the operator's to approve line by line. None is applied,
and the reason for keeping both priced is in the generator row.

| Constant | Today | Proposed | Tag | Why |
| --- | --- | --- | --- | --- |
| `ROLES["generator"]` | one call per item, 7,784 calls | retired in favour of `ROLES["template"]`, 348 calls | [inferred] | Direction 1. Keeping both priced side by side is deliberate until the gate passes on a real template |
| `JUDGED_POINTS` used whole for the grader | 1,200 points, all reaching a model | split into a deterministic share and a model share | [inferred] | Direction 2. The split is a measurement the operator can make offline today |
| `GRADER_SAMPLES` | 3 on every point | 2, with a third on disagreement | [inferred] | Direction 7. The measured disagreement share replaces the assumed 0.25 after one month |
| `ROLES["grader"]["thinking"]` | 700 | 0 | [inferred] | Direction 4, and only after the sweep 13 names |
| `ROLES["verifier"]["model"]` | `gemini-3.8-flash` | `gemini-3.5-flash-lite` | [inferred] | Direction 8. Both prices are in the table already so the comparison recomputes |
| `MONTHLY_RUNS` applied to golden set 2 at 3 samples | 9 runs at 3 samples | 9 canary runs at 1 sample plus 2 full runs | [inferred] | Direction 3 |
| `GOLDEN_SET_1_RUNS` | 4 paid runs | 0 paid runs, the gate replaces it | [inferred] | Direction 5 |
| `INCORRECT_ATTEMPTS` used whole for the diagnostician | 1,610 | the recurring share | [inferred] | Direction 6 |
| `CHARACTERS_PER_TOKEN` | 3.1 | replaced by measured counts from `count_tokens` | [verified that the endpoint is free] | Every token figure in 13 and here is a character count divided by 3.1 |
| `TEMPLATE_THINKING_TOKENS` | 2,400 | the measured value from a real authoring call's `usage.output_tokens_details.thinking_tokens` | [inferred] | It is the largest uncertain quantity in direction 1 |
| `TEMPLATE_ATTEMPTS` | 2.5 | the measured attempts per archetype from the first gated pass | [inferred] | It scales direction 1 linearly |

## Open questions for the operator [uncertain]

Each one is a decision only the operator can make, and each blocks or sizes a direction above.

1. **Does the unit of verification stay the item, or may it become the template?** Per item blind
   re-solve is $12.71 on Flash-Lite. Per template sampled re-solve is cheaper and, as the floor is
   written today, serves unverified items. The floor is the operator's to restate or to keep.
   Keeping it is what the $95.03 tier assumes.

2. **Which of the 76 BC-PT records have an `earns` text fully expressible as one of the four
   deterministic checks?** This is the labelling pass that turns the grader line from a bound into a
   number, it costs nothing, it needs no key, and the whole tier's headroom depends on it. Without
   it the worst case is $129.25.

3. **Will a provider key be available for one session of `count_tokens` calls before any paid work
   starts?** It is free, it converts every token assumption in 13 and here from inferred to
   measured, and `BUILD-LEDGER.md` already lists it as the blocker on a P1 gate.

4. **Does the bank pass run before 2026-12-31?** The Gemini promotional prices end that day and the
   verifier line doubles from $20.20 to $40.40 on 3.8 Flash, or holds at $12.71 on Flash-Lite, which
   prints no end date.

5. **If direction 1's gate cannot be passed on real archetypes, what is the fallback?** The choices
   are the per item pass at $177.62, which does not fit the ceiling, or a smaller published bank,
   which is a learning decision about repeat exposure. This document does not choose between them.

6. **Is the operator's machine able to run a 14B model at a rate that makes the local verifier
   fallback real?** Per quantisation VRAM is unpublished, so the answer is a measurement on the
   operator's own hardware and nowhere else.

7. **Is $95.03 the target, or is the ceiling a hard stop that wants margin?** Headroom is $4.97. One
   re-authoring pass after a prompt bump is $7.51, which alone exceeds it. If the ceiling is hard,
   direction 7 should be taken at the same time as direction 2 rather than held in reserve.

## Claims I could not source [verified]

Every gap 13 lists is still a gap and is not repeated here unless this document leans on it harder.
These are the new ones.

- **The template authoring call's thinking token count.** Priced at 2,400, `[inferred]` as twice the
  per item generator's 1,200 at the same effort. No provider page prints a thinking count for any
  task shape, and this is now the largest uncertain quantity in the largest direction.
- **The compliant template body size.** Measured at 778.10 tokens over 26 artifacts and priced at
  1,100, because all 26 predate four required field groups. The measurement that replaces it is the
  first template that passes the extended gate.
- **The authoring attempts per archetype.** Priced at 2.5, `[inferred]` from
  `MAX_GENERATION_ATTEMPTS = 3` and from 0 of 26 templates passing today.
- **Whether a structured output schema is billed as input tokens.** Not printed on the structured
  outputs page as loaded. The cost model charges the 2,280 character schema as uncached input, which
  errs high.
- **The grader's true model share.** Bounded at 17 of 76 point types by the three required fields
  and unbounded above, because the second condition 03 states is a per record judgement the data
  does not carry.
- **The share of incorrect attempts on a recurring error path.** Priced at 0.35, `[inferred]`, with
  no source and no simulation behind it.
- **The share of judged points on which two grader samples disagree.** Priced at 0.25, `[inferred]`.
  The escalation rate measures it for free once grading is live, which is why direction 7 is ranked
  below the directions that do not need a live measurement first.
- **Gemini 3.5 Flash-Lite's blind re-solve quality on BC content.** The capability list is printed
  and the price is printed; no accuracy figure for AP Calculus BC exists on any page loaded, here or
  for any other model. The direction rests on the deterministic checks bracketing the role, not on a
  measured accuracy.
- **Gemini 3.5 Flash-Lite's explicit cache minimum and whether its thinking is billed as output.**
  The model page prints caching and thinking as supported and prints no minimum and no billing rule.
  The verifier is priced uncached, which is the same treatment 13 gives 3.8 Flash and errs high.
