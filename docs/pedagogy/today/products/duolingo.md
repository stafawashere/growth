---
title: Duolingo, how it picks the next exercise
research_date: 2026-09-29
status: draft
purpose: Record how Duolingo decides what to give next through half-life regression, Birdbrain and the session generator, how lessons are sized and how mistakes are replayed, as evidence for the design of the Growth daily practice set.
---

# Duolingo, the daily practice set

This file studies exercise selection. The Duolingo Math lesson format is in `../../products/duolingo-math.md` and is not repeated. Duolingo Math is covered here only where its documented behavior differs from the language courses. A number I could not source is written as unknown.

## 1. What decides the next problem [verified]

Two independent kinds of source agree that a learner model feeds a session generator. The 2016 ACL paper says the student model records what was learned and estimates recall at any moment, and that practice sessions are lessons whose exercises come from words due for practice (https://research.duolingo.com/papers/settles.acl16.pdf, accessed 2026-09-29). The Birdbrain blog says Birdbrain feeds the Session Generator, which crafts lessons from a wide pool of exercises and picks those at the right difficulty for this learner (https://blog.duolingo.com/learning-how-to-help-you-learn-introducing-birdbrain, accessed 2026-09-29). IEEE Spectrum reports that the switch to fully personalized recommendations came in May 2022 after tests showed gains in engagement and learning (https://spectrum.ieee.org/duolingo, accessed 2026-09-29). Personalization works inside the curriculum, so the path decides which unit, and the model decides which exercises fill a lesson from that unit's pool (2023 whitepaper, https://duolingo-papers.s3.amazonaws.com/reports/Duolingo_whitepaper_duolingo_method_2023.pdf, accessed 2026-09-29).

## 2. How a set is sized and ordered [uncertain]

In 2016 a lesson ran until the student mastered its target words, judged by a mixture model of short-term learning curves, so length varied (https://research.duolingo.com/papers/settles.acl16.pdf, accessed 2026-09-29).

The 2023 whitepaper says a lesson takes no more than a few minutes on average, gives no exercise count, and describes ordering that adapts, with harder exercises typically near the end (https://duolingo-papers.s3.amazonaws.com/reports/Duolingo_whitepaper_duolingo_method_2023.pdf, accessed 2026-09-29). An unofficial course-data site puts a typical lesson at 15 questions (https://duolingodata.com/, search snippet, accessed 2026-09-29), which I could not confirm from Duolingo. A Duolingo blog post reports that shorter lessons lowered time spent learning well, while longer paths raised it, and that Daily Quests are ordered from easiest to hardest (https://blog.duolingo.com/time-spent-learning-well/, accessed 2026-09-29). A Mistakes practice round holds up to 10 questions according to a fan guide (https://duoplanet.com/duolingo-practice-hub/, accessed 2026-09-29).

## 3. How difficulty is chosen and estimated [single-source]

Birdbrain is a logistic regression inspired by item response theory, where the chance of a correct answer depends on learner ability and exercise difficulty, and each completed exercise triggers one step of stochastic gradient descent on both, a generalization of Elo. Exercise difficulty is a sum over its features such as type and vocabulary. Version 2 replaced the single ability number with a 40-dimensional vector produced by an LSTM that updates after every exercise (https://spectrum.ieee.org/duolingo, accessed 2026-09-29). The whitepaper adds the rule that a learner doing well gets slightly harder exercises, that difficult exercises are placed late as desirable difficulty, and that difficulty falls if the learner keeps failing them (https://duolingo-papers.s3.amazonaws.com/reports/Duolingo_whitepaper_duolingo_method_2023.pdf, accessed 2026-09-29). The target success rate is not published. By 2020 Birdbrain personalized over 20 percent of lessons (https://blog.duolingo.com/learning-how-to-help-you-learn-introducing-birdbrain, accessed 2026-09-29). All of this is vendor description, with A/B results reported but no data.

## 4. What happens after a wrong answer [single-source]

The learner gets a hint, and an exercise on the same concept returns at the very end of the lesson (2023 whitepaper, https://duolingo-papers.s3.amazonaws.com/reports/Duolingo_whitepaper_duolingo_method_2023.pdf, accessed 2026-09-29).

In Duolingo Math the whitepaper says the learner may redo the exercise immediately and again at lesson end, and the unit review skill later presents earlier mistakes mixed with other unit exercises. The Practice hub logs every mistake for a Mistakes round and some later lessons include earlier mistakes (https://blog.duolingo.com/guide-to-duolingo-practice-hub/, accessed 2026-09-29). How a mistake is chosen for replay among many is not stated in the hub post.

## 5. How review is compressed or deduplicated [single-source]

The 2016 paper gives the spacing rule. Recall probability is 2 to the power of minus lag over half-life, half-life is 2 raised to a weighted sum of features such as counts of correct and incorrect exposures, and words whose predicted recall has decayed are ranked for practice (https://research.duolingo.com/papers/settles.acl16.pdf, accessed 2026-09-29).

Scheduling was per word, not per skill, and I found no mechanism that credits one item for practicing another. Review is instead folded into new lessons, as the whitepaper says personalized practice happens inside units and through Birdbrain's dynamic lessons (accessed 2026-09-29), and the Practice hub post says personalized practice is baked into each unit. The current spacing formula after Birdbrain is not public, and whether HLR still runs is not stated, so treat its retirement as my inference.

## 6. What the student sees on the day screen [uncertain]

A path of units with the next lesson highlighted, plus daily quests, streak and the Practice tab (https://blog.duolingo.com/time-spent-learning-well/ and https://blog.duolingo.com/guide-to-duolingo-practice-hub/, accessed 2026-09-29). In 2016 the home was a skill tree with strength meters of four bars, where a golden skill was fresh and fewer bars meant stale (https://research.duolingo.com/papers/settles.acl16.pdf, accessed 2026-09-29).

Duolingo says the Practice hub is free, while a fan guide says it needs a subscription (https://blog.duolingo.com/guide-to-duolingo-practice-hub/ against https://duoplanet.com/duolingo-practice-hub/, accessed 2026-09-29). The sources conflict and I did not open the app.

## 7. What is public about the engineering [verified]

The most public of the three products. The HLR paper is on the research site and code is on GitHub (https://research.duolingo.com/papers/settles.acl16.pdf and https://github.com/duolingo/halflife-regression, accessed 2026-09-29). It reports 12.9 million student-word traces, over 45 percent error reduction against baselines, and a 12 percent engagement gain in an operational test (paper, accessed 2026-09-29).

The second experiment reached 3.3 million students. Birdbrain has a blog post, an IEEE Spectrum article and a search-visible engineering account of a Scala session generator rewrite that cut delivery from 750 ms to 14 ms (search summary, accessed 2026-09-29). The Birdbrain code and V2 data are not public.

## 8. What it does badly [single-source]

The HLR paper itself reports that in the first live test practice sessions fell significantly, because learners felt sessions did not review what they needed, and that learners complained of words decaying quickly until lexeme features were dropped (https://research.duolingo.com/papers/settles.acl16.pdf, accessed 2026-09-29).

An independent analysis by the papousek.github.io author questions the model's assumptions, notes it has no learner features, and reports a calibration AUC near 0.54 on his own data (https://papousek.github.io/analysis-of-half-life-regression-model-made-by-duolingo.html, accessed 2026-09-29). For Duolingo Math, a review site notes explanations stay brief and depth fades (https://nibble-app.com/blog/duolingo-math, accessed 2026-09-29), and Keith Devlin is quoted as doubting that games improve non-basic problem solving (https://www.the74million.org/article/duolingo-the-language-learning-app-giant-wants-to-teach-kids-math/, search summary, accessed 2026-09-29). A qualitative study argues that gamification can misfire in a language app (https://arxiv.org/pdf/2203.16175, title only, accessed 2026-09-29).

## 9. Sources [verified]

- https://research.duolingo.com/papers/settles.acl16.pdf, accessed 2026-09-29. HLR paper, read in full text.
- https://github.com/duolingo/halflife-regression, accessed 2026-09-29. Public code.
- https://blog.duolingo.com/learning-how-to-help-you-learn-introducing-birdbrain, accessed 2026-09-29. Birdbrain launch.
- https://spectrum.ieee.org/duolingo, accessed 2026-09-29. Birdbrain V2, May 2022 switch.
- https://duolingo-papers.s3.amazonaws.com/reports/Duolingo_whitepaper_duolingo_method_2023.pdf, accessed 2026-09-29. Mistakes, difficulty, spacing, Math.
- https://blog.duolingo.com/guide-to-duolingo-practice-hub/, accessed 2026-09-29. Practice hub.
- https://blog.duolingo.com/time-spent-learning-well/, accessed 2026-09-29. Lesson length, quests.
- https://duoplanet.com/duolingo-practice-hub/, https://duolingodata.com/, accessed 2026-09-29. Fan and unofficial sources.
- https://papousek.github.io/analysis-of-half-life-regression-model-made-by-duolingo.html, accessed 2026-09-29. Critic.
- https://nibble-app.com/blog/duolingo-math, https://www.the74million.org/article/duolingo-the-language-learning-app-giant-wants-to-teach-kids-math/, https://arxiv.org/pdf/2203.16175, accessed 2026-09-29. Duolingo Math critics.
