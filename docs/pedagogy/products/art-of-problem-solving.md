---
title: Art of Problem Solving (Alcumus, books, online classes), how it teaches
research_date: 2026-09-29
status: draft
purpose: Document how AoPS teaches through Alcumus, its problem-first textbooks and its text-based live classes, as evidence for a lesson-framework redesign.
---

# Art of Problem Solving

## Who it serves [single-source]

AoPS targets high-performing middle and high school students. The Calculus textbook says it is meant to "challenge high-performing middle and high school students" and draws problems from the Putnam and the Harvard-MIT Math Tournament (https://artofproblemsolving.com/store/item/calculus, accessed 2026-09-29). Alcumus is free and spans pre-algebra through number theory and probability (https://mathgeekmama.com/alcumus-online-learning-a-review/, accessed 2026-09-29). A reviewer notes it is "different from your math curriculum", so it may not follow a school's order. Classes are live and paid; a self-paced format exists with the same core curriculum (https://artofproblemsolving.com/school/handbook/prospective/liveorselfpaced, accessed 2026-09-29).

## Lesson anatomy [single-source]

Alcumus has no fixed lesson. The unit is a topic, and the student answers a stream of problems until the progress bar turns green ("passed") or blue ("mastery"). Each problem allows up to two tries. After a correct answer, a give-up, or two wrong answers, the student is shown the answer and a solution (https://artofproblemsolving.com/school/handbook/current/alcumus, accessed 2026-09-29). Session length and problems per topic are unknown; I found no published figure.

A textbook section starts with problems, then the text presents solutions "through which" techniques are taught (https://artofproblemsolving.com/store/item/intro-algebra, accessed 2026-09-29). The Calculus book is 336 pages of text plus 128 pages of solutions, with hundreds of problems (https://artofproblemsolving.com/store/item/calculus, accessed 2026-09-29).

A live class session runs 90 minutes. The instructor leads students through problems of increasing complexity (https://artofproblemsolving.com/school/about-classroom, accessed 2026-09-29).

## How it introduces a concept [single-source]

The books use a discovery order: pose a problem, let the student attempt it without help, give the solution, state the theorem the solution exposed, then use it in the next problem. Complicated problems are split into parts so techniques appear one piece at a time (search summary of book descriptions, https://artofproblemsolving.com/store/item/intro-algebra and the Goodreads listing https://www.goodreads.com/en/book/show/1366499, accessed 2026-09-29). Only the first-party sentence about "each section starts with problems" was directly fetched for Algebra. The Calculus store page does not state the discovery approach at all, so whether the Calculus book follows it is unknown from what I read.

Alcumus introduces nothing. It presents a problem and relies on the solution, which "can include links to readings in our textbooks, or videos" (https://artofproblemsolving.com/blog/articles/what-is-alcumus-why-we-called-it-that, accessed 2026-09-29). AoPS says the first Alcumus, a "scattershot" approach, left early students adrift, and the current version maps topics in a sequence (same source).

In class, instructors pose strategic questions and students supply the ideas by typing answers (https://artofproblemsolving.com/school/about-classroom, accessed 2026-09-29).

## Worked examples and practice [single-source]

In the books, the worked example is the solution to a problem the student has already tried, so practice precedes the example. Solutions sit in the text, with full solutions to all problems in a separate manual, "not just answers" (https://artofproblemsolving.com/store/item/intro-algebra, accessed 2026-09-29). Calculus has hundreds of problems ranging from routine to competition level (https://artofproblemsolving.com/store/item/calculus, accessed 2026-09-29).

In Alcumus, the solution appears only after the attempt. AoPS states it deliberately requires attempts before viewing solutions, and it includes an achievement for a correct second try, aimed at perfectionism (https://artofproblemsolving.com/blog/articles/what-is-alcumus-why-we-called-it-that, accessed 2026-09-29). The problem pool is about 13,000 problems, and 319,000 students had answered 110 million problems as of that post.

## Response to a wrong answer [single-source]

After a first wrong answer the student gets a second try and, per one reviewer, sees the first answer marked so the same mistake is not repeated (https://mathgeekmama.com/alcumus-online-learning-a-review/, accessed 2026-09-29). After the second wrong answer the correct answer and full solution appear. Later, the rating for that topic drops, and a wrong answer on a review problem can un-pass a previously passed topic (https://artofproblemsolving.com/school/handbook/current/alcumus, accessed 2026-09-29). Hints as a separate tool: unknown; I searched the handbook, the wiki and the reviews and found none described, so the second try appears to be the only step before the solution.

In class, the moderator decides which student messages reach the main panel, and private help goes through whispers or one-on-one chats with assistants (https://artofproblemsolving.com/school/about-classroom, accessed 2026-09-29).

## Adaptation and sequencing [verified]

Two sources describe an Elo-like rating. AoPS's blog says every topic has a 0 to 100 rating meaning the probability of getting an average problem in that topic right, with success probability modelled as 1/(1 + e^(problem score - student score)) and Bayesian updating of the belief (https://artofproblemsolving.com/blog/articles/alcumus-a-peek-under-the-hood-of-our-adaptive-learning-tool, accessed 2026-09-29). A US patent on an adaptive system with automatically rated problems and pupils (US 10,720,072, https://patents.google.com/patent/US10720072B2/en, accessed 2026-09-29) describes problem and student ratings on one scale, where equal ratings mean about 50 percent success. Both raise the student rating on a correct answer and lower it on a wrong one, and the patent also moves the problem's rating the opposite way, so difficulty is calibrated from student data. The patent gives an example threshold of 5 attempts per concept before rating changes slow. I cannot confirm the patent's constants match production.

Selection is randomized but weighted by the current topic versus review topics, the student's topic rating, and whether the problem was seen before; a difficulty setting can constrain it (blog above). The patent adds prerequisite topics and a user-chosen focus. Passed topics return as review problems (handbook above). The Focus Topic wiki page returned 403, so focus behaviour comes only from the patent and one reviewer.

## What it measures [single-source]

Per topic, the probability of a correct answer on an average problem, on a 0 to 100 scale (blog above). Pass and mastery are thresholds on that rating (handbook above). It measures final answers, not reasoning steps. The patent notes ratings are unbounded, which lets it separate strong students (patent above).

## Interaction patterns and visual design [uncertain]

The AoPS classroom is text and image only. Students type into an entry box, instructors drive a main panel, and students are told to keep pencil and paper handy (https://artofproblemsolving.com/school/about-classroom, accessed 2026-09-29). A full transcript is saved and downloadable. Alcumus answers are typed, and problem text sometimes gives format instructions such as "Enter all possible values of x, separated by commas" (AoPS handbook search result, accessed 2026-09-29). Alcumus also has XP, quests and achievements that do not affect progression (handbook above). Mobile behaviour, motion and typography: unknown; I did not open the app.

## Engineering signals [single-source]

The public engineering is the patent and the blog. Problems carry topic and concept tags, difficulty ratings are learned from responses, topics form a prerequisite hierarchy, and selection picks a topic and then a problem within a rating window of about 5 to 100 points (patent above). The spaced repetition is a review-problem mechanism rather than a published interval schedule. No published efficacy study of Alcumus turned up in my search. Item authoring pipeline: unknown.

## What it does badly [uncertain]

AoPS admits early Alcumus gave no guidance and was "terrible for teaching" as a scattershot (https://artofproblemsolving.com/blog/articles/what-is-alcumus-why-we-called-it-that, accessed 2026-09-29; the quoted wording is from a search summary, so treat it as a paraphrase). Answer parsing is strict and depends on format instructions. Some problems are too hard, and AoPS advises students not to skip all of them (handbook above). It may not match a school curriculum (mathgeekmama review above). No independent efficacy evidence was found, and a search summary of an AoPS resources page says Alcumus works best when wrapped in teaching (https://artofproblemsolving.com/resources, accessed 2026-09-29; not fetched directly). Problem-first discovery has no measured outcome data in what I read, and the Calculus book's own page does not claim it.

## Sources [verified]

- https://artofproblemsolving.com/blog/articles/alcumus-a-peek-under-the-hood-of-our-adaptive-learning-tool, accessed 2026-09-29: rating scale, logistic model, Bayesian updating, selection weights.
- https://artofproblemsolving.com/blog/articles/what-is-alcumus-why-we-called-it-that, accessed 2026-09-29: design philosophy, problem counts, early version history.
- https://artofproblemsolving.com/school/handbook/current/alcumus, accessed 2026-09-29: two tries, pass and mastery colours, review problems, XP.
- https://patents.google.com/patent/US10720072B2/en, accessed 2026-09-29: rating update rule, prerequisites, attempt threshold.
- https://artofproblemsolving.com/store/item/intro-algebra, accessed 2026-09-29: problem-first section structure.
- https://artofproblemsolving.com/store/item/calculus, accessed 2026-09-29: Calculus textbook scope and size.
- https://www.goodreads.com/en/book/show/1366499, accessed 2026-09-29: discovery order description (search result only).
- https://artofproblemsolving.com/school/about-classroom, accessed 2026-09-29: class format, 90 minutes, moderation, transcripts.
- https://artofproblemsolving.com/school/handbook/prospective/liveorselfpaced, accessed 2026-09-29: live versus self-paced.
- https://mathgeekmama.com/alcumus-online-learning-a-review/, accessed 2026-09-29: reviewer view of wrong-answer flow and fit.
- https://artofproblemsolving.com/resources, accessed 2026-09-29: search snippet only.
