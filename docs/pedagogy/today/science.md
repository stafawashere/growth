---
title: Learning science and psychometrics behind choosing the next practice problem
research_date: 2026-09-29
status: draft
purpose: The literature on which problem to give next, how many, in what order, at what difficulty and with what feedback, set against what Growth's engine already does and what the selection study measured.
---

# Learning science and psychometrics behind choosing the next practice problem

This file reads the literature that bears on item selection, not on lesson design. It reuses the sources in docs/pedagogy/learning-science.md by name (Cepeda 2008, Roediger and Karpicke 2006, Adesope 2017, Rohrer 2020, Wisniewski 2020, Sinha and Kapur 2021) and adds new ones. Every URL was accessed 2026-09-29 and is listed at the end. Each section says what the literature reports with numbers, what Growth already does according to docs/plan/01, 02 and 03, and what Growth does not do. A number appears only where a fetched page or a search summary carried it, and "not retrieved" marks the rest. Several publisher pages (Springer, Nature, PNAS, ACM) refused the fetch, so their figures come from search summaries and the tags say so.

The selection study (docs/operator/selection-study.md) is the yardstick for the last section. It found that two-term selection is nearly random because due coverage fires on 1.1 percent of block 2 choices at 60 days and 7.5 percent at 226 days, and that the forgetting oracle led on delayed retention with a best cell of 91.0 percent.

## 1. Spacing and the schedulers [verified]

(a) The literature. SM-2 is the 1987 SuperMemo rule, published in 1990. Every item starts at an ease factor of 2.5, the first two intervals are 1 and 6 days, later intervals multiply the previous one by the ease factor, and the factor is kept between 1.1 and 2.5. The Leitner box system dates from Leitner's 1972 book and moves a card up a box on success and back to box one on failure. Both are hand-set heuristics with no fitted forgetting curve.

Half-life regression (Settles and Meeder 2016, ACL) fitted a per-word half-life from Duolingo logs. The paper reports error reduced by more than 45 percent against baselines including Leitner and Pimsleur, and a 12 percent lift in daily engagement in an operational test.

DASH (Lindsey, Shroyer, Pashler and Mozer 2014, Psychological Science 25(3)) put a personalised model into a semester-long middle-school Spanish course and, with review time matched, reported a 16.5 percent gain in cumulative-exam retention over massed study and 10.0 percent over a one-size-fits-all spaced schedule. Sample size was not retrieved.

FSRS descends from Ye, Su and Cao 2022 (KDD, 220 million MaiMemo logs). The srs-benchmark repository scores prediction of recall on 9,999 Anki collections and 349,923,850 reviews (519,296,315 when same-day reviews are kept). The table below is the benchmark's own README, without same-day reviews. Lower log loss is better.

| Algorithm | Log loss | RMSE (bins) | AUC |
|---|---|---|---|
| FSRS-7 with recency | 0.3370 | 0.0593 | 0.7220 |
| FSRS-7 | 0.3401 | 0.0634 | 0.7167 |
| FSRS-6 | 0.3460 | 0.0653 | 0.7034 |
| FSRS-5 | 0.3561 | 0.0742 | 0.7010 |
| FSRS-4.5 | 0.3625 | 0.0764 | 0.6891 |
| DASH | 0.3682 | 0.0838 | 0.6311 |
| HLR | 0.4694 | 0.1275 | 0.6369 |

An older Expertium summary page puts SM-2 near 0.53 log loss and AUC near 0.595, read off charts, so that figure is approximate. With same-day reviews included the gap opens, FSRS-7 at 0.3206 against FSRS-6 at 0.3842, which is the version difference that matters to a system that ignores same-day repeats. The benchmark measures prediction of recall on flashcards only. It does not measure whether a schedule improves learning.

MEMORIZE (Tabibian et al 2019, PNAS) casts scheduling as stochastic optimal control. For two memory models, if the learner maximises recall subject to a cost on review frequency, the optimal schedule is given by the recall probability itself. I read that as review intensity rising with the probability of forgetting. The exact form was not retrieved from the paper. The natural experiment on Duolingo data reported better memorisation under MEMORIZE-like schedules, with no effect size retrieved.

Cepeda et al 2008 (over 1350 people, gaps to 3.5 months, tests to a year) gives the ridgeline. The best gap was about 20 percent of the test delay at delays of weeks, and 5 to 10 percent at a year. Too short a gap costs more than too long a gap.

Spacing for procedural mathematics has a small literature. Rohrer and Taylor 2006 (216 college students, Applied Cognitive Psychology) found that ten practice problems split across two sessions roughly doubled four-week performance against massing them, with no benefit at one week, and that solving 3 or 9 problems in one session made no difference at either delay.

