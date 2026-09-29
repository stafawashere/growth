---
title: Learning science behind the lesson framework
research_date: 2026-09-29
status: draft
purpose: The evidence base for the lesson-framework redesign, one section per instructional mechanism, adding what plan 01 and plan 15 do not already record.
---

# Learning science behind the lesson framework

Plan 01 (docs/plan/01-learning-model.md) already records evidence with URLs and tags for interleaving, spacing, retrieval, mastery, fading, feedback, hypercorrection, self-explanation, split attention and productive failure. This file cites those sections by name and adds sources they lack. An effect size appears only where a fetched page or search summary carried it, otherwise the text says "effect size not retrieved". Pages behind a publisher block were confirmed through search summaries and the tag says so.

## 1. Worked examples and fading [verified]

Studying a solved problem loads working memory with schema construction instead of means-ends search, so novices learn a procedure faster than by solving the same problems. The benefit reverses as knowledge grows (expertise reversal), which is why the support has to fade, and fade backward so the learner meets the last step first.

- Sweller and Cooper 1985, Cognition and Instruction 2(1). Learners given problems to solve took almost six times longer on the learning sequence and made more errors than learners given examples. Figure from a secondary summary, so [single-source]. https://www.tandfonline.com/doi/abs/10.1207/s1532690xci0201_3 (accessed 2026-09-29)
- Atkinson, Derry, Renkl and Wortham 2000, Review of Educational Research 70(2). A review deriving design principles, among them several examples per problem type, varied formats and labelled conceptual structure. Effect size not retrieved. [single-source] https://journals.sagepub.com/doi/10.3102/00346543070002181 (accessed 2026-09-29)
- Barbieri, Miller-Cotto, Clerjuste and Chawla 2023, Educational Psychology Review 35. 43 articles, 55 studies, 181 effect sizes, mean g = 0.48 for worked examples on mathematics performance, from elementary school to adults. [verified against the ERIC and Springer records] https://link.springer.com/article/10.1007/s10648-023-09745-1 (accessed 2026-09-29)
- Renkl, Atkinson, Maier and Staley 2002, Salden et al, Kalyuga et al 2003 (fading, adaptive fading, expertise reversal) are in plan 01 "Adaptive worked-example fading", all [single-source]. No source gives a switching threshold.

Plan 01 cites a 2023 Educational Psychology paper (doi 10.1080/01443410.2023.2273762) as a review reporting inflated worked-example effects at f = 0.25. The publisher page returned HTTP 403 and search identifies that DOI as Chen, Retnowati, Chan and Kalyuga, "The effect of worked examples on learning solution steps and knowledge transfer", which reads as a single study. The inflation claim is therefore [uncertain] and should be re-read before anyone leans on f = 0.25. Barbieri 2023 reports its moderators (incorrect examples, self-explanation prompts, timing) but its abstract did not state an inflation correction. Boundary conditions are the novice restriction, near-zero or negative benefit for learners who already solve the problem, and no evidence on delayed AP-style transfer.

What Growth already does: plan 01 "Adaptive worked-example fading" runs the example, completion and unsupported ladder on a per-skill estimate, and plan 15 "What a lesson is" builds check 1 as the completion form of worked example 1 and drops the lesson for the high knowledge band.

## 2. Interleaving [verified]

Mixing problem types forces the learner to choose a strategy before executing it, which blocked practice removes. The gain is in discrimination, so it is large for confusable procedures and small where nothing needs telling apart.

- Rohrer, Dedrick, Hartwig and Cheung 2020: 787 students, 54 classes, d = 0.83 at one month. [verified] http://uweb.cas.usf.edu/~drohrer/pdfs/Rohrer_et_al_2020JEdPsych.pdf (accessed 2026-09-29)
- Brunmair and Richter 2019: 59 studies, 238 effect sizes, g = 0.42, near zero for expository text. [verified] https://pubmed.ncbi.nlm.nih.gov/31556629/ (accessed 2026-09-29)

