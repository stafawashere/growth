---
title: Fluency Training for Calculator Procedures
research_date: 2026-09-29
status: draft
purpose: What the learning-science literature and the documentation of practice products say about building speed and accuracy on a short tool procedure, and what that supports and rules out for a Desmos drill in the app.
---

# Fluency Training for Calculator Procedures

None of the sources below is in the local cache. Each claim carries the URL it was read from in this session, as docs/plan/01-learning-model.md does. Where a PDF was read in full, the page number is the journal page unless marked as a PDF page. Three URLs are carried over from docs/plan/01-learning-model.md without being reloaded here, and they are marked as such. Nothing in this file is an exam fact or a tool fact for the app. Exam facts stay in research/exam/exam-structure.md and Desmos facts stay in the cached `desmos-*` documents.

## The practice curve for a procedure [verified]

Newell and Rosenbloom 1981 is known here only through Heathcote, Brown and Mewhort, whose preprint says Newell and Rosenbloom compared power and exponential functions across many tasks and found power functions fit better "in every case" (PDF p.3). https://users.cs.northwestern.edu/~paritosh/papers/KIP/power-law-repealed.pdf [verified]

Heathcote, Brown and Mewhort 2000 refit the question on individual learners. They fit both functions to 40 data sets covering 7910 learning series from 475 subjects in 24 experiments. The exponential fit better in every unaveraged set, and "averaging produced a bias in favour of the power function" (PDF p.2). The distinction matters for interpretation. An exponential implies a constant learning rate relative to what is left to learn, while the power function implies a mechanism that slows learning as practice goes on (PDF p.5). Same URL, [verified]. The PubMed record for the published article is https://pubmed.ncbi.nlm.nih.gov/10909131/ (the page did not render in this session).

Two consequences follow, both [inferred]. First, a curve drawn from the class average will look like a power law even when each student's curve is exponential, so the app should show each student their own curve and never a cohort curve as a norm. Second, both laws agree that gains are large early and small late, so a student's time on a Desmos procedure should flatten after a modest number of repetitions, and further repetitions in the same session buy little speed.

## Speed and accuracy are traded, so both are recorded [verified]

Heitz 2014 calls the covariation of decision speed and accuracy "an inescapable property of choice behavior" across species (p.1). He opens with Luce's advice to study the tradeoff and "devise some summary statistic to describe it" (p.1). The methodological point is that "group means obtained at a single criterion provide only a snapshot of performance" which conflates strategy with task difficulty, and that with the criterion free, results can range from very fast responses at chance accuracy to slow responses at asymptotic accuracy (p.4, citing Wickelgren 1977). Speed instructions are the most common manipulation because they "yield large effect sizes" (p.6). https://www.frontiersin.org/journals/neuroscience/articles/10.3389/fnins.2014.00150/pdf [verified]

Ericsson, Krampe and Tesch-Römer 1993 describe the usual laboratory arrangement for speed training as easy tasks where accuracy is reached quickly and subjects are "instructed to increase the speed of performance while maintaining the high level of accuracy" (p.367). https://gwern.net/doc/psychology/writing/1993-ericsson.pdf [verified]

For a drill this means, [inferred], that a timer shown or rewarded moves the student's criterion toward speed and buys time with errors. Time and correctness must be stored as separate fields per attempt, and a time is only meaningful beside the accuracy it was earned at. A single blended score such as characters per minute net of errors hides the trade.

## Demonstration before practice [single-source]

Sweller's worked-example effect, as summarised in the encyclopedia entry, is that studying a step-by-step demonstration helps a learner with few schemas more than solving unaided, that the benefit reverses as expertise grows (Kalyuga et al), and that removing steps one at a time eases the move from examples to problems. https://en.wikipedia.org/wiki/Worked-example_effect [single-source, secondary]

The primary sources are those already in docs/plan/01-learning-model.md and were not reloaded in this session. Renkl, Atkinson, Maier and Staley 2002 on backward fading, https://link.springer.com/article/10.1023/B:TRUC.0000021815.74806.f6 [single-source, carried from plan 01]. Kalyuga, Ayres, Chandler and Sweller 2003 on expertise reversal, https://www.tandfonline.com/doi/abs/10.1207/S15326985EP3801_4 [single-source, carried from plan 01]. Salden, Aleven, Schwonke and Renkl on adaptive fading, http://www.cee.uma.pt/ron/Salden%20et%20al.%20-%20The%20Expertise%20Reversal%20Effect%20and%20Worked%20Examples.pdf [single-source, carried from plan 01; the server refused the connection in this session].

