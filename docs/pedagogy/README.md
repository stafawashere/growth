---
title: Pedagogy research base, index
research_date: 2026-09-29
status: in_progress
purpose: Index of the research base behind the lesson-framework redesign of 2026-09-29, what each file holds, how it was built and how to read its evidence tags.
---

# Pedagogy research base

Built on 2026-09-29 during the overnight lesson redesign, on the operator's delegation. The product files were written by claude-sonnet-5-5 research agents from the live web, one product per agent, under one shared brief; the learning-science file by another; the synthesis, the clean-slate design, the gap analysis and the rulings file by claude-fable-5-1, the orchestrator. Nothing here was written by a person, and nothing here is a mathematical or scoring claim inside a lesson: CLAUDE.md's rule that lesson facts come only from the local library holds, and the web was read only to study products and learning science.

## Files

| File | What it holds |
|---|---|
| `products/khan-academy.md` | Khan Academy's AP Calculus BC course and mastery system |
| `products/brilliant.md` | Brilliant's interactive lesson format and engagement mechanics |
| `products/math-academy.md` | Math Academy's knowledge graph, FIRe spaced repetition and lesson dose |
| `products/duolingo-math.md` | Duolingo Math's implicit-learning exercises, Birdbrain and engagement design |
| `products/art-of-problem-solving.md` | Alcumus's rating-driven problem stream, the problem-first books, the text classroom |
| `products/ixl.md` | IXL's SmartScore, post-error explanations and diagnostic |
| `products/deltamath.md` | DeltaMath's generated practice, solutions in the student's values, penalty settings |
| `products/aleks.md` | ALEKS's knowledge-space placement, learning mode escalation and Knowledge Checks |
| `products/desmos-classroom.md` | Desmos Classroom's predict-then-check screens, interpretive feedback and building code |
| `products/photomath.md` | Photomath's expandable step solutions and the evidence on solver apps |
| `products/explanatory-video.md` | 3Blue1Brown-style video as a content form and the instructional video literature |
| `products/anki-fsrs.md` | Anki, FSRS, the mnemonic medium and the limits of card spacing for procedures |
| `learning-science.md` | Fifteen mechanisms with sources, effect sizes where published, boundary conditions and what Growth already does with each |
| `synthesis.md` | The techniques that recur, ranked by evidence and fit, the warnings the products supply, and the techniques rejected under the ground rules |
| `clean-slate-design.md` | How a lesson app for every BC skill would be built from nothing today, with each decision tied to the evidence |
| `growth-gap-analysis.md` | The measured state of the 127 lessons and the reader before the redesign, each flaw named against the synthesis and the clean-slate design |
| `rulings-for-operator.md` | Every technique a project rule forbids and every cap the framework designed inside, for the operator to rule on |

## How to read the tags

Every level-two heading carries one tag. `[verified]` means two independent sources agree on the section's main claims. `[single-source]` means one source carries them, usually the vendor describing itself. `[inferred]` means the writer deduced them from product behaviour or from other sections. `[uncertain]` means the sources conflict or are thin. Most product sections are `[single-source]` because vendors document themselves and few independent measurements exist; the synthesis says so and leans on the learning-science file for ranking.

## What the research base is not

It is not a source of lesson content. A lesson's facts, worked steps, error descriptions and scoring claims come from the authoring bundle, `research/` and `cache/text/` only, as `docs/lessons/TEMPLATE.md` requires. The research base decides how a lesson is shaped, paced and checked, never what it says about calculus.

## Where the conclusions went

The framework that follows from these files is in `docs/lessons/TEMPLATE.md` (revised), `docs/plan/15-lessons.md` (the "Plan amendments, 2026-09-29" section), `schemas/lessons/lesson.schema.json`, `tools/check_lessons.py`, `tools/check_lesson_designs.py`, `prompts/generator/lesson_v2.md` and `app/web/src/lessons/`. The build is recorded in `BUILD-LEDGER.md`, "Lesson framework redesign, 2026-09-29".
