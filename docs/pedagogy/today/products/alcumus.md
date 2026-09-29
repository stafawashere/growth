---
title: Alcumus, how it decides the next practice problem
research_date: 2026-09-29
status: draft
purpose: Record how Art of Problem Solving's Alcumus rates students, picks a problem from its pool, passes topics, handles wrong answers and mixes review, so the Today set design can borrow or avoid each mechanism. Lesson-side content is in docs/pedagogy/products/art-of-problem-solving.md and is not repeated here.
---

# Alcumus, the daily practice set

## 1. What decides the next problem [verified]

The student chooses a topic, and Alcumus chooses the problem inside it. AoPS says each topic carries a rating, that Alcumus first decides between a current-topic problem and a review problem from a passed topic, that a low rating prefers easier problems and a high rating prefers harder ones, and that problems seen before are less likely to be served (https://artofproblemsolving.com/blog/articles/alcumus-a-peek-under-the-hood-of-our-adaptive-learning-tool, accessed 2026-09-29). The student handbook says it picks problems from the student's level in that topic (https://artofproblemsolving.com/school/handbook/current/alcumus, accessed 2026-09-29), and a parent thread on the Davidson forum reports review problems mixed in and a focus topic that the student can set or ignore (https://giftedissues.davidsongifted.org/BB/ubbthreads.php/topics/161593/How_does_Alcumus_work.html, accessed 2026-09-29).

There is no documented topic queue. The AoPS blog says the first version treated topics as isolated islands and the current one lays them on a map (https://artofproblemsolving.com/blog/articles/what-is-alcumus-why-we-called-it-that, accessed 2026-09-29). A focus topic is the topic the student is working on now, per a search summary of the AoPS wiki page, which returned 403 to my fetch. The AoPS wiki, the Fandom wikis and two forum threads also returned 403 or 402, so focus-topic behaviour beyond that is unknown.

A correction to the earlier AoPS file. The patent US 10,720,072, with its K values of 50 and 20 and its rating windows of plus or minus 5 to 100, is assigned to Expii Inc, with inventors including Po-Shen Loh (https://patents.google.com/patent/US10720072B2/en, accessed 2026-09-29). It is not AoPS's patent, and nothing I read ties it to Alcumus. Those constants must not be attributed to Alcumus.

## 2. How a set is sized and ordered [single-source]

There is no fixed set. AoPS says there is no fixed number of problems per topic, and the topic bar turns green at "pass" and blue at "mastery" (handbook above). The rating thresholds for pass and mastery are not published in anything I could read, so they are unknown. Each problem allows up to two tries. Session length and problems to pass are unknown. A poster on the Davidson thread says the difficulty setting controls the rate to mastery, and another parent noticed no difference between Easy and Normal (thread above), so the setting's effect is unverified. The handbook lists difficulty settings up to "insanely hard".

## 3. How difficulty is chosen and estimated [single-source]

AoPS defines a topic rating from 0 to 100 as the probability of solving an average problem in that topic, so 75 means about three in four. It models success as 1 divided by (1 + e to the power of problem score minus student score), which gives 50 percent when the two are equal, and updates the student's rating by Bayesian updating from a prior such as 50 percent average, 25 percent above and 25 percent below (AoPS blog above, accessed 2026-09-29). Ratings swing early and settle as data accumulates. The blog's problem score implies each problem carries a difficulty, but how those scores are assigned or recalibrated is not stated in what I read.

One limit is stated openly. If a topic has only hard problems, an Easy setting still serves hard problems, and AoPS gives Advanced Quadratics as its example. The pool was about thirteen thousand problems at the time of the "why we called it that" post, whose date I could not read.

## 4. What happens after a wrong answer [verified]

The student gets a second try. A reviewer reports that the first answer is shown as wrong so the mistake is not repeated (https://mathgeekmama.com/alcumus-online-learning-a-review/, accessed 2026-09-29). After a second wrong answer, a correct answer or a give-up, the answer and solution appear, and the solution may link to readings or videos (handbook and blog above). AoPS says a student must submit wrong answers before Alcumus lets them give up and view the solution. The topic rating falls, and a wrong review answer can un-pass a passed topic (handbook above). A parent reports that repeated misses or give-ups lower difficulty (Davidson thread above).

Achievements are not penalties. The handbook says XP, quests and achievements have no effect on progression, and the blog describes one achievement earned only by a correct second try, aimed at perfectionism (blog above). A fan wiki lists a hidden achievement for a deliberate junk second guess that gains and loses no XP, seen only in a search summary (https://alcumus.fandom.com/wiki/Just_Guessing). I found no achievement documented as a warning to the student.

## 5. How review is compressed or deduplicated [single-source]

Review is a probabilistic draw. Passed topics come back as review problems (handbook), the choice between review and current topic is a weighted coin, and seen problems are down-weighted rather than excluded (AoPS blog, accessed 2026-09-29). There is no published interval schedule and no known cap on review per session. The un-pass rule is the only forgetting signal, and it acts only when a review problem is missed.

Two things are unknown. One is how often review is drawn relative to current-topic problems, since the blog gives no probabilities. The other is whether a passed topic can be un-passed by a rating decay without any miss, and nothing I read says it can.

## 6. What the student sees on the day screen [uncertain]

There is no daily set screen. A student picks a class and topic and receives one problem at a time. The topic bar shows progress and turns green or blue. XP, quests and a hall of fame sit beside it, and a reviewer notes reporting for a teacher or parent on problems attempted and results (mathgeekmama link above). I did not open the app, so layout, the topic list and any calculus topics are unknown. A search summary says Alcumus covers prealgebra through precalculus and that no calculus topic list was found, which I could not confirm.

## 7. What is public about the engineering [single-source]

Only the AoPS blog posts and the handbook. The under-the-hood post gives the logistic model, Bayesian updating and the selection weights, and it says Alcumus works best when wrapped in some teaching (AoPS blog, accessed 2026-09-29). No paper, code or calibration method is published, and the patent that describes a similar Elo-style design belongs to Expii, so it can serve as a model of an approach and not as a description of Alcumus.

## 8. What it does badly [uncertain]

Independent criticism is thin. AoPS itself says the first version was a scattershot with topics as isolated islands (why-we-called-it post above). A reviewer notes Alcumus may not follow a school's order or cover everything a curriculum needs (mathgeekmama link above). AoPS notes that a topic containing only hard problems ignores an Easy setting, and that Alcumus works best inside teaching (blog above). A parent found the difficulty setting hard to notice. I found no independent efficacy study and no published complaint about the rating penalty for a wrong answer.

## 9. Sources [verified]

- https://artofproblemsolving.com/blog/articles/alcumus-a-peek-under-the-hood-of-our-adaptive-learning-tool, 2026-09-29, rating meaning, logistic model, Bayesian update, selection weights.
- https://artofproblemsolving.com/blog/articles/what-is-alcumus-why-we-called-it-that, 2026-09-29, second-try achievement, no-give-up-before-wrong, topic map, pool size.
- https://artofproblemsolving.com/school/handbook/current/alcumus, 2026-09-29, two tries, green and blue bar, review, un-pass, XP.
- https://patents.google.com/patent/US10720072B2/en, 2026-09-29, assigned to Expii Inc, not AoPS.
- https://mathgeekmama.com/alcumus-online-learning-a-review/, 2026-09-29, wrong-answer flow, reviewer criticism.
- https://giftedissues.davidsongifted.org/BB/ubbthreads.php/topics/161593/How_does_Alcumus_work.html, 2026-09-29, parent report on review, focus topic, difficulty setting.
- https://alcumus.fandom.com/wiki/Just_Guessing, 2026-09-29, search summary only, page returned 402.
- https://artofproblemsolving.com/wiki/index.php/Focus_Topic, 2026-09-29, search summary only, page returned 403.
