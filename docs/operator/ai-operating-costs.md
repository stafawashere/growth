---
title: AI operating costs
research_date: 2026-09-20
status: in_progress
purpose: What to set on each model role, what it will spend to exam day, what to watch, and what to do when a cap binds.
---

# AI operating costs

The reasoning behind every number here is in `docs/plan/13-ai-engineering.md`. This file is the
operating guide: settings, spend, signals, and what to do at each cap. Prices were read from the
providers' own pages on 2026-09-20 and are in `13-ai-engineering.md` with their URLs. Every dollar
figure below is printed by `python3 tools/cost_model.py`, and `tests/tools/test_cost_model.py`
fails if this file prints one the calculator does not.

## What to set

Environment, on the composition root.

```
GROWTH_AI_BACKEND=api
ANTHROPIC_API_KEY=...
GROWTH_TUTOR_CAP_USD=1.00
GROWTH_TUTOR_CAP_TOKENS=250000
```

That block is the paid fallback. The default backend is `subscription`, which runs the tutor on
the operator's Claude subscription and never reads the key (docs/plan/07-ai-provider-layer.md,
"The subscription backend"). A key alone wires nothing, and only `GROWTH_AI_BACKEND=api` spends
on it.

Per-role model and call settings. Six roles, and only the tutor is live today.

| Role | Model | Thinking | Effort | Temperature | max output | Cache TTL | Streams |
| --- | --- | --- | --- | --- | --- | --- | --- |
| tutor | claude-sonnet-5 | disabled | low | none | 600 | 1h | yes |
| grader | claude-sonnet-5 | on | medium | none | 2000 | 1h | progress only |
| transcriber | claude-sonnet-5 | disabled | low | none | 1500 | 1h | no |
| diagnostician | claude-sonnet-5 | on | medium | none | 2000 | 1h | no |
| generator | claude-opus-5, Batch API | on | medium | none | 16000 | 1h | no |
| verifier | gemini-3.5-flash-lite, batch, paid tier | unknown, see below | medium | none | 3000 | none, the prefix is below Gemini's 4096 minimum | no |

Two rows changed on 2026-09-20 with `14-token-economy.md`. The generator is called once per
archetype to author a parameterised template, not once per item, so its `max output` is 16000 as
`tools/template_trial.py` already sets; a truncated template that still parses is the failure the
gate has to catch, so watch `stop_reason` on that role. And the verifier moved one Gemini tier down
to `gemini-3.5-flash-lite`, whose model page prints structured outputs, thinking, caching and the
Batch API as supported and whose price carries no promotional end date.

Three of those settings are the ones that actually move the bill, and two of them are not set
anywhere in the code today.

**Thinking.** On claude-sonnet-5 and claude-opus-5 thinking is on by default and its tokens are
billed as output. Not sending a thinking parameter leaves it on. The tutor and the transcriber
send `thinking: {"type": "disabled"}`. Leaving the tutor's thinking on costs **$8.56** more over
the 230 days to exam day and, worse, can consume the whole output budget so the student sees an
empty feedback sentence. The prompt cache is a separate $1.35; do not credit one to the other.

**Temperature: send none.** A non-default `temperature` returns 400 on claude-opus-5 and
claude-sonnet-5 at any value, including 0. The table above deliberately has no temperature
column. `app/providers/anthropic.py` sent one on every call until 2026-09-20; the field is gone from the wire body and from `ProviderRequest`, and `tests/providers/test_anthropic.py` asserts its absence.

**Effort.** `output_config.effort` defaults to `high`, which the documentation describes as
spending as many tokens as needed. Every role sets it explicitly. On the generator alone, `medium`
rather than `high` is worth $126.49 on one full bank pass.

**max output.** The old value of 400 on the tutor is below what thinking plus a paragraph needs,
which is why it is raised to 600 even with thinking off. If you ever see `stop_reason: "max_tokens"`
in a tutor response, raise the number or lower the effort; do not ignore it.

Two settings that are not negotiable, for reasons in `09-security-and-privacy.md` rather than cost.
The Gemini key must be a paid-tier key: on the unpaid tier Google uses submitted content to improve
its products and human reviewers may read it. And no role ever sends a tool definition. 09 commits only the tutor to that in so many words; the general rule is in `07-ai-provider-layer.md`, which records that no role uses tools and that `app/providers/anthropic.py` refuses to forward a tool definition on any call.