Hopkins, Lyle, Hieb and Ralston 2016 (Educational Psychology Review 28(4)) spaced weekly quiz questions per learning objective in engineering precalculus and found better final-exam and next-semester calculus performance. Lyle, Bego, Hopkins, Hieb and Ralston 2020 (32(1)) crossed amount and spacing within subjects and found both raised the final exam, with the largest gain when both rose.

Lyle, Bego, Ralston and Immekus 2022 found in calculus that spacing raised end-of-semester retention while lowering performance on the first two practice-quiz questions. Effect sizes and n were not retrieved for any of the three.

The meta-analysis of Murray, Horner and Goebel 2025 (Educational Psychology Review) gives g = 0.28 for spacing in mathematics over 27 studies and 53 effects, larger for isolated material (0.43) than for course-embedded material (0.24).

(b) What Growth does. Plan 02 "Decay" schedules reviews from the FSRS-7 retrievability curve against a desired retention of 0.90, raised to 0.95 from 2027-03-15. A review is due when retrievability is below that line, block 1 of "Session assembly" serves up to 5 items or 5 forecast minutes of them, and same-day repeats do not grow stability. Hypercorrection requeues bypass the schedule at one day. Plan 02 states that no validation of FSRS, SM-2 or HLR on procedural mathematics was found.

(c) What Growth does not do. The due test, `due_coverage`, counts only skills the engine has declared mastered, and mastery needs three unaided successes on three days over at least seven days. Every scheduler above starts spacing at the first successful retrieval, SM-2 at a 1 day interval, Leitner at box one, MEMORIZE and HLR over every item seen, and Lyle et al over every learning objective. Growth's schedule therefore starts weeks after the learning it is meant to consolidate, which is the mechanism behind the 1.1 and 7.5 percent figures. Block 3 does admit a skill after one unaided success (RETRIEVAL_ENTRY = 1), but it draws from that pool by interleaving constraints, not by predicted forgetting. The evidence on procedural mathematics is a spacing benefit of small to moderate size (g = 0.28) that appears at delays of weeks, so a schedule tested only at 60 days with 1-day delayed measures cannot show it.

## 2. Retrieval practice and desirable difficulties [uncertain]

(a) The literature. Roediger and Karpicke 2006 found 61 against 40 percent recall at one week for tested against restudied passages and no advantage at five minutes. Adesope, Trevisan and Sundararajan 2017 pooled 272 effects from 188 experiments at g = 0.51. Bjork's desirable-difficulties framing (Bjork 1994, Bjork and Bjork 2011) attributes both effects to conditions that slow acquisition and improve retention. No effect size was retrieved for it.

Mathematics is where the effect is least secure. Murray et al 2025 report g = 0.18 for testing against restudy in mathematics, with a confidence interval crossing zero, and conclude the literature does not support a consistent retrieval effect there, possibly because few studies exist. Yeo and Fazio 2019 (Journal of Educational Psychology 111(1), 73 to 90) split the answer by goal. Repeated study of worked examples was more efficient than repeated testing for learning a mathematical procedure when tested after five minutes. After one week repeated testing was ahead. On one-week tests with new problems, non-identical problem scenarios favoured worked examples and identical scenarios favoured problem solving. Their n and effect sizes were not retrieved.

(b) What Growth does. Plan 01 "Practice testing over restudy" keeps generation as the response format and admits a skill to retrieval after one unaided success. Plan 02 serves a first attempt at the example stage for a low-knowledge skill and moves to unsupported after two consecutive credited successes, so the first exposure is a worked example and later exposures are retrieval.

(c) What Growth does not do. It does not separate a repeated identical problem from a new instance of the same skill, the distinction that flipped Yeo and Fazio's result. Plan 04 variants are new instances, which suits the transfer half of their finding. The weak mathematics effect means Growth should not assume a 0.5 standard deviation gain from retrieval and, more to the point, cannot lean on retrieval alone to explain why a review block is worth its minutes.

## 3. Interleaving and blocking [verified]

(a) The literature. Rohrer and Taylor 2007 (Instructional Science 35) taught college students the volumes of four solids and found a one-week test advantage for mixed over blocked practice, d = 1.34, with a reported 63 against 20 percent.

Rohrer, Dedrick and Stershic 2015 (Journal of Educational Psychology, 126 seventh graders, three months of assignments) reported d = 0.42 on a test the next day and d = 0.79 at 30 days, and the design met What Works Clearinghouse standards. Rohrer et al 2020 (787 students, 54 classes) reported d = 0.83 at one month.

Brunmair and Richter 2019 pooled 59 studies and 238 effects at g = 0.42, with g = 0.34 for mathematics tasks, wide heterogeneity, and a positive moderator for similarity between categories and a negative one for similarity within a category.

The mechanism most cited is discriminative contrast, that mixing forces the learner to pick a strategy before executing it. Foster, Mueller, Was, Rawson and Dunlosky 2019 (Memory and Cognition 47(6)) tested how much of the effect comes from contrast and how much from the spacing that interleaving incidentally adds. Their result was not retrieved.

