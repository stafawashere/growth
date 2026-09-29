---
title: Explanatory video (3Blue1Brown style), how it teaches
research_date: 2026-09-29
status: draft
purpose: Record what is documented about animated explanatory video as a content form for calculus, and what the instructional video literature says it can and cannot do, as evidence for a lesson-framework redesign.
---

# Explanatory video (3Blue1Brown style)

This file treats the form, not one product. The reference case is the 3Blue1Brown "Essence of Calculus" series by Grant Sanderson. Section meanings are adapted: "who it serves" is the intended viewer, "lesson anatomy" is the shape of one video, "wrong answer" is what the form does when the viewer holds a misconception, and "what it measures" is what the form and its research can and cannot tell us about learning.

## Who it serves [single-source]

The series targets a self-selected viewer who wants to see why calculus works, not to drill it. Its own lesson page states the aim as making viewers feel they could have invented calculus themselves, with no explicit prerequisites beyond geometry such as circle area (https://www.3blue1brown.com/lessons/essence-of-calculus, accessed 2026-09-29). Sanderson says the ideal explanation depends heavily on the individual learner and that video works best beside human teachers (https://www.dwarkesh.com/p/grant-sanderson, accessed 2026-09-29). The series is therefore not built as a course for a student who must pass an exam, and no source states an exam audience for it.

## Lesson anatomy [single-source]

The Essence of Calculus playlist has 12 videos totalling 3 hours 11 minutes, so about 16 minutes per video. Chapter 1 runs 17:05, chapter 2 16:50, chapter 3 17:34, chapter 4 15:56 and chapter 5 13:50 (search listing of the YouTube playlist, https://www.youtube.com/playlist?list=PLZHQObOWTQDMsr9K-rj53DwVRMYO3t5Yr, accessed 2026-09-29; I could not open the playlist page itself, so individual times are from a search summary). Each video is one narrated animation built around a single problem, and Chapter 1 works from the area of a circle (https://www.3blue1brown.com/lessons/essence-of-calculus, accessed 2026-09-29). Sanderson says he will not start a video without a central "aha" and that the video length follows the content rather than a plan (https://podcasts.happyscribe.com/lex-fridman-podcast-artificial-intelligence-ai/118-grant-sanderson-math-manim-neural-networks-teaching-with-3blue1brown, accessed 2026-09-29, summarised, not quoted). The written adaptation of Chapter 1 on the site adds embedded multiple choice questions, for example on ring area, that act as check prompts rather than a problem set (same lesson page).

## How it introduces a concept [single-source]

The concept arrives as an answer to a visual puzzle. Sanderson describes the hook as curiosity, with the picture as "the prompt" that the story then resolves (https://blog.dropbox.com/topics/work-culture/grant-sanderson-channels-his-passion-for-math-into-marvelously-i, accessed 2026-09-29, via search summary). In Chapter 1 the circle is cut into rings, the rings become thin rectangles, and the rectangle heights are read off a graph, so the integral is reached before its notation (lesson page above). The Summer of Math Exposition rules, which Sanderson wrote, ask that motivation be clear within the first 30 seconds (https://www.3blue1brown.com/blog/some1/, accessed 2026-09-29). Sanderson also says he writes the animation in code because that is how he thinks the idea through (dwarkesh.com page above).

## Worked examples and practice [verified]

Video contains worked demonstrations but almost no practice. Sanderson says calculation work is where intuition is solidified and that self-learners skip it, and that most people use interactive explanations passively (dwarkesh.com and happyscribe.com pages above). Two independent literature sources agree that watching alone is weak. The ICAP review ranks passive watching below active, constructive and interactive engagement (https://www.tandfonline.com/doi/abs/10.1080/00461520.2014.965823, accessed 2026-09-29). Brame's guideline table recommends embedded questions, guiding questions and packaging video with problems to apply the concepts (Brame 2016, https://summeracademy.academic.wlu.edu/files/2020/07/RECOMMENDED-PRACTICES-from-Brame.pdf, accessed 2026-09-29). A randomised design by Kestin and Miller found that embedding questions increased learning and that the gain was larger when visuals were also enhanced (https://journals.aps.org/prper/abstract/10.1103/PhysRevPhysEducRes.18.010148, accessed 2026-09-29; I could not retrieve the sample size).

## Response to a wrong answer [single-source]

A linear video has no wrong-answer channel. The viewer is never asked to commit, so nothing is graded and nothing is corrected. The strongest evidence is Muller and colleagues, who randomly assigned first-year physics students to four presentations of Newton's laws. The groups whose presentation stated common misconceptions, or used a tutor and student dialogue, gained significantly more than the two traditional presentations. In a related report viewers rated the clear explanation highly while their reasoning stayed unchanged (https://onlinelibrary.wiley.com/doi/abs/10.1111/j.1365-2729.2007.00248.x, accessed 2026-09-29, abstract via search summary). The implication for the form is that a clean, correct explanation can produce a feeling of understanding without the change.

## Adaptation and sequencing [single-source]

None inside the video. The playlist is a fixed order of 12 chapters, from the essence of calculus through derivatives, the chain and product rules, e, implicit differentiation, limits, integration, higher order derivatives and Taylor series (playlist listing above, partly truncated in the source, so the twelfth title is unknown to me). There is no mastery model, spacing or difficulty control, and Sanderson's own remark that spaced repetition and problem solving are what stop lectures becoming "intellectual candy" places retention outside the medium (happyscribe.com page above, summarised).

## What it measures [uncertain]

Nothing in the form measures learning. The research that exists measures engagement or short outcomes in other settings. Guo, Kim and Rubin analysed 6.9 million video watching sessions across four edX courses and treated engagement, meaning watch time and problem attempts, as a necessary but not sufficient prerequisite for learning (https://pg.ucsd.edu/publications/edX-MOOC-video-production-and-engagement_LAS-2014.txt, accessed 2026-09-29, and the full text at https://www.cs.rochester.edu/hci/pubs/pdfs/edX-MOOC-video-production-and-engagement_LAS-2014.pdf, accessed 2026-09-29). I found no published learning outcome study of the 3Blue1Brown series itself, after searching the SoME pages, the Manim repository and general search. The Summer of Math Exposition scores entries on clarity, motivation, novelty and memorability via peer pairwise comparison, which measures reception by peers, not learning (https://www.3blue1brown.com/blog/some1/ and https://www.3blue1brown.com/blog/some1-results/, accessed 2026-09-29). Its results page reports over 1,200 entries and about 13,000 comparisons.

## Interaction patterns and visual design [verified]

The visual grammar is a dark background, colour as a consistent label for a quantity, and objects that transform continuously so the viewer sees one thing become another. Sanderson's tool, Manim, is an MIT licensed Python engine for programmatic animation of explanatory math videos, with the original 3b1b version and a community fork from 2020 (https://github.com/3b1b/manim, accessed 2026-09-29). The Bouzelmate and Rittaud paper on math video design agrees that animation is very important for mathematics video, and warns against putting on screen the text being spoken and against filming a classroom lesson (https://arxiv.org/pdf/2212.01204, accessed 2026-09-29). Mayer's principles that apply are signalling, segmenting, coherence and modality. A meta-analysis of 92 Mayer articles gave an overall g of 0.37, with segmenting at d = 0.34 and signalling at g = 0.38 (https://www.sciencedirect.com/science/article/pii/S1747938X25000673, accessed 2026-09-29, via search summary, not opened). Brame lists signalling, segmenting, weeding out extraneous material and matching modality as the ways to manage cognitive load (Brame table above). The form is pause and play with no manipulable objects, so it offers no direct manipulation.

## Engineering signals [single-source]

Public: Manim is open source, and scenes are Python classes rendered from the command line (github page above). Every animation is code, so figures are reproducible and parameterisable, which suggests figures for a web client could be generated from the same kind of code. The cost signal is Sanderson's own remark that scripting is "the worst" part, meaning production is slow and hand authored (happyscribe.com page above, summarised). No public content model, item bank or analytics exists for the series.

## What it does badly [verified]

Length: Guo and colleagues found median engagement was at most 6 minutes regardless of video length, and students often watched less than half of videos over 9 minutes. Problem attempts after videos fell from 56% to 31% across five length buckets, shortest to longest (Guo et al., full text above). The Essence of Calculus videos run 13:50 to 17:34, above that range, though the data come from MOOC lectures, not animated explainers.

Illusion of understanding: see Muller above.

Complex tasks: a 2025 study of over 300 high school students found live instruction outperformed recorded video as problem complexity rose, with no difference on simple problems (https://journals.aps.org/prper/abstract/10.1103/PhysRevPhysEducRes.21.010117, accessed 2026-09-29).

No practice or feedback, and a passive posture, are conceded by Sanderson and by Bouzelmate and Rittaud. Judging a video by its first 5 to 10 minutes and its opening 30 seconds (SoME rules above) rewards hooks over retention.

## Sources [verified]

1. https://www.3blue1brown.com/lessons/essence-of-calculus, accessed 2026-09-29. Chapter 1 format, aim, embedded questions.
2. https://www.youtube.com/playlist?list=PLZHQObOWTQDMsr9K-rj53DwVRMYO3t5Yr, accessed 2026-09-29. Playlist size, 3 h 11 min, chapter list (via search summary).
3. https://www.3blue1brown.com/blog/some1/, accessed 2026-09-29. SoME criteria, 30 second and 5 to 10 minute guidance.
4. https://www.3blue1brown.com/blog/some1-results/, accessed 2026-09-29. Entry count, ranking method.
5. https://podcasts.happyscribe.com/lex-fridman-podcast-artificial-intelligence-ai/118-grant-sanderson-math-manim-neural-networks-teaching-with-3blue1brown, accessed 2026-09-29. Sanderson on process, length, passivity (summarised).
6. https://www.dwarkesh.com/p/grant-sanderson, accessed 2026-09-29. Sanderson on calculation work, teachers, thinking in code.
7. https://blog.dropbox.com/topics/work-culture/grant-sanderson-channels-his-passion-for-math-into-marvelously-i, accessed 2026-09-29. Hook and story (via search summary).
8. https://github.com/3b1b/manim, accessed 2026-09-29. Manim description, license, versions.
9. https://www.cs.rochester.edu/hci/pubs/pdfs/edX-MOOC-video-production-and-engagement_LAS-2014.pdf, accessed 2026-09-29. Guo, Kim, Rubin 2014, 6.9 million sessions, length findings.
10. https://summeracademy.academic.wlu.edu/files/2020/07/RECOMMENDED-PRACTICES-from-Brame.pdf, accessed 2026-09-29. Brame 2016 practice table.
11. https://journals.aps.org/prper/abstract/10.1103/PhysRevPhysEducRes.18.010148, accessed 2026-09-29. Kestin and Miller 2022, embedded questions and visuals.
12. https://journals.aps.org/prper/abstract/10.1103/PhysRevPhysEducRes.21.010117, accessed 2026-09-29. Recorded versus live instruction, 2025.
13. https://onlinelibrary.wiley.com/doi/abs/10.1111/j.1365-2729.2007.00248.x, accessed 2026-09-29. Muller et al. 2008, misconceptions in multimedia (via search summary).
14. https://www.tandfonline.com/doi/abs/10.1080/00461520.2014.965823, accessed 2026-09-29. Chi and Wylie 2014, ICAP.
15. https://arxiv.org/pdf/2212.01204, accessed 2026-09-29. Bouzelmate and Rittaud, math video design.
16. https://www.sciencedirect.com/science/article/pii/S1747938X25000673, accessed 2026-09-29. Meta-analysis of Mayer research (via search summary, not opened).
