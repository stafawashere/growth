---
title: Khan Academy, how it picks the next problem
research_date: 2026-09-29
status: draft
purpose: Record how Khan Academy's mastery levels, exercises, mastery challenges and unit tests decide what a learner practices next, as evidence for the design of the Growth daily practice set.
---

# Khan Academy, the daily practice set

This file studies practice selection. Course contents and lesson anatomy are in `../../products/khan-academy.md` and are not repeated. Most Khan help-center pages returned HTTP 403 to my fetch tool on 2026-09-29, so several rules below rest on search-result snippets of those pages, and each such case is marked. A number I could not source is written as unknown.

## 1. What decides the next problem [single-source]

Mostly the learner. The course is one fixed linear order of skills, quizzes, unit tests and a course challenge, and the learner picks what to open (https://www.khanacademy.org/math/ap-calculus-bc, accessed 2026-09-29). The one algorithmic selector documented today is the mastery challenge, whose skills and questions are "personalized and adapted" from the time since the learner last reviewed a skill and the skill's level, and which unlocks only after 3 Familiar skills, 1 Proficient skill and 12 hours since the last one (https://support.khanacademy.org/hc/en-us/articles/360037127892-What-are-Mastery-Challenges-in-course-mastery and https://support.khanacademy.org/hc/en-us/articles/360037494231-What-are-Mastery-Challenges, both search snippets, accessed 2026-09-29). Older mastery mechanics also recomputed which exercises to offer as practice tasks after each task (https://mattfaus.com/2014/07/03/khan-academy-mastery-mechanics/, accessed 2026-09-29). The current ranking rule for that recompute is unknown.

## 2. How a set is sized and ordered [uncertain]

A mastery challenge is always 6 questions over 3 skills, 2 per skill, drawn from anywhere in the course (https://support.khanacademy.org/hc/en-us/articles/360037494231-What-are-Mastery-Challenges, snippet, accessed 2026-09-29). Practice exercises have a fixed question count that the pre-exercise card states, and I did not find the number; user post titles refer to 6 of 7 and 7 of 7, so 7 occurs (https://support.khanacademy.org/hc/en-us/community/posts/18856054184717-Why-is-perfection-required-for-proficiency-6-7-questions-correct-should-be-enough, title only, accessed 2026-09-29). I could not confirm the range of 4 to 7 named in the brief. The 2014 mechanics post describes 5 correct in a row as the completion rule then (https://mattfaus.com/2014/07/03/khan-academy-mastery-mechanics/, accessed 2026-09-29), which is older and may not hold.

Unit test and course challenge lengths are unknown. Question order inside an exercise is drawn at random from a bank; a 2013 note describes a per-user jump through the bank so that consecutive students do not see a pattern (https://johnresig.com/blog/random-khan-exercises/, search snippet, accessed 2026-09-29).

## 3. How difficulty is chosen and estimated [single-source]

Difficulty is fixed by the skill, not chosen per problem. The 2014 mechanics post admits that "all items within an exercise are assumed to have equivalent discernibility," which the author calls a known compromise (https://mattfaus.com/2014/07/03/khan-academy-mastery-mechanics/, accessed 2026-09-29). An earlier Khan machine learning post describes a logistic regression on six engineered features from practice history, a proficiency badge at 94 percent predicted accuracy, then a separate model per exercise with evidence from other exercises, which let capable learners reach proficiency within five problems. It reports learning gains up 33 percent in the top ten topics from that change (https://derandomized.com/post/51729670543/khan-academy-machine-learning-measurable, accessed 2026-09-29; vendor authors, undated, and superseded by the level system). The current level rules are explicit thresholds and not a fitted model, as far as the help pages show.

Levels move on score. Under 70 percent gives Attempted, 70 to 99 percent Familiar and 100 percent Proficient, while only a mixed assessment moves Proficient to Mastered (https://support.khanacademy.org/hc/en-us/articles/5548760867853--How-do-Khan-Academy-s-Mastery-levels-work, as quoted in the existing lesson file, accessed 2026-09-29). A search snippet of the same help page gives Familiar as 70 to 85 percent, so the upper bound conflicts and I record it as unresolved.

## 4. What happens after a wrong answer [single-source]

In an exercise a hint can be used before any attempt and marks the question wrong even if the learner then answers correctly, while in quizzes and tests hints appear only after a wrong submission (https://support.khanacademy.org/hc/en-us/community/posts/115003344211-Use-of-hints, snippet, accessed 2026-09-29). Hints appear one at a time and the last one gives the answer (https://khan-exercises.readthedocs.io/en/latest/exercises/hints.html, accessed 2026-09-29).

A practice exercise with exactly one error offers a bonus question, and a correct answer erases the error and grants Proficient (https://support.khanacademy.org/hc/en-us/articles/35916723756685-How-does-a-student-earn-Proficient-on-a-practice-exercise, accessed 2026-09-29). In a mastery challenge two wrong answers on a skill lower its level and one of each holds it (https://support.khanacademy.org/hc/en-us/articles/360037494231-What-are-Mastery-Challenges, accessed 2026-09-29).

Unit tests show no step-by-step solution afterward according to users (https://support.khanacademy.org/hc/en-us/community/posts/12175192853389-If-you-get-a-question-wrong-you-can-not-view-a-step-by-step-solution, title only, accessed 2026-09-29). A missed question does not enter a personal queue of mistakes as far as I found.

## 5. How review is compressed or deduplicated [single-source]

It is not compressed. Each skill is reviewed on its own, two questions at a time, three skills per mastery challenge, and no document I found gives encompassing credit from harder skills to easier ones. The 2014 post says a delay between promotions is "one way we use spaced repetition" (https://mattfaus.com/2014/07/03/khan-academy-mastery-mechanics/, accessed 2026-09-29), and the mastery challenge help page says it offers personalized spaced repetition based on elapsed time and level (snippet, accessed 2026-09-29). The spacing function is not published. The 12-hour gate limits how many challenges run per day, so that gate is the only volume cap I found.

## 6. What the student sees on the day screen [single-source]

The course page shows units with skills in a vertical list, a five-color level legend, quiz and test markers, the mastery percentage and, once unlocked, the mastery challenge button on the main course page (https://www.khanacademy.org/math/ap-calculus-bc and the mastery challenge help snippet, accessed 2026-09-29).

A newer learner dashboard shows classes, progress toward mastery and "the work they should focus on next," with a learner queue, daily or weekly missions and gems for class-wide challenges (https://blog.khanacademy.org/meet-the-new-khan-academy-classroom-experience/, accessed 2026-09-29). That description is teacher-assigned classroom flow, and what a self-directed learner sees on the Learn tab I could not read.

After each activity a card lists which skills leveled up, stayed or leveled down (https://support.khanacademy.org/hc/en-us/articles/115002552631-What-are-Course-and-Unit-Mastery, as quoted in the existing lesson file, accessed 2026-09-29).

## 7. What is public about the engineering [verified]

Two independent kinds of evidence agree that some machinery is public and the current selector is not. Perseus, the exercise renderer and editor, is open source (https://github.com/Khan/perseus, accessed 2026-09-29), and the older exercise framework is documented (https://khan-exercises.readthedocs.io/en/latest/exercises/hints.html, accessed 2026-09-29). Former engineers wrote about the proficiency model and mastery mechanics (https://derandomized.com/post/51729670543/khan-academy-machine-learning-measurable and https://mattfaus.com/2014/07/03/khan-academy-mastery-mechanics/, accessed 2026-09-29). An academic paper on running in vivo experiments on the platform exists at https://arxiv.org/pdf/1502.04245 (title only, accessed 2026-09-29). The mastery challenge selector and the present level thresholds appear only in help articles.

## 8. What it does badly [single-source]

Dan Meyer cites a Khan engineer saying some students progressed in exercises without demonstrating understanding (https://blog.mrmeyer.com/2013/pattern-matching-in-khan-academy/, accessed 2026-09-29). A teacher on the bonus question post reports a student who restarted an exercise nine times to reach 100 percent and guessing that moves many skills down in a course challenge (https://support.khanacademy.org/hc/en-us/community/posts/36008745490317-Update-Introducing-bonus-questions, accessed 2026-09-29). Another thread asks why perfection is needed when 6 of 7 seems enough (https://support.khanacademy.org/hc/en-us/community/posts/18856054184717-Why-is-perfection-required-for-proficiency-6-7-questions-correct-should-be-enough, title only, accessed 2026-09-29), and a further thread is titled as saying the mastery system is flawed (https://support.khanacademy.org/hc/en-us/community/posts/360075658631-The-mastery-system-is-flawed, title only, accessed 2026-09-29). The 2014 author's own admission of equal item difficulty is a vendor-side limit.

## 9. Sources [verified]

- https://support.khanacademy.org/hc/en-us/articles/360037494231-What-are-Mastery-Challenges, accessed 2026-09-29. Snippet only.
- https://support.khanacademy.org/hc/en-us/articles/360037127892-What-are-Mastery-Challenges-in-course-mastery, accessed 2026-09-29. Snippet only.
- https://support.khanacademy.org/hc/en-us/articles/5548760867853--How-do-Khan-Academy-s-Mastery-levels-work, accessed 2026-09-29. Snippet and prior file.
- https://support.khanacademy.org/hc/en-us/articles/35916723756685-How-does-a-student-earn-Proficient-on-a-practice-exercise, accessed 2026-09-29. Bonus question.
- https://mattfaus.com/2014/07/03/khan-academy-mastery-mechanics/, accessed 2026-09-29. Mechanics, 2014.
- https://derandomized.com/post/51729670543/khan-academy-machine-learning-measurable, accessed 2026-09-29. Proficiency model, undated.
- https://blog.khanacademy.org/meet-the-new-khan-academy-classroom-experience/, accessed 2026-09-29. Learner dashboard, queue, missions.
- https://blog.mrmeyer.com/2013/pattern-matching-in-khan-academy/, accessed 2026-09-29. Critic.
- https://github.com/Khan/perseus, https://khan-exercises.readthedocs.io/en/latest/exercises/hints.html, https://arxiv.org/pdf/1502.04245, accessed 2026-09-29. Public engineering.
