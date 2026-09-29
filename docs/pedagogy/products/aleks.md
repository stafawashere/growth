---
title: ALEKS, how it teaches
research_date: 2026-09-29
status: draft
purpose: Document ALEKS's assessment-then-practice loop, mastery rule, wrong-answer handling and evidence base as input to the Growth lesson-framework redesign.
---

# ALEKS (McGraw Hill)

## Who it serves [verified]

ALEKS (Assessment and LEarning in Knowledge Spaces) began at UC Irvine in 1994 with National Science Foundation funding and was bought by McGraw-Hill Education in 2013 (https://en.wikipedia.org/wiki/ALEKS, accessed 2026-09-29). It spans K-12, higher education and continuing education, from basic arithmetic to precalculus and MBA accounting (same source). Institutions buy it, and instructors configure it through an Instructor Module, so the student is usually a course-assigned learner, not a self-selected one (https://www.aleks.com/highered/math/New_ALEKS_Student_Module_Reference_Guide.pdf, accessed 2026-09-29). A calculus course was released on 15 September 2025 for higher education STEM students, and it includes 134 prerequisite topics from algebra and precalculus (https://investors.mheducation.com/news/news-details/2025/McGraw-Hill-Releases-AI-Powered-ALEKS-for-Calculus/default.aspx, accessed 2026-09-29). I found no public topic list for the calculus course proper; the course-products page lists titles only (https://www.aleks.com/about_aleks/course_products?cmscache=detailed&detailed=gk12high27_calk, accessed 2026-09-29).

## Lesson anatomy [single-source]

There is no fixed lesson. The unit is a topic, and the loop is: initial assessment, pie chart, a topic from the Ready to Learn carousel, an optional learning page, problem instances until a point total is reached, then a later Knowledge Check. The details below come from a 2015 McGraw-Hill internal student guide, so the current interface may differ (Student Module Reference Guide, accessed 2026-09-29).

A topic ends when the student reaches 5 points. A correct answer earns 1 point, an incorrect answer costs 1 point (floor of zero), and two correct answers in a row without opening the explanation earn 2 points for the second. The bar sometimes shows 3 segments instead of 5, because ALEKS adjusts it to what it believes the student knows (same guide). Time per topic is not stated in any source I read. A consumer review site claims "five-minute lessons" (https://practicetestgeeks.com/aleks/aleks-assessment-and-learning-in-knowledge-spaces-aleks-prep, accessed 2026-09-29), which I treat as unverified.

## How it introduces a concept [single-source]

By default the student may see a learning page before the first problem, showing one example of the problem type and how to solve it. Instructors can switch this page off (Student Module Reference Guide). Otherwise the student attempts a problem cold. Underlined terms link to a dictionary. The topic is selected by the system as a Ready to Learn topic, meaning its prerequisites are already in the student's knowledge state (https://www.aleks.com/about_aleks/knowledge_space_theory, accessed 2026-09-29, for the state concept; the guide for the carousel). I found no source describing how explanations are written or reviewed.

## Worked examples and practice [single-source]

Practice is a stream of algorithmically generated instances of one topic; the Explanation button opens a pop-up that solves the current problem and does not reduce the score directly, though it forfeits the double credit (Student Module Reference Guide). Each new instance changes the numbers, so an example is never repeated verbatim. Problems are open-response, not multiple choice (https://www.aleks.com/about_aleks/knowledge_space_theory, accessed 2026-09-29, which says the assessment poses open-ended problems in its search results snippet; the guide describes an answer editor). Fading of examples is not documented.

## Response to a wrong answer [single-source]

The guide describes a fixed escalation. The first miss shows "Try again" and allows a second attempt at the same instance. The second miss turns the progress bar yellow and shows the explanation page, and Continue gives a new instance. Two more misses turn the bar orange, then a fifth miss turns it red, shows the correct answer and offers "Work on Something Else", which moves the topic to the last card of the carousel (Student Module Reference Guide). Later, a Knowledge Check can remove topics from the mastered count and tag them Needs More Practice, and ALEKS usually queues these at the front of the carousel (same guide). Students also report a lockout after repeated misses (https://finishmymathclass.com/i-hate-aleks-reddit-complaints/ via search summary, not fetched; treat as anecdote).

## Adaptation and sequencing [verified]

The domain is a knowledge structure, a set of feasible knowledge states over roughly 350 concepts for Algebra 1, generating millions of states (https://www.aleks.com/about_aleks/knowledge_space_theory, accessed 2026-09-29). Placement is a Bayesian search. The system holds a likelihood distribution over states, picks the question that splits the likelihood roughly in half, updates with careless-error and lucky-guess parameters, and stops when the top state passes a threshold of about 0.50 or higher (https://pmc.ncbi.nlm.nih.gov/articles/PMC10616228, accessed 2026-09-29). The initial assessment is 25 to 30 questions in the KST page and "less than 30" in the guide, so the two sources agree. The output is the set of known topics plus the outer fringe, the topics ready to learn. Locked topics appear when prerequisites are unmet (Student Module Reference Guide). Difficulty within a topic is not graded by the student's level in any source I found. Spacing is coarse: a Knowledge Check is triggered generally after 20 topics learned and five hours in the system, or at the end of an instructor Objective, and the student gets up to 24 hours to start it (same guide).

## What it measures [verified]

The measured object is a knowledge state, a set of topics, not a numeric score (PMC10616228). The pie chart shows slices per course area, with darker color for mastered and lighter for learned. Learned means practiced in Learning Mode; mastered means confirmed in a Knowledge Check, so retention is the criterion for mastery (Student Module Reference Guide; https://www.aleks.com/independent/students/tour_stu_pie, accessed 2026-09-29). A review notes ALEKS grades only the final answer and does not observe the strategy used (search result summary, https://arxiv.org/pdf/1607.07284, not fetched).

## Interaction patterns and visual design [inferred]

Documented controls are a Check and Re-Check button, an Explanation button, a progress indicator in the upper right that changes color and reads "2 in a row! Double credit!", a topic carousel that pulls down from a tab, dictionary links, and an on-page answer editor and calculator (Student Module Reference Guide). The homepage shows a timeline and a next-Knowledge-Check indicator. The calculus release adds a graphing tool meant to replicate pencil-and-paper sketching (investors.mheducation.com release above). I did not observe the live product, so layout, typography, motion and mobile behavior are unknown here.

## Engineering signals [single-source]

The content model is a prerequisite graph over topics with algorithmically generated instances, the theory published in Falmagne, Albert, Doble, Eppstein and Hu, Knowledge Spaces: Applications in Education (Springer, 2013) (https://www.amazon.com/Knowledge-Spaces-Applications-Jean-Claude-Falmagne/dp/364243441X, accessed 2026-09-29). Question selection, error parameters and termination rules are in PMC10616228. McGraw Hill says the calculus prerequisite set was chosen from "billions of ALEKS data points" and that AI-driven machine learning supports diagnosis (investors.mheducation.com release). The forgetting model behind Knowledge Check timing is unknown; I found only the 20 topics and five hours trigger. Authoring pipeline, item bank size and answer-checking logic are unknown.

## What it does badly [uncertain]

The strongest outside evidence is a meta-analysis of 15 studies (2005 to 2015, 24 samples) concluding ALEKS was as good as, not better than, traditional teaching, with larger effects at shorter usage durations (Fang, Ren, Hu and Graesser, Educational Psychology 39(10), 2019, https://eric.ed.gov/?id=EJ1232632 via search summary, accessed 2026-09-29). Vendor claims are institutional case studies, for example a College Algebra success rate rising from 34% to 74% at one community college, with no design or denominator given (https://www.mheducation.com/highered/digital-products/aleksppl/efficacy-and-research.html, accessed 2026-09-29). An IES-funded randomized trial in 10 Pennsylvania schools (about 1,320 students per year) ran 2014 to 2017, but the IES page reports no results (https://ies.ed.gov/use-work/awards/efficacy-aleks-improving-student-algebra-achievement?ID=1518, accessed 2026-09-29).

Student complaints, which are anecdotal, are: answer-format strictness marks correct math wrong, Knowledge Checks erase topics and reset progress, varied problem structure confuses, and short lessons lack depth (https://www.commonsense.org/education/reviews/4109561/teacher-reviews and https://www.trustpilot.com/review/aleks.com, both via search summary, not fetched). Because ALEKS records only final answers, it cannot see reasoning. Prerequisite-heavy content also means calculus concepts sit behind a large algebra diagnostic.

## Sources [verified]

- https://www.aleks.com/about_aleks/knowledge_space_theory, accessed 2026-09-29. Domain of about 350 concepts, 25 to 30 question assessment.
- https://www.aleks.com/highered/math/New_ALEKS_Student_Module_Reference_Guide.pdf, accessed 2026-09-29. 2015 internal guide: 5-point rule, wrong-answer escalation, Knowledge Check triggers.
- https://pmc.ncbi.nlm.nih.gov/articles/PMC10616228, accessed 2026-09-29. Half-split selection, Bayesian update, error parameters, outer fringe.
- https://www.aleks.com/independent/students/tour_stu_pie, accessed 2026-09-29. Pie chart slices and shading.
- https://en.wikipedia.org/wiki/ALEKS, accessed 2026-09-29. History and ownership.
- https://investors.mheducation.com/news/news-details/2025/McGraw-Hill-Releases-AI-Powered-ALEKS-for-Calculus/default.aspx, accessed 2026-09-29. Calculus course, 134 prerequisites, graphing tool.
- https://eric.ed.gov/?id=EJ1232632, accessed 2026-09-29 (search summary). Fang et al. 2019 meta-analysis.
- https://ies.ed.gov/use-work/awards/efficacy-aleks-improving-student-algebra-achievement?ID=1518, accessed 2026-09-29. Trial design, no results.
- https://www.mheducation.com/highered/digital-products/aleksppl/efficacy-and-research.html, accessed 2026-09-29. Vendor case studies.
- https://www.commonsense.org/education/reviews/4109561/teacher-reviews, accessed 2026-09-29 (search summary only). Student and teacher criticism.
