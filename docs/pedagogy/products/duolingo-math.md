---
title: Duolingo Math, how it teaches
research_date: 2026-09-29
status: draft
purpose: Record how Duolingo Math structures lessons, responds to errors, adapts, and what evidence exists for it, as input to the Growth lesson-framework redesign.
---

# Duolingo Math

## Who it serves [verified]

Duolingo's own math page says the course gives "complete curriculum coverage for Grades 2 to 12", aligned to Common Core, in English only, free, on iOS, Android and web (S1, checked in a browser). The page lists Arithmetic, Geometry, Pre-Algebra, Algebra I, Algebra II, Statistics, Calculus and Linear Algebra (S1). Earlier sources describe a narrower product: third grade through early middle school at the August 2022 launch (S2), and "up to grade 8" in a March 2026 review (S3), so the high-school expansion is recent and I could not date it. Duolingo's 2023 research report describes two audiences, students and adult "brain training" learners (S4). The report gives no definition of Brain Training beyond that, and I found no primary page describing it, so its content is unknown. The page also says learners "can jump directly to any unit or concept" without prerequisites (S1).

## Lesson anatomy [single-source]

The only primary description of structure is the 2023 report (S4). Each skill has "a discrete learning objective" with sequenced, varied exercises. A unit opens with an accessible introductory skill, and ends with a review skill that mixes earlier mistakes with other unit exercises. Speed rounds are optional and can be timed or untimed. Tech & Learning calls lessons "five-minute" lessons (S5), and TechRadar reports the free tier gives roughly ten to fifteen minutes before an energy limit, about one or two lessons (S3). I found no published count of exercises or screens per lesson, so treat that as unknown. Each lesson ends with XP, and a lesson mid-flow can include a conversation-style level where the learner helps a character work out a purchase (S3).

## How it introduces a concept [single-source]

Duolingo's stated method is implicit learning: learners are not given "a lecture or an explicit explanation" first, and instead infer patterns from varied examples (S4, sections 2.1 and 3.3). In math, a new principle is introduced with a "follow the pattern" exercise that pairs representations of numbers and shapes, and spatially aligned items force the learner to integrate both sides to answer (S4). Sequencing follows concrete, representational, abstract order, with concreteness fading, for example moving between partitioned figures, number lines, number grids and fraction notation (S4). The job listing for the Learning Designer, Math role mentions "implicit and explicit" math teaching, so some explicit content exists, but I found no example of it (S6).

## Worked examples and practice [uncertain]

I found no source describing worked examples as such. Practice is the main mode. The design blog lists addition with countable blocks, perimeter, trapezoid classification, building quadrilaterals, money and measurement word problems, liquid volume with animated water, and pie-slicing for fractions (S7). Difficulty within a topic scales by changing visuals and number range, for example addition with a maximum result of 10, then 100, then 500 (S7). Only two sources are thin on this, and neither shows a full lesson, so this section is uncertain.

## Response to a wrong answer [single-source]

The report states that after a mistake the learner "receives a hint", may retry the exercise immediately, and sees an exercise on the same concept again at the end of the lesson (S4). Correct answers get a sound, a green flash, haptics and encouraging text, with praise at unpredictable intervals (S3, S4). Later, the unit review skill replays earlier mistakes interleaved with other items (S4). Tappable hints let the learner choose their level of scaffolding (S4). Whether the math course shows a worked explanation of the error is unknown. Duolingo's "Explain My Answer" is documented for language courses (S8) and I found no statement that it covers math. The Practice Hub mistakes review is documented for language courses only (S9). Hearts are documented generally (S10) but I did not confirm current heart or energy behaviour in math, and TechRadar mentions an "energy" limit (S3).

## Adaptation and sequencing [verified]

Two independent primary sources describe Birdbrain, the learner model. The IEEE Spectrum article by Duolingo staff says it is "logistic regression inspired by item response theory", a generalization of Elo, updated by one stochastic gradient step after each exercise, with Birdbrain V2 using an LSTM that compresses a learner's history into 40 numbers (S11). The 2023 report says Birdbrain learns learner proficiency and exercise difficulty from over 1 billion exercises a day and builds "dynamic lessons" (S4). The report names the design targets: the zone of proximal development, "desirable difficulty" with harder items at the end of a lesson, and spaced repetition (S4). Whether Birdbrain V2 actually runs on math items is not stated by either source, so I treat math coverage as inferred. Sequencing follows Common Core, NCTM, OECD and TIMSS recommendations (S4). Placement exists: a secondary source describes a short placement flow (S12), and the primary page says learners can jump to any unit (S1).

Half-life regression (HLR), Settles and Meeder 2016, is a language-learning model. It sets recall probability p = 2^(-delta/h), where delta is time since last practice and h is a half-life estimated as 2^(theta dot x) from counters of times seen, correct and incorrect plus about 20,000 word-level indicator features (S13). The paper reports over 45 percent lower error than baselines and a 12 percent engagement gain in an operational study (S13). I found no source saying HLR is used for math items.

## What it measures [uncertain]