Ericsson et al add that tasks should be designed so they "can be correctly understood after a brief period of instruction" (p.367, same URL as above) [verified].

Applied to a tool procedure, [inferred]. The literature is about problem-solving schemas, not keystroke sequences, so the transfer is a reasoning step. A Desmos procedure such as entering a definite integral has a small number of steps whose order and syntax a novice cannot guess, which is the case the worked-example effect covers. The demonstration should be shown once, then withdrawn, and not shown again unprompted to a student who already performs the procedure correctly, which is the expertise-reversal guard plan 01 already applies to calculus skills.

## Spacing and mixing of procedure practice [verified]

Shea and Morgan 1979 had subjects learn three motor tasks in a blocked or a random order. Retention and transfer were greater after random (high interference) practice, most notably on the most complex transfer task. https://eric.ed.gov/?id=EJ215260 [single-source, abstract only]

Ericsson et al summarise training studies of daily practice duration as showing "essentially no benefit from durations exceeding 4 hr per day" and reduced benefit beyond 2 hours, and report that studies of typing skill acquisition (Baddeley and Longman 1978; Dvorak et al 1936) indicate the effective daily duration may be closer to 1 hour (p.370). https://gwern.net/doc/psychology/writing/1993-ericsson.pdf [verified, as a secondary report of the typing studies]

Cepeda, Vul, Rohrer, Wixted and Pashler 2008 on the optimal gap relative to the retention interval is already in docs/plan/12-open-questions.md and plan 01, https://laplab.ucsd.edu/articles/Cepeda%20et%20al%202008_psychsci.pdf [verified in plan 01, not reloaded here].

What follows, [inferred]. The Desmos procedures a Calculus BC student uses are few and similar, so interleaving them (a zero, then an integral, then a derivative at a point) is the contextual-interference arrangement, and it should look worse during the session than blocked practice while retaining better. A drill's in-session times are therefore a poor guide to what was learned, and the useful measurement is the first attempt at a procedure on a later day. Short sessions spread over days fit the typing evidence better than long single sessions.

## Deliberate practice on components [verified]

Ericsson et al define deliberate practice as a structured activity in which "specific tasks are invented to overcome weaknesses" and performance is monitored for cues to improve (p.368). Conditions include immediate informative feedback and repeated performance of the same or similar tasks, and without adequate feedback "mere repetition of an activity will not automatically lead to improvement" in accuracy (p.367). They also claim deliberate practice "requires effort and is not inherently enjoyable" (p.368). https://gwern.net/doc/psychology/writing/1993-ericsson.pdf [verified]

The 1993 framework rests on expert musicians and a ten-year horizon, which is far from a student learning five calculator procedures. A 2019 replication paper exists at https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6731745/ and was not read in this session, so its findings are not stated here [uncertain].

For a drill, [inferred]. The component is the single procedure (graph and read a zero, evaluate an integral, evaluate a derivative at a point, set the window, check radian mode), practised one at a time with feedback on correctness immediately after each attempt. The student's weakest procedure, by their own accuracy record, is the one to offer, not the one they are fastest at.

## Automaticity, precision teaching and curriculum-based measurement [single-source]

Binder 1996 defines behavioral fluency as "that combination of accuracy plus speed of responding that enables competent individuals to function efficiently and effectively in their natural environments", and describes frequency aims as empirically determined performance frequency ranges that define fluency, linked to retention, endurance and application. https://pmc.ncbi.nlm.nih.gov/articles/PMC2733609 [single-source, abstract level; the full text was not read]

Haring and Eaton's instructional hierarchy, as summarised by Intervention Central, has four stages. In acquisition the learner cannot yet perform the task reliably and needs demonstration and corrective feedback. In fluency the learner is accurate but slow and the recommended techniques are frequent practice with feedback on speed and accuracy. Generalization and adaptation follow. The same summary also lists "praise for improved fluency" as a fluency-stage technique. https://www.interventioncentral.org/academic-interventions/general-academic/instructional-hierarchy-linking-stages-learning-effective-in [single-source, secondary]

