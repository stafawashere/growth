---
title: Live tutor agent, research index
research_date: 2026-09-29
status: draft
purpose: Index the research strands behind the live tutor agent and state the conventions every file follows.
---

# Live tutor agent, research index

Research for the live tutor agent that lives in Growth's top bar. Written 2026-09-29 on the branch `agent/live-tutor`. The design and plan documents that follow from it are one directory up, in `docs/agent/`.

## Files [verified]

| File | Strand | Written by |
| --- | --- | --- |
| `providers.md` | The Claude subscription backend through the Claude Code CLI, the API key path, and every other provider plan 07 lists, with streaming, caching, structured output, prices, retention terms and the fallback chain for a live agent. Ends with a measured section from four live calls | Opus 5.5 agent; measured section by the orchestrator |
| `memory.md` | How long-lived assistants keep memory of one person, what Growth already holds about the learner, and the memory layer to add | Opus 5.5 agent |
| `live-assistant-ux.md` | How in-product assistants stay one click away, with reference designs and the panel, shortcut, context line, streaming, mathematics and degraded-state recommendations | Opus 5.5 agent |
| `math-tutoring.md` | What makes a tutor good at AP Calculus BC: the guardrail evidence, the conversational moves, the grounding packet, the AP scoring language rules and the multi-turn eval checks | Opus 5.5 agent |
| `self-tuning.md` | A per-learner tutoring profile, its evaluation signals and their arithmetic, the experiment switch, the guarding eval and the failure modes | Opus 5.5 agent |
| `synthesis.md` | The ranked decisions the strands support, the disagreements and their resolution, and the rulings that need the operator | Orchestrator |

## Conventions [verified]

Every file carries the project front matter and one evidence tag on each H2. A web claim is [verified] only where two independent sources agree, each cited with its URL and access date. One source is [single-source]. The writer's own reasoning is [inferred]. Unknowns are stated as unknown under [uncertain]. No source is quoted beyond 25 words. No em dashes, no en dashes as punctuation, no emojis. No study advice, no schedules, no praise copy and no prediction talk, in the research as in the product.

Facts about Growth were read from the repository on 2026-09-29 and cite the file. Facts about providers were read from current primary documentation on the same day. Nothing is recalled from memory as if sourced.