Mixed practice costs performance during practice, since blocked students know the strategy before they read the problem (Rohrer et al 2015). The evidence for blocking helping novices is indirect. I found no study that isolates a novice-only benefit of a blocked first pass, and plan 01 states the first blocked exposure as a design choice.

(b) What Growth does. Plan 01 "Interleaving" and plan 02's `filter_interleaving` cap consecutive same-primary-skill items at two, require at least four skills and two units per ten items, and fix a minimum share of translation items. Block 3 of session assembly is the mixed-review pool. Plan 15 T5 serves a decision lesson when method-selection accuracy drops below execution accuracy.

(c) What Growth does not do. Interleaving in Growth is a constraint on order, not a choice of which confusable skills to mix. Brunmair and Richter's similarity moderator says the gain lies in mixing skills that look alike and need different procedures, and a random draw within the fringe mixes mostly unlike skills. Plan 02's `pending_probes` is the only mechanism that pairs confusable items on purpose. The random tie-break that dominates two-term selection already supplies mixing, which is one reason the study found it hard to separate two-term from random.

## 4. Expertise reversal and fading [single-source]

(a) The literature. Kalyuga, Ayres, Chandler and Sweller 2003 (Educational Psychologist 38, 23 to 31) report that instructional aids that help novices become redundant and then harmful as knowledge grows, so learners with more prior knowledge do better without worked steps. Renkl and Atkinson's backward fading, cited in plan 02, removes the last step first. Salden, Aleven, Renkl and Schwonke 2009 (Topics in Cognitive Science 1) compared a plain Cognitive Tutor with fixed and adaptive fading of worked examples in one lab and one classroom experiment, and report that adaptive fading was useful in both. Effect sizes were not retrieved. Barbieri et al 2023 gives g = 0.48 for worked examples generally (from learning-science.md). No source retrieved gives a switching threshold for when to fade.

(b) What Growth does. Plan 02 "Fading ladder" moves example, completion and unsupported on two consecutive credited successes and drops on two failures, with an example skip when every hard prerequisite is mastered and the first attempt succeeds. The initial stage comes from `p_A_knowledge` bands at 0.50 and 0.90 for a skill with no credited attempt.

(c) What Growth does not do. Both thresholds are inferred and have no source. The selection study found that `lambda` under two-term changes only the fading stage, and that arm 6 differed from two-term on 75 to 82 of 200 students yet beat it on at most 3.5 percent. That is consistent with fading stage being the one selection lever Growth pulls, with no evidence of its optimal setting. A fading ladder driven by two consecutive events is also noisy, since two consecutive successes occur by chance often at a success rate of 0.8.

## 5. Knowledge tracing [verified]

(a) The literature. Bayesian knowledge tracing has a binary latent state with four parameters per skill and no forgetting. Performance factors analysis (Pavlik, Cen and Koedinger 2009) is a logistic model on counts of prior successes and failures. Deep knowledge tracing (Piech et al 2015) uses a recurrent network. Gervet, Koedinger, Schneider and Mitchell 2020 (Journal of Educational Data Mining 12(3), nine datasets) found logistic regression with the right features led on moderate-sized datasets and on datasets with many interactions per student, deep knowledge tracing led on large datasets or where precise timing mattered, and Bayesian knowledge tracing trailed.

Mandalapu, Gong and Chen 2021 reached the same conclusion on EdNet, the largest public set, where feature-engineered logistic regression beat the deep models. The pyKT benchmark (Liu et al 2022, NeurIPS, 7 datasets, 10 models) reports that the gain of many deep models over the original DKT is minimal, and simpleKT (ICLR 2023) beats many deep models by modelling question-level differences.

For 2024 to 2026 the retrieved items are LLM-based or foundation-model trackers, CIKT (arXiv 2505.17705), an LLM dual-channel difficulty model (arXiv 2502.19915), ConceptKT for concept-level deficiency (arXiv 2603.24073) and Live Knowledge Tracing with tabular foundation models (arXiv 2602.06542, revised April 2026), whose abstract claims competitive prediction with up to 53 times faster runs by in-context learning. I read only the last abstract in full. The others come from search summaries, and the field's headline results are prediction accuracy on logged data, which is not the same as improved learning.

(b) What Growth does. Plan 02 "The strength formula" is PFA with log-rescaled counts, the Best-LR form from Gervet et al, with `alpha` dropped because one learner makes it unidentifiable, with credit weights by diagnosed state, fractional prerequisite propagation (0.3 at one hop, 0.09 at two) from Math Academy's FIRe, and FSRS retrievability kept outside the strength. It carries a per-skill state machine for mastery, un-mastery and fading.

