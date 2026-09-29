---
title: Math Academy, how it picks the next problem
research_date: 2026-09-29
status: draft
purpose: Record how Math Academy decides what to put in the daily task queue, how it sizes, orders and adapts practice and how it compresses review, as evidence for the design of the Growth daily practice set.
---

# Math Academy, the daily practice set

This file studies the daily task queue. Lesson anatomy, worked examples and the price are in `../../products/math-academy.md` and are not repeated. Every claim below carries its URL and the access date 2026-09-29. A number I could not source is written as unknown.

## 1. What decides the next problem [single-source]

A knowledge graph of about 2,500 topics, each holding 3 to 4 knowledge points, is built by hand by domain experts, and every prerequisite link carries an encompassing weight, the fraction of the earlier topic that is practiced on average when a problem in the later topic is solved (https://www.justinmath.com/how-math-academy-creates-its-knowledge-graph/, accessed 2026-09-29). The founder says the task selection model "started working really, really well" only after those weights were entered (same page). The vendor states that the queue picks tasks by mastery learning plus "layering", meaning a student moves to a new topic as soon as its prerequisites are mastered, and that it also weighs interleaving, spaced repetition and the avoidance of interference between similar topics (https://www.mathacademy.com/how-our-ai-works, accessed 2026-09-29). Reviews come from two triggers, spaced repetition due dates and quiz mistakes (https://www.mathacademy.com/faq, accessed 2026-09-29). Nothing in these pages gives the ranking function itself, so its exact scoring is unknown.

## 2. How a set is sized and ordered [single-source]

The dashboard offers a set of tasks the student may choose from, varied in topic, task type and XP, so ordering within the day is partly the student's choice (https://www.mathacademy.com/how-it-works, accessed 2026-09-29). A search-result summary of the same page says the set holds five tasks (accessed 2026-09-29); I did not see the number on the fetched text, so treat it as unconfirmed.

Size is set by time. One XP is about one minute of focused effort, the recommended load is 20 to 40 XP a day on 3 to 5 days a week, and a timed quiz becomes available every 150 XP (https://www.mathacademy.com/faq, accessed 2026-09-29). Within a task the number of questions moves with accuracy, fewer when the student answers well and more after errors (https://www.mathacademy.com/how-our-ai-works, accessed 2026-09-29). The order in which tasks are offered when a student has an unfinished lesson and several reviews is not published.

## 3. How difficulty is chosen and estimated [single-source]

Difficulty is not picked problem by problem. Placement comes from an adaptive diagnostic of 30 to 45 minutes that locates the student's knowledge frontier, using a compressed graph so that only the most informative questions are asked out of a possible 500 to 1,000 topics. Slow correct answers earn less confidence, and borderline topics are marked conditionally completed and adjusted backward if the student struggles later (https://www.mathacademy.com/how-it-works and https://www.mathacademy.com/how-our-ai-works, accessed 2026-09-29). After placement, difficulty is the graph itself, since a student only sees topics whose prerequisites are done.

Quizzes aim at about 80 percent accuracy, with harder variants above that and easier ones below (https://www.mathacademy.com/how-our-ai-works, accessed 2026-09-29). Learning speed per student and topic is a ratio of student ability to topic difficulty, where 2x makes one review count as two repetitions (https://www.justinmath.com/individualized-spaced-repetition-in-hierarchical-knowledge-structures/, accessed 2026-09-29). How ability and topic difficulty are estimated is unknown.

## 4. What happens after a wrong answer [single-source]

Too many errors in a lesson halts it, the student works on unrelated topics, and a second halt without progress triggers remedial reviews aimed at specific prerequisites found through the graph. Failed lessons are rescheduled within a few days (https://www.mathacademy.com/how-our-ai-works and https://www.mathacademy.com/faq, accessed 2026-09-29). A missed quiz question makes that topic an immediate review, and an optional retake with different questions opens afterward (https://www.mathacademy.com/faq, accessed 2026-09-29). Failure also flows forward in FIRe, penalizing advanced topics that depend on the failed skill (https://www.justinmath.com/individualized-spaced-repetition-in-hierarchical-knowledge-structures/, accessed 2026-09-29). Every question has an explanation available.

## 5. How review is compressed or deduplicated [single-source]

This is the central mechanism. Fractional Implicit Repetition lets a repetition on an advanced topic trickle down to component topics scaled by the encompassing weight, discounted when the repetition comes earlier than its due date. The vendor states that due reviews "can typically be compressed" into a smaller set of tasks, and the selector prefers tasks whose implicit repetitions knock out other due reviews, like dominoes. It also fends off upcoming reviews and climbs the graph evenly to keep choices broad (https://www.justinmath.com/individualized-spaced-repetition-in-hierarchical-knowledge-structures/, accessed 2026-09-29; https://www.mathacademy.com/how-our-ai-works, accessed 2026-09-29).

Weights are set by experts only where they are nontrivial, and the founder estimates about 7,500 links took roughly 250 hours to weight (https://www.justinmath.com/how-math-academy-creates-its-knowledge-graph/, accessed 2026-09-29). No independent test of the compression claim was found.

One reviewer counted fewer than three reviews a day on average (https://frankhecker.com/2025/02/17/math-academy-part-10/, accessed 2026-09-29), which is consistent with compression but does not measure it.

## 6. What the student sees on the day screen [single-source]

A dashboard with the task queue and a knowledge profile that updates as tasks finish. Each task earns XP whether it is a lesson, review, multistep task or quiz, with partial credit for partial correctness (https://www.mathacademy.com/how-it-works, accessed 2026-09-29). A daily XP target, leaderboards and streak-style accountability are present according to reviewers (https://drgore.substack.com/p/my-review-of-math-academy and https://frankhecker.com/2025/02/17/math-academy-part-10/, accessed 2026-09-29). The layout and the exact visual order of task types are unknown, because I did not view a logged-in dashboard.

## 7. What is public about the engineering [single-source]

The founder's blog describes hierarchical spaced repetition, FIRe, encompassing weights and the graph build, and states that no public code or academic papers are referenced (https://www.justinmath.com/how-math-academy-creates-its-knowledge-graph/, accessed 2026-09-29). Andy Matuschak's notes list what is missing, namely how topics needing reinforcement are found beyond topic-level tracking, what triggers extra diagnostics or quiz gates, and long-term retention data for the hierarchical approach (https://notes.andymatuschak.org/Math_Academy, accessed 2026-09-29). A book, The Math Academy Way, exists as a PDF (https://www.justinmath.com/files/the-math-academy-way.pdf, accessed 2026-09-29), but it was too large for my fetch tool, so I did not read it. Item response fitting, the diagnostic algorithm and the ranker are unpublished.

## 8. What it does badly [verified]

Critics, not the vendor, say the following. Oz Nova argues the review rule is mechanical, requiring reviews after any wrong answer and treating typos like conceptual gaps, and that the rigid prerequisite path can force years of remedial topics (https://newsletter.ozwrites.com/p/a-balanced-review-of-math-academy, accessed 2026-09-29). Frank Hecker found quizzes stressful because of the time limit and distrusted the progress estimates, which showed conflicting numbers (https://frankhecker.com/2025/02/17/math-academy-part-10/, accessed 2026-09-29). A reviewer at drgore.substack.com wanted more multistep questions that test application (https://drgore.substack.com/p/my-review-of-math-academy, accessed 2026-09-29). Andy Matuschak reports that the queue feels opaque, that tasks emphasize procedural work with no transfer tasks, that his forgetting of earlier material exceeded his own spaced repetition system, and that grouping review exercises by topic and announcing the topic in advance may harm transfer (https://notes.andymatuschak.org/Math_Academy, accessed 2026-09-29). A reviewer summary seen only through search results adds that problems repeat worked examples with new numbers and that XP rewards speed (https://nor-blog.pages.dev/posts/2025-04-16-mathacademy/, accessed 2026-09-29).

## 9. Sources [verified]

- https://www.mathacademy.com/how-our-ai-works, accessed 2026-09-29. Diagnostic, queue, compression, difficulty, wrong answers.
- https://www.mathacademy.com/faq, accessed 2026-09-29. XP, daily goal, quiz cadence, reviews.
- https://www.mathacademy.com/how-it-works, accessed 2026-09-29. Dashboard, diagnostic length.
- https://www.justinmath.com/individualized-spaced-repetition-in-hierarchical-knowledge-structures/, accessed 2026-09-29. FIRe, weights, speed ratio.
- https://www.justinmath.com/how-math-academy-creates-its-knowledge-graph/, accessed 2026-09-29. Graph size, hand build, no public code.
- https://frankhecker.com/2025/02/17/math-academy-part-10/, accessed 2026-09-29. Reviewer, review counts, quizzes.
- https://newsletter.ozwrites.com/p/a-balanced-review-of-math-academy, accessed 2026-09-29. Critique of reviews and path.
- https://drgore.substack.com/p/my-review-of-math-academy, accessed 2026-09-29. Reviewer, XP, FIRe, gaps.
- https://notes.andymatuschak.org/Math_Academy, accessed 2026-09-29. Independent notes, criticisms, missing information.
- https://www.justinmath.com/files/the-math-academy-way.pdf, accessed 2026-09-29. Not read, fetch limit exceeded.
- https://nor-blog.pages.dev/posts/2025-04-16-mathacademy/, accessed 2026-09-29. Search summary only.
