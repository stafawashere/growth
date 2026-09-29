---
title: Photomath, how it teaches
research_date: 2026-09-29
status: draft
purpose: Record how Photomath turns a scanned problem into a stepwise, explained solution and what evidence exists on its learning effects, as input to the Growth lesson-framework redesign.
---

# Photomath

## Who it serves [single-source]

Photomath is a phone app for secondary and early undergraduate students, and for parents helping them. Its support page lists content from numbers and operations through functions, vectors, matrices, trigonometry and calculus (https://support.google.com/photomath/answer/14328427, accessed 2026-09-29). Wikipedia reports over 220 million downloads and 2.2 billion problems solved per month as of 2021, and Google ownership announced in May 2022 (https://en.wikipedia.org/wiki/Photomath, accessed 2026-09-29). Sources disagree on the close date of the acquisition (March versus June 2023), so it is not stated here. The user brings the problem, so the product serves homework help, not a course sequence.

## Lesson anatomy [single-source]

There is no lesson. The unit of instruction is one solution card for one problem the user supplies. The flow is: point the camera at a problem, optionally resize the viewfinder by dragging a corner, then see a solution card at the bottom of the screen and tap "Show Solving Steps" to expand it (https://photomath.com/articles/photomath-101-get-math-with-photomath/, accessed 2026-09-29). Photomath's help page says the free tier gives step-by-step solutions, while Plus adds hints and "third-level steps" for when the student is stuck (https://support.google.com/photomath/answer/14328660, accessed 2026-09-29). Time per unit and number of screens per solution are unknown: I found no official figure, and the length depends on the problem.

## How it introduces a concept [uncertain]

It does not introduce concepts in sequence. Concept explanation is attached to a step after the fact: Plus includes "contextual hints and concepts explanations" (https://support.google.com/photomath/answer/14328660, accessed 2026-09-29). Photomath's blog says the app gives "deep explanations and reasoning behind each step," covering the "how" and "why" (https://photomath.com/articles/photomath-101-get-math-with-photomath/, accessed 2026-09-29). Both are the vendor describing itself, and I found no independent audit of how often a "why" note appears or how deep it is. Animated tutorials, described as over 400 in some secondary coverage, are the closest thing to concept teaching, but the 400 figure comes from a third-party summary and is unconfirmed by a primary page I could open.

## Worked examples and practice [single-source]

The product is a worked example generator for the student's own problem. The app "often" shows multiple cards with different methods or alternative explanations (https://photomath.com/articles/photomath-101-get-math-with-photomath/, accessed 2026-09-29). Animated Tutorials are Plus features with custom animation per step, plus written instructions that can be read or listened to (https://photomath.com/articles/math-from-all-angles-photomath-for-different-learning-styles/, accessed 2026-09-29). Interactive graphs can be zoomed and tapped for definitions (same source). Plus also carries solutions for every problem in 300+ named textbooks, reported by the vendor's own social post and repeated in review sites (https://www.facebook.com/Photomathapp/videos/textbooks-solutions/241400461073052/, accessed 2026-09-29). Practice is not part of the product as far as I found: no source describes generated practice problems, self-explanation prompts, or faded examples.

## Response to a wrong answer [inferred]

There is no answer-entry step, so there is no wrong-answer response in the usual sense. Students use the solution to check their own work, which the app does only by showing a full solution to compare against. I found no source describing error diagnosis, misconception detection, or a later review of a mistake. This section is inferred from the absence of any such feature in the help pages and reviews I read. Critics also note that an app "rarely tells you" that the underlying difficulty began earlier, for example with fractions or notation (https://coolmathguy.com/photomath-and-mathway-vs-actually-learning-math-what-solver-apps-miss, accessed 2026-09-29).

## Adaptation and sequencing [single-source]

None found. There is no placement, mastery model, prerequisite graph or spaced repetition described in any source I read. The only adaptivity is the student's choice of problem and whether to expand steps, hints (Plus) and animations. The Cool Math Guy article says solver apps do not build "sequence, practice, recall, and judgment" (https://coolmathguy.com/photomath-and-mathway-vs-actually-learning-math-what-solver-apps-miss, accessed 2026-09-29). That page cites no research and is a commercial tutoring site, so it counts as opinion.

## What it measures [uncertain]

Nothing about the learner that I could find. The app records scans and, per Google-era commentary, may use solved-problem data for model improvement, but that claim comes from a low-quality review site (https://www.myengineeringbuddy.com/blog/photomath-reviews-alternatives-pricing-offerings/, accessed 2026-09-29) and I treat it as unverified. No published learner model, mastery estimate or progress metric was found.

## Interaction patterns and visual design [single-source]

Input is the camera scan of printed or handwritten math, with typed entry as a fallback (Wikipedia and review sources, https://en.wikipedia.org/wiki/Photomath, accessed 2026-09-29). Handwriting recognition was added in 2016 (same source). Output is a bottom card of collapsed steps that expand on tap, with alternate method cards, animated steps and interactive graphs. Pacing is under student control: the blog says explanations "allow you to set your own pace" (https://photomath.com/articles/math-from-all-angles-photomath-for-different-learning-styles/, accessed 2026-09-29). It is phone-first. Typography and colour choices: unknown, I did not view the app.

## Engineering signals [uncertain]

Wikipedia describes the stack as an OCR engine (originating at Microblink) feeding a computer algebra system (https://en.wikipedia.org/wiki/Photomath, accessed 2026-09-29). The help page says the image goes to cloud servers and a neural network determines the formula, after which "a problem-solving algorithm" generates answer and steps (https://support.google.com/photomath/answer/14328660, accessed 2026-09-29). The blog says an in-house math team, many former teachers, decides how problems are explained; I found this only in search summaries, so the authoring pipeline is unconfirmed. Calculus coverage per the support page: limits, derivatives by various methods, tangent lines by derivative or limit, antiderivatives, integrals, and also power series, differential equations, Taylor and Maclaurin polynomials and convergence (https://support.google.com/photomath/answer/14328427, accessed 2026-09-29). The unsupported list was not visible in my fetch.

## What it does badly [uncertain]

The peer-reviewed evidence is weak. Two small quasi-experimental studies report positive results: 60 primary students with learning difficulties (30 versus 30) outperformed controls on a concept test after AI tools "like Photomath" (https://malque.pub/ojs/index.php/msj/article/view/8130, accessed 2026-09-29), and 46 first-year pre-service teachers in Rwanda showed significant gains in attitude, conceptual understanding of integration and independent learning (https://spm-online.com/jrmste/index.php/journal/article/view/61, accessed 2026-09-29). Neither is a randomised trial with a delayed transfer test, the samples are small, and the Rwandan design is described as survey based. Both flag overreliance, cheating and reduced interest in studying. A systematic review and a Grade 7 utilisation study exist (listed on ResearchGate) but I did not read them. I found no large independent trial of solver apps on retention or transfer, so the effect on the AP-level student is unknown. Non-academic criticism: solution display invites pattern copying without concept transfer (https://coolmathguy.com/photomath-and-mathway-vs-actually-learning-math-what-solver-apps-miss, accessed 2026-09-29). The animated tutorials, third-level steps and textbook solutions are behind a subscription, reported at $9.99 per month or $69.99 per year on review sites, not verified against a primary page.

## Sources [verified]

- https://support.google.com/photomath/answer/14328660 (accessed 2026-09-29): official overview, scanning, cloud processing, free versus Plus features.
- https://support.google.com/photomath/answer/14328427 (accessed 2026-09-29): official supported content list including calculus topics.
- https://photomath.com/articles/photomath-101-get-math-with-photomath/ (accessed 2026-09-29): vendor description of scan flow, expandable steps, multiple method cards.
- https://photomath.com/articles/math-from-all-angles-photomath-for-different-learning-styles/ (accessed 2026-09-29): vendor description of animated tutorials, graphs, pacing.
- https://en.wikipedia.org/wiki/Photomath (accessed 2026-09-29): history, OCR plus computer algebra system, download figures.
- https://malque.pub/ojs/index.php/msj/article/view/8130 (accessed 2026-09-29): quasi-experimental study, 60 students.
- https://spm-online.com/jrmste/index.php/journal/article/view/61 (accessed 2026-09-29): quasi-experimental study, 46 students, integration.
- https://coolmathguy.com/photomath-and-mathway-vs-actually-learning-math-what-solver-apps-miss (accessed 2026-09-29): uncited practitioner criticism.
- https://www.facebook.com/Photomathapp/videos/textbooks-solutions/241400461073052/ (accessed 2026-09-29): vendor post on 300+ textbooks.
- https://www.myengineeringbuddy.com/blog/photomath-reviews-alternatives-pricing-offerings/ (accessed 2026-09-29): pricing and data claims, low reliability.