(c) What Growth does not do. Its parameters are all inferred and nothing has been fitted, because there is no multi-learner data before phase P8. With one learner the deep-versus-logistic question is moot, and the Gervet finding supports the choice of the logistic family at Growth's scale. The gap is that PFA carries no time term, which is why forgetting was bolted on through FSRS and then disabled (`lambda` 0). No retrieved paper shows a knowledge tracer improving a learning outcome when used to choose the next item, so the pairing of a good predictor with a good selector remains untested, and the selection study is the only test Growth has.

## 6. Item response theory and Elo for difficulty [verified]

(a) The literature.

Pelanek 2016 (Computers and Education 98, 169 to 179) describes Elo as a robust online estimator of student ability and item difficulty, gives an uncertainty function U(n) = a / (1 + b n) with a = 1 and b = 0.05 as a starting point, and shows in a geography-facts system that at least 100 students are needed for good item-difficulty estimates. He describes incorporating response time in the update, as in the Math Garden high-speed, high-stakes rule, and warns that adaptive selection biases item estimates, since the items a student sees depend on the estimate. A new item is added by setting its rating to 0 and letting the data move it.

Wauters, Desmet and Van den Noortgate 2012 (Computers and Education 58(4), 1183 to 1193) compared six ways to estimate difficulty against IRT calibration on 318 Flemish students and roughly twenty items. Proportion correct had the strongest relation to IRT difficulty, then learner feedback, then Elo, then expert rating. IRT, proportion correct and Elo were reliable at 200 to 250 learners, and the cheaper methods were suggested as priors for adaptive sequencing before IRT is reliable. The two floors, 100 students for Elo on facts and 200 to 250 for IRT-quality estimates on items, agree in order of magnitude and come from different domains.

(b) What Growth does. Plan 02 "Calibration plan for item difficulty" fixes item `beta` from the count of BC-DF difficulty factors plus a 0.4 logit shift for each variant direction and freezes ratings (Elo with the item K at 0) until 100 learners exist in phase P8, then runs item-side Elo from the declared `beta` and compares learned against declared difficulty. It monitors drift by first-attempt accuracy against the model's raw probability and by the held-out diagnostic item, and it notes a facility spread above 0.15 within template families.

(c) What Growth does not do. It has no response-time term in difficulty, although Pelanek and Papousek treat time as informative, and plan 02 rules speeded rehearsal out of the mastery update on other grounds. It has no rule for the intermediate stage between zero data and 100 learners, where Wauters suggests proportion correct as a prior. With a single learner every item's data is confounded with the selection policy, which Pelanek's simulation shows, so the two-term policy's near-randomness is useful for calibration. The 100-student floor is a lower bound taken from a facts domain, and the 200 to 250 figure is nearer the multi-step calculus case.

## 7. Mastery criteria and the cost of overpractice [single-source]

(a) The literature. Corbett and Anderson's 0.95 threshold is the Cognitive Tutor convention, described by Pavlik et al as current practice. Cen, Koedinger and Junker 2007 (AIED) used Learning Factors Analysis on the Cognitive Tutor geometry curriculum to find over-practiced and under-practiced skills. A 2025 paper citing them (arXiv 2506.17577) reports that about 33 percent of practice attempts occurred after mastery and produced no significant posttest gain. That figure is second-hand, so the section is single-source. Kaeser, Klingler and Gross 2016 (LAK, 289 to 298) propose a when-to-stop policy that needs only the model's probability that the next item is correct, and that can represent forgetting and detect wheel spinning. Its numbers were not retrieved. ALEKS separates learned, meaning practised in Learning Mode, from mastered, meaning confirmed later in a Knowledge Check, so retention is the criterion for mastery.

Rohrer and Taylor 2006 supply a matching result from a single session. Nine problems produced no more retention than three at one week or four.

Kulik, Kulik and Bangert-Drowns 1990 and Kulik and Fletcher 2016 (learning-science.md) put mastery learning effects at 0.4 to 0.6 and a median of 0.66 for tutors, both shrinking on standardized tests.

(b) What Growth does. Plan 02 "Mastery declaration and un-mastery" uses `sigmoid(m_k) >= 0.9`, three unaided successes, two archetypes where the library allows, three days, a seven-day span and retrievability at or above the desired retention. It cites the 0.95 convention and declines it, and it does not count same-day repeats.

(c) What Growth does not do. Its criterion is stricter in evidence per skill than the tutors it cites, which lengthens time on a skill exactly where Cen's over-practice figure applies. The mastery count, 13.6 skills per student at 60 days and 32.2 at 226, shows how slowly the criterion is met, and slow mastery is what starves due coverage. Nothing retrieved says three successes on three days is right for calculus, and the ALEKS learned and mastered split is a design Growth's un-mastery rule approximates without a separate confirmation event.

## 8. Difficulty targeting [uncertain]