Deno 2003 describes curriculum-based measurement as standard, short, repeated measurement tasks, including "writing correct answers/digits in solving problems in arithmetic" (p.185), with specified sample duration, administration and scoring. In the formative evaluation model a baseline is plotted, "a goal is established", and a line from baseline to goal shows the rate of improvement required (p.185). https://files.eric.ed.gov/fulltext/EJ785942.pdf [verified]

Two points, [inferred]. The hierarchy supports ordering demonstration (acquisition) before timed practice (fluency), and supports measuring accuracy before speed is looked at. The rate aims of precision teaching and the goal lines of CBM are targets, and the project forbids targets. The app takes the measurement practice (standard task, repeated, timed, scored for correctness, plotted per student) and leaves out the aim, the goal line and the praise. Plan 15's `fluent` label, which compares a skill's median time with the part budget from research/exam/exam-structure.md, is a threshold of this kind, and a Desmos drill should not inherit it.

## How practice products present speed and accuracy [single-source]

Each row is what the cited page says the product shows, read in this session. A product feature not on the cited page is not claimed.

| Product | Measured number shown | Goal, streak, badge or ranking | Source |
|---|---|---|---|
| keybr | Per-key statistics from every keystroke, progress graphs on a profile page | A user-set target typing speed; new letters unlock on reaching it; the product predicts how many lessons remain to the target | https://github.com/aradzie/keybr.com [single-source, project README] |
| Monkeytype | Labels for wpm, acc, raw, consistency and time in the result markup | A daily leaderboard label in the same markup | https://monkeytype.com/about [single-source; the page is script-rendered and only its static labels were readable] |
| Duolingo | The streak, a count of consecutive days with a completed lesson | Streak freeze; Duolingo describes loss aversion growing with streak length, reports +1.7 percent 7-day return from streak animations, +0.38 percent daily active learners from allowing two freezes, and learners at a 7-day streak 3.6 times as likely to finish a course; it also says a broken streak can feel demotivating | https://blog.duolingo.com/how-duolingo-streak-builds-habit [single-source, vendor] |
| Duolingo, criticism | Not applicable | Hadi Mogavi et al, L@S 2022, analysed nine years of Duolingo forum posts and 15 interviews and define gamification misuse as users becoming too fixated on gamification and distracted from learning | https://arxiv.org/abs/2203.16175 [single-source] |
| Math Academy | XP, about one minute of focused effort each, awarded for correct answers; timed quizzes about every 150 XP | An adjustable daily XP goal; negative XP when the system detects rushing and guessing; exceeding a quiz time limit triggers review as an incorrect answer does, on the stated view that a student who cannot perform in the time given has not mastered the material | https://www.mathacademy.com/faq [single-source, vendor] |
| Bluebook, SAT practice | Scores in My Practice; Score Details lists every question, the submitted answer and the correct answer, with explanations and skill domains | A custom question set for skills that "might need a boost" | https://satsuite.collegeboard.org/practice/bluebook [single-source] |
| Bluebook, practice page | Full-length tests are timed like real tests and scored when signed in; test previews are untimed; AP practice is sent to AP Classroom | None stated | https://bluebook.collegeboard.org/students/practice [single-source] |
| Bluebook, AP test preview | None; students receive no scores or feedback on answers; previews contain sample multiple-choice and free-response questions and are untimed | None stated | https://apcentral.collegeboard.org/help-center/can-students-try-sample-ap-exam-questions-bluebook-testing-app-exam-day and https://bluebook.collegeboard.org/students/ap-exams [single-source] |
| Desmos | The College Board versions of the four-function, scientific and graphing calculators, and a Test Practice Page; nothing is measured | None on the page | `desmos-testing p.1` [verified] and `desmos-help-testing-calculators p.1` [verified] |

On the College Board side, the AP route shows a student nothing about their answers. The only place a student can practise the exam's Desmos calculator is Desmos's own route, which offers the calculator and no measure of speed or accuracy (`desmos-testing p.1`, `desmos-help-testing-calculators p.1`) [verified]. A Desmos drill that records time and correctness is therefore adding a measurement neither source provides, [inferred].

## What this supports for a Desmos drill [inferred]