Both are taken from plan 01 "Interleaving" and were not re-fetched, because plan 15 states the lesson layer leaves interleaving untouched. Boundary conditions are the first blocked exposure (a novice needs a blocked pass first), the unmeasured cost to felt fluency, and materials where the categories are already distinct.

What Growth already does: plan 01 "Interleaving" sets hard set constraints of at most two consecutive same-skill items and four skills per block of ten, and plan 15 "Re-teaching" trigger T5 serves a decision lesson when method-selection accuracy drops below execution accuracy.

## 3. Retrieval practice [verified]

Reconstructing an answer from memory strengthens and reorganises the trace more than seeing it again. The benefit needs a delay before the test, because immediate massed retrieval leaves the answer in working memory.

- Adesope, Trevisan and Sundararajan 2017: 188 experiments, 272 effects, g = 0.51 against restudy. [verified] https://journals.sagepub.com/doi/abs/10.3102/0034654316689306 (accessed 2026-09-29)
- Rowland 2014: 159 effect sizes, mean g = 0.50, stronger with feedback. In plan 01; the PubMed page was blocked by a cookie wall on this access, so [single-source] here. https://pubmed.ncbi.nlm.nih.gov/25150680/ (accessed 2026-09-29)
- Roediger and Karpicke 2006: 61 against 40 percent at one week, no advantage at five minutes, the massed null. [verified] https://journals.sagepub.com/doi/10.1111/j.1467-9280.2006.01693.x (accessed 2026-09-29)
- Karpicke and Blunt 2011, Science 331(6018). Retrieval practice beat concept mapping on a one-week delayed test, including on inference questions and on a concept-map criterion. Effect size not retrieved. [single-source] https://pubmed.ncbi.nlm.nih.gov/21252317/ (accessed 2026-09-29)