(a) The literature. Wilson, Shenhav, Straccia and Cohen 2019 (Nature Communications 10, 4646) derive an optimal training error of 15.87 percent under Gaussian noise, 18.39 percent under Laplacian and 25 percent under Cauchy noise. The derivation covers stochastic-gradient-descent learners on binary classification with one-dimensional difficulty, and the paper says extensions to multi-category tasks are open and that human evidence is limited. Verified in simulations of perceptrons, a network on MNIST and a model of primate perceptual learning. A 2026 Scientific Reports paper titled "Enforcing a high success percentage interferes with reward-based motor learning" was found by title only and not read. Math Academy raises or lowers quiz variant difficulty around an 80 percent score and cites Rosenshine's roughly 80 percent success in effective classrooms, both vendor or secondary statements. The zone of proximal development is a qualitative claim, and Wilson et al present their result as a formalisation of that intuition, not a test of it.

Guessing changes the arithmetic. Under the plan's four-option model, knowledge probability is (raw minus 0.25) over 0.75, so an 85 percent raw target on a four-option item is an 80 percent knowledge target, and a 0.5 knowledge target is 0.625 raw.

(b) What Growth does. Plan 02 sets `TARGET_LEARN` at 0.80 on the knowledge scale and applies it as a stage filter, not a score term. The two-term score does not target difficulty at all. Plan 02 "Guessing correction" converts targets for MCQ. Plan 01 "Session shape" states a 60 to 85 percent first-attempt band with no source.

(c) What Growth does not do. It does not steer item difficulty toward any success rate at learning time, and the study's five-term score, the only place a target enters the choice, lost to two-term on the mean at 60 days. The retrieved evidence does not say that difficulty targeting should have won. The 85 percent rule is derived for a different learner class, and the human data are thin, so its failure to help in the simulator is neither surprising nor informative about students. Where Growth can act is the fading stage, and the honest reading is that no source ties a particular stage rule to a success rate.

## 9. Feedback timing and elaborated feedback [verified]

(a) The literature. Kulik and Kulik 1988 (Review of Educational Research 58(1), 53 studies) found that applied studies with real classroom quizzes favoured immediate feedback, while experimental studies of acquisition of test content found the opposite.

Shute 2008 concludes that elaborated feedback beats verification-only, and that timing results are inconsistent, with immediate suiting procedural acquisition and delay suiting transfer (no effect size retrieved). Bangert-Drowns et al 1991 found feedback helps when it supplies information the learner cannot already anticipate. Wisniewski, Zierer and Hattie 2020 pooled 435 studies and 994 effects at d = 0.48, larger for information-rich feedback. Hattie and Timperley 2007 report an average near 0.79 across syntheses with wide variance and no benefit from feedback directed at the self.

In mathematics, Fyfe, Rittle-Johnson and DeCaro 2012 (Journal of Educational Psychology 104(4), 1094 to 1108) gave second and third graders 12 novel equivalence problems with no, outcome or strategy feedback. Feedback helped children with little prior knowledge of a correct strategy and did not help those with some. A classroom study from the same group (SREE 2015) found children who already had instruction learned more from practice without feedback than with it. A meta-analytic review (Fyfe and Brown 2018, Thinking and Reasoning 24(2)) exists and its effect sizes were not retrieved. Prior knowledge is the recurring moderator, the same variable as in expertise reversal.

(b) What Growth does. Plan 03 "Feedback policy" gives immediate step-level feedback at the example and completion stages and none until submission at the unsupported stage and on exam-shaped items. Feedback names the violated rule, the scoring consequence and the correct step, is written from deterministic selections, requeues the corrected item at 1 to 2 days, and never states a misconception as established.

(c) What Growth does not do. The split by stage is the right structure by Shute and Fyfe, but its switch, two consecutive successes, is not the prior-knowledge measure Fyfe used. A student with strong prior knowledge who lands at the example stage gets step feedback that the Fyfe classroom study found harmful. The skip rule (every prerequisite mastered and a first success) is the only guard. Nothing measures the effect of feedback on the next attempt, and the requeue gap, one to two days, is unsourced beyond Cepeda's lower bound.

## 10. Hypercorrection and error-driven learning [single-source]

(a) The literature. Butterfield and Metcalfe 2001 found that errors made with high confidence are corrected more often than low-confidence errors.

Metcalfe 2017 (Annual Review of Psychology 68, 465 to 489) reviews the effect and reports that it holds at immediate and delayed retests, that learning from an error grows when the learner processes the correct answer with an explanation, and that in Butler, Fazio and Marsh 2011 the effect persisted over a week while high-confidence errors tended to return.

Kornell, Hays and Bjork 2009 (JEP: LMC, six experiments) found that an unsuccessful retrieval attempt before the answer enhanced later learning against reading question and answer together. Effect sizes were not retrieved for any of these. The samples are general-knowledge trivia and word pairs.