## What it will spend

To exam day, 2027-05-10, about 230 study days, one student. The full arithmetic is in
`13-ai-engineering.md`.

| Role | Calls over the cycle | Cost |
| --- | --- | --- |
| tutor, 12 calls a session | 2,760 | $5.01 |
| grader, 3 samples on the model-judged share of 1,200 points | 804 | $10.11 |
| transcriber, 200 photographed pages | 200 | $3.41 |
| diagnostician, on a recurring error path only | 564 | $8.21 |
| generator, one gated template per archetype at 2.5 attempts | 348 | $17.37 |
| verifier, blind re-solve per published item on Flash-Lite batch | 6,178 | $12.71 |
| Haiku 4.5 screen between transcriber and grader | 200 | $0.20 |
| evals, golden set 1 on the gate, golden set 2 mixed, golden set 3 monthly | 2,565 | $38.00 |
| **Total** | | **$95.03** |

Anthropic $82.31, Google $12.71. Two accounts, two keys.

Four tiers, so the choice is visible.

| Tier | To exam day | What it is |
| --- | --- | --- |
| Minimum viable | $5.01 | The tutor only. The whole P1 product runs: adaptive selection, mastery gating, deterministic grading, elaborated feedback. No generated bank, no graded free response |
| Token economy, the recommendation | $95.03 | Every role, a 5,560-item verified bank built from 139 gated templates, the eval schedule below. Fits the $100.00 ceiling with $4.97 of headroom. Derived line by line in `14-token-economy.md` |
| Per-item generation | $348.05 | The same product with generation called once per item instead of once per archetype, golden set 1 as a paid eval, the grader called on every judged point and the diagnostician on every incorrect attempt. This is the fallback if the template gate cannot be passed on real archetypes |
| Uncapped | $1,145.55 | Effort high on every role that thinks, 60 items per archetype, five grader samples, Opus 5 on the verifier and the diagnostician. Not recommended: the extra $797.50 is almost all thinking tokens |

**Two savings deliberately not taken, and what would release them.** Grader thinking off is $25.20
and a third grader sample drawn only on disagreement is $11.02. Both are quality decisions with no
evidence behind them yet. Thinking off is released by the sweep in `13-ai-engineering.md`, meaning
escalation rate and exact match with thinking on against off on the same golden set 2 responses. The
conditional third sample is released by the measured disagreement share over the first month against
the assumed 0.25. Together they are the remedy if the grader line comes in at its worst case.

**The one number this tier rests on that does not exist.** 17 of the 76 active BC-PT records answer
yes to at least one of `justification_required`, `interpretation_required` or
`hypotheses_required`, which is a lower bound on the share of judged points reaching a model and not
the share, because `03-diagnosis-and-feedback.md` adds a second condition the data does not carry.
If every judged point needs a model the grader line returns to $44.34 and the total becomes $129.25,
an overrun of $29.25, which the two gated savings above bring back to $99.33. Labelling all 76
records costs nothing and needs no key, and it is the first thing to do.

**Run the bank pass before 2026-12-31.** Gemini's promotional prices end that day. The verifier line
is $12.71 on Flash-Lite, which prints no end date, and $20.20 on 3.8 Flash before the date against
$40.40 after.

**Against the $20.00 of credit on hand, and this is what the template architecture changed.** Under
per-item generation, $20.00 bought 876 generated items, 630 published, or 4.54 published per
archetype, fewer than the 10 per archetype already authored by hand for P1, so the credit could not
start the bank at all. Under template authoring at $0.0540 a call, $20.00 buys 370 authoring calls,
which at 2.5 attempts per archetype is 148 archetypes against the 139 that exist. The credit on hand
now covers the whole authoring pass with $2.63 left. It does not cover verification, which is $12.71
and is the next thing to fund, and an archetype with no published item is still excluded from
selection entirely, so a half-verified bank still silently narrows what the student can be served.

**Staging the bank is now free rather than a premium.** Under per-item generation two waves of 28
cost $90.10 each, $180.19 against $177.62 for one pass of 56, because each wave paid its own 139
prefix writes. Under template authoring the bank is instantiated by the backend from templates that
are already paid for, so publishing 20 now and 20 later costs nothing extra and the measurement that
sizes the second wave, the 95th percentile per-archetype serve count over the first 60 days, can be
taken without buying anything first.

