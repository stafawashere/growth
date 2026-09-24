---
title: Offline authoring on the Claude Code subscription
research_date: 2026-09-23
status: in_progress
purpose: How the operator runs item authoring, blind re-solve and distractor audit passes inside Claude Code sessions on a Pro or Max plan, at $0 API spend, and where that boundary stops.
---

# Offline authoring on the Claude Code subscription

`docs/plan/14-token-economy.md` "Offline work on the operator's Claude Code subscription" prices
this line at $0.00 against the API key and moves $40.81 of the $92.95 Claude-only tier onto it.
This file is the operating guide for that move: what a Claude Code session actually does, in what
order, and the one rule that never crosses from a Claude Code session into a runtime key.

## The workflow shape, as run on 2026-09-23

The 130 drafts under `content/items_p1_agent/` were produced this way, and the same shape is what
`docs/plan/14-token-economy.md` prices as the template author and verifier lines.

1. **One agent per archetype authors.** Each archetype gets its own Claude Code session. The
   session reads the archetype's record in `data/archetypes.json`, its BC-PT scoring points and
   the BC-ERR error records its skills hold, then drafts items (or, under the template
   architecture, one parameterised template) with a key, a worked solution and four distractors,
   each distractor tagged to a single named error.
2. **An independent agent re-solves blind.** A second, separate Claude Code session, with no
   access to the first agent's draft reasoning and never given the drafted key, re-solves each
   item from the stem alone and writes its own key and worked solution to a file of its own. A
   script, not the agent, then reads the two files and compares the re-solved key against the
   drafted key; the agent that re-solved the item never sees the drafted key at any point, the way
   `docs/plan/13-ai-engineering.md` requires the verifier never see the key. This is the verifier
   re-solve `docs/plan/14-token-economy.md` prices at $26.94 on the API key and $0.00 offline; the
   agent plays the verifier's role, the deterministic checks around it are unchanged because the
   comparison itself stays a script rather than a model judgment, an unverified item is still
   never served, and a disagreement still routes to review rather than to publication.
3. **The same or a further agent audits every distractor against its tagged error.** For each
   option, the auditor re-derives the value a student following the named `BC-ERR` path would
   actually compute and checks it against the option's own value, the way the twenty-sixth session
   audited 360 distractor options across twelve archetypes on 2026-09-23 and repaired 167 that did
   not match. A spot check solves a random sample by hand and with SymPy as a second, code-level
   check independent of any model.
4. **`tools/check_items.py` gates every pass.** `.venv/bin/python tools/check_items.py
   content/items_p1_agent` runs after every authoring, re-solve or audit session and must print
   "clean" with zero violations before the pass counts as done. A session that leaves the gate red
   has not finished, whatever it drafted.

## What stays on the API key

The tutor, the grader, the transcriber, the diagnostician and the Haiku 4.5 screen each serve a
live student or grade a live attempt inside the running app. None of that traffic may route
through a Claude Code subscription token, because the Claude Agent SDK quickstart states: "Unless
previously approved, Anthropic does not allow third party developers to offer claude.ai login or
rate limits for their products, including agents built on the Claude Agent SDK. Please use the API
key authentication methods described in this document instead."
(https://code.claude.com/docs/en/agent-sdk/quickstart.md [verified]). A runtime call authenticates
with `ANTHROPIC_API_KEY` as `docs/operator/ai-operating-costs.md` already sets it, never with a
Claude Code login, and that boundary does not move because the operator happens to also run Claude
Code for authoring.

## Why this is development work and not a routed runtime call

A session of Claude Code on a Pro or Max plan is the operator's own development tool, the same
category as an editor or a terminal, authenticated the way
`https://code.claude.com/docs/en/authentication.md` [verified] describes, including headless use
(`https://code.claude.com/docs/en/headless.md` [verified]). Item authoring, blind re-solving and
distractor audits each produce a file the operator reviews and commits, `content/items_p1_agent/`
or a template under `var/`; nothing served by the running app is generated inside the session, and
no student session or graded attempt ever touches it. That is the distinction
`docs/plan/14-token-economy.md` prices on: the app's runtime calls buy a response for a student
waiting on it, and this work buys a committed artefact reviewed before anything downstream sees
it.

## Pacing

A Pro or Max plan's usage is capped by a rolling five hour window and a weekly limit, and neither
is published as a call or token count (https://code.claude.com/docs/en/authentication.md
[verified]), so this line is not free of limits, only free of API spend. Batch API's 50 percent
discount and the cache minimums, 4,096 tokens on Haiku 4.5 and 1,024 on Sonnet 5
(https://platform.claude.com/docs/en/build-with-claude/prompt-caching.md [verified]), describe
what the retired API-priced rows would have cost and do not apply inside a Claude Code session at
all. A full pass, 348 template-authoring calls and 6,178 verifier re-solves priced at API rates in
`tools/cost_model.py`, is sized to run across several sessions rather than in one sitting; the
twenty-sixth session's audit already split by archetype for exactly this reason, one agent per
archetype rather than one agent for all twelve. Schedule accordingly and do not assume a whole
authoring or audit pass clears in a single five hour window.

## Stage 1 variant: blind formulation instead of blind re-solve [verified]

For the per-unit banks of [items-units-4-to-10.md](items-units-4-to-10.md), run on 2026-09-24,
the independent reader writes code rather than prose: a separate agent receives a file of stems
only and writes the bank's `key_formulations.py`, a SymPy computation per item, using the helpers
in `tools/key_recheck.py`. The recheck script, not an agent, compares those answers with the
stored keys and every option, with its planted-error control. The authoring agents each computed
their keys and distractors in SymPy in their own scratch folders and ran `tools/check_items.py`
to clean, but they know their keys, so their checks are not the independent one.