(b) What Growth does. Plan 02 "Hypercorrection flag" sets `hypercorrection_due` to tomorrow after a credited failure rated confident, overrides the FSRS date, and serves it in block 1. Plan 01 rates confidence on a three-point scale. Plan 15 R35 records the productive-failure opener as unwired.

(c) What Growth does not do. The retrieved literature is about facts. Hypercorrection has not been shown for multi-step calculus procedures, where a confident wrong answer may be a slip in a step and not a belief. Growth's rule pulls the review to one day and does nothing else with the confidence signal, for instance in choosing between a re-attempt and a contrast pair. The one-day gap is the floor of Cepeda's ridgeline and the retrieved review says errors of this kind can return within a week, so a single early requeue may not be enough.

## 11. Choice and autonomy in practice [verified]

(a) The literature. Karpicke 2009 (JEP: General, four experiments) had learners study foreign-language items under assigned repeated testing, repeated study or removal after recall, and under self-control. Given control, many learners removed items instead of practising retrieval, and their retention was poor. Kornell and Bjork 2008 (Memory 16, 125 to 136, four experiments) studied dropping flashcards and found small but consistently negative effects on learning, because dropping rests on inaccurate monitoring and on the value students assign to more study. Kornell and Bjork 2007 (Psychonomic Bulletin and Review) frame the perils of self-regulated study as depending on monitoring accuracy and a realistic model of learning. A second Kornell and Bjork 2008 paper on learning concepts and categories (Psychological Science) turned up in the search and was not read. Effect sizes were not retrieved for any of these.

Choice and motivation pull the other way. SDT treats autonomy as a need whose support raises intrinsic motivation (Ryan and Deci 2000), and a badge-choice study cited in Sailer 2017 found that choice fulfils the autonomy need. I found no study of letting a learner choose the next problem in a mathematics tutor and measuring learning.

(b) What Growth does. Plan 02 selects the next item, and the student does not choose. The student authors an error note and rates confidence, and plan 08 shows progress as a fading map.

(c) What Growth does not do. It offers no choice at all within a session, which matches the evidence that unaided choice degrades retrieval scheduling. The evidence supports control of the schedule by the system and does not say anything against choice within a scheduled set, for instance of order among due items or of which of two equally due skills to work, where autonomy support is cheap and the harm found by Karpicke and Kornell (dropping items) cannot occur.

## 12. Session length and volume [uncertain]

(a) The literature. Baddeley and Longman 1978 (Ergonomics) found that one hour a day beat two hours a day and twice-daily schedules per hour of practice, so the most distributed schedule was the most efficient per hour. Cepeda et al 2006 (254 studies, over 14,000 participants) is the distributed-practice meta-analysis. Neither addresses session length for mathematics, and plan 01 states that no optimal session length for mathematics was found. I found none either.

The volume evidence is observational. College Board and Khan Academy's 2017 study of about 250,000 students reported a 90-point rise from PSAT/NMSQT to last SAT, of which 30 points were attributed to six to eight hours on Official SAT Practice, and 20 hours were linked to a 115-point average gain.

The 2019-cohort technical report (over half a million students) reports 21 additional points at six or more hours on the first SAT and 39 when a best-practice behaviour was present, those behaviours being levelling up skills, taking a full-length practice test and following personalised recommendations. About 8 percent of students combined six hours with a best practice. The report says its design cannot control self-selection.

Khan's MAP Accelerator results (over 180,000 students, 649 schools) associate 30 minutes a week with 0.26 standard deviations of extra growth against under 15 minutes, again observational. Koedinger et al 2015 (learning-science.md) find doing predicts learning far more than watching, correlationally. For AP I found no College Board study relating AP Classroom usage to AP scores, and no study linking practice-item volume to AP Calculus outcomes.

(b) What Growth does. Plan 01 "Session shape" forecasts 40 to 60 minutes, stops when the four blocks are empty and has no daily quota, no item count and no timer. It states that its session numbers are unsourced. It logs accuracy by minute to find the student's own fatigue point.

(c) What Growth does not do. It has no volume target because none is supported, and the closest evidence says quality-of-practice behaviours (recommendation following, full practice tests, levelling up) carried a larger association than raw hours. The design fits that reading, since the queue is set by need and not by time. The retrieved volume studies are SAT and grade school MAP, not AP, and none is causal.

## 13. Motivation without gamification [uncertain]

(a) The literature. Self-determination theory (Deci and Ryan 1985, Ryan and Deci 2000) names autonomy, competence and relatedness as needs whose support raises intrinsic motivation. Deci, Koestner and Ryan 1999 (Psychological Bulletin, 128 studies) found expected tangible rewards undermined free-choice intrinsic motivation, with d = -0.40 for engagement-contingent, -0.36 for completion-contingent and -0.28 for performance-contingent rewards, and a comment in the same issue disputes the meta-analysis's use.

