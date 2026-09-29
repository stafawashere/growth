---
title: Brilliant, how the daily problem and practice set are chosen
research_date: 2026-09-29
status: draft
purpose: Record what is publicly known about how Brilliant picks the next problem, the daily challenge and practice sets, and treat its engagement mechanics as warnings, so Growth's daily practice set can borrow the stated design intent and avoid streak and limit pressure that is not tied to learning.
---

# Brilliant, the daily problem

The lesson-side reading is in docs/pedagogy/products/brilliant.md and is not repeated. Brilliant publishes very little about selection, so most answers below are the vendor's own sentences, and several are unknown. All pages were read on 2026-09-29. The daily challenge pages and much of the help center render in the browser, so I read them as raw HTML or through search summaries, and say so.

## What decides the next problem [single-source]

Brilliant's About page says that for personalized practice it predicts the optimal next problem X to ask so that the learner is adequately prepared to answer a future question Y (https://brilliant.org/about/, accessed 2026-09-29).

The same page says the tutor Koji combines intelligent tutoring system techniques, classic recommender-system machine learning and natural language to model what a learner knows. The home page says Koji tracks what is mastered and missed, builds practice around the gaps, and speeds up or slows down (https://brilliant.org/, accessed 2026-09-29).

What model, features or objective sit behind X and Y is not public. For the daily challenge, the public pages show a title and a standalone problem, and I found no statement of how it is chosen or whether it depends on the learner. That is unknown.

Wikipedia records that the site began as individual puzzles with a Problem of the Week, before turning to courses (https://en.wikipedia.org/wiki/Brilliant_(website), accessed 2026-09-29, via a summary).

## How a set is sized and ordered [uncertain]

Every lesson has associated practice sets, and the About page says their frequency, timing, composition, length and difficulty are areas of active experimentation, and that review sets combining problems from preceding lessons are being rolled out course by course with human review (https://brilliant.org/about/, accessed 2026-09-29).

A January 2025 engineering post says a pre-algebra course has 50 or more concepts, needs 20 or more problems per concept and so over 1,000 problems (https://blog.brilliant.org/hand-crafted-machine-made/, accessed 2026-09-29).

Free users get 2 keys a day and each key opens one lesson or one practice set, reset at midnight in the user's time zone, so a free day is at most two units. Premium has no keys (https://brilliant.org/help/pricing-and-plans/what-s-the-difference-between-free-and-premium/, accessed 2026-09-29).

Free users must go through a course in order, and Premium can jump to any lesson. How many problems a set holds is not stated. The daily challenge count per day is also not stated in anything I could read.

## How difficulty is chosen and estimated [single-source]

Difficulty is mostly authored. The engineering post says designers spend weeks on each topic's game and on levels, aiming for a difficulty curve that keeps the learner in flow (https://blog.brilliant.org/hand-crafted-machine-made/, accessed 2026-09-29). The About page describes levels of progressively harder problem solving in a topic, says the level system intentionally shows a more reductive view of prerequisites than the underlying reality, and lists "determining level of effective automaticity" and "optimal length and difficulty per set" as things under test (https://brilliant.org/about/, accessed 2026-09-29).

It gives no formula for estimating a learner's level or a problem's difficulty. The home page says regular mastery assessments follow lessons (https://brilliant.org/, accessed 2026-09-29). Whether the daily challenge has any difficulty targeting is unknown.

## What happens after a wrong answer [single-source]

In lessons, Koji sees the screen and the wrong guesses and guides the reasoning without giving the answer (https://brilliant.org/faq/, accessed 2026-09-29, and https://blog.brilliant.org/a-world-class-tutor-in-every-home/, accessed 2026-09-29).

In practice sets the scaffolding is removed, with no visual aids or hints, so the set works as a low-stakes quiz (https://brilliant.org/about/, accessed 2026-09-29). The home page says that if a learner comes up short on a mastery assessment, Koji creates targeted practice (https://brilliant.org/, accessed 2026-09-29).

The About page also mentions pass and fail feedback and routing, and gives no rule for it. I found no public rule for when a missed problem returns, and no text on the daily challenge after a miss.

## How review is compressed or deduplicated [single-source]

The stated design is spaced repetition especially in weak areas, and mixing problems from different concepts so the learner must identify the approach (https://brilliant.org/about/, accessed 2026-09-29). The word used for the current state of these is "testing" and "rolled out", so it is a stated program and not a documented behavior. Repeating a lesson on the same day earns no extra XP and doing it on a later day can (https://brilliant.org/help/using-brilliant/what-is-xp/, accessed 2026-09-29). Nothing public says how a duplicate problem is avoided across days.

## What the student sees on the day screen [single-source]

The help center says the streak count is on the home page, streak charges show there as batteries, and weekly XP for Leagues is shown in a Leagues section of the home page (https://brilliant.org/help/using-brilliant/what-is-a-streak/ and https://brilliant.org/help/using-brilliant/what-is-a-streak-charge/, accessed 2026-09-29). On iOS a widget shows streak status and practice prompts.

The marketing page says streaks, levels and daily goals are shown (https://brilliant.org/, accessed 2026-09-29).

Two reviews say a Today tab holds the free daily challenges (https://upskillwise.com/reviews/brilliant/, accessed 2026-09-29, via a summary), which I could not confirm on the vendor's own pages. Brilliant also lists a K to 5 Math Practice library in beta as a separate free product (https://brilliant.org/faq/, accessed 2026-09-29).

## What is public about the engineering [single-source]

The public record is the About page, two engineering blog posts and marketing pages. The January 2025 post describes an AI pipeline that generates puzzles for its game engine, with a stated success rate of 93 percent for gear-train puzzles after making the engine's representations easier for a language model, and says authors keep control of objective and progression (https://blog.brilliant.org/hand-crafted-machine-made/, accessed 2026-09-29).

The May 2026 post introduces Koji as a graphical tutor that sees the screen (https://blog.brilliant.org/a-world-class-tutor-in-every-home/, accessed 2026-09-29). I found no paper, benchmark or code for the knowledge model or the next-problem predictor.

## What it does badly [uncertain]

Brilliant's "6x more effective" claim is cited to a trade article and its science page cites no peer-reviewed research, which the lesson file already records (https://brilliant.org/faq/, accessed 2026-09-29).

Independent reviewers name the STEM-only scope, a paywall on most features, occasional steep difficulty jumps between courses, and surprise annual auto-renewal (https://makeheadway.com/blog/brilliant-review/, accessed 2026-09-29, via a summary). Complaint sites and a Trustpilot page are summarized as calling some learning rote or shallow, with too little practice for mastery, and with many problems assuming prior knowledge, which I have only through a search summary (https://www.trustpilot.com/review/brilliant.org, accessed 2026-09-29).

An outside review says it does not mention adaptive personalization at all (https://upskillwise.com/reviews/brilliant/, accessed 2026-09-29, via a summary). No independent test of the next-problem predictor exists that I could find.

## Engagement mechanics as warnings [inferred]

A streak day needs only 3 problems or one lesson, so the streak measures showing up, not learning (https://brilliant.org/help/using-brilliant/what-is-a-streak/, accessed 2026-09-29).

Streak charges, capped at 2, are earned by completing lessons or practice and auto-applied when a day is missed, which turns a miss into a resource to manage (https://brilliant.org/help/using-brilliant/what-is-a-streak-charge/, accessed 2026-09-29).

Leagues are weekly XP races in groups of 30 across 10 levels, and XP scales with time and effort, so the ranking rewards volume (https://brilliant.org/help/features/what-are-leagues-and-leaderboards/ and https://brilliant.org/help/using-brilliant/what-is-xp/, accessed 2026-09-29). The two-key daily limit for free users gates practice by count, not by need.

The About page says the company is testing mechanics "to extend your learning session", which is the vendor naming session length as a target (https://brilliant.org/about/, accessed 2026-09-29). My reading is that none of these signals tells the scheduler what the learner is about to forget, and Growth's day screen should not count activity as progress.

## Sources [verified]

- https://brilliant.org/about/, accessed 2026-09-29. Next-problem statement, practice sets, review sets, level system.
- https://brilliant.org/ and https://brilliant.org/faq/, accessed 2026-09-29. Koji adaptivity, mastery assessments, K to 5 practice, 6x claim.
- https://blog.brilliant.org/hand-crafted-machine-made/, accessed 2026-09-29. 20 problems per concept, difficulty curves, generation pipeline.
- https://blog.brilliant.org/a-world-class-tutor-in-every-home/, accessed 2026-09-29. Koji sees the screen.
- https://brilliant.org/help/pricing-and-plans/what-s-the-difference-between-free-and-premium/, accessed 2026-09-29. Keys, sequencing.
- https://brilliant.org/help/using-brilliant/what-is-a-streak/, https://brilliant.org/help/using-brilliant/what-is-a-streak-charge/, https://brilliant.org/help/using-brilliant/what-is-xp/ and https://brilliant.org/help/features/what-are-leagues-and-leaderboards/, accessed 2026-09-29. Streak, charge, XP, leagues.
- https://en.wikipedia.org/wiki/Brilliant_(website), accessed 2026-09-29. History, via a summary.
- https://makeheadway.com/blog/brilliant-review/ and https://upskillwise.com/reviews/brilliant/, accessed 2026-09-29. Reviews, via summaries.
- https://www.trustpilot.com/review/brilliant.org, accessed 2026-09-29. Complaint themes, via a search summary.
