---
title: IXL, how it teaches
research_date: 2026-09-29
status: draft
purpose: Document how IXL structures practice, scoring, feedback and diagnosis so the Growth lesson framework can borrow or avoid each technique.
---

# IXL

## Who it serves [single-source]

IXL sells to schools, teachers and parents, pre-K through grade 12, in math, English language arts, science, social studies and Spanish (https://www.ixl.com/skill-plans, accessed 2026-09-29). Its calculus section is a practice list, not a course. It is written to be assigned by a teacher against a textbook, test or state standard, or self-directed by a student who picks a skill.

## Lesson anatomy [inferred]

IXL has no lesson in the sense of a sequenced explain, example, practice arc. The unit is a "skill", a single narrow topic (for example "Find limits using tables"), practiced as an open-ended stream of generated questions. The sidebar shows questions attempted, time elapsed, SmartScore and medals (https://www.ixl.com/userguides/us/IXLUserGuide.pdf, accessed 2026-09-29). A skill ends when the student stops or reaches 100. IXL says the number of questions to mastery "varies with every student" (same guide). Its family guide says a student may need as many as 10 correct answers in a row in the top band (https://www.ixl.com/materials/SmartScore_Guide.pdf, accessed 2026-09-29). I could not retrieve a skill page in full, so the presence and layout of any "learn with an example" panel or video on calculus skills is unknown; my fetches returned only navigation text.

## How it introduces a concept [uncertain]

Sources describe IXL as practice, not instruction. One competitor-authored review states that "IXL is a practice platform, not a teaching tool" (https://www.myengineeringbuddy.com/blog/ixl-learning-reviews-pricing-2026-honest-look/, accessed 2026-09-29), and that source sells tutoring. IXL's own materials describe no concept introduction, only skills, questions and explanations after errors. Its guide tells students who miss a challenge question to read the explanation and, if still stuck, to use an in-skill recommendation to "build up foundational knowledge" (SmartScore_Guide.pdf above). Whether a skill page carries a worked example before the first question is unknown; not found in fetched pages.

## Worked examples and practice [single-source]

Practice is generated, unlimited and varied in form. IXL states questions include word problems, visual representations and interactive activities, answered by multiple choice, fill in the blank, or drawing a graph (IXLUserGuide.pdf above). Difficulty moves with performance. IXL's blog says correct answers lead to harder questions and incorrect answers to simpler ones (https://blog.ixl.com/2020/11/11/ixl-smartscore-the-key-to-mastery-based-learning/, accessed 2026-09-29). The only worked examples I could source are the post-error explanations.

The calculus list, as extracted from https://www.ixl.com/math/calculus (accessed 2026-09-29), has 23 unit groups lettered A to W and about 127 skills by the page's own total, though the unit counts the extractor gave do not sum cleanly, so treat the count as approximate. Groups run limits, continuity, derivatives, derivative applications, integration, differential equations and applications of integration (areas, disk and washer volumes). The extracted list shows no series, parametric, polar or vector topics, so BC-only content appears absent. That gap is from a machine-summarized page and should be rechecked by hand.

## Response to a wrong answer [verified]

The student clicks Submit. If wrong, "IXL provides the right answer with a question-specific step-by-step explanation" (IXLUserGuide.pdf above), and IXL's blog says the same and adds that the next questions become easier (blog above). The SmartScore drops. The explanation is tied to the specific generated question, not to a diagnosis of the error type; one review says the student gets only the answer and a short explanation, without adaptive questioning about why (myengineeringbuddy link above, competitor bias). Later, IXL offers in-skill recommendations of prerequisite skills (SmartScore_Guide.pdf above). Students can also click "I don't know this yet" to skip a diagnostic question, and the diagnostic tells them only right or wrong, with no explanation (IXLUserGuide.pdf above).

## Adaptation and sequencing [verified]

SmartScore runs 0 to 100 and starts at 0. IXL defines 0 to 70 as learning and practicing with large gains and small penalties, 71 to 90 as mid to high rigor, 80 as proficiency, 90 as entry to the "Challenge Zone", and 100 as mastery. In the Challenge Zone, correct answers add 1 to 2 points and wrong answers subtract 3 to 8 (SmartScore_Guide.pdf above; https://www.ixl.com/help-center/article/1272663/how_does_the_smartscore_work, accessed 2026-09-29, reached only through a secondary quote). The exact formula is proprietary. IXL lists inputs as correctness, question difficulty, recent answers, consistency and number of questions, and says it is not a percentage (IXLUserGuide.pdf above).

There is no visible prerequisite graph inside a skill. Sequencing comes from skill plans, curated lists aligned to over 40 textbook series, standardized tests and all 50 state standards (IXLUserGuide.pdf above), and from diagnostic action plans showing up to five recommended skills per strand (https://blog.ixl.com/2021/08/17/what-is-ixls-diagnostic-action-plan/, accessed 2026-09-29). I found no spaced repetition algorithm; scores drop on error but I found no scheduled review.

The Real-Time Diagnostic takes about 45 minutes per subject to place a student, then 10 to 15 questions a week keep levels current (https://blog.ixl.com/2021/01/28/common-questions-about-the-ixl-real-time-diagnostic/; https://www.ixl.com/materials/us/i_guides/Teacher_Plan_Diagnostic, both accessed 2026-09-29). Levels are grade-scaled numbers, where 450 means about half of grade 4. A level shows as a range, then narrows to a star once pinpointed. IXL's pages call the ongoing mode a "Continuous Diagnostic" (https://www.ixl.com/diagnostic/info, accessed 2026-09-29). Whether the diagnostic reaches calculus is unknown; sources speak of grade levels and math and ELA only.

## What it measures [single-source]

Skill-level proficiency (SmartScore) and grade-level working level per strand (diagnostic). Teacher reports add time, questions and skills mastered, and a Trouble Spots report groups students by scaffolding level (https://www.ixl.com/membership/teachers/how-it-works, via search summary, accessed 2026-09-29). Achievements count questions, time, days practiced and streaks (IXLUserGuide.pdf above).

## Interaction patterns and visual design [inferred]

Single question per screen, typed or selected answer, explicit Submit, a persistent right-hand progress panel, medals and achievements for motivation, audio support for pre-K to grade 8, and a graph-drawing input for some skills (IXLUserGuide.pdf above). I did not observe the calculus skill screens directly, so typography, motion and mobile behavior are unknown.

## Engineering signals [uncertain]

Content is a large catalog of parameterized, auto-generated questions with question-specific explanations; IXL states "nearly 1,500 math skills in Grades 3-5" alone (https://www.ixl.com/materials/us/research/Randomized-Control_Efficacy_Study_of_IXL_Math.pdf, accessed 2026-09-29). The SmartScore is a proprietary difficulty-aware score, not a published model such as Elo or Bayesian knowledge tracing. No public authoring pipeline, item response model or calibration method found.

Efficacy evidence is mostly IXL-commissioned. A cluster randomized trial in Holland, Michigan (545 students, grades 3 to 5, spring 2023) found a 10 point Star Math gain, effect size 0.13, and a non-significant M-STEP effect of 0.03; Evidence for ESSA rates it "Strong" on that single study (https://evidenceforessa.org/program/ixl-math/, accessed 2026-09-29). A quasi-experimental study of about 4,000 pre-K to 12 charter students over one semester used matched controls (https://www.ixl.com/ESSA/ESSA-Research-Report.pdf, accessed 2026-09-29), and a three-year Oklahoma study compared 179 IXL schools with 179 others, reporting about 4 percent more students proficient (search summary of https://www.ixl.com/materials/us/research/IXL_Math_3-Year_QED_ESSA_Tier_2.pdf). None targets calculus or grades 9 to 12 alone that I could find.

A 2023 IXL report argues that fluctuating SmartScore paths produce more growth than steady ones, but it measures growth with IXL's own diagnostic (https://www.ixl.com/materials/us/research/How_IXLs_SmartScore_Supports_Student_Learning.pdf, accessed 2026-09-29), so the outcome is not independent.

## What it does badly [single-source]

The main documented complaint is SmartScore asymmetry. Near mastery, one miss costs more than one hit earns, and critics report large drops, for example one anecdote of 97 falling to the mid 60s (myengineeringbuddy link above) and a student score falling from 99 to 89 (via https://www.boddlelearning.com/article/ixl-punishes-wrong-answers, accessed 2026-09-29). Both critics sell competing products, and the anecdotes are unverified; IXL's own stated range is 3 to 8 points. Critics say it raises anxiety and reads as a verdict on ability. IXL's response is that setbacks are productive struggle, and it cites its own study (SmartScore report above).

Other weaknesses: no concept instruction sourced, feedback is answer plus worked steps and not error diagnosis, more practice of the same type when stuck, no scheduled spaced review found, unknown coverage of BC-only topics, and efficacy evidence limited to grades 3 to 8 outcomes.

## Sources [verified]

- https://www.ixl.com/materials/SmartScore_Guide.pdf, 2026-09-29, milestones, Challenge Zone point ranges, in-skill recommendations.
- https://www.ixl.com/userguides/us/IXLUserGuide.pdf, 2026-09-29, wrong-answer explanation, question types, skill plans, SmartScore inputs.
- https://www.ixl.com/help-center/article/1272663/how_does_the_smartscore_work, 2026-09-29, cited by others; page body did not load.
- https://blog.ixl.com/2020/11/11/ixl-smartscore-the-key-to-mastery-based-learning/, 2026-09-29, difficulty adaptation and walkthrough after errors.
- https://www.ixl.com/math/calculus, 2026-09-29, calculus skill list (machine-summarized).
- https://www.ixl.com/diagnostic/info, 2026-09-29, 45 minute diagnostic, continuous updates.
- https://blog.ixl.com/2021/01/28/common-questions-about-the-ixl-real-time-diagnostic/, 2026-09-29, 10 to 15 questions weekly, level stars and ranges.
- https://www.ixl.com/materials/us/i_guides/Teacher_Plan_Diagnostic, 2026-09-29, diagnostic setup (search snippet and PDF).
- https://blog.ixl.com/2021/08/17/what-is-ixls-diagnostic-action-plan/, 2026-09-29, up to five skills per strand.
- https://www.ixl.com/skill-plans, 2026-09-29, plan categories.
- https://www.ixl.com/materials/us/research/Randomized-Control_Efficacy_Study_of_IXL_Math.pdf, 2026-09-29, RCT.
- https://evidenceforessa.org/program/ixl-math/, 2026-09-29, independent rating of the RCT.
- https://www.ixl.com/ESSA/ESSA-Research-Report.pdf, 2026-09-29, quasi-experimental charter school study.
- https://www.ixl.com/materials/us/research/How_IXLs_SmartScore_Supports_Student_Learning.pdf, 2026-09-29, IXL study on score fluctuation.
- https://www.boddlelearning.com/article/ixl-punishes-wrong-answers, 2026-09-29, criticism, competitor.
- https://www.myengineeringbuddy.com/blog/ixl-learning-reviews-pricing-2026-honest-look/, 2026-09-29, criticism, tutoring competitor.