Boundary conditions are the feedback condition (Rowland's larger effect with feedback), the element-interactivity dispute in plan 01 (van Gog and Sweller against Karpicke and Aue), and undergraduate verbal samples rather than calculus.

What Growth already does: plan 01 "Practice testing over restudy" keeps generation as the response format and makes retrieval eligible only after one unaided success, and plan 15 keeps the lesson's checks uncredited because a check seconds after reading is massed retrieval.

## 4. Spacing [verified]

Each successful retrieval after some forgetting raises stability more than one at full recall, so the best gap scales with how long the memory must last.

- Cepeda et al 2008: over 1350 participants, optimal gap about 20 percent of the retention interval at weeks, 5 to 10 percent at a year. [verified] https://laplab.ucsd.edu/articles/Cepeda%20et%20al%202008_psychsci.pdf (accessed 2026-09-29)
- Cepeda et al 2006: 254 studies, over 14,000 participants. [single-source] https://pubmed.ncbi.nlm.nih.gov/16719566/ (accessed 2026-09-29)
- FSRS. Ye, Su and Cao 2022, KDD, fitted a memory model to 220 million MaiMemo review logs and is the origin of FSRS. [single-source] https://dl.acm.org/doi/10.1145/3534678.3539081 (accessed 2026-09-29). The srs-benchmark repository scores predicted recall on roughly 10,000 Anki users and 727 million reviews and states that it measures prediction accuracy only, not learning outcomes. [single-source] https://github.com/open-spaced-repetition/srs-benchmark (accessed 2026-09-29)

The gap is that no source shows FSRS scheduling improves a learning outcome, only that it predicts recall of flashcard-style items well. Boundary conditions are trivia and vocabulary materials, and one small mathematics study (Rohrer and Taylor 2006, plan 01).

What Growth already does: plan 01 "Spaced retrieval scheduled to the exam date" schedules each skill by FSRS retrievability against a retention target, and plan 15 "Re-teaching" fires refreshers on state (T2, retrievability below 0.5) instead of on a timer.

## 5. Self-explanation [verified]

Generating the reason for a step forces integration of the step with prior knowledge and exposes gaps the learner had not noticed.

- Bisra et al 2018: 64 reports, 69 effect sizes, g = 0.55. [verified] https://link.springer.com/article/10.1007/s10648-018-9434-x (accessed 2026-09-29)
- Rittle-Johnson, Loehr and Durkin 2017, ZDM 49, a meta-analysis on mathematics. Prompted self-explanation gave small to moderate gains on procedural knowledge, conceptual knowledge and procedural transfer when tested immediately, but evidence for retention over a delay or for classroom settings was much more limited. Scaffolded explanations did better than open prompts. Effect sizes not retrieved from the summary. [single-source] https://eric.ed.gov/?id=EJ1149060 (accessed 2026-09-29)
- Chi et al 1989 is in plan 01 [single-source].

Boundary conditions are the immediate-test limit, the practice time the prompts consume, and open prompts underperforming scaffolded ones.

What Growth already does: plan 01 "Structured self-explanation" allows exactly one scaffolded prompt per worked example and per corrected error, and plan 15 "What a lesson is" keeps that prompt on the graded item and gives the lesson a 25-word why line per step.

## 6. Cognitive load and split attention [verified]

Working memory holds a few interacting elements at once. Intrinsic load comes from element interactivity, extraneous load from how the material is presented, and forcing the learner to integrate separated sources or process duplicated ones adds extraneous load.

- Schroeder and Cenkci 2018: 58 comparisons, n = 2426, g = 0.63 favouring integrated presentation. [verified] https://link.springer.com/article/10.1007/s10648-018-9435-9 (accessed 2026-09-29)
- Noetel et al 2022, Review of Educational Research 92(3): overview of 29 reviews, 1,189 studies, 78,177 participants, finding significant positive effects for spatial and temporal contiguity, signalling, and verbal redundancy among 11 learning principles. Per-principle values were not in the abstract. [verified] https://eric.ed.gov/?id=EJ1338120 (accessed 2026-09-29)
- Mayer's median effect for redundancy is d = 0.87 (section 7), but the redundancy effect in plan 01 rests on a Wikipedia page and van Gog and Sweller disputes generality as element interactivity rises [single-source].

Boundary conditions are expertise reversal again (integration aids become redundant for experts) and the difficulty of measuring element interactivity independently of difficulty.

What Growth already does: plan 01 "Split-attention-free presentation" requires labels inside figures and one new idea per screen, and plan 15 caps the orientation at 60 words and the lesson at 900 words.

## 7. Dual coding and multimedia principles [verified]

Paivio's dual coding theory holds that verbal and imagistic information are processed in separate systems whose codes reinforce each other, and Clark and Paivio 1991 draw the educational implications. Mayer's principles apply that with a limited-capacity assumption, so a picture helps only when it is integrated and does not add competing text or narration.

- Mayer, median effect sizes as reproduced in a 2017 review summary. Coherence d = 0.70, signalling 0.46, redundancy 0.87, spatial contiguity 0.79, temporal contiguity 1.30, segmenting 0.70, pretraining 0.46, modality 0.72, personalization 0.79. The multimedia principle's own median was not retrieved. [single-source] https://onlinelibrary.wiley.com/doi/abs/10.1111/jcal.12197 (accessed 2026-09-29)
- Noetel et al 2022 (see section 6): the largest benefits were for captioned second-language video, contiguity and signalling, and robust evidence for modality, coherence, segmentation and verbal redundancy. [verified] https://eric.ed.gov/?id=EJ1338120 (accessed 2026-09-29)
- Clark and Paivio 1991. Effect size not retrieved. [single-source] https://link.springer.com/article/10.1007/BF01320076 (accessed 2026-09-29)

Medians from lab studies with short sessions and immediate tests overstate classroom effects, which Noetel's pooled estimates show only as ordering. Modality effects concern narrated animation, and Growth has none.

What Growth already does: plan 01 "Split-attention-free presentation" bans simultaneous duplicate channels and caption-only labels, and plan 15's cue line on each worked-example step is a signalling device. Nothing yet on segmenting or pretraining beyond the section order, and there is no narration policy, so the modality principle is unused.

## 8. Concreteness fading [single-source]

Beginning with a concrete representation anchors meaning, and fading to idealised symbols in stages supports transfer that a concrete-only or abstract-only sequence lacks.

- Fyfe, McNeil, Son and Goldstone 2014, Educational Psychology Review 26, a systematic review of concreteness fading in mathematics and science. It argues for sequencing concrete to abstract over either extreme. Effect size not retrieved. [single-source] https://eric.ed.gov/?id=EJ1036777 (accessed 2026-09-29)
- Goldstone and Son on idealised versus concrete simulations is the source of the fading sequence but was not fetched here, so nothing further is claimed. [uncertain]

Boundary conditions are the small child and college samples, the lack of calculus studies, and Ainsworth's warning in plan 01 that unsupported multiple representations can hurt.

What Growth already does: nothing yet. Plan 15's `representations` block is one static section for the low band, and no lesson moves from a concrete case (a table of velocities) to the symbolic rule in stages.

## 9. Productive failure and error-based learning [verified]

Attempting a problem before instruction activates prior knowledge and reveals the gaps the instruction then fills, and studying wrong solutions does the same for procedures already taught.

- Sinha and Kapur 2021: 53 studies, 166 comparisons, g = 0.36, CI [0.20, 0.51]. [verified] https://journals.sagepub.com/doi/10.3102/00346543211019105 (accessed 2026-09-29)
- Loibl, Roll and Rummel 2017, Educational Psychology Review 29. Problem solving followed by instruction fosters learning only when contrasting cases are used or the instruction builds on the students' own failed solutions. [verified] https://link.springer.com/article/10.1007/s10648-016-9379-x (accessed 2026-09-29)
- Adams et al 2014, Computers in Human Behavior 36. Middle-school decimals, web tutor. No difference on the immediate post-test, better performance for the erroneous-examples group on a test one week later. Sample size not retrieved. [single-source] https://www.learntechlib.org/p/209945/ (accessed 2026-09-29)
- Durkin and Rittle-Johnson 2012, Learning and Instruction 22(3). Grades 4 and 5, decimal magnitude. Comparing incorrect with correct examples beat studying correct examples alone on procedural and conceptual knowledge. [single-source] https://www.sciencedirect.com/science/article/abs/pii/S0959475211000880 (accessed 2026-09-29)

Boundary conditions are conceptual rather than procedural targets, the mandatory comparison step, and the Barbieri 2023 moderator on incorrect examples (section 1), whose direction was not retrieved.

What Growth already does: plan 01 "Productive-failure openers" caps the opener at five conceptual targets and requires the comparison step, though plan 15 records it as not yet wired (R35). Plan 15 `common_errors` shows the wrong step beside the right step, but the student is not asked to find the error.

## 10. Mastery learning [verified]

Holding progression until a criterion is met, with corrective work in between, removes the accumulation of unfilled prerequisites.

- Bloom 1984 and Kulik, Kulik and Bangert-Drowns 1990 are in plan 01 "Mastery gating". The Kulik 1990 synthesis covers 108 evaluations and found larger effects on locally prepared examinations than on nationally standardized tests. [verified] https://journals.sagepub.com/doi/10.3102/00346543060002265 (accessed 2026-09-29)
- Slavin 1987, reported in a secondary summary. Positive effects on criterion-referenced tests and no significant effect on norm-referenced standardized tests. Kulik et al dispute his study selection. [single-source] http://www.edpsycinteractive.org/files/mastlear.html (accessed 2026-09-29)
- Kulik and Fletcher 2016: median 0.66 SD for tutors, smaller on standardized tests. [verified] https://journals.sagepub.com/doi/abs/10.3102/0034654315581420 (accessed 2026-09-29)

The shrinkage is the finding that matters for an AP course, because the criterion is a standardized exam. Guskey's reviews of mastery learning were not fetched, so no Guskey claim is made.

What Growth already does: plan 01 "Mastery gating" requires per-skill evidence before progression, and plan 15 "The better than a school class hypothesis" plans against the six-week released-item checkpoint so local-test inflation is visible.

## 11. Immediate versus delayed feedback [verified]

Feedback changes a learner's knowledge only when it carries information the learner lacked, and its timing interacts with task type and spacing.

- Wisniewski, Zierer and Hattie 2020, Frontiers in Psychology 10: 435 studies, 994 effects, N above 61,000, d = 0.48, with heavy heterogeneity and larger effects for information-rich feedback and for cognitive outcomes than for motivational ones. [verified] via search summary of the article and its index pages https://www.semanticscholar.org/paper/08dba618dd4fe18935409da79873b1149d85f373 (accessed 2026-09-29)
- Shute 2008, Kulik and Kulik 1988, Bangert-Drowns et al 1991 and Hattie and Timperley 2007 are in plan 01 "Feedback timing and elaboration". The timing result is unresolved there and remains so.

Boundary conditions are task complexity, correct-answer feedback given before a commitment, and self-directed feedback, which the plan finds weak.

What Growth already does: plan 01 "Feedback timing and elaboration" gives step-level immediate feedback at example and completion stages, withholds it until submission at the unsupported stage, and requeues each corrected item.

## 12. Hypercorrection [single-source]

Errors made with high confidence are corrected more often than low-confidence errors, apparently because the surprise draws attention to the correction.

- Metcalfe 2017, Annual Review of Psychology 68, 465 to 489. Reviews the effect and adds that learning from an error grows when the learner processes the correct answer together with an explanation. Effect size not retrieved. [single-source] https://www.annualreviews.org/content/journals/10.1146/annurev-psych-010416-044022 (accessed 2026-09-29)
- Butterfield and Metcalfe 2001 is in plan 01 "Confidence rating and hypercorrection routing" [single-source].

Boundary conditions are that the evidence is mostly general-knowledge trivia with short delays, and that the effect needs the corrective feedback to actually arrive.

What Growth already does: plan 01 "Confidence rating and hypercorrection routing" flags a high-confidence error and pulls its requeue to one day. Nothing yet in a lesson, where the confidence rating is not read at all.

## 13. Prediction and activation before instruction [verified]

Answering before being taught, even wrongly, primes the learner to notice the answer and encode it. Predict-observe-explain extends that to phenomena, by committing to a prediction, seeing the result, and reconciling the two.

- Richland, Kornell and Kao 2009, Journal of Experimental Psychology: Applied 15(3). Five experiments. Posttest performance was better after a pretest than after extended study in all of them, counting only items missed on the pretest. Effect size not retrieved. [verified] https://pubmed.ncbi.nlm.nih.gov/19751074/ (accessed 2026-09-29)
- Kornell, Hays and Bjork 2009, Journal of Experimental Psychology: Learning, Memory, and Cognition. Unsuccessful retrieval attempts enhanced later learning, reported via a secondary summary. [single-source] https://www.researchgate.net/publication/26655655_Unsuccessful_Retrieval_Attempts_Enhance_Subsequent_Learning (accessed 2026-09-29)
- Pan and Sana 2021, JEP: Applied 27(2). Five experiments, combined n = 1,573, expository passages. Both pretesting and posttesting beat no test at 5 minutes and 48 hours, with pretesting higher overall. [verified] https://sc-pan.github.io/pdf/PS_2021.pdf (accessed 2026-09-29)
- The Educational Psychology Review paper on prequestioning and pretesting (doi 10.1007/s10648-023-09814-5) redirected to a login page, so its effect sizes and boundary conditions are not retrieved. [uncertain] https://link.springer.com/article/10.1007/s10648-023-09814-5 (accessed 2026-09-29)

Boundary conditions are text passages and word pairs as materials, gains concentrated on the tested items rather than on untested content in the reviews I could not open, and no evidence for multi-step calculus derivations. No predict-observe-explain source was retrieved, so that half of the heading is [inferred].

What Growth already does: nothing yet in the lesson. Plan 15 opens with an orientation block and gives no prediction prompt, and the only pre-instruction attempt is the unwired productive-failure opener.

## 14. Comparison of contrasting cases [verified]

Laying two cases side by side lets the learner see which features matter, so the later explanation attaches to differences the learner has already noticed.

- Schwartz and Bransford 1998, Cognition and Instruction 16(4). Three studies. Students who analysed contrasting cases before a lecture applied the concepts to novel problems better than other conditions, while all conditions did equally well on a fact test. [single-source] https://www.tandfonline.com/doi/abs/10.1207/s1532690xci1604_4 (accessed 2026-09-29)
- Alfieri, Nokes-Malach and Schunn 2013, Educational Psychologist 48(2). 57 experiments, 336 tests. Case comparisons prepared learners for later direct instruction, and prompted and guided comparison gave equivalent effect sizes. Numeric mean not retrieved. [single-source] https://www.tandfonline.com/doi/full/10.1080/00461520.2013.775712 (accessed 2026-09-29)
- Rittle-Johnson and Star 2007, Journal of Educational Psychology. 70 seventh graders solving equations. Comparing methods beat studying methods one at a time on procedural knowledge and flexibility, with comparable conceptual gains. [single-source] https://eric.ed.gov/?id=EJ772031 (accessed 2026-09-29)

The two source families agree that comparison helps and are independent, which supports the section tag. Boundary conditions are prior knowledge (Durkin and Rittle-Johnson's mixed results for novices), and the need for the learner to have enough structure to see the differences.

What Growth already does: plan 15 "What a lesson is" gives each `strategy` block a named rival approach from `wrong_approaches`, and plan 15 "Re-teaching" T5 serves a decision lesson on a confusable set. Both state the rival rather than have the student compare two solved cases.

## 15. Learning by doing versus watching [single-source]

Time spent producing answers predicts learning better than time spent reading or watching, and short videos hold attention better than long ones, although neither result isolates a cause.

- Koedinger et al 2015, Learning at Scale. A psychology MOOC with 18,645 MOOC-only students and 9,075 in a combined course. One standard deviation more doing was associated with more than six times the learning benefit of one more of watching or reading. The analysis is correlational with causal-inference adjustments. [single-source] https://dl.acm.org/doi/10.1145/2724660.2724681 (accessed 2026-09-29)
- Guo, Kim and Rubin 2014, Learning at Scale. 6.9 million video sessions across four edX courses. Shorter videos, with a break near six minutes, and informal tablet-style presentations were watched longer, and engagement was measured by watch time and problem attempts, not learning. [single-source] https://dl.acm.org/doi/10.1145/2556325.2566239 (accessed 2026-09-29)

Boundary conditions are self-selection, a single introductory psychology course, and engagement standing in for learning in the video study.

What Growth already does: plan 01 "Practice testing over restudy" keeps at least 70 percent of session time on attempted problems, and plan 15 caps reading at 6 minutes for the full lesson with graded checks inside it. There is no video.

## Sources [verified]

All URLs accessed 2026-09-29.

- https://link.springer.com/article/10.1007/s10648-023-09745-1, Barbieri 2023 worked-examples meta-analysis.
- https://www.tandfonline.com/doi/abs/10.1207/s1532690xci0201_3, Sweller and Cooper 1985.
- https://journals.sagepub.com/doi/10.3102/00346543070002181, Atkinson et al 2000.
- https://www.tandfonline.com/doi/full/10.1080/01443410.2023.2273762, page blocked, identified only through search.
- http://uweb.cas.usf.edu/~drohrer/pdfs/Rohrer_et_al_2020JEdPsych.pdf, Rohrer 2020, taken from plan 01.
- https://pubmed.ncbi.nlm.nih.gov/31556629/, Brunmair and Richter 2019, taken from plan 01.
- https://journals.sagepub.com/doi/abs/10.3102/0034654316689306, Adesope et al 2017, taken from plan 01.
- https://pubmed.ncbi.nlm.nih.gov/25150680/, Rowland 2014, cookie wall on fetch.
- https://journals.sagepub.com/doi/10.1111/j.1467-9280.2006.01693.x, Roediger and Karpicke 2006.
- https://pubmed.ncbi.nlm.nih.gov/21252317/, Karpicke and Blunt 2011.
- https://laplab.ucsd.edu/articles/Cepeda%20et%20al%202008_psychsci.pdf, Cepeda 2008.
- https://pubmed.ncbi.nlm.nih.gov/16719566/, Cepeda 2006.
- https://dl.acm.org/doi/10.1145/3534678.3539081, Ye, Su and Cao 2022.
- https://github.com/open-spaced-repetition/srs-benchmark, FSRS benchmark, prediction only.
- https://link.springer.com/article/10.1007/s10648-018-9434-x, Bisra et al 2018.
- https://eric.ed.gov/?id=EJ1149060, Rittle-Johnson, Loehr and Durkin 2017.
- https://link.springer.com/article/10.1007/s10648-018-9435-9, Schroeder and Cenkci 2018.
- https://eric.ed.gov/?id=EJ1338120, Noetel et al 2022.
- https://onlinelibrary.wiley.com/doi/abs/10.1111/jcal.12197, Mayer 2017 medians, via search summary.
- https://link.springer.com/article/10.1007/BF01320076, Clark and Paivio 1991.
- https://eric.ed.gov/?id=EJ1036777, Fyfe et al 2014.
- https://journals.sagepub.com/doi/10.3102/00346543211019105, Sinha and Kapur 2021.
- https://link.springer.com/article/10.1007/s10648-016-9379-x, Loibl, Roll and Rummel 2017.
- https://www.learntechlib.org/p/209945/, Adams et al 2014 erroneous examples.
- https://www.sciencedirect.com/science/article/abs/pii/S0959475211000880, Durkin and Rittle-Johnson 2012.
- https://journals.sagepub.com/doi/10.3102/00346543060002265, Kulik et al 1990.
- http://www.edpsycinteractive.org/files/mastlear.html, Slavin 1987 summary.
- https://journals.sagepub.com/doi/abs/10.3102/0034654315581420, Kulik and Fletcher 2016.
- https://www.semanticscholar.org/paper/08dba618dd4fe18935409da79873b1149d85f373, Wisniewski, Zierer and Hattie 2020.
- https://www.annualreviews.org/content/journals/10.1146/annurev-psych-010416-044022, Metcalfe 2017.
- https://pubmed.ncbi.nlm.nih.gov/19751074/, Richland, Kornell and Kao 2009.
- https://www.researchgate.net/publication/26655655_Unsuccessful_Retrieval_Attempts_Enhance_Subsequent_Learning, Kornell, Hays and Bjork 2009.
- https://sc-pan.github.io/pdf/PS_2021.pdf, Pan and Sana 2021.
- https://link.springer.com/article/10.1007/s10648-023-09814-5, prequestioning review, login redirect, not read.
- https://www.tandfonline.com/doi/abs/10.1207/s1532690xci1604_4, Schwartz and Bransford 1998.
- https://www.tandfonline.com/doi/full/10.1080/00461520.2013.775712, Alfieri et al 2013.
- https://eric.ed.gov/?id=EJ772031, Rittle-Johnson and Star 2007.
- https://dl.acm.org/doi/10.1145/2724660.2724681, Koedinger et al 2015.
- https://dl.acm.org/doi/10.1145/2556325.2566239, Guo, Kim and Rubin 2014.
