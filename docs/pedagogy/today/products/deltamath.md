---
title: DeltaMath, how it decides the next practice problem
research_date: 2026-09-29
status: draft
purpose: Record how DeltaMath's assignment model, random problem draws, required-correct count, penalty settings, solutions and timed modes choose and size daily practice, so the Today set design can borrow or avoid each mechanism. Lesson-side content is in docs/pedagogy/products/deltamath.md and is not repeated here.
---

# DeltaMath, the daily practice set

## 1. What decides the next problem [single-source]

The teacher decides which skills exist in an assignment, and a random draw decides which problem the student sees inside a skill. The help center says almost every skill has a bank of 100 questions served randomly to students, and that a teacher can restrict a skill to chosen subtypes or use "Assign THIS Problem" so every student sees one fixed question (https://help.deltamath.com/assignments/add-skills-to-an-assignment, accessed 2026-09-29). The company's site says only that problems are randomized (https://www.deltamath.com/, accessed 2026-09-29).

This corrects a loose reading in the earlier lesson file, which called each skill a parameterised generator. The help center describes a finite bank served at random. Whether each bank entry is itself built from parameter draws is unknown, and I found no primary text that settles it. Mixed problem sets serve skills at random with a teacher-set frequency from 1 to 9, and the help center says it cannot guarantee that every student sees every skill (same page). Whether a student may pick the order of skills inside an assignment is not stated in the pages I read.

## 2. How a set is sized and ordered [verified]

Size is a threshold, not a count of problems. Each skill has a Required number of correct answers, default 5, and grades use the student's high score against it (https://help.deltamath.com/assignment-skill-settings and https://help.deltamath.com/data/assignment-grade-calculation, accessed 2026-09-29). A teacher blog confirms the model, describing a teacher choosing how many problems a student must complete per module (https://www.hoffmath.com/2021/03/howtousedeltamath.html, accessed 2026-09-29). Max Problems defaults to unlimited, and the options "2 times required" and "Equal to required" turn the skill into accuracy grading. Weight defaults to 1, and 0 marks a skill optional. Late work earns a set fraction of credit, 50 percent in the help center's example.

Timed skills ask for the required number of correct answers within a set number of seconds, and setting seconds to 0 removes the time rule while keeping the accuracy rule (assignment-skill-settings, accessed 2026-09-29). Assignments can also carry a time limit, where the timer runs even after the student logs out, with 1.5 times and 2 times extra-time multipliers (https://help.deltamath.com/assignment-overview-settings-gc, accessed 2026-09-29). Tests grade accuracy, while assignments grade completion or mastery (https://help.deltamath.com/en_US/tests/introduction-to-tests, accessed 2026-09-29). The order of problems inside a skill is not documented. Total minutes per skill is unknown.

## 3. How difficulty is chosen and estimated [single-source]

Difficulty is fixed by the skill and subtype the teacher picks, not estimated per student. I found no adaptive model, item rating or ability estimate in the help center or on the site. The site describes teachers as able to "control rigor" by mixing sets (https://www.deltamath.com/, accessed 2026-09-29). Guided skills add scaffolded prompts with hints when an intermediate step is wrong (https://help.deltamath.com/content-overview?kb_language=en_US, accessed 2026-09-29), which changes support, not the next problem. That there is no adaptivity is an absence finding, so it stays single-source.

## 4. What happens after a wrong answer [verified]

Two teacher settings decide it. The first is Solutions Shown, with the options Yes, On incorrect only, On correct only and No, listed among the PLUS and INTEGRAL tier settings, so the free-tier default is unknown (https://help.deltamath.com/assignment-overview-settings-gc, accessed 2026-09-29). The solution is for the problem the student saw, so it uses that student's own numbers. The second is the penalty. No Penalty adds nothing. 0.5 off requires one extra correct answer per two wrong ones. 1 off requires one extra correct answer per wrong one. Back to Zero resets the skill to zero on any miss, so the required answers must be consecutive (https://help.deltamath.com/assignment-skill-settings, accessed 2026-09-29).

A teacher blog gives the arithmetic. With 4 required and a 1 off penalty, a miss on the fourth problem leaves the score at 2, so two more correct answers finish it, and the author prefers no penalty because careless slips on easy items cause excess work (hoffmath.com link above, accessed 2026-09-29). A search-engine summary once described Back to Zero as allowing one free miss, which contradicts the help center, so I used the help center. Multiple attempts per question can be allowed, and a wrong attempt does not count against the student at first (assignment-skill-settings). A miss never lowers the recorded grade, since grades use the high score (assignment-grade-calculation).

## 5. How review is compressed or deduplicated [uncertain]

I found no spaced review, no deduplication and no prior-skill re-testing. The only review tool is a mixed problem set, where skills are drawn at random with a frequency weight (add-skills page, accessed 2026-09-29). With a bank of about 100 questions per skill, repeats are possible after heavy use, though no page says how the draw avoids questions already seen. Nothing in the help center describes carrying a wrong skill forward to a later day.

## 6. What the student sees on the day screen [uncertain]

The help center's student preview page says its view differs from what students see and does not describe the student interface (https://help.deltamath.com/additional-tools-c/sample-student-page-canvas, accessed 2026-09-29). Confirmed pieces are a timer icon and duration shown before a timed assignment opens, an embedded video that the teacher can show or hide, and step solutions according to the setting above (assignment-overview-settings-gc). A search summary of student guides adds that answers are checked immediately and that a full green bar means a skill is complete, but I could not tie that to a primary page, so treat it as unverified. Teachers see each attempt, its time and whether help videos were played (https://help.deltamath.com/assignment-data-view, accessed 2026-09-29). There is no adaptive daily set. I did not view a student session.

## 7. What is public about the engineering [uncertain]

Nothing beyond product documentation. I found no paper, patent, talk or code for DeltaMath's problem banks, answer equivalence checking or randomization. The help center gives bank sizes and tagging by standards, and the company describes teacher-authored problems on paid tiers (https://help.deltamath.com/create-your-own-problems-gc/intro-to-create-your-own-problems-gc, listed in search results, accessed 2026-09-29). One small outcome study in South Tangerang found no significant difference, seen only as a search summary of a ResearchGate page.

## 8. What it does badly [single-source]

Michael Pershan, a teacher, describes individual-device practice where stuck students click around and do not ask for help, and he prefers whole-group use of the skill bank (https://pershmail.substack.com/p/practice-software-is-struggling, accessed 2026-09-29). A teacher blogger prefers no penalty because escalating penalties inflate work after careless errors (hoffmath.com above). An educator review warns that repeated correct answers do not prove understanding (https://www.educatorstechnology.com/2023/03/deltamath-practice-math-through.html, accessed 2026-09-29). Trustpilot shows 2.2 of 5 on 20 reviews with complaints about correct answers marked wrong and progress stalling after a miss (https://uk.trustpilot.com/review/deltamath.com, accessed 2026-09-29), a small self-selected sample.

## 9. Sources [verified]

- https://help.deltamath.com/assignment-skill-settings, 2026-09-29, Required, penalties, max problems, weight, timed skills.
- https://help.deltamath.com/data/assignment-grade-calculation, 2026-09-29, high score, weighting, late credit.
- https://help.deltamath.com/assignment-overview-settings-gc, 2026-09-29, Solutions Shown, time limit, video visibility.
- https://help.deltamath.com/assignments/add-skills-to-an-assignment, 2026-09-29, bank of 100, subtypes, Assign THIS Problem, mixed-problem frequency.
- https://help.deltamath.com/en_US/tests/introduction-to-tests, 2026-09-29, tests versus assignments.
- https://help.deltamath.com/content-overview?kb_language=en_US, 2026-09-29, skill formats.
- https://help.deltamath.com/assignment-data-view, 2026-09-29, teacher view of attempts.
- https://help.deltamath.com/additional-tools-c/sample-student-page-canvas, 2026-09-29, student view not described.
- https://www.deltamath.com/, 2026-09-29, randomization claim, instant explanation.
- https://www.hoffmath.com/2021/03/howtousedeltamath.html, 2026-09-29, teacher account of penalties.
- https://pershmail.substack.com/p/practice-software-is-struggling, 2026-09-29, critique.
- https://www.educatorstechnology.com/2023/03/deltamath-practice-math-through.html, 2026-09-29, independent review.
- https://uk.trustpilot.com/review/deltamath.com, 2026-09-29, user complaints.