Hanus and Fox 2015 ran a 16-week study of two courses and found that the class with a badge and leaderboard scheme reported lower motivation, satisfaction and empowerment and scored lower on the final exam. Sailer et al 2017 found the opposite direction for competence, with badges, leaderboards and performance graphs raising competence satisfaction.

A 2024 meta-analysis (Educational Technology Research and Development) reports that gamification raises intrinsic motivation, autonomy and relatedness with minimal effect on competency. The Duolingo streak figure (14 percent at day 14, plan 01) is company-reported engagement and not learning. Nothing retrieved tests a queue-completion streak, so the evidence for framing a day as an emptied due queue is an extrapolation from the completion-contingent d = -0.36, which is on tangible rewards and not on a symbolic marker.

(b) What Growth does. Plan 01 "Implementation intention and queue-bound streak" defines the streak unit as a completed due queue, never minutes or session length, awards nothing for volume, allows freeze days, and states that the streak must never enter the mastery model.

(c) What Growth does not do. The design avoids paying for volume, which is where the undermining result sits, but the gamification literature is split and none of it measures learning in calculus. The claim that a queue-bound streak avoids the harm is inferred. One interaction bears on selection. Because the streak unit is an emptied due queue and the selection study shows the due test rarely fires, the streak as designed would often close on very little practice. That reading is inferred and no source tests it.

## What bears on the selection study [inferred]

The retrieved sources and the study fit together in a specific way. Two-term selection is near random because its one informative signal, due coverage, needs a mastered skill, and every scheduler above begins spacing at the first success. The forgetting oracle wins on delayed retention because it reviews the skill the student has most nearly forgotten, which is the MEMORIZE result and the FSRS premise, and it wins by more at 30 days than at one because Cepeda's gap ratio and Rohrer and Taylor's one-week null both say the benefit appears only after a delay.

The simulator's negative control scoring within 7 points of the oracle is what the real literature would predict of a world where half-life growth ignores lag, because in that world spacing has no effect to find. The real effect is smaller than the oracle's 91.0 percent suggests. Spacing in mathematics is g = 0.28 and retrieval g = 0.18 with an interval spanning zero (Murray et al 2025), and the 90 percent per-student bar asks for a share that even a real effect of that size would not give. The ruling that reads the paired mean difference with its interval is consistent with that.

Two design points follow from the evidence and are inferences, not findings. A due test that admits any skill after one unaided success, ranked by predicted retrievability, would make the schedule the literature describes fire on far more than 1.1 or 7.5 percent of choices. A world in which stability gain grows with lag would be the test that could tell that schedule from a bad one, and the 60-day horizon with day-after measurement is shorter than the gaps Cepeda's ridgeline puts at 20 percent of the retention interval. Nothing here has been run, and the simulator's invented world model remains the limit on every simulated number.

## Sources [verified]

All URLs accessed 2026-09-29. Items marked search-only were confirmed through a search summary, the page itself having refused the fetch.

