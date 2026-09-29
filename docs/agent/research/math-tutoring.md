---
title: What makes an AI tutor good at AP Calculus BC
research_date: 2026-09-29
status: draft
purpose: Ground the live tutor agent's conversational moves, per-turn context, AP scoring language and multi-turn evals in published tutoring evidence and in Growth's own library records.
---

# What makes an AI tutor good at AP Calculus BC

This file covers one strand of the live tutor research. It reads the published evidence on LLM tutors in mathematics and the learning-science mechanisms those tutors lean on, then reads what Growth already holds (plan 03, plan 01, the research library, the College Board cache, the registries, the lessons, the three tutor-role prompt templates and the tutor golden set) and turns both into rules the agent can follow and checks the app can run.

## Scope and standing constraints [inferred]

The constraints below come from the orchestrator's brief and from `docs/plan/03-diagnosis-and-feedback.md`. They are stated as fixed inputs. Nothing later in this file argues against them.

- During practice the agent never states the answer, never receives the student's unsubmitted answer or the key, never evaluates in-progress work on an unsupported or exam-shaped item, and asks before it tells. Worked solutions reach it only after submission.
- Nothing the agent says or the student types writes mastery evidence.
- No student-written text reaches a system prompt. Every field substitutes below the prompt-variables marker (`app/providers/base.py` `render_template`), untrusted fields are JSON-encoded into the user message, and the output is screened.
- No tool definitions are sent by default. Context is composed by the app.
- No study advice, no schedules, no quotas, no praise copy and no prediction talk about what the exam will hold.
- Every call goes through `app/providers/guard.py` with the tutor role's own caps. `app/feedback/tutor.py` sets `TUTOR_CALLS_PER_SESSION = 20` and `TUTOR_CALLS_PER_ITEM = 3`.
- The tutor role is never routed to claudebox.

"AP Calculus BC specifically" means three things in this file. The agent speaks in the language AP readers use when they award or withhold a point. It grounds every claim in a library record id rather than in model recall. And it respects the fading stage and item shape that decide whether mid-item help is allowed at all.

## The guardrail field experiment [single-source]

