---
title: IXL, how it decides the next practice question
research_date: 2026-09-29
status: draft
purpose: Record how IXL's SmartScore, Challenge Zone, Real-Time Diagnostic and recommendations choose and size daily practice, so the Today set design can borrow or avoid each mechanism. Lesson content is covered in docs/pedagogy/products/ixl.md and is not repeated here.
---

# IXL, the daily practice set

## 1. What decides the next problem [single-source]

Inside one skill the state is the SmartScore and the recent answer history. IXL's design paper says a correct answer brings a similar or slightly harder question next, and IXL's blog says a wrong answer brings easier ones (https://www.ixl.com/research/IXL_Design_Principles.pdf and https://blog.ixl.com/2020/11/11/ixl-smartscore-the-key-to-mastery-based-learning/, accessed 2026-09-29). The user guide states that time spent on a question does not change the SmartScore (https://www.ixl.com/userguides/us/IXLUserGuide.pdf, accessed 2026-09-29).

Which skill comes next is mostly the student's or teacher's choice, not the algorithm's. A student picks from the Recommendations wall, pinned skill plans, the subject and standards tabs or the awards board, and a teacher can star skills onto the wall (IXLUserGuide.pdf, accessed 2026-09-29). The Real-Time Diagnostic adds its own recommended skills to the wall. The design paper says the intent is to give students information so they choose, "instead of locking students into a path" (Design_Principles.pdf, accessed 2026-09-29).

## 2. How a set is sized and ordered [single-source]

There is no fixed set. A skill runs until the student stops or reaches 100, and IXL says the number of questions to mastery varies with every student (IXLUserGuide.pdf, accessed 2026-09-29). The family guide says a student may need as many as 10 correct answers in a row in the top band (https://www.ixl.com/materials/SmartScore_Guide.pdf, accessed 2026-09-29). IXL suggests 80 as a stopping point and says the platform works best when a student reaches 80 in at least two skills per week (same guide). The teacher guide for the diagnostic suggests working one recommended skill to 80 each day (https://www.ixl.com/materials/diagnostic/IXL_Real-Time_Diagnostic_Guide_for_Teachers.pdf, accessed 2026-09-29).

A skill is saved on exit. The last question and the score wait for the student, and the timer pauses after two, four or six minutes of inactivity depending on grade (IXLUserGuide.pdf, accessed 2026-09-29). Order inside a skill is not documented beyond the difficulty rule above. I found no published count of questions per session.

## 3. How difficulty is chosen and estimated [single-source]

IXL states the SmartScore uses question difficulty, correctness, recent answers and consistency, and is not percent correct (SmartScore_Guide.pdf, accessed 2026-09-29). Bands are 0 to 70 (large gains, small penalties), 71 to 90 (mid to high rigor, proficiency at 80) and 90 to 100, the Challenge Zone (gains of 1 to 2 points, penalties of 3 to 8 points). How an item's difficulty is estimated is not stated for skills. The design paper says the Diagnostic uses Item Response Theory on data from both skill practice and the diagnostic Arena (Design_Principles.pdf, accessed 2026-09-29). The Trouble Spots report groups questions into "item types" (IXLUserGuide.pdf), which suggests a difficulty label sits at that grain, but that is my inference.

The Diagnostic is a separate selector. It starts at grade level, offers two questions at a time that IXL calls equally valuable, and narrows a level range until a star marks an exact level (https://www.ixl.com/userguides/us/IXLQuickStart_Diagnostic.pdf, accessed 2026-09-29). A student can press a "not learned yet" control to skip. Its stopping rule is none, "as many as you like" (same guide). Whether it reaches calculus is unknown, since every source speaks of grade levels in math and English language arts.

## 4. What happens after a wrong answer [single-source]

The score drops, and IXL shows the right answer with a question-specific step-by-step explanation (IXLUserGuide.pdf, accessed 2026-09-29). The next questions get easier (IXL blog above). The family guide tells students who miss a Challenge Zone question to read the explanation and, if still stuck, to open an in-skill recommendation that builds foundational knowledge (SmartScore_Guide.pdf, accessed 2026-09-29).

Sources conflict on a second try. The design paper says an incorrect answer earns an explanation and a chance to try again, while the user guide and blog describe answer plus explanation only (Design_Principles.pdf versus IXLUserGuide.pdf, accessed 2026-09-29). I could not settle which is current.

## 5. How review is compressed or deduplicated [uncertain]

I found no scheduled review and no documented deduplication. Every skill starts at 0, so mastery of a skill is not re-tested by the skill itself. The only cross-time mechanism is the Diagnostic, where students are asked to answer 10 to 15 questions a week to keep levels current, and levels also update from skill practice (Teacher guide above; Design_Principles.pdf, accessed 2026-09-29). Because questions are generated from item types, repeats of an exact question are possible, but I found nothing that says so.

## 6. What the student sees on the day screen [single-source]

There is no daily set screen. The Recommendations wall lists skills tailored to what the student has been working on, teacher stars and the Diagnostic entry (IXLUserGuide.pdf, accessed 2026-09-29). The Diagnostic stats page shows a level per strand as a range that narrows to a starred exact level, and each strand lists its recommended skills, for example "2 recommended skills" under a strand heading in the sample action plan (Teacher guide above). The action plan is printable. Teachers see a blue icon on skills that came from an action plan. Inside a skill the right panel shows questions, time, SmartScore and medals (IXLUserGuide.pdf). I did not open a signed-in home screen, so layout, ordering of the wall and any calculus content there are unknown.

## 7. What is public about the engineering [single-source]

The SmartScore formula is proprietary and unpublished. What is public is a design paper that names Item Response Theory for the Diagnostic (Design_Principles.pdf), IXL commissioned efficacy studies, and one 2023 report by an IXL researcher on 6,290 math students in grades 2 to 6 (https://www.ixl.com/materials/us/research/How_IXLs_SmartScore_Supports_Student_Learning.pdf, accessed 2026-09-29). That report found that skills reached with a fluctuating score, defined as 50 to 80 percent correct before proficiency, predicted an end-of-year Diagnostic gain of about 60 points per skill per week, against about 3 for steadily rising skills. It measures growth with IXL's own Diagnostic and is observational, so a student who fluctuates may simply be attempting harder skills, which is my reading and not the report's. No code, item model or calibration method is published.

## 8. What it does badly [verified]

The asymmetry of the Challenge Zone is documented by IXL itself (gains of 1 to 2, penalties of 3 to 8) and criticised by others. Boddle Learning, a competitor, quotes a petition where 99 fell to 89 after one miss (https://www.boddlelearning.com/article/ixl-punishes-wrong-answers, accessed 2026-09-29). Petition text in search summaries claims drops of up to 20, which conflicts with IXL's range and is unverified (https://www.change.org/p/paul-mishkin-change-ixl-s-smartscore-rate, via search summary, accessed 2026-09-29). Critics report anxiety and score protection instead of learning, and a teacher review on Common Sense, quoted in a roundup, says she limits IXL use because finishing a skill feels overwhelming to her students (https://nibble-app.com/blog/is-ixl-worth-it, a competitor, accessed 2026-09-29). IXL answers that setbacks are productive struggle and cites its own report.

Other points from the sources are that the explanation is tied to the generated question and not to a diagnosed error, that recommendations point to a skill and not to a prepared review, and that no independent study covers grades 9 to 12 alone (see docs/pedagogy/products/ixl.md for the efficacy sources).

## 9. Sources [verified]

- https://www.ixl.com/materials/SmartScore_Guide.pdf, 2026-09-29, bands, point ranges, 10 in a row, 80 in two skills a week.
- https://www.ixl.com/userguides/us/IXLUserGuide.pdf, 2026-09-29, recommendations wall, timer, save on exit, wrong-answer explanation.
- https://www.ixl.com/research/IXL_Design_Principles.pdf, 2026-09-29, adaptive rule, IRT claim, choice over locked path.
- https://blog.ixl.com/2020/11/11/ixl-smartscore-the-key-to-mastery-based-learning/, 2026-09-29, harder after correct, easier after wrong.
- https://www.ixl.com/materials/us/research/How_IXLs_SmartScore_Supports_Student_Learning.pdf, 2026-09-29, fluctuation study.
- https://www.ixl.com/materials/diagnostic/IXL_Real-Time_Diagnostic_Guide_for_Teachers.pdf, 2026-09-29, action plan, one skill a day, 10 to 15 questions a week.
- https://www.ixl.com/userguides/us/IXLQuickStart_Diagnostic.pdf, 2026-09-29, Arena steps, two-question choice.
- https://www.ixl.com/help-center/article/1272663/how_does_the_smartscore_work, 2026-09-29, page body did not load.
- https://www.boddlelearning.com/article/ixl-punishes-wrong-answers, 2026-09-29, critic, competitor.
- https://nibble-app.com/blog/is-ixl-worth-it, 2026-09-29, critic roundup, competitor, search summary only.
- https://www.change.org/p/paul-mishkin-change-ixl-s-smartscore-rate, 2026-09-29, petition, search summary only.
