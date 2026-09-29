---
title: Brilliant, how it teaches
research_date: 2026-09-29
status: draft
purpose: Record what is publicly documented about Brilliant's lesson format, feedback, sequencing and engagement mechanics as evidence for the Growth lesson-framework redesign.
---

# Brilliant

## Who it serves [single-source]

Brilliant teaches math, science, computer science and data topics to general adult and teen learners, not to a specific exam. Its calculus offering is "Calculus in a Nutshell", which lists prerequisites of algebra and basic function skills (https://brilliant.org/courses/calculus-nutshell/, accessed 2026-09-29), and a companion "Integral Calculus" course (https://brilliant.org/courses/calculus-ii/, accessed 2026-09-29). Neither is aligned to AP Calculus BC as far as the fetched pages show. A separate educator site exists (https://educator.brilliant.org/, seen in search results only, not read). The only formal study found used 60 tenth graders in Colombia on linear algebra (https://files.eric.ed.gov/fulltext/EJ1394390.pdf, accessed 2026-09-29).

## Lesson anatomy [uncertain]

Brilliant's FAQ says most courses can be finished "in 2-6 weeks with just 15 minutes of daily learning" (https://brilliant.org/faq/, accessed 2026-09-29). A third-party review gives lessons as 5 to 15 minutes (https://beginnersinai.org/brilliant-explained/, accessed 2026-09-29). Calculus in a Nutshell has 42 lessons, 353 exercises and 8 levels, which is about 8.4 exercises per lesson on average (https://brilliant.org/courses/calculus-nutshell/, accessed 2026-09-29). The levels are: What is a Derivative, Using Derivatives, Finding Derivatives, Integrals, Three Dimensions, Sequences and Series, Limits and Continuity, Advanced Topics. Brilliant's About page says each lesson mixes direct instruction with blocked problem solving, starting from visual intuition, then hands-on manipulation, then concrete computation (https://brilliant.org/about/, accessed 2026-09-29). No source I found gives a screen-by-screen sequence with minutes. I did not open the product itself.

## How it introduces a concept [single-source]

Brilliant states it does not teach a procedure before asking questions, and describes this as pretesting: the learner tries a problem first (https://brilliant.org/about/, accessed 2026-09-29, quoted: "We don't teach how to do something before asking questions"). A review describes a Pythagorean Theorem lesson that runs several animations before moving to harder applications, and progression from "simple questions and stories" to capability-testing problems (https://careerkarma.com/blog/brilliant-stem-learning-platform-deep-dive/, accessed 2026-09-29). The calculus course begins with rate of change and tangent lines before differentiation rules, so the concrete idea precedes the formal rule (https://brilliant.org/courses/calculus-nutshell/, accessed 2026-09-29).

## Worked examples and practice [single-source]

The About page says practice sets act as low-stakes quizzes where "scaffolding falls away", so the learner solves without the lesson's supports (https://brilliant.org/about/, accessed 2026-09-29). Premium users get "personalized practice", and the site says it predicts the next problem to ask so the learner is prepared for later questions (https://brilliant.org/faq/ and https://brilliant.org/about/, accessed 2026-09-29). Classic worked examples with fully written solutions are not described in any source I read. What exists instead is guided problem sequences. I could not find how many problems a practice set contains.

## Response to a wrong answer [uncertain]

The FAQ says the tutor, named Koji, "guides the learner through the reasoning step by step instead of simply revealing the answer" (https://brilliant.org/faq/, accessed 2026-09-29). The About page describes Koji as asking instead of telling and able to see the learner's screen (https://brilliant.org/about/, accessed 2026-09-29). The marketing pages also claim "custom, intelligent feedback catches mistakes" (https://brilliant.org/science/, accessed 2026-09-29). The explanation-after-answer pattern is implied by all three but no source specifies what appears on screen after a miss, whether a retry is allowed, or when the missed item returns. No hearts or lives mechanic appears in the FAQ text.

## Adaptation and sequencing [single-source]

Brilliant says it combines "techniques from intelligent tutoring systems, classic ML recommender systems, and natural language conversations" to model what a learner knows (https://brilliant.org/about/, accessed 2026-09-29). Its FAQ says recommendations depend on interests, skill level and progress, and that the app suggests whether to practice or learn new material (https://brilliant.org/faq/, accessed 2026-09-29). Courses are fixed linear paths of levels. The mastery model, prerequisite graph and spacing algorithm are unknown; I searched the About page, FAQ, science page and web results for an engineering blog and found none.

## What it measures [uncertain]

XP is earned by completing lessons and solving problems, scaled to time and effort, and repeats earn none (https://brilliant.org/help/using-brilliant/what-is-xp/, seen in search result only). A streak counts consecutive days with 3 problems or one full lesson completed, and a Streak Charge automatically covers a missed day (https://brilliant.org/help/using-brilliant/what-is-a-streak/, accessed 2026-09-29). Leagues are weekly XP competitions in groups of 30, with 10 levels from Hydrogen to Einsteinium, resetting Sundays at 8 PM PT (https://brilliant.org/help/features/what-are-leagues-and-leaderboards/, seen in search result only). These measure activity, not learning. Brilliant says it uses data from "millions of problem tries every day" to test approaches (https://brilliant.org/about/, accessed 2026-09-29), but its learner-facing measure of mastery is not documented.

## Interaction patterns and visual design [uncertain]

Brilliant says lessons prioritize visual representations and hands-on manipulation, with animations and simulations where a learner can change a curve or shape and see the result (https://brilliant.org/about/ and search summary of https://brilliant.org/math/, accessed 2026-09-29). One review says interactivity is mostly sliders and quiz-style inputs (Learnopoly and similar, via search result, not read in full). Koji is said to generate "on-the-fly visual and interactive" content (https://brilliant.org/about/, accessed 2026-09-29). I did not view the app, so input controls, typography, motion timing and mobile behavior are unknown from my own observation. The one-question-per-screen pacing is consistent with the "bite-sized lessons" wording (https://brilliant.org/science/, accessed 2026-09-29) but no source states it directly.

## Engineering signals [single-source]

Public signals are limited to the About page: an ITS plus recommender plus language-model tutor, a knowledge model, next-problem prediction, and on-the-fly generated interactive content (https://brilliant.org/about/, accessed 2026-09-29). Lessons are hand authored by teachers and domain experts, per the site's statement that courses are "crafted by award-winning teachers and professionals" (https://brilliant.org/science/, accessed 2026-09-29). No item-generation pipeline, spaced repetition algorithm or mastery threshold is published. I searched for an engineering blog and found none.

## What it does badly [uncertain]

Brilliant's efficacy claim, "6x more effective", is cited on its FAQ to an Education World article, and the science page cites no peer-reviewed research (https://brilliant.org/faq/ and https://brilliant.org/science/, accessed 2026-09-29). The only academic study found (de la Puente and Perez, Mathematics Teaching Research Journal, 2023) reports 60 students, a mean final grade of 87.42 against 79.63 for controls (t(58) = 2.63), but its abstract is written in future tense, it lists limited sample size and no control of prior knowledge as weaknesses, and it tests linear algebra rather than calculus (https://files.eric.ed.gov/fulltext/EJ1394390.pdf, accessed 2026-09-29). I treat it as weak evidence. Reviews criticize the content as shallow, better for revisiting than first learning, with limited practice depth, no certificates, no video, and a high price (https://brighterly.com/blog/is-brilliant-org-worth-it/ and search summaries, accessed 2026-09-29). The calculus course is an overview and not an exam-preparation sequence, and free users get two lessons a day (https://brilliant.org/faq/, accessed 2026-09-29). Streaks and leagues reward volume of daily activity, and XP is not tied to retention as documented.

## Sources [verified]

1. https://brilliant.org/about/, 2026-09-29. Pretesting statement, Koji, scaffolding falls away, ITS plus recommender, team.
2. https://brilliant.org/faq/, 2026-09-29. 15 minutes daily, 2 to 6 weeks, Koji feedback, free limit, "6x" claim.
3. https://brilliant.org/science/, 2026-09-29. Marketing pedagogy claims, no research citations.
4. https://brilliant.org/courses/calculus-nutshell/, 2026-09-29. 42 lessons, 353 exercises, 8 levels, prerequisites.
5. https://brilliant.org/courses/calculus-ii/, 2026-09-29. Fetch returned only a header; course existence.
6. https://brilliant.org/help/using-brilliant/what-is-a-streak/, 2026-09-29. Streak rule and Streak Charge.
7. https://brilliant.org/help/using-brilliant/what-is-xp/ and https://brilliant.org/help/features/what-are-leagues-and-leaderboards/, 2026-09-29. XP and league rules, via search result text only.
8. https://files.eric.ed.gov/fulltext/EJ1394390.pdf, 2026-09-29. Colombian quasi-experimental study.
9. https://careerkarma.com/blog/brilliant-stem-learning-platform-deep-dive/, 2026-09-29. Review of lesson feel.
10. https://beginnersinai.org/brilliant-explained/ and https://brighterly.com/blog/is-brilliant-org-worth-it/, 2026-09-29. Lesson length and criticisms, via search summaries.