Bastani, Bastani, Sungu, Ge, Kabakcı and Mariman ran a randomized field experiment with nearly 1,000 students in about 50 classrooms (grades 9 to 11) at one high school in Turkey during the 2023 to 2024 school year (https://pmc.ncbi.nlm.nih.gov/articles/PMC12232635/, accessed 2026-09-29). Each 90-minute session had a teacher lecture, assisted practice, then an unassisted exam. The three arms were control (books and notes), GPT Base (a ChatGPT-like interface) and GPT Tutor (the same model with a guardrail prompt).

| Measure | GPT Base vs control | GPT Tutor vs control |
|---|---|---|
| Assisted practice grades | 48 percent higher | 127 percent higher |
| Unassisted exam grades | 17 percent lower | statistically indistinguishable from control |
| Exam point estimate reported in the paper | minus 0.054 | minus 0.004 |

Figures are from the PMC full text (accessed 2026-09-29). The PNAS page (https://www.pnas.org/doi/10.1073/pnas.2422633122) and the SSRN page (https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4895486) both returned HTTP 403 on 2026-09-29, and PubMed (https://pubmed.ncbi.nlm.nih.gov/40560616/) returned only a cookie notice. The published correction (https://pmc.ncbi.nlm.nih.gov/articles/PMC12403119/, accessed 2026-09-29) changes one author affiliation and no numbers. Because only the paper itself was read, the numbers carry [single-source]. They match what plan 03 already cites.

Three details matter for Growth. First, the GPT Tutor prompt contained the solution, teacher-written hints and common student mistakes, with an instruction to give hints without giving the answer (PMC full text, accessed 2026-09-29). Second, the paper describes GPT Base users treating the tool as a "crutch" by asking for and copying solutions. Third, the best exam outcome of the guardrailed arm was parity with control, not a gain. That is why plan 03 calls the guardrail a floor.

Growth's rule is stricter than the GPT Tutor arm. Growth's practice tutor never receives the key or the worked solution before submission. That removes the leak path the Bastani guardrail had to police by instruction. It also removes the model's ability to check its own hints against a solution. The compensation proposed below is to pass the archetype's `expected_solution_path`, which names each method step without values.

## Human-AI and AI tutoring trials in mathematics and physics since 2024 [single-source]

**Tutor CoPilot (Wang, Ribeiro, Robinson, Loeb and Demszky).** This was a randomized trial of an LLM that suggests moves to human tutors in real time. It reports a 4 percentage point rise in topic mastery (p < 0.01) and a 9 point rise for students of lower-rated tutors, at about $20 per tutor per year. The two versions read disagree on sample size. The arXiv abstract page gives 900 tutors, 1,800 students and more than 550,000 messages (https://arxiv.org/abs/2410.03017, accessed 2026-09-29). The November 2025 EdWorkingPaper gives more than 700 tutors, 1,000 students and more than 350,000 messages (https://edworkingpapers.com/sites/default/files/ai24_1054_v2.pdf, accessed 2026-09-29). The working paper reports that the tool increased probing questions and reduced generic praise. The tutors were human, so this is evidence about which moves help, not evidence that an autonomous model helps.

**Eedi and LearnLM exploratory RCT (LearnLM Team, Google and Eedi, 2025-11-11).** N = 165 students in Years 9 and 10 at five UK secondary schools, 91 control and 74 in the tutoring condition, with 17 expert tutors supervising every LearnLM draft (https://storage.googleapis.com/deepmind-media/LearnLM/learnLM_nov25.pdf, accessed 2026-09-29). Tutors accepted 74.4 percent of 3,617 drafts without edits and 76.4 percent with zero or minimal edits. Five drafts, 0.1 percent, contained factual errors. Transfer to a novel problem on a later topic was 66.2 percent after LearnLM-supported tutoring, 60.7 percent after human tutoring and 56.2 percent after a static hint. The LearnLM minus human difference was 5.5 points with a 95 percent credible interval of minus 1.4 to plus 12.4, so it includes zero. Misconception resolution was 95.4, 94.9 and 86.8 percent in the same three conditions. Of the drafts tutors edited, 44.3 percent of edits adjusted pacing, because Socratic questioning went on past the student's patience. Another 19.5 percent adjusted persona or tone, and one tutor said the emoji use came across as fake. This is the most direct evidence on what a math tutor model gets wrong in conversation. The failures were pacing and tone, not mathematics.

**LearnLM technical report (Modi and 44 co-authors, arXiv 2412.16429, revised 2025-08-22).** It frames tutoring as "pedagogical instruction following": the developer states the desired pedagogy in the system instructions and the model is trained to follow it (https://arxiv.org/abs/2412.16429, accessed 2026-09-29). Expert raters preferred LearnLM by 31 percent over GPT-4o, 11 percent over Claude 3.5 Sonnet and 13 percent over Gemini 1.5 Pro. The number of raters was not in the fetched abstract and is unknown here. These are preference ratings, not learning outcomes.

**Gupta, Reddig, Calo, Weitekamp and MacLellan, arXiv 2503.16460 (2025).** On college algebra, the models tested reached correct final answers on 85.5 percent of problems. As interactive tutors, 90 percent of dialogues gave high-quality instructional support but only 56.6 percent were entirely correct (https://arxiv.org/abs/2503.16460, accessed 2026-09-29). The authors conclude that LLMs need oversight or correctness mechanisms. The models were GPT-3.5 Turbo to o1-preview, and whether the rate holds for the models Growth routes to is unknown.

**Pisan, arXiv 2608.12292 (2026-08-12).** This paper describes a supervisor architecture that enforces answer withholding with a non-LLM policy core, a detector and a separate LLM judge, tuned with scripted student personas and no new human-subject study (https://arxiv.org/abs/2608.12292, accessed 2026-09-29). It supports putting the leak check outside the model.

**CoMeT (Hou and seven co-authors, arXiv 2609.22993, 2026-09-19).** A within-subjects study of 131 adult learners on three Python tasks compared an escalate-and-fade tutor with an unrestricted assistant and a question-only tutor (https://arxiv.org/abs/2609.22993, accessed 2026-09-29). The question-only tutor surrendered the full answer in one session in six, against one in sixteen for CoMeT, and frustrated learners more. The domain is programming, not calculus. The relevance is that a prompt-only "just ask questions" policy leaked in about 17 percent of sessions and annoyed learners. That agrees with the Eedi pacing finding.

## Kestin et al AI tutor RCT in physics [verified]

Kestin, Miller, Klales and colleagues ran a crossover RCT with 194 students in Harvard's Physical Sciences 2 in Fall 2023. Each student had one topic taught by in-class active learning and the other by an AI tutor at home (https://pmc.ncbi.nlm.nih.gov/articles/PMC12179260/, accessed 2026-09-29). Quantile regression gave effects of 0.73 to 1.3 standard deviations in favour of the AI tutor. Linear regression gave 0.63. Median time was 49 minutes for the AI group against an assumed 60 in class. A second source reports the same 194 students and the same 0.73 to 1.3 range (https://impactaieducation.substack.com/p/a-harvard-randomized-controlled-trial, accessed 2026-09-29, search-result summary), so the headline is [verified]. The mechanism detail comes from the full text only.

The tutor followed seven stated practices, including managing cognitive load, scaffolding and targeted timely feedback, and self-pacing. Its prompts were "enriched" with step-by-step answers written by the instructors. The platform walked students through each part in order. The limits the authors state are one institution, introductory material and unknown retention. For Growth this is the strongest evidence that a scripted, solution-grounded tutor can teach. It is not evidence for an unsupervised chat beside exam-shaped retrieval practice, which is the case Bastani covers.

## Tutoring decisions, verification and benchmarks [single-source]

**Bridge (Wang, Zhang, Robinson, Loeb and Demszky, NAACL 2024).** Cognitive task analysis of expert math tutors produced a three-part decision made before speaking: (A) identify the student's error, (B) choose a remediation strategy, (C) choose an intention. On 700 annotated real tutoring conversations, GPT-4 responses conditioned on expert decisions were 76 percent more preferred than without. Random decisions lowered quality by 97 percent relative to expert ones (https://arxiv.org/abs/2310.10648, accessed 2026-09-29). The implication for Growth is that the app, not the model, should choose the error and the move. The library already holds (A) as BC-ERR records. The moves listed later in this file are (B) and (C).

**Stepwise verification (Daheim, Macina, Kapur, Gurevych and Sachan, arXiv 2407.09136).** On 1,000 math reasoning chains with teacher-annotated error steps, feeding a verifier's error location into the response generator gave more targeted feedback with fewer hallucinations (https://arxiv.org/abs/2407.09136, accessed 2026-09-29). Effect sizes were not in the fetched abstract. Growth already does the verifier half deterministically, because plan 03 picks the violated `expected_solution_path` step and the matched BC-ERR before the tutor writes.

**MathTutorBench (Macina, Daheim, Hakimi, Kapur, Gurevych and Sachan, EMNLP 2025).** The benchmark finds that solving ability does not translate into good teaching, that expertise and pedagogy trade off, and that tutoring gets harder in longer dialogs where simple questioning stops working (https://arxiv.org/abs/2502.18940, accessed 2026-09-29, and https://github.com/eth-lre/mathtutorbench, accessed 2026-09-29). Its reward model is trained to separate expert from novice teacher turns. The public benchmark targets school word problems, not calculus, so its scores would not transfer directly to Growth.

**SocraticLM (NeurIPS 2024 spotlight).** A fine-tune on SocraTeach, 35K multi-round Socratic dialogues (208K single-round) built by a Dean-Teacher-Student agent pipeline over elementary math problems (https://proceedings.neurips.cc/paper_files/paper/2024/hash/9bae399d1f34b8650351c1bd3692aeae-Abstract-Conference.html, accessed 2026-09-29). No learner-outcome study was found. Growth cannot fine-tune on its operator's subscription, so the relevance is the move vocabulary, not the model.

## Learning-science mechanisms the moves rest on [verified]

**Self-explanation prompts.** Bisra, Liu, Nesbit, Salimi and Winne meta-analysed 69 effect sizes from 64 reports and found a random-effects weighted mean g = 0.55 (https://eric.ed.gov/?id=EJ1186664 and https://link.springer.com/article/10.1007/s10648-018-9434-x, both accessed 2026-09-29). Plan 01 records roughly 6,000 participants. The abstract recommends computer-generated prompts as a future direction. Plan 01 restricts prompts to worked examples and corrected errors because mathematics studies show a practice-volume cost (Rittle-Johnson, cited there, [single-source]). The agent's "which rule justifies this step" question is this mechanism.

**Elaborated feedback.** Shute's review in RER 78(1) defines formative feedback and lists the guidelines as nonevaluative, supportive, timely and specific. It reports growing consensus that response-specific elaborated feedback beats verification-only (https://eric.ed.gov/?id=EJ787077 and https://journals.sagepub.com/doi/10.3102/0034654307313795, both accessed 2026-09-29; the Sage page returned 403 and the ERIC record plus a search summary were read). It is a narrative review. A single pooled effect size for elaboration is not given and is unknown here. "Nonevaluative" is the basis for the no-praise rule below, together with Hattie and Timperley's finding, cited in plan 03, that feedback aimed at the self does not help.

**ICAP.** Chi and Wylie (Educational Psychologist 49, 219 to 243) order engagement modes as Passive, Active, Constructive and Interactive, and hypothesise that learning rises in that order. The support comes from note-taking, concept-mapping and self-explaining studies (https://eric.ed.gov/?id=EJ1044018 and https://education.asu.edu/lcl/publications/chi-m-t-h-wylie-r-2014-icap-framework-linking-cognitive-engagement-active-learning, both accessed 2026-09-29). No single effect size was found. For the agent, a turn where the student generates the next step is constructive, and a turn where the agent explains is at best passive for the student. That is the reason for asking before telling.

## Worked examples and the expertise reversal effect [single-source]

Kalyuga, Ayres, Chandler and Sweller (Educational Psychologist 38, 23 to 31, 2003) describe expertise reversal as a redundancy effect. Guidance that helps novices becomes redundant, and then harmful, for learners who already hold the schema (https://www.tandfonline.com/doi/abs/10.1207/S15326985EP3801_4, accessed 2026-09-29, abstract via search result). Plan 01 carries the rest of this evidence: backward fading (Renkl et al 2002), adaptive fading on a per-skill estimate (Salden et al), and a caution that earlier worked-example effect sizes may be overestimated. Each is tagged [single-source] there. Effect sizes for the worked-example effect were not refetched and are unknown in this file.

For the agent this means the amount of explanation depends on the skill's `fading_stage`. At `unsupported` the student is by definition past the example stage. There, a long explanation mid-item is the harmful case, besides being forbidden mid-item feedback.

## What Growth already specifies for the tutor [single-source]

Everything in this section was read from the repository on 2026-09-29.

**Plan 03, "Feedback policy".** Timing follows fading stage and item shape. Stages `example` and `completion` get step-level verification. Stage `unsupported` and every exam-shaped item get nothing until the whole item is submitted. Feedback on a lost point is elaborated and has three parts in order: the rule violated, in the BC-PT record's language when the archetype lists point types and as the violated `expected_solution_path` step otherwise; the scoring consequence from `errors.scoring_consequence` or the BC-PT `does_not_earn` text; and what the correct response would have shown, at the level of the step. The app selects the content and the tutor role writes the sentence (R35). Feedback never names a misconception as established and may raise the leading hypothesis only as the discriminating probe. At most two representations appear, which is the one-translation rule.

**Plan 03, "The tutor during practice".** The tutor restates the prompt, names the representation, asks what the student has tried, and offers the next question the student could ask themselves. It does not evaluate in-progress work on an unsupported or exam-shaped item. It has no tools and its output is rendered as text or KaTeX, never treated as instructions. A free chat box beside every item was rejected on the 17 percent number.

**Plan 01.** The mechanics are interleaving, spaced retrieval scheduled to the exam date, practice testing over restudy, mastery gating, adaptive worked-example fading, feedback timing and elaboration, confidence rating and hypercorrection routing, structured self-explanation, split-attention-free presentation, productive-failure openers, representation translation drills, FRQ justification writing as criterion practice, implementation intention and a queue-bound streak, session shape, metacognitive judgments of learning, and measurement against released AP material every 6 weeks. The tutor touches four of them directly: fading (how much it may say), feedback timing (when it may speak about correctness), self-explanation (its one question type after an error), and FRQ justification writing (the scoring language it uses).

**The prompt templates.**

| Template | Called when | Fields it receives | Notes |
|---|---|---|---|
| `prompts/tutor/guardrailed_practice_v1.md` | during practice | `misconception_list`, `item_skills`, `guardrail_level` | Not wired to any route. `tests/fixtures/provider_cassettes/tutor_guardrailed_practice_v1.json` says so. It receives no item text and no representation, so it cannot restate the prompt or name the representation that plan 03 requires |
| `prompts/feedback/elaborated_v2.md` | after a wrong submission at `unsupported` | `violated_step`, `observed_behavior`, `scoring_consequence`, `worked_solution` | Plain text, no LaTeX, no verdict, no praise, no step numbers, never names a misconception as held |
| `prompts/tutor/frq_points_v1.md` | after FRQ grading | `points_not_earned`, `observed_errors` | Refers to points by part letter, no study advice, no prediction |
| `prompts/tutor/correct_reinforcement_v1.md` | correct answer rated a guess or unsure | `expected_solution_path`, worked solution | At most two sentences naming the deciding step |

**The tutor golden set.** `content/golden/tutor.json` has 48 cases, 24 acceptable and 24 not, each labelled `names_rule`, `states_consequence`, `describes_correct_response` and `reveals_final_answer`. `app/evals/golden.py:47` defines `TUTOR_CHECKS` as the first three. Line 206 accepts a case when all three hold and `reveals_final_answer` is false. The set's note says every sentence and label was written by claude-opus-5-5 on the operator's delegation, not by a human. Every case is a single post-submission paragraph, so the set has no multi-turn case and no practice-time case.

## The library records a tutor can ground in [single-source]

Counts were taken from the files on 2026-09-29 by treating a record as live unless `status` is `retired`.

| Registry | Records | Live | Fields the tutor needs |
|---|---|---|---|
| `data/errors.json` | 427 | 393 | `name`, `observed_behavior`, `scoring_consequence`, `possible_misconceptions`, `discriminating_probe`, `archetypes` |
| `data/misconceptions.json` | 236 | 213 | `name`, `description`, `discriminating_probe`, `observable_errors`, `exposing_archetypes`, `rival_misconceptions` |
| `data/archetypes.json` | 153 | 148 | `expected_solution_path`, `skills`, `point_types`, `representations`, `common_distractors` |
| `data/scoring_points.json` | 76 | 76 | `name`, `earns`, `does_not_earn`, `justification_required`, `units_required`, `notation_requirements`, `eligibility_after_error` |
| `content/lessons/*.json` | 127 | 127 lessons, all `kind: concept` | section `id`, `type` |

All 393 live errors carry `scoring_consequence`, and 390 carry at least one `possible_misconceptions` id, for 772 error-to-misconception links. All 213 live misconceptions carry `observable_errors`. The link is many-to-many and stored on both sides, which matches the library rule that errors (what was seen) and misconceptions (maybe why) stay separate records. Plan 01 still says 390 active errors. The live count is 393.

`observed_behavior` describes the response, not the student. An example is BC-ERR-99006, where a definite integral is presented with no differential or a differential in the wrong variable. `scoring_consequence` is already in exam terms: the setup point is not earned when the expression is ambiguous, and later points in the part can go with it. These two fields have a mean combined length of 212 characters.

Of 148 active archetypes, 87 carry `point_types` and 61 carry none. Plan 03 says 56 carry none, so the count has moved or was taken differently. The median `expected_solution_path` has 4 steps and the mean serialized length is 203 characters. Errors linked to an archetype through `errors.archetypes` number 3 at the median and 11 at most, and 12 active archetypes have none. One oddity: BC-QA-06001, a Riemann sum from a table, lists BC-PT-99022, named "Product rule", and BC-PT-99026, named as decided from concavity, although its path decides over or under from monotonicity. The agent should therefore name a point type only when the app selected it for the violated step, not by walking the archetype's list.

A lesson such as `content/lessons/LSN-CON-06004.json` has addressable sections with ids of the form `LSN-CON-06004#s1` to `#s6`, plus `#err-BC-ERR-06005`-style common-error sections and `#prq-BC-PRQ-06008`-style prerequisite bridges. Across the 127 lessons the section types are: common_error 399, prerequisite_bridge 216, strategy 182, key_ideas 181, worked_example 157, prediction 127, orientation 127, what_a_reader_scores 83, representations 11. The sections a tutor can point to are `key_ideas` (the rule, with an `ek_id`), `strategy` (cue, method, the rival method and the separating feature), `what_a_reader_scores` (each point's earns and not-earned lines with scoring-guideline page citations), `common_error` (the matching BC-ERR with a wrong step and a right step), and `prerequisite_bridge`. The `worked_example` section uses its own parameter draw, so it is not the item's solution. Pointing a student to it during practice is still a presentation decision, and the expertise reversal guard in plan 01 says the example is never shown unprompted once a skill reaches `unsupported`.

## AP scoring language from the reader's side [single-source]

These are College Board documents in `cache/text/`, one organization, so [single-source]. Page numbers are the cache page files. No question stem is reproduced.

**Justification is a named, separate point, and a bare claim does not earn it.** In the 2025 Chief Reader report, responses that stated a function was continuous without justification did not earn the continuity point (crabbc-25:11). The scoring guideline for the maximum question says a local argument or an incorrect global argument does not earn the justification point but stays "eligible for P9 with the correct answer" (sg-25:5). The report says few responses earned that point, because of candidates-test errors or "stopping short of a global argument" (crabbc-25:4). `research/scoring/justification-requirements.md` indexes the forms: global versus local arguments, sign analysis, the candidates test, theorem hypotheses, and reasons tied to the object the prompt names.

**Reasons must name the function.** BC-ERR-99001 records vague pronoun reasoning across cr-22 and cr-23, where "it" or "the function" is used without saying which of f, f prime or f double prime is meant. The 2024 report flags statements such as "the velocity is moving right" as poor communication (cr-24:7).

**Units are their own point.** One 2025 part awarded P2 for units whether or not a number was attached (sg-25:11). The report says many responses gave no units, and some gave the units of R(t) where R prime of t was asked (crabbc-25:11). Another part's units were words per minute per minute (crabbc-25:10).

**Notation and linkage.** Incorrect or unclear communication between a correct integral and a correct answer is treated as scratch work and not scored (sg-25:3). Decimal answers must be accurate to three places after the decimal point, and at most one point per question is lost for rounding (sg-25:2). The 2025 report asks teachers to stress notation and clear communication of sign-chart reasoning (crabbc-25:23), and it counts incomplete analysis or communication as the most common reason one sign-analysis point was not earned (crabbc-25:21). `research/scoring/notation-requirements.md` and `research/scoring/common-point-losses.md` index these by point family: setup, answer, units, interpretation, justification, notation, precision.

**Eligibility chains.** Points depend on earlier points. A response with one error in a three-term sum earned the first point but was not eligible for the next (crabbc-25:11). The `eligibility_after_error` field on BC-PT records carries this, and an error's consequence is often "this point and the dependent one".

The reader's checklist a tutor can speak from is therefore short. What does the prompt command (the BC-CV verb)? Which function does the reason name? Is the argument global when the question asks for an absolute extremum? Are the theorem's hypotheses stated? Are units present and for the right quantity? Is the setup present before the answer? Is the decimal accurate to three places? A tutor that speaks this checklist is speaking the scoring guideline's language without reproducing a rubric.

## Conversational moves during practice [inferred]

Each move is an app-selected intention in Bridge's sense. The app decides which moves are open from `fading_stage`, the item shape and the turn count, and the model writes the sentence. Moves are listed in the order the agent should prefer them. ICAP and the Eedi pacing finding both argue for starting with the student's own work and getting to a named rule quickly.

| Move | What the agent says | Allowed at | Grounding it needs |
|---|---|---|---|
| M1 restate | The task in its own words, with the command verb and the quantity asked for | all stages | item text (app-owned), BC-CV verb |
| M2 name the representation | Which representation the givens use (table, graph of f prime, verbal) and what that representation lets you read directly | all stages | BC-REP code and name |
| M3 ask what was tried | One question about the student's last step or plan, never about their answer | all stages | none beyond the conversation |
| M4 offer the next self-question | A question the student can ask themselves, such as which function the reason must name, or whether the question asks for a global or a local conclusion | all stages | `expected_solution_path` step names |
| M5 name a rule or concept | The rule that governs the step the student is on, stated generally, with no value from this item | example and completion; at unsupported only after M3 got a reply or twice no reply | `key_ideas` text or BC-PT `earns`, skill name |
| M6 point to a lesson section | "Section LSN-CON-06004#s4 separates the monotonicity case from the concavity case" | all stages, but never a `worked_example` section at unsupported | lesson section ids and types |
| M7 step verification | Whether a finished step is right | example and completion only, per plan 03 | the step's expected form, supplied by the deterministic checker, not the model |

The agent never does these things during practice: state or bound the final answer; say whether the student's current work is right at `unsupported` or on an exam-shaped item; name a BC-ERR or a distractor pattern for the current item; name a misconception as the student's; or write the next line of the solution. Naming a BC-ERR during an MCQ is excluded because `common_distractors` on the archetype and the error records describe the wrong options, so naming one is option elimination, which is mid-item evaluation in another form.

Pacing. The Eedi supervisors' most common edit was cutting Socratic questioning that outlasted the student's patience (44.3 percent of edits), and CoMeT's question-only tutor frustrated learners and still leaked the answer in one session in six. So the app, not the model, escalates. The first turn on an item is M3 or M1. After one unanswered or "I don't know" reply the next turn may use M5 or M6. The existing per-item ceiling of 3 calls then ends the conversation. After that the student either submits or asks for the example, which the fading ladder already controls. This keeps "asks before tells" true without turning it into repeated questioning.

## Moves after submission [inferred]

After submission the key and the worked solution may reach the agent, and the three-part contract in plan 03 governs.

| Move | What the agent says | Grounding |
|---|---|---|
| P1 name the point not earned | The BC-PT by name and its earning condition in the record's own words, or the violated path step when the archetype has no point types | BC-PT `name`, `earns`, `does_not_earn` |
| P2 state the consequence | Which point was lost and, where `eligibility_after_error` says so, which dependent point went with it | BC-ERR `scoring_consequence` |
| P3 discuss the worked solution at the violated step | What the correct response showed at that step, not the whole solution and not the step number | worked solution, violated step |
| P4 one self-explanation question | "Which rule justifies this step, and why does it apply here", on corrected errors only | the step and its BC-PT |
| P5 the discriminating probe | The leading misconception's probe asked as a question, never as a diagnosis | BC-MIS `discriminating_probe`, only when the diagnostician ran |
| P6 one translation | The same point in the second representation, only when the leading misconception's `exposing_archetypes` use it | BC-REP pair, one-translation rule |
| P7 point to the lesson | The `common_error` section for the matched BC-ERR, or the `what_a_reader_scores` section | lesson section ids |

A follow-up question from the student after feedback stays at the level of the violated step. If the student asks about a different part of the item, the app sends that part's step and point, not the whole rubric.

## Grounding each turn and its token cost [inferred]

The app composes one grounding packet per turn from ids it already knows: the item's archetype, the fading stage, the violated step and matched BC-ERR after submission, and the leading BC-MIS if the diagnostician ran. The model never retrieves anything. Token counts below divide characters by 3.1, the divisor `tools/cost_model.py` uses per plan 13. They are estimates, not `count_tokens` measurements.

**Practice packet.** It holds the archetype `id`, `name`, `expected_solution_path`, `representations` with names, point type ids with names, lesson section ids with types, the student's persistent misconception names (already a template variable), and the item text and command verb. It excludes the key, the worked solution, the student's draft, BC-ERR records and `common_distractors`. Measured on BC-QA-06001 with LSN-CON-06004, a packet including three error names and their misconception names came to 2,140 characters, about 690 tokens. Dropping the error and misconception names, which this file excludes during practice, leaves about 450 tokens plus the item text.

**Post-submission packet.** It holds the practice packet, plus the one violated step, one BC-ERR `observed_behavior` and `scoring_consequence` (212 characters mean, about 70 tokens), one BC-PT `name`, `earns` and `does_not_earn` (231 characters mean, about 75 tokens), the worked solution, and the matched `common_error` section id. Measured on the same archetype with one error and one point type, the packet was 2,258 characters, about 730 tokens before the worked solution.

**Which records.** During practice, no BC-ERR and no BC-MIS for the current item. The persistent misconception list is the exception, and it names only misconceptions already corrected earlier, so the agent does not repeat a correction. After submission, exactly one BC-ERR (the matched one) and, only when the diagnostician ran, the top BC-MIS by probability, as a probe question. From the archetype, `expected_solution_path` and `representations` always, and `point_types` only as the single point the app selected. From the lesson, section ids and types only, never section bodies. The student can open the section, and bodies cost tokens without adding grounding the packet lacks.

**Cache placement.** Plan 13 already puts the guardrail-level definitions and the misconception list in the cached prefix at about 1,100 tokens. The packet goes below the prompt-variables marker as JSON in the user message. The student's turn goes there too, JSON-encoded as untrusted content.

## Style rules for AP scoring language [inferred]

| Rule | Allowed | Forbidden |
|---|---|---|
| Name the function in every reason | "The reason has to name g prime, since the question is about where g increases." | "It's positive there, so it goes up." |
| Say which point, in rubric terms | "That costs the justification point. The answer point is still available." | "You lost some marks there." |
| Global when the question is absolute | "An absolute maximum needs a global argument such as the candidates test." | "Just check the sign change and you're done." |
| Units for the quantity asked | "Units are for the rate R prime of t, so per minute per minute." | "Don't forget units!" |
| Talk about the work, never the student | "The setup is missing a differential." | "You're careless with notation." |
| No praise, no verdict words | "The sign analysis names f prime on each interval." | "Great job!", "Nice!", "Oops" |
| No study advice | "Section LSN-CON-06004#s3 states the monotonicity rule." | "Review Riemann sums tonight.", "Practice more of these." |
| No prediction talk | "Readers score this as the justification point (sg-25:5)." | "This shows up on every exam.", "Expect this on May 10." |
| Misconception only as a question | "If velocity and acceleration are both negative, is the particle speeding up or slowing down, and why?" | "You think negative acceleration means slowing down." |
| Ask before telling | "What does the table let you read directly?" | "Multiply each value by its width." (as a first turn) |
| Ids only when real | "BC-PT-99018 is the form point for a Riemann sum." | "BC-PT-99999 covers this." (an id not in the packet) |
| No dashes | "The setup is right, but the bounds are not." | a sentence joined with an em dash or a spaced en dash |

Citations such as sg-25:5 are allowed because they point to the scoring guideline page. They quote nothing beyond the record's own 25-word anchor. No exam counts or times appear in agent output. If the student asks about exam format, the agent cites `research/exam/exam-structure.md` and states nothing from memory.

## Multi-turn eval checks [inferred]

The existing checks, `names_rule`, `states_consequence`, `describes_correct_response` and `reveals_final_answer`, stay for the post-submission paragraph. A multi-turn case is a scripted student side (a persona in Pisan's and CoMeT's sense) plus the app packets, replayed through the cassette book. Each check below is scored per turn or per conversation, and each is deterministic where it can be, with a judge only where it cannot.

| Check | Scope | How it is decided |
|---|---|---|
| `no_answer_before_submission` | every practice turn | Deterministic. The key (canonical SymPy form, decimal to three places, the MCQ option letter and option text) must not appear in the turn. The eval harness holds the key even though the model never does. A judge label covers paraphrase such as "the answer is a bit over 60" |
| `no_mid_item_evaluation` | practice turns at unsupported or exam-shaped | Judge label. No statement that the student's current work is right, wrong, close or on track |
| `asks_before_tells` | first agent turn per item and per new stuck point | Deterministic. The turn contains a question mark and contains no M5 rule statement. M5 is open only after a student turn |
| `names_rule` | at least one turn by the ceiling, and every post-submission turn | Deterministic match of a BC-PT name, a path step string or a `key_ideas` rule from the packet, with a judge fallback |
| `no_study_advice` | every turn | Deterministic phrase list (study, review, practice more, tonight, before the exam, each day, schedule, minutes) plus a judge |
| `no_prediction_talk` | every turn | Deterministic phrase list (will be on, likely to appear, always tested, expect this, the exam will) plus a judge |
| `no_praise` | every turn | Deterministic list (great, nice, good job, well done, excellent, awesome, perfect, you got this, oops) plus a judge for tone |
| `no_dash` | every turn | Deterministic. No U+2014, and no U+2013 used as punctuation |
| `cites_real_id` | every turn that contains an id | Deterministic. Every token matching `BC-(ERR|MIS|PT|QA|SKL|CON|REP|CV)-[0-9A-Z-]+` or `LSN-[A-Z]+-[0-9]+(#[a-z0-9-]+)?` must resolve in the packet sent that turn, not merely in the library |
| `no_misconception_asserted` | every turn | Judge. A BC-MIS appears only as a probe question |
| `turns_within_ceiling` | conversation | Deterministic. No more than `TUTOR_CALLS_PER_ITEM` calls per item |
| `stays_on_violated_step` | post-submission follow-ups | Judge. No step beyond the violated one is worked unless the student asks about that part |

Every deterministic check also runs in the live output screen, not only in evals, because a check that holds only in evals does not protect the student. Following the testing discipline in this repository, a new check counts only after a deliberately leaking or praising turn has been shown to fail it.

## What remains unknown [uncertain]

No published RCT tests an LLM tutor on AP Calculus BC or on any calculus course, so every transfer from Bastani (high school math in Turkey), Kestin (undergraduate physics), Eedi (UK Years 9 and 10) and CoMeT (adult Python learners) is an inference. Whether a tutor that never sees the solution during practice gives more wrong hints than Bastani's GPT Tutor, which did see it, is unknown. Gupta et al's 56.6 percent entirely-correct rate suggests the risk is real, but their models were older. The Tutor CoPilot sample size differs between versions (900 and 1,800 on arXiv, more than 700 and 1,000 in the November 2025 working paper), and this file could not settle which is final. The number of LearnLM raters and the effect sizes in Daheim et al were not retrieved. The Sage, Springer, Nature, PNAS and SSRN pages returned 403 or login redirects, so those numbers come from PMC, ERIC, arXiv and search summaries as cited.

## What this means for Growth [inferred]

Ranked by expected tutoring quality per token spent.

1. **Put the leak, praise, dash, advice, prediction and id checks in a deterministic output screen on every tutor turn.** Cost is zero tokens. CoMeT's question-only tutor leaked in one session in six, and Pisan's architecture puts the withholding check outside the model. Alternative rejected: relying on the prompt's instruction to withhold, because both papers show instructions alone leak at a measurable rate.
2. **Wire `guardrailed_practice` with the item text, BC-CV verb, BC-REP name and `expected_solution_path` step names, about 150 to 250 tokens beyond the current template.** Without them the template cannot do M1 or M2, which plan 03 lists first. Alternative rejected: passing the worked solution as Bastani and Kestin did, because Growth's rule forbids it during practice and the path names give method without values.
3. **Let the app choose the move (M1 to M7, P1 to P7) and pass it as a field, about 20 tokens.** Bridge found a 76 percent preference gain from expert decisions and a 97 percent loss from random ones. Alternative rejected: letting the model pick the strategy from the conversation, because MathTutorBench shows questioning degrades in longer dialogs and Eedi supervisors most often had to correct pacing.
4. **After submission, pass exactly one BC-ERR (`observed_behavior`, `scoring_consequence`) and one BC-PT (`name`, `earns`, `does_not_earn`), about 145 tokens.** This is plan 03's three-part contract and the verified-error grounding Daheim et al found reduces hallucination. Alternative rejected: sending every error and point type linked to the archetype, because the BC-QA-06001 point list shows archetype-level lists can include unrelated points.
5. **Pass lesson section ids and types, not bodies, about 60 tokens.** This lets the agent point (M6, P7) and lets `cites_real_id` verify every pointer. Alternative rejected: including `key_ideas` and `strategy` text, which roughly doubles the packet for content the student can open with one click.
6. **Build a multi-turn golden set with scripted student personas, human-labelled, covering the twelve checks above.** The existing 48 cases are single paragraphs written and labelled by the same model. Alternative rejected: extending `content/golden/tutor.json` with more single-paragraph cases, because the failures in the literature (pacing, leakage over turns) only appear across turns.
7. **Escalate by turn count in the app: question first, rule or lesson pointer after one unanswered turn, stop at the per-item ceiling of 3.** Alternative rejected: pure Socratic questioning, on the Eedi pacing edits and CoMeT's frustration result.
8. **Keep misconceptions out of practice turns and raise them after submission only as the discriminating probe.** Alternative rejected: naming the student's persistent misconception during practice to pre-empt it, because plan 03 forbids asserting a diagnosis and naming it on an MCQ can act as distractor elimination.
9. **Do not add tools or retrieval.** Every record the agent needs is addressable by an id the app already holds at the moment of the call. Alternative rejected: a lookup tool over the registries, because it adds an injection surface and no information the packet lacks.

## Sources [verified]

- https://pmc.ncbi.nlm.nih.gov/articles/PMC12232635/ (accessed 2026-09-29)
- https://pmc.ncbi.nlm.nih.gov/articles/PMC12403119/ (accessed 2026-09-29)
- https://www.pnas.org/doi/10.1073/pnas.2422633122 (accessed 2026-09-29, HTTP 403)
- https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4895486 (accessed 2026-09-29, via search listing only)
- https://pubmed.ncbi.nlm.nih.gov/40560616/ (accessed 2026-09-29, cookie notice only)
- https://arxiv.org/abs/2410.03017 (accessed 2026-09-29)
- https://edworkingpapers.com/sites/default/files/ai24_1054_v2.pdf (accessed 2026-09-29)
- https://pmc.ncbi.nlm.nih.gov/articles/PMC12179260/ (accessed 2026-09-29)
- https://www.nature.com/articles/s41598-025-97652-6 (accessed 2026-09-29, login redirect)
- https://impactaieducation.substack.com/p/a-harvard-randomized-controlled-trial (accessed 2026-09-29, search summary)
- https://arxiv.org/abs/2412.16429 (accessed 2026-09-29)
- https://storage.googleapis.com/deepmind-media/LearnLM/learnLM_nov25.pdf (accessed 2026-09-29)
- https://arxiv.org/abs/2503.16460 (accessed 2026-09-29)
- https://arxiv.org/abs/2608.12292 (accessed 2026-09-29)
- https://arxiv.org/abs/2609.22993 (accessed 2026-09-29)
- https://arxiv.org/abs/2310.10648 (accessed 2026-09-29)
- https://arxiv.org/abs/2407.09136 (accessed 2026-09-29)
- https://arxiv.org/abs/2502.18940 (accessed 2026-09-29)
- https://github.com/eth-lre/mathtutorbench (accessed 2026-09-29)
- https://proceedings.neurips.cc/paper_files/paper/2024/hash/9bae399d1f34b8650351c1bd3692aeae-Abstract-Conference.html (accessed 2026-09-29)
- https://eric.ed.gov/?id=EJ1186664 (accessed 2026-09-29)
- https://link.springer.com/article/10.1007/s10648-018-9434-x (accessed 2026-09-29, login redirect, abstract via search result)
- https://eric.ed.gov/?id=EJ787077 (accessed 2026-09-29)
- https://journals.sagepub.com/doi/10.3102/0034654307313795 (accessed 2026-09-29, HTTP 403)
- https://eric.ed.gov/?id=EJ1044018 (accessed 2026-09-29)
- https://education.asu.edu/lcl/publications/chi-m-t-h-wylie-r-2014-icap-framework-linking-cognitive-engagement-active-learning (accessed 2026-09-29)
- https://www.tandfonline.com/doi/abs/10.1207/S15326985EP3801_4 (accessed 2026-09-29, abstract via search result)
- Repository files read on 2026-09-29: `docs/plan/03-diagnosis-and-feedback.md`, `docs/plan/01-learning-model.md`, `docs/plan/13-ai-engineering.md`, `research/README.md`, `research/exam/exam-structure.md`, `research/scoring/justification-requirements.md`, `research/scoring/notation-requirements.md`, `research/scoring/common-point-losses.md`, `cache/text/crabbc-25/page-003.txt`, `page-004.txt`, `page-010.txt`, `page-011.txt`, `page-021.txt`, `page-023.txt`, `cache/text/cr-24/page-007.txt`, `cache/text/sg-25/page-002.txt`, `page-003.txt`, `page-005.txt`, `page-011.txt`, `data/errors.json`, `data/misconceptions.json`, `data/archetypes.json`, `data/scoring_points.json`, `content/lessons/LSN-CON-06004.json`, `prompts/tutor/guardrailed_practice_v1.md`, `prompts/feedback/elaborated_v2.md`, `prompts/tutor/frq_points_v1.md`, `prompts/tutor/correct_reinforcement_v1.md`, `content/golden/tutor.json`, `app/evals/golden.py`, `app/feedback/tutor.py`, `tests/fixtures/provider_cassettes/tutor_guardrailed_practice_v1.json`
