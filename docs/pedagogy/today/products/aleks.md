---
title: ALEKS, how the next topic is chosen
research_date: 2026-09-29
status: draft
purpose: Record how ALEKS decides what a student practises next, how learned and mastered are decided, how Knowledge Checks compress review, and where the public evidence is weak, so Growth's daily practice set can borrow fringe-based selection and check-based confirmation without its known costs.
---

# ALEKS, the next topic

The lesson-side reading is in docs/pedagogy/products/aleks.md and is not repeated. Everything below was read on 2026-09-29. The main sources are ALEKS's own 2015 student guide, three papers by its research team and one independent theoretical paper, so almost all evidence is the vendor describing itself.

## What decides the next problem [uncertain]

The unit is a topic, a problem type with many equal-difficulty instances, and the state of a student is the set of topics they know, out of a knowledge structure of prerequisite-consistent states. The outer fringe of a state K is the set of topics not in K that could be added to K and still leave a valid state, which ALEKS calls the topics the student is "ready to learn". The inner fringe is the set of topics whose removal still leaves a valid state (Matayoshi, Uzun and Cosyn, J. Math. Psychology 101, 2021, https://jmatayoshi.github.io/publications/JMP2021_KST_ALEKS_preprint.pdf, accessed 2026-09-29). That paper says the student chooses any topic from the outer fringe and practises it, and a typical course has about 300 to 600 topics. The 2015 guide says the Topic Carousel is sorted from easiest to hardest Ready to Learn topics by default, can be reordered by pie slice, and the home page's Start My Path button leads into it (https://www.aleks.com/highered/math/New_ALEKS_Student_Module_Reference_Guide.pdf, accessed 2026-09-29). A 2025 paper says the system presents one topic and that students tend to work on that one (https://jedm.educationaldatamining.org/index.php/JEDM/article/view/900, accessed 2026-09-29). So who picks within the fringe, and by what rule beyond easiest first, is not public.

The two accounts differ and I cannot reconcile them.

## How a set is sized and ordered [single-source]

There is no fixed daily set. Learning is a stream of one topic at a time until it is learned or a break is suggested, then a progress Knowledge Check appears. The guide says a check generally comes after learning 20 topics and about five hours, or after an Objective, that the student has 24 hours to start it, and that a Next Knowledge Check indicator on the home page shows what remains (https://www.aleks.com/highered/math/New_ALEKS_Student_Module_Reference_Guide.pdf, accessed 2026-09-29). The student handout says timing is set by the instructor and spaced so there are not too many in a short time (https://www.aleks.com/resources/ALEKS_Knowledge_Checks_Overview_for_Students.pdf, accessed 2026-09-29). The initial assessment is capped at 30 questions, of which up to 29 are adaptive and one is a random extra problem used for research (JMP 2021 preprint above).

After the deployment of July 2020 the average progress test fell from 19.6 to 13.3 questions (https://jmatayoshi.github.io/publications/AIED2021_progress_update.pdf, accessed 2026-09-29).

## How difficulty is chosen and estimated [single-source]

Difficulty is not tuned per student. Instances inside a topic are described as equal in difficulty (https://jedm.educationaldatamining.org/index.php/JEDM/article/view/900, accessed 2026-09-29). What varies is which topics are available and how much evidence is required. The assessment keeps a probability over knowledge states, selects each next question with likelihood close to 0.5, updates after each answer, and stops when items are above 80 percent or below 20 percent or when 30 questions are reached (JMP 2021 preprint). An "I don't know" button sharply raises the probability of states without the item, because open-ended answers make lucky guesses very unlikely. The paper's footnote gives update constants of about 35 for a correct answer, 5 for an incorrect one and 50 for "I don't know", with variation by course.

The guide says the progress bar sometimes shows three bars instead of five because ALEKS adjusts to what the student knows.

The 2025 paper gives the rule, a target score of 5 for topics classed unknown after the initial assessment and 3 for uncertain ones.

## What happens after a wrong answer [single-source]

Scoring is points. A correct answer adds 1, a second consecutive correct answer adds 2, a wrong answer subtracts 1 with a floor of 0, and opening the explanation changes nothing except that it breaks the streak (JMP 2021 preprint).

A first wrong answer allows a second try at the same instance, a second wrong answer shows the explanation and a fresh instance, and five wrong answers in a row end the attempt with an invitation to work on something else, which moves the topic to the end of the carousel (guide above). The 2025 paper adds that a score is reset whenever a progress assessment is taken. Across 21,769,811 Algebra I attempts, 84.1 percent succeeded, 3.0 percent failed, 8.5 percent were incomplete and 4.4 percent were left at once after the example (JMP 2021 preprint, Table 4).

## How review is compressed or deduplicated [single-source]

Review happens inside the Knowledge Check, not as separate sets. Topics learned are only "learned" until a check confirms them, and a check may also ask topics already mastered (student handout above).

Topics lost in a check are tagged Needs More Practice and generally queued first in the carousel, and a topic that was learned then removed needs only a score of 3 to be learned again (guide above, JMP 2021 preprint).

Since 2020 the check uses a neural network to pick topics the student is likely to forget, favours topics learned less recently, and dropped average questions by about 32 percent and hours per student by about 26 percent (AIED 2021 paper above).

The paper's own estimate is that students using it learned 9.8 topics more, about 9 percent, but the comparison is 2020 against 2019 and the authors say COVID makes the groups unlikely to be equivalent. Progress assessments also "run a local search" near the states the student recently crossed (JMP 2021 preprint).

## What the student sees on the day screen [single-source]

The home page shows the ALEKS Pie, with one slice per topic category, dark shading for mastered topics, light shading for learned topics and no color for remaining ones, and a counter in the middle equal to mastered plus learned (guide above). Selecting a slice shows counts of mastered, learned and remaining. A blue Primary Guidance Menu holds UP NEXT with a Start My Path button, WORKING TOWARD with goals and due dates, and the Next Knowledge Check indicator. Locked topics in the carousel show a lock icon until prerequisites are learned. The Ready to Learn count per slice appears in the carousel drop-down.

## What is public about the engineering [verified]

The team publishes at https://jmatayoshi.github.io/publications (accessed 2026-09-29). Its papers cover forgetting curves and the testing effect (EDM 2018), a neural retention model (AIED 2019), retrieval practice (L@S 2020, best paper co-winner), research-based updates (AIED 2021), the practical KST paper of 2021 and a 2025 randomized mastery-threshold experiment (J. Educational Data Mining 17(1)).

The 2021 paper reports retention curves from 6,701,233 students, 2016 to 2019, using 8,352,006 extra problems. Correct rate on a learned topic drops steeply within days for topics in the first inner layer and levels near 0.6, ends near 0.67 for layer 2, and near 0.8 for layers of 5 or more.

The 2019 paper finds that the identity of the problem type matters most, more than time since learning. The L@S paper finds delayed retrieval is associated with better retention and that learning closely related content is associated with even higher retention than being assessed. Doroudi's AIED 2020 paper shows that a simplified ALEKS mastery rule is optimal for a variant of Bayesian knowledge tracing, an independent reading seen through a search summary only (https://link.springer.com/chapter/10.1007/978-3-030-52240-7_16, accessed 2026-09-29). I found no public code.

## What it does badly [uncertain]

The strongest independent outcome evidence is old. A meta-analysis of 15 studies and 24 samples from 2005 to 2015 found ALEKS as good as, not better than, traditional teaching, with larger effects at shorter use (Fang, Ren, Hu and Graesser, https://eric.ed.gov/?id=EJ1232632, accessed 2026-09-29).

The vendor's own randomized test found that a higher mastery threshold reduces forgetting but the difference shrinks over time, with a modelled retention gain of about 0.021 (JEDM 2025 above). The vendor found "assessment fatigue" in long assessments and that students prefer learning to being assessed (EDM 2018 and AIED 2021 papers above). The handout admits that topics drop out of the pie after a check.

Teacher and student complaints about strict answer formats and reset progress are anecdotal (https://www.commonsense.org/education/reviews/4109561/teacher-reviews, accessed 2026-09-29, search summary only, cited in the lesson file). I found no independent audit of the fringe or of the ordering inside it.

## Sources [verified]

- https://www.aleks.com/highered/math/New_ALEKS_Student_Module_Reference_Guide.pdf, accessed 2026-09-29. 2015 guide, pie, carousel, scoring, checks.
- https://www.aleks.com/resources/ALEKS_Knowledge_Checks_Overview_for_Students.pdf, accessed 2026-09-29. Learned versus mastered, 30 question cap.
- https://jmatayoshi.github.io/publications/JMP2021_KST_ALEKS_preprint.pdf, accessed 2026-09-29. Fringes, assessment, scoring, retention curves.
- https://jmatayoshi.github.io/publications/AIED2021_progress_update.pdf, accessed 2026-09-29. Neural-selected progress test.
- https://jedm.educationaldatamining.org/index.php/JEDM/article/view/900, accessed 2026-09-29. Thresholds 5 and 3, randomized test.
- https://jmatayoshi.github.io/publications, accessed 2026-09-29. Publication list, EDM 2018, AIED 2019, L@S 2020 abstracts.
- https://www.aleks.com/about_aleks/knowledge_space_theory, accessed 2026-09-29. About 25 to 30 question assessment.
- https://link.springer.com/chapter/10.1007/978-3-030-52240-7_16, accessed 2026-09-29. Doroudi, search summary only.
- https://eric.ed.gov/?id=EJ1232632, accessed 2026-09-29. Fang et al. meta-analysis.
- https://www.commonsense.org/education/reviews/4109561/teacher-reviews, accessed 2026-09-29. Complaints, search summary only.
