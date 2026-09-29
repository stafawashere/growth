---
title: Desmos Classroom, how it teaches
research_date: 2026-09-29
status: draft
purpose: Document how Desmos Classroom and Amplify Desmos Math structure activities, feedback and teacher orchestration, as evidence for a calculus lesson-framework redesign.
---

# Desmos Classroom

## Who it serves [single-source]

Desmos Classroom is a teacher-run, whole-class platform. Desmos states it builds activities for "classrooms, not individuals" and designs the dashboard around orchestrating discussion (https://blog.desmos.com/articles/introducing-the-new-desmos-activity-dashboard/, accessed 2026-09-29). Teachers can build their own activities in Activity Builder or use published ones, and Amplify Desmos Math is a full curriculum layered on the same engine for K to 12 (https://amplify.com/programs/amplify-desmos-math/, accessed 2026-09-29). The public calculus material is mostly teacher-authored, for example a "Definite Integrals and Limits of Riemann Sums" activity credited to a teacher and based on College Board material (https://classroom.amplify.com/activity/5fcfe26b94aec50d300e0ced, accessed 2026-09-29). It is not a self-paced tutor for an individual learner.

## Lesson anatomy [verified]

In Amplify Desmos Math grades 6 to 8, each lesson is a Warm-Up, one to three Activities, a Synthesis and a Show What You Know, and each activity runs Launch, Monitor, Connect (https://edreports.org/reports/detail/amplify-desmos-math-2026/sixth-to-eighth/gateway-three, accessed 2026-09-29). A separate Amplify help page describes the same components for high school and adds that the activities fit a 45-minute period (https://service.amplify.com/article/adm-ga2-integrated-1, accessed 2026-09-29). A "Lesson at a Glance" gives suggested timing per part, but I could not find the minute split or a typical screen count. Standalone Activity Builder activities are sequences of screens, and card sorts are described as having only "a handful of screens" (https://blog.mrmeyer.com/2016/the-desmos-guide-to-building-great-digital-math-activities/, accessed 2026-09-29).

## How it introduces a concept [single-source]

Concepts are introduced through a task before any exposition. The building code asks for "Estimations before calculations. Conjectures before proofs. Sketches before graphs. Verbal rules before algebraic rules." (https://blog.mrmeyer.com/2016/the-desmos-guide-to-building-great-digital-math-activities/, accessed 2026-09-29). One published example, Pomegraphit, puts fruit on an ungridded coordinate plane so students reason about direction before coordinates, and only then adds precision (https://blog.mrmeyer.com/2017/pomegraphit-how-desmos-designs-activities/, accessed 2026-09-29). The "Create a Need" principle asks that students experience why a tool was invented before receiving it (https://blog.desmos.com/articles/desmos-guide-to-building-great-digital-math-2021/, accessed 2026-09-29). Exposition is kept short: "Students tend to ignore screens with paragraphs of expository text", so it moves to teacher notes or is tied to earlier student answers via the computation layer (same 2016 source).

## Worked examples and practice [uncertain]

The published design writing is about concept development, not worked examples or drill, and I found no Desmos statement on worked-example use. The Amplify curriculum adds personalized practice, mini-lessons and a spaced-repetition Fluency Practice for basic facts (https://amplify.com/blog/problem-based-learning/meet-amplify-desmos-math/ was not retrievable, so this rests on a search summary of Amplify pages, accessed 2026-09-29), plus sub-unit quizzes and end-of-unit assessments with four-point rubrics (EdReports URL above). I could not confirm problem counts per lesson. Card Matching (one correct pairing) and Card Sort (open grouping) are the two card-sort modes (https://teacher.desmos.com/activitybuilder/, accessed 2026-09-29).

## Response to a wrong answer [verified]

Desmos separates immediate feedback from feedback that "interprets rather than evaluates". Its guide says to show students what their answer means, for example by using a sketch to drive a parachutist's path, then let them revise (https://blog.desmos.com/articles/desmos-guide-to-building-great-digital-math-2021/, accessed 2026-09-29). For concept development the stated rule is: "Delay feedback briefly... Then ask the student to check her prediction on a subsequent screen." (https://blog.mrmeyer.com/2016/the-desmos-guide-to-building-great-digital-math-activities/). In Pomegraphit the system reports "Your graph and your checkboxes disagree" and leaves reconciliation to the student (Pomegraphit URL above). Later, the teacher can anonymize names, project selected student work and use pacing to stop the class for discussion (https://blog.desmos.com/articles/how-do-you-use-the-teacher-dashboard-in-class/, accessed 2026-09-29). In Amplify Desmos Math, teachers can also send written digital feedback visible to students in real time (EdReports URL above).

The evidence for delay is thin and Meyer says so. He cites Simmons and Cope (1993), where immediate feedback led to more trial and error, and an informal survey of about 500 Twitter respondents, and he caveats that novices may need exploratory trial and error first and that a week's delay is worse than instant feedback (https://blog.mrmeyer.com/2017/desmos-design-why-were-suspicious-of-immediate-feedback/, accessed 2026-09-29). A 2016 post cites a state-capitals study where a 10 second delay helped a test a week later, and states "feedback is complicated" (https://blog.mrmeyer.com/2016/when-delayed-feedback-is-superior-to-immediate-feedback/, accessed 2026-09-29).

## Adaptation and sequencing [uncertain]

Activity Builder has no adaptive model. Sequencing is set by the author and the teacher, and the teacher controls pacing by pausing the class on one or more screens (https://blog.desmos.com/articles/introducing-the-new-desmos-activity-dashboard/). Amplify Desmos Math adds a beginning-of-year screener, pre-unit checks and personalized practice for K to 8, but I found no public description of the mastery model, prerequisite graph or spacing rules beyond the Fluency Practice claim (EdReports and Amplify URLs above).

## What it measures [single-source]

In Amplify Desmos Math, the measurements are rubric-scored assessments (Meeting, Approaching, Developing, Beginning) tied to standards, plus lesson-level Show What You Know tasks (EdReports URL above). In Activity Builder, the platform records every student response and interaction on each screen, and the dashboard summarizes them class-wide with histograms so the teacher picks whom to call on (dashboard articles above). It measures what students did and said, not a mastery estimate.

## Interaction patterns and visual design [single-source]

Screen types named in Desmos materials include the embedded graphing calculator, sketch or drawing over a blank page or uploaded image, card sort, multiple choice and text or number entry, and a scripting layer called Computation Layer that lets activities react to student input (https://teacher.desmos.com/activitybuilder/, and the Pomegraphit post, accessed 2026-09-29). The building code asks for a variety of "verbs" so students predict, argue, compare and validate, not only calculate (2016 guide URL above). The dashboard has Snapshot, Summary, Teacher and Student views, with a ribbon of screen thumbnails for pacing (https://blog.desmos.com/articles/introducing-the-new-desmos-activity-dashboard/). Amplify Desmos Math includes text-to-speech, enlarged fonts, braille mode and language selection (EdReports URL above). I did not verify mobile behavior.

## Engineering signals [uncertain]

The content model is a screen sequence with typed components, and the Computation Layer is a public scripting language (dashboard article above). Authors build in a browser editor and can copy others' activities (https://blog.desmos.com/articles/the-desmos-activity-builder-community/ appeared in search results only). I found no source on item generation, the spaced repetition algorithm or the Amplify mastery model.

## What it does badly [uncertain]

The only efficacy evidence I found is a retrospective WestEd matched comparison of about 900 schools (about 150 users, about 750 comparison) in nine states for 2021 to 2022, published by the vendor without effect sizes and described as unable to establish causation (https://amplify.com/news/new-efficacy-study-finds-desmos-math-6-8-significantly-improves-student-learning-outcomes-in-middle-grades/, accessed 2026-09-29). EdReports notes inconsistent guidance for multilingual learners and general, not embedded, links to students' lived experience (EdReports URL above). The delayed-feedback rule rests on small studies and the design authors' own caveats, and the activities depend on a teacher orchestrating discussion, so a solo learner loses the Monitor and Connect phases. I searched for independent teacher criticism about too little practice and found none in reachable sources, so that concern is unresolved.

## Sources [verified]

- https://blog.mrmeyer.com/2016/the-desmos-guide-to-building-great-digital-math-activities/ (2026-09-29): building code quotes on prediction, delayed feedback, card sorts, verbs, exposition.
- https://blog.desmos.com/articles/desmos-guide-to-building-great-digital-math-2021/ (2026-09-29): 2021 principles, interpret rather than evaluate, create a need.
- https://blog.mrmeyer.com/2017/desmos-design-why-were-suspicious-of-immediate-feedback/ (2026-09-29): delayed-feedback argument and caveats.
- https://blog.mrmeyer.com/2016/when-delayed-feedback-is-superior-to-immediate-feedback/ (2026-09-29): timing as a continuum.
- https://blog.mrmeyer.com/2017/pomegraphit-how-desmos-designs-activities/ (2026-09-29): worked design example.
- https://blog.desmos.com/articles/introducing-the-new-desmos-activity-dashboard/ (2026-09-29): dashboard views and pacing.
- https://blog.desmos.com/articles/how-do-you-use-the-teacher-dashboard-in-class/ (2026-09-29): teacher use of pacing and student work.
- https://teacher.desmos.com/activitybuilder/ (2026-09-29): card sort modes and components, via search summary.
- https://edreports.org/reports/detail/amplify-desmos-math-2026/sixth-to-eighth/gateway-three (2026-09-29): lesson structure, assessments, weaknesses.
- https://service.amplify.com/article/adm-ga2-integrated-1 (2026-09-29): high school components and 45-minute period, via search summary.
- https://amplify.com/news/new-efficacy-study-finds-desmos-math-6-8-significantly-improves-student-learning-outcomes-in-middle-grades/ (2026-09-29): WestEd study design.
- https://classroom.amplify.com/activity/5fcfe26b94aec50d300e0ced (2026-09-29): a calculus activity, thin detail.
