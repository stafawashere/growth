---
title: Math Academy, how it teaches
research_date: 2026-09-29
status: draft
purpose: Record how Math Academy structures lessons, sequencing, spaced review and feedback, as evidence for the Growth lesson-framework redesign.
---

# Math Academy

## Who it serves [verified]

Math Academy (mathacademy.com) is a paid online platform for learners from 4th grade through university mathematics, run by a team led by Justin Skycak. Its knowledge graph spans "multiple thousands" of topics (https://www.mathacademy.com/how-our-ai-works, accessed 2026-09-29). Skycak describes roughly 2,500 topics, each with 3 to 4 knowledge points (https://www.justinmath.com/how-math-academy-creates-its-knowledge-graph/, accessed 2026-09-29). Users include school students, homeschoolers and adult self-learners; one reviewer priced it at $49 per month (https://biggo.com/news/202508150714_Math_Academy_Price_Debate, search listing only, accessed 2026-09-29). The AP Calculus BC course is described as aligned to the College Board framework, with 16 sections and about 250 or more topics, and roughly 6,000 XP including quizzes, reviews and Test Prep Mode (https://mathacademy.com/courses/ap-calculus-bc, accessed 2026-09-29; the XP figure comes from a search-result summary of the same page and I did not see it on the fetched text). The 16 sections are Limits, Continuity, Introduction to Differentiation, Advanced Differentiation, Contextual and Analytical Applications of Differentiation, Integration, Techniques of Integration, Differential Equations, Applications of Integration, Parametric, Polar, Particle Dynamics, Sequences and Series, Power Series, and Applications of Technology.

## Lesson anatomy [single-source]

The official page says lessons begin with tutorials and worked examples, followed by up to 5 practice problems, and a student advances only after demonstrated mastery of the previous step (https://www.mathacademy.com/how-it-works, accessed 2026-09-29). A student reviewer describes lessons as short, each with at least two worked examples, then questions that are "generally variations on a theme" (https://frankhecker.com/2025/02/17/math-academy-part-10/, accessed 2026-09-29). Another reviewer gives 5 to 15 minutes per lesson (https://nor-blog.pages.dev/posts/2025-04-16-mathacademy/, accessed 2026-09-29). A lesson is split into knowledge points, each a worked example plus a few problems, with 3 to 4 per lesson (Skycak on the graph, above). Andy Matuschak observes that a lesson "unfurls" behind a Continue button, revealing small segments in sequence with a progress indicator (https://notes.andymatuschak.org/Math_Academy, accessed 2026-09-29). Skycak's stated rule is minimum effective doses: a few minutes of explanation, a worked example, then immediate practice (https://www.justinmath.com/chalk-and-talk-podcast-42/, search listing only, accessed 2026-09-29). Other task types are quizzes (about every 150 XP), reviews, and the diagnostic.

## How it introduces a concept [single-source]

Concepts arrive as compact text with visualizations, designed around the worked-example effect and dual coding, with no reported video lecture (https://www.mathacademy.com/how-it-works, accessed 2026-09-29). Skycak describes worked examples as the main tool for reducing cognitive load when understanding is low, introduced one at a time and paired with a similar question (https://www.justinmath.com/cognitive-science-of-learning-minimizing-cognitive-load/, accessed 2026-09-29). Reviewers find explanations minimal with little motivating context (https://newsletter.ozwrites.com/p/a-balanced-review-of-math-academy, accessed 2026-09-29) and note proofs that can look like tricks (nor-blog, above). The prerequisites are guaranteed by the graph, so a concept is only introduced once its prerequisites are mastered (how-our-ai-works, above).

## Worked examples and practice [single-source]

Worked examples come first, then practice questions similar to them. Skycak states that initial lessons should scaffold with questions resembling the example, while review problems should be mixed so the best reference is not obvious (Skycak cognitive load page, above). Question formats include multiple choice and typed answers (Hecker, above). Reviewers report that questions can be answered by pattern matching from the example (nor-blog, above) and that multiple choice can mask misunderstanding (Matuschak, above). Frank Hecker notes that scaffolding teaches the simplest case, such as synthetic division only for linear factors, leaving gaps for general cases (https://frankhecker.com/2025/02/18/math-academy-part-11/, accessed 2026-09-29). Quiz items are drawn at random from previously learned topics with difficulty tuned so the average score is about 80% (how-our-ai-works, above). Calculators are not needed until the Trigonometry course (https://www.mathacademy.com/faq, accessed 2026-09-29), and students work with pencil and paper.

## Response to a wrong answer [single-source]

Immediately, after more wrong answers the system adds extra questions and can halt the lesson (how-our-ai-works, above); Matuschak likewise saw more practice items added after multiple misses. A search-result summary states the solution is shown, the error explained, and prerequisite knowledge tagged, but I could not confirm this on a primary page, so treat it as unverified. Later, a failed lesson is marked to be readdressed and is served again "within a few days" (FAQ, above); Matuschak says it can reappear with verbatim content. A missed quiz item triggers a remedial review of that topic at once (FAQ and how-our-ai-works). Remedial reviews target "key prerequisites" exercised in each part of the lesson. The FIRe model gives failed repetitions negative credit and penalizes advanced topics when prerequisite work fails (https://www.justinmath.com/individualized-spaced-repetition-in-hierarchical-knowledge-structures/, accessed 2026-09-29). On the diagnostic, one reviewer reports a single mistake sent him into a long run of trivial trigonometry problems he could not skip (Oz Nova, above).

## Adaptation and sequencing [verified]

Placement is an adaptive diagnostic of 30 to 45 minutes measuring mastery and automaticity and locating the student's "knowledge frontier" (how-it-works, above), with question selection cut "by an order of magnitude" by a custom algorithm and borderline topics marked "conditionally completed" (how-our-ai-works, above). The graph is a hand-built prerequisite DAG: each prerequisite edge carries an encompassing weight between 0 and 1, loosely the probability a random advanced problem encompasses a random simpler one (FIRe article, above). Spaced repetition is per student and per topic: memory decays as 0.5 to the power (days over interval); credit flows down the graph from advanced work; speed (ability divided by topic difficulty) scales the schedule, for example 2x for easy topics and 0.5x for hard ones; when speed is below 1, implicit credit is discarded and explicit review is forced (FIRe article and how-our-ai-works). Spaced repetition compression picks tasks whose implicit repetitions knock out other due reviews. The Math Academy Way book has a technical section on hierarchical spaced repetition, diagnostics and topic prioritization (https://www.justinmath.com/books/, accessed 2026-09-29).

## What it measures [verified]

XP is meant to equal about one minute of focused effort, with a recommended 20 to 40 XP per day on 3 to 5 days per week (FAQ, above). XP also rewards habits such as showing work and reviewing mistakes (how-it-works, above). It measures per-topic mastery shown as knowledge-graph shading, first-attempt lesson success, quiz scores against an 80% target, response quality and timing (through the speed and rawDelta terms), and detected weaknesses (FIRe article; how-our-ai-works). Quizzes come about every 150 XP, are timed, and are taken without reference materials (FAQ; how-it-works). Hecker questions whether XP shows what mathematics was learned (part 11, above).

## Interaction patterns and visual design [uncertain]

Evidence is thin and comes from reviewers, not the vendor. Lessons reveal in segments via Continue, with a progress indicator (Matuschak). Matuschak also says the queue is algorithmic and opaque and feels like "living inside a database table". Answers are chosen or typed (Hecker). A league and leaderboard system exists and can be disabled (nor-blog). No skip button is reported for content a student already knows (nor-blog; Oz Nova). Mobile behaviour, typography, motion and manipulable figures: unknown, I searched the FAQ, reviews and how-it-works page and found nothing specific.

## Engineering signals [verified]

Content, metadata and exercises are written in-house by mathematics experts, and the graph is hand-encoded; Skycak reports about 250 hours to encode prerequisite relations for 1,500 topics (https://www.justinmath.com/how-math-academy-creates-its-knowledge-graph/, accessed 2026-09-29). Questions and solutions are handcrafted by the team (same page). The scheduling algorithm is published in outline: FIRe, encompassing weights, spaced repetition compression, and student-topic speed (FIRe article). Code, the exact interval formula, and any item-parameterization or generation pipeline are not public; I found no statement on how many variants each question has.

## What it does badly [single-source]

Reviewers converge on several points. Explanations are thin and procedural, with little intuition or motivation (Oz Nova, Matuschak). Strict sequencing leaves little room for exploration, in Oz Nova's phrase "the hubris of the DAG". Diagnostic mistakes can trigger long unskippable remedial runs (Oz Nova, nor-blog). Multiple choice and pattern matching allow gaming (nor-blog, Matuschak). Spaced repetition may be too conservative for a strong learner (Matuschak). Speed emphasis is criticized as overemphasizing pace (Hecker cites Michael Pershan). Gamification and leagues push XP accumulation (Hecker, Oz Nova). Efficacy: no independent controlled study found. Skycak's Pasadena Math Academy article says most students who took AP Calculus BC in eighth grade passed and most of those scored 5, but gives no counts, and says outcomes are not tracked systematically (https://www.justinmath.com/math-academys-eurisko-sequence-5-years-later/, accessed 2026-09-29). That program is a separate school program with students at or above the 90th percentile on a placement test, so it does not measure the online platform.

## Sources [verified]

- https://www.mathacademy.com/how-it-works, 2026-09-29, official lesson, diagnostic, XP and quiz description.
- https://www.mathacademy.com/how-our-ai-works, 2026-09-29, graph scale, diagnostic, adaptivity, wrong-answer handling, quiz target.
- https://www.mathacademy.com/faq, 2026-09-29, XP definition, recommended pace, quiz frequency, re-serving failed lessons.
- https://mathacademy.com/courses/ap-calculus-bc, 2026-09-29, BC section list and topic count.
- https://www.justinmath.com/individualized-spaced-repetition-in-hierarchical-knowledge-structures/, 2026-09-29, FIRe mechanics.
- https://www.justinmath.com/how-math-academy-creates-its-knowledge-graph/, 2026-09-29, authoring process and graph size.
- https://www.justinmath.com/cognitive-science-of-learning-minimizing-cognitive-load/, 2026-09-29, worked-example and scaffolding principles.
- https://www.justinmath.com/books/, 2026-09-29, The Math Academy Way structure.
- https://www.justinmath.com/math-academys-eurisko-sequence-5-years-later/, 2026-09-29, Pasadena AP outcomes and caveats.
- https://www.justinmath.com/chalk-and-talk-podcast-42/, 2026-09-29, minimum effective dose (search listing only).
- https://newsletter.ozwrites.com/p/a-balanced-review-of-math-academy, 2026-09-29, critical review.
- https://nor-blog.pages.dev/posts/2025-04-16-mathacademy/, 2026-09-29, user review.
- https://frankhecker.com/2025/02/17/math-academy-part-10/ and https://frankhecker.com/2025/02/18/math-academy-part-11/, 2026-09-29, student experience and critique.
- https://notes.andymatuschak.org/Math_Academy, 2026-09-29, UI and spaced-repetition observations.
- https://biggo.com/news/202508150714_Math_Academy_Price_Debate, 2026-09-29, price (search listing only).