- https://super-memory.com/english/ol/sm2.htm, SM-2 (search summary).
- https://en.wikipedia.org/wiki/Leitner_system, Leitner 1972 (search summary).
- https://research.duolingo.com/papers/settles.acl16.pdf, Settles and Meeder 2016 (search summary).
- https://journals.sagepub.com/doi/abs/10.1177/0956797613504302, Lindsey et al 2014 (search-only).
- https://github.com/open-spaced-repetition/srs-benchmark, README tables read directly.
- https://expertium.github.io/Benchmark.html, older SM-2 figures, read directly, chart-derived.
- https://dl.acm.org/doi/10.1145/3534678.3539081, Ye, Su and Cao 2022, from learning-science.md.
- https://www.pnas.org/doi/abs/10.1073/pnas.1815156116, Tabibian et al 2019 (fetch refused 403, search-only).
- https://laplab.ucsd.edu/articles/Cepeda%20et%20al%202008_psychsci.pdf, Cepeda 2008 (search summary this session).
- https://onlinelibrary.wiley.com/doi/10.1002/acp.1266, Rohrer and Taylor 2006 (search summary).
- https://link.springer.com/article/10.1007/s10648-015-9349-8, Hopkins et al 2016 (search-only).
- https://link.springer.com/article/10.1007/s10648-019-09489-x, Lyle et al 2020 (search-only).
- https://link.springer.com/article/10.1007/s10648-022-09677-2, Lyle et al 2022 (search-only).
- https://link.springer.com/article/10.1007/s10648-025-10035-1, Murray, Horner and Goebel 2025 (search-only).
- https://andymatuschak.org/files/papers/Yeo,%20Fazio%20-%202019%20-%20The%20optimal%20learning%20strategy%20depends%20on%20learning%20goals%20and%20processes2.pdf, Yeo and Fazio 2019 (search summary).
- https://journals.sagepub.com/doi/10.1111/j.1467-9280.2006.01693.x and https://journals.sagepub.com/doi/abs/10.3102/0034654316689306, from learning-science.md.
- https://link.springer.com/article/10.1007/s11251-007-9015-8, Rohrer and Taylor 2007 (d = 1.34 read in the 2015 paper, percentages search-only).
- https://files.eric.ed.gov/fulltext/ED557355.pdf, Rohrer, Dedrick and Stershic 2015, read directly.
- http://uweb.cas.usf.edu/~drohrer/pdfs/Rohrer_et_al_2020JEdPsych.pdf, Rohrer 2020, from learning-science.md.
- https://link.springer.com/article/10.3758/s13421-019-00918-4, Foster et al 2019 (title and venue only).
- https://www.psychologie.uni-wuerzburg.de/fileadmin/06020400/2019/Brunmair_Richter_in_press__2019_META-ANALYSIS_OF_INTERLEAVED_LEARNING.pdf, Brunmair and Richter 2019 (search summary).
- https://www.tandfonline.com/doi/abs/10.1207/S15326985EP3801_4, Kalyuga et al 2003 (search summary).
- https://onlinelibrary.wiley.com/doi/10.1111/j.1756-8765.2008.01011.x, Salden et al 2009 (search summary).
- https://eric.ed.gov/?id=EJ1273917, Gervet et al 2020, abstract read directly.
- https://arxiv.org/pdf/2101.08349, Mandalapu et al 2021, abstract read directly.
- https://arxiv.org/abs/2206.11460 and https://arxiv.org/abs/2302.06881, pyKT and simpleKT (search summaries).
- https://arxiv.org/pdf/2602.06542, Live Knowledge Tracing, abstract read directly.
- https://arxiv.org/pdf/2505.17705, https://arxiv.org/pdf/2502.19915 and https://arxiv.org/pdf/2603.24073, LLM-based tracing (search summaries only).
- https://www.fi.muni.cz/~xpelanek/publications/CAE-elo.pdf, Pelanek 2016, read directly.
- https://kulak.kuleuven.be/~u0006844/publications/2012,%20Wauters,%20Item%20difficulty%20estimation,%20Computers%20and%20Education.pdf, Wauters et al 2012, read directly.
- https://arxiv.org/pdf/2506.17577, Cen et al 2007 as cited (second-hand).
- https://dl.acm.org/doi/abs/10.1145/3079628.3079667 and the Kaeser et al 2016 LAK record (search summary only).
- https://jmatayoshi.github.io/publications/JMP2021_KST_ALEKS_preprint.pdf, ALEKS retention study, from plan 02, learned and mastered from docs/pedagogy/products/aleks.md.
- https://pmc.ncbi.nlm.nih.gov/articles/PMC6831579/, Wilson et al 2019, read directly.
- https://www.nature.com/articles/s41598-026-39639-5, 2026 motor learning paper (title only, fetch refused).
- https://www.mathacademy.com/how-our-ai-works, Math Academy 80 percent (search summary).
- https://journals.sagepub.com/doi/10.3102/00346543058001079, Kulik and Kulik 1988 (search summary).
- https://eric.ed.gov/?id=EJ994029, Fyfe et al 2012 (search summary). https://eric.ed.gov/?id=ED562489, Fyfe SREE 2015. https://doi.org/10.1080/13546783.2017.1359208, Fyfe and Brown 2018 (existence only).
- https://www.annualreviews.org/content/journals/10.1146/annurev-psych-010416-044022, Metcalfe 2017 (search summary).
- https://web.williams.edu/Psychology/Faculty/Kornell/Publications/Kornell.Hays.Bjork.2009.pdf, Kornell et al 2009 (search summary).
- https://learninglab.psych.purdue.edu/downloads/2009/2009_Karpicke_JEPGeneral.pdf, Karpicke 2009 (search summary).
- https://www.tandfonline.com/doi/abs/10.1080/09658210701763899, Kornell and Bjork 2008 (search summary).
- https://research.collegeboard.org/media/pdf/osp-technical-report.pdf, Official SAT Practice report, read directly.
- https://newsroom.collegeboard.org/new-data-links-20-hours-personalized-official-sat-practice-khan-academy-115-point-average-score, 2017 SAT result (search summary).
- https://blog.khanacademy.org/khan-academy-efficacy-results-november-2024/, MAP Accelerator results (search summary).
- https://pubmed.ncbi.nlm.nih.gov/10589297/, Deci, Koestner and Ryan 1999 (search summary).
- https://link.springer.com/article/10.1007/s11423-023-10337-7, gamification meta-analysis (search summary).
- https://www.researchgate.net/publication/265644737, Hanus and Fox 2015 (search summary).