## What to watch

Five signals, in the order they would tell you something is wrong.

**Cache hit rate per role.** Read `cache_read_input_tokens` from the provider's own usage block,
not from the client estimate. A hit rate of zero on a role that sets a cache breakpoint means the
prefix is below the model's minimum and is being processed uncached with no error. That is the
state the tutor template is in today: its static prefix measures about 529 tokens against Sonnet
5's 1,024 minimum. Inside a generation batch, expect 30 to 98 percent rather than 100 percent,
because batch requests run concurrently and cache hits there are best effort.

**Thinking tokens as a share of output.** Read `usage.output_tokens_details.thinking_tokens`. The
adapter discards this field today and should not. If a role's thinking share climbs, the effort
setting has drifted or a prompt change made the task look harder to the model.

**`stop_reason` distribution.** Any `max_tokens` on an interactive role is a truncated answer a
student saw.

**Estimate against invoice.** The `budgets` table holds the client's reconciliation; the provider
invoice is the record. Compare monthly. A persistent gap means the token estimate, the price table
or the batch discount is wrong in the guard.

**Escalation rate on the grader.** It is computed from the three samples disagreeing with each
other, needs no operator labels, and costs nothing. A rising rate is healthy. A falling rate
alongside a rising key error rate is the correlated-failure case and is the worst signal in the
system.

## The eval schedule

| Eval | When | Cost a run |
| --- | --- | --- |
| Golden set 1, generated items | Moved onto the template gate. `tools/template_trial.py draw` over 300 seeded draws per template, offline, no key | $0.00. A full 139-archetype re-author after a prompt bump is $7.51 |
| Golden set 2, escalation rate | Continuously, on real gradings | $0 |
| Golden set 2, monthly canary | Monthly, one sample, catching a provider-side model update behind an unchanged id | $2.16 |
| Golden set 2, full labelled run | Every grader template bump and every model id change, three samples | $6.48 |
| Golden set 3, transcription | Monthly, plus every model id change, plus every image-pipeline change | $0.62 |
| Leniency calibration | Attached to golden set 2's labelled run | $0 |

## What to do at each cap

The caps degrade support before they degrade correctness, and never degrade correctness silently.

| Role at its cap | What the student sees | What you do |
| --- | --- | --- |
| tutor | One line on the session screen saying the tutor is unavailable for the rest of today. The practice queue is unaffected | Nothing, usually. A tutor cap binding on an ordinary day means the per-item ceiling of 3 calls is not being enforced, or the thinking setting has drifted back on. Check the thinking share before raising the cap |
| grader | The attempt shows as awaiting grading with the expected time | Let it queue. Grading with a degraded model is not an option: a wrong point decision is worse than a late one |
| diagnostician | Feedback names the rule and the scoring consequence without a misconception hypothesis | Let it degrade. This is the designed fallback and it is honest about what it does not know |
| transcriber | The capture screen offers typed entry through MathLive instead of the camera | Let it degrade |
| generator | Nothing, unless the bank is short for a fringe archetype, in which case selection avoids it | Check the coverage-gap audit entries. An archetype with no published item is excluded from selection, which is the fail-closed rule and is correct |
| verifier | Nothing. Unverified items stay unpublished | Never relax this. An unverified item is never served, at any budget |
| a role with no configured cap | The role does not run | Configure the cap. A role whose caps are both unset is refused rather than run uncapped, deliberately |

**Raising a cap after a stop.** Today the stop does not clear when the cap is raised: the budget row
keeps `hard_stopped = 1` and every later call is refused with `cap="hard_stopped"` whatever the new
cap says. Until that is fixed, raising a cap mid-day does not restart the role and the role resumes
at the next day's budget row. This is recorded as a defect in `13-ai-engineering.md`.

**If the whole month's spend cap is hit.** The Start tier caps monthly spend at $500 and returns
429 with `error.details.error_code: "enforced_spend_limit_reached"` and no `retry-after`, resuming
at 00:00 UTC on the first of the next month (https://platform.claude.com/docs/en/api/rate-limits,
read 2026-09-20). Nothing in this project's recommended tier approaches
that in a month unless a full bank pass and a full eval sweep land in the same month, which is a
reason to run the bank pass on its own.