Ranked by the strength of the evidence behind each, strongest first. All of it is the author's reasoning from the sections above.

1. Record time and accuracy separately on every attempt and show them together. Speed is bought with accuracy under any speed emphasis (Heitz p.1, p.4, p.6), so neither number means anything alone and no blended score is computed.
2. Show the student their own median time and accuracy, with denominators, and no target. Individual curves are exponential and averages mislead (Heathcote et al PDF p.2), so no cohort curve and no norm is shown. The number is described as what was measured, never as a level to reach.
3. One procedure per task, with feedback on correctness right after the attempt. Deliberate practice works on components and needs informative feedback (Ericsson et al p.367 to p.368).
4. Demonstrate, then drill. A single worked demonstration of the procedure before the first attempt, withdrawn once the student performs it correctly (worked-example effect and expertise reversal, Demonstration before practice; acquisition before fluency, Haring and Eaton via Intervention Central).
5. Space repeats of a procedure across days and mix procedures within a session. Random practice retains and transfers better than blocked (Shea and Morgan), daily practice beyond an hour or two adds little and typing studies point to about an hour (Ericsson et al p.370), and the gap should scale with the retention interval (Cepeda et al 2008, via plan 01). The first attempt on a later day is the measurement that counts.
6. Stop a session when the student decides to stop, not at a quota. Gains flatten within a session (Heathcote et al PDF p.5), so a count to reach adds repetitions of low value, and a quota is a target the project forbids.

Rejected mechanics, each with the reason and the page that shows it.

| Mechanic | Seen at | Reason for rejecting |
|---|---|---|
| Streak and streak freeze | Duolingo blog | A count of days kept alive by loss aversion is a goal on attendance, not a measure of the procedure; Duolingo's own page says breaking it can demotivate, and Hadi Mogavi et al document fixation that displaces learning. It is a quota under another name. |
| Leaderboard | Monkeytype daily leaderboard label | Ranks speed against other people, pushes the criterion toward speed (Heitz p.6), and compares against a cohort rather than the student's own record. |
| Target speed and lessons-to-target prediction | keybr README | A target, and a prediction of when it will be reached; both are forbidden by the project rules. |
| Daily XP goal | Math Academy FAQ | A quota. |
| Time limit treated as a wrong answer | Math Academy FAQ | Makes speed part of correctness and mastery, which plan 15 rules out ("Time is a pacing metric, never mastery evidence"); a slow correct Desmos entry is recorded as correct and slow. |
| Pass mark, rate aim or goal line | Binder 1996 frequency aims; Deno 2003 p.185 goal line | Targets. The measurement practice is kept and the aim is dropped. |
| Praise for improved speed | Intervention Central summary of the instructional hierarchy | Praise is forbidden; the student sees the change in their own numbers and nothing is said about it. |
| Badges | Listed with points and leaderboards as the gamification elements studied by Hadi Mogavi et al (abstract page, not the full text) | Rewards collection rather than the procedure. |

On the wrong side of the project's line, from what was cited, are the Duolingo streak and freeze, the Monkeytype leaderboard, keybr's target speed and its prediction, Math Academy's daily XP goal and its use of the time limit as a mastery criterion, the rate aims of precision teaching, the goal line of CBM, and the instructional hierarchy's praise. Math Academy's negative XP for detected rushing is the one mechanic aimed at the same problem as item 1, a speed bought with guessing, but it does so through a points penalty, and recording accuracy beside time exposes the same behaviour without one.

## Claims that could not be sourced in this session [uncertain]

TypingClub's display of speed, accuracy, stars or badges was not loaded, so nothing is said about it. Settled by its help pages. The keybr and Monkeytype web pages render by script, so only keybr's README and Monkeytype's static labels were read; how Monkeytype defines accuracy and consistency is not stated. Settled by the Monkeytype source or documentation. Newell and Rosenbloom 1981 and Wickelgren 1977 were read only through Heathcote et al and Heitz. The Macnamara and Maitra 2019 replication of Ericsson et al was found but not read. No study was found that tests worked examples or contextual interference on calculator or software procedures specifically, so the transfer from motor and problem-solving tasks to Desmos entry is reasoning, not evidence. Settled by a search of human-computer interaction and calculator-training literature.