Internally it estimates per-learner proficiency and per-item difficulty and predicts probability correct (S11, S4). For learners it shows XP, streak days and league rank (S3). I found no learner-facing skill mastery report for math. Duolingo's efficacy page lists studies on language courses, and I found no published efficacy study of the math course (S14). The 2023 report cites outside research for its design choices and reports no math outcome data (S4). The 74 reported no efficacy data either (S15).

## Interaction patterns and visual design [single-source]

Per the report, learners drag items into equal groups for division, slide a finger along a time number line to match an analog clock, and move clock hands, protractors, rulers and number lines, and build fractions by partitioning shapes (S4). Highlighting is used, for example shading a clock from 12:00 to the elapsed hour, and "every element on a screen" is tied to the task (S4). The design blog says visuals are generated by code and moved from iOS CAShapeLayer drawing to the Rive animation tool for cross-platform interactions (S7). Characters were redone as 3D figures, exercises use minimal words, and haptics accompany answers (S4). The design is mobile first (S4).

## Engineering signals [verified]

Visual exercise classes generate thousands of variants programmatically (S7). Birdbrain has a session generator that the Duolingo blog said personalized over 20 percent of lessons in October 2020 (S16). Birdbrain V2 moved from daily batch updates to updates within minutes (S11). HLR code and 13 million learning traces are public (S13, S17). Streak, leagues and notification results come from a former Duolingo chief product officer's newsletter: a 17 percent rise in learning time after leagues, and share of daily actives with 7 or more day streaks up almost three times (S18). These are company-reported and not peer reviewed.

## What it does badly [single-source]

Keith Devlin is quoted by The 74 saying games mostly do not improve solving of multi-step problems beyond basic skills, and another expert warns of "procedural knowledge without deep comprehension" (S15). Independent HLR analysis found AUC of 0.537 on Duolingo's public data and no learner-level features (S19), which limits HLR as a model, and it is a language model anyway. I found no controlled evidence of math learning gains, and the explanation depth in the math course is unknown. Free use is capped by energy (S3), and the streak and league mechanics reward daily activity, which is a different target from mastery (S18).

## Sources [verified]

- S1 https://www.duolingo.com/math (accessed 2026-09-29): grades 2 to 12 coverage, topic list, jump anywhere, free, platforms.
- S2 https://www.the74million.org/article/duolingo-the-language-learning-app-giant-wants-to-teach-kids-math/ (accessed 2026-09-29): launch scope, implicit learning, expert criticism.
- S3 https://www.techradar.com/computing/websites-apps/duolingo-math (accessed 2026-09-29): March 2026 hands-on review, XP, quests, energy limit, conversation level.
- S4 https://duolingo-papers.s3.amazonaws.com/reports/Duolingo_whitepaper_duolingo_method_2023.pdf (accessed 2026-09-29): Duolingo Method report, math design principles, Birdbrain, error handling.
- S5 https://www.techlearning.com/how-to/what-is-duolingo-math-and-how-can-it-be-used-to-teach-tips-and-tricks (accessed 2026-09-29): five-minute lessons, ages, manipulatives.
- S6 https://startup.jobs/learning-designer-math-duolingo-2-5934727 (accessed 2026-09-29): job listing, implicit and explicit teaching, CCSS and NCTM.
- S7 https://blog.duolingo.com/developing-math/ (accessed 2026-09-29): exercise types, number ranges, Rive.
- S8 https://blog.duolingo.com/explain-my-answer-now-free (accessed 2026-09-29, search snippet only): Explain My Answer for language courses.
- S9 https://blog.duolingo.com/guide-to-duolingo-practice-hub/ (accessed 2026-09-29): mistakes practice, language courses only.
- S10 https://duoplanet.com/how-to-beat-the-heart-system-on-duolingo/ (accessed 2026-09-29, search snippet only): general hearts behaviour.
- S11 https://spectrum.ieee.org/duolingo (accessed 2026-09-29): Birdbrain IRT, Elo, SGD, LSTM V2.
- S12 https://nibble-app.com/blog/duolingo-math (accessed 2026-09-29, search snippet only): placement flow, secondary.
- S13 https://research.duolingo.com/papers/settles.acl16.pdf (accessed 2026-09-29): HLR equations, features, results.
- S14 https://www.duolingo.com/efficacy/studies (accessed 2026-09-29, search snippet only): efficacy studies list, language focus.
- S15 The 74 article, same URL as S2 (accessed 2026-09-29): Devlin and Darvasi criticism, no efficacy data.
- S16 https://blog.duolingo.com/learning-how-to-help-you-learn-introducing-birdbrain (accessed 2026-09-29): Birdbrain v1, 20 percent of lessons.
- S17 https://github.com/duolingo/halflife-regression (accessed 2026-09-29, search snippet only): public code and data.
- S18 https://www.lennysnewsletter.com/p/how-duolingo-reignited-user-growth (accessed 2026-09-29): streak and leagues effects, company-reported.
- S19 https://papousek.github.io/analysis-of-half-life-regression-model-made-by-duolingo.html (accessed 2026-09-29): independent HLR critique.
