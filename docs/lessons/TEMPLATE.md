---
title: Lesson design template
research_date: 2026-09-29
status: draft
purpose: The one shape every lesson design document under docs/lessons/ takes, one section per plan 15 section in plan order plus the exam-attack parts and the 2026-09-29 framework additions (prediction, contrast pair, faded second example, fix prompts, figure presence, served-text rule), with the source fields, caps and machine-checkable form tools/check_lesson_designs.py validates.
---

# Lesson design template

A lesson design is an authoring spec. It is concrete enough that an author fills the JSON sections
of docs/plan/15-lessons.md (Content model) without making a teaching decision, and it is checked
by `PYTHONPATH=. .venv/bin/python tools/check_lesson_designs.py <file>` before it counts as
designed. The document has two layers:

1. Prose sections, in the order below, which carry what the served lesson teaches and why: the
   recognition features, the method choice, the time budget, the band plan and the sources. An
   author reads them. A student never sees them directly.
2. One fenced JSON block under `## Machine record`, which carries every sentence the student
   reads, every worked step as a SymPy string, every check and every source id. The checker
   computes over this block. It is plan 15's lesson record in design form: the same sections, the
   same caps, SymPy strings in place of MathJSON.

Nothing in either layer comes from model memory. Every fact, scoring claim and quote comes from
the authoring bundle (`app/lessons/source.py authoring_bundle`), the research files or the cached
text under cache/text/, cited by id (`BC-*`), page (`ced:<page>`, `sg-YY:<page>`,
`cr-YY:<page>`) or research heading (`research/<file>.md#<heading>`). A tactic with no source is
tagged `[inferred]` in the prose and listed in the machine record's `inferred` array with what
would settle it.

## What changed on 2026-09-29, and why

The redesign of 2026-09-29 (docs/pedagogy/synthesis.md, docs/pedagogy/clean-slate-design.md,
docs/pedagogy/growth-gap-analysis.md) found that the student was told before being asked, that
the completion check sat behind every trap, that the traps were read and never worked, that the
rival method was named but never shown, that the second example was never faded, and that half the
lessons had nothing to look at. Six things changed, all additive to the record and all checked:

1. A `prediction` opens every concept lesson: one committed answer on the concept's core claim,
   posed on worked example 1's own numbers, resolved on the key idea screen (pretesting,
   learning-science.md 13; Sinha and Kapur, 9).
2. The first strategy block carries a `contrast` pair: a stem that is this concept beside a near
   miss that is not, with the separating feature (contrasting cases, learning-science.md 14).
3. Check 1 follows worked example 1 at once; the traps come after it (synthesis rank 1).
4. Every error block whose wrong and right steps differ as expressions is a fix prompt: the student
   writes the right step before it is shown (erroneous examples, learning-science.md 9).
5. The second worked example is faded (`fade_from`): the student produces the answer from the
   steps shown, then the rest reveals (backward fading, learning-science.md 1).
6. Every lesson carries a drawn block or states `no_figure_reason` (synthesis rank 6), and no
   served sentence carries a record id, a page citation, an evidence tag or a leading label.

Nothing was loosened: every cap of plan 15 stands, the checks stay 2 or 3, and the prompts
(prediction, fix, fade) are section fields stored as lesson responses, never counted as checks and
never credited (plan 15 L0).

## Rules the checker enforces

| Rule | What it checks |
|---|---|
| front_matter | `title`, `research_date`, `status`, `purpose` present |
| sections | every section for the lesson kind present, non-empty, in template order |
| machine_record | the JSON block parses and carries the keys for its kind; `time.exam_part` is one of I-A, I-B, II-A, II-B with the matching `budget_minutes` |
| manifest_id | file name, `id`, `kind`, `target_id` and location agree with the manifest computed from the snapshot; a decision lesson's skills are a confusable set |
| referential | every `BC-*` id anywhere in the document is active in the snapshot or in data/ids.json |
| citations | every `ced:`, `sg-YY:`, `cr-YY:` and `crabbc-YY:` page cited has a cached page under cache/text/ |
| research_lines | every `research/...md#heading` exists, and every `research_lines` entry's `line` is a substring of its file |
| caps | orientation 60 words; key idea 120 words each, at most 2 core; strategy 80 words each, at most 3; cue 20 words; why 25 words; bridge 60 words; at most 4 error blocks; 2 or 3 checks; 2 to 4 decision stems |
| band_caps | `word_count.full` and `.brief` equal the words the low and mid plans serve; full at most 900 words and 6 minutes, brief at most 450 and 3; minutes never below words at 150 per minute |
| style | no em dash or en dash anywhere; no emoji; no praise, study advice, schedule or second-person belief statement (the tools/check_lessons.py patterns) |
| prediction | none of schemas/common.py FORBIDDEN_PREDICTION anywhere |
| quotes | at most one quote per key idea, at most 25 words, found on the cited cached page |
| steps | every worked step's `expr` parses; each valued step follows from the previous valued step under its `relation`; the answer equals the last valued step |
| keys | every check's key equals its last valued step; a completion check's key equals the answer of the example it completes; the key option equals the key; distractor values are distinct |
| errors | `observed_behavior` and `scoring_consequence` are the record's text; `possible_reason` is taken from a linked BC-MIS description; wrong and right steps parse and their `relation` is recomputed |
| distractor_paths | every distractor carries an `error_path` held by the lesson's skills and, on a concept lesson, anchored to an error block |
| reader_scores | scoring lines equal `reader_checks` recomputed; tagged point types are ones the archetype lists; no scoring on an archetype without `point_types` |
| draw_exclusion | no example or check `parameter_draw` equals a published item's `parameter_draw` on the same archetype |
| decision_stems | stems differ in exactly `selecting_feature`, name distinct methods; checks are discrimination checks with no execution steps and a key label that is one of the methods |
| inferred | every `inferred` entry has a claim and what settles it; a strategy block on an archetype without `asked_to_produce` and `common_givens` carries `evidence_tag: inferred` |
| delivery | exactly one `delivery` entry per served block; the mode is in the vocabulary; worked examples and error blocks are `step_reveal`; a decision lesson's stems are `contrast`; figure, table, motion, interactive and model entries carry a `spec` with every label placed inside, a `fallback` and `keyboard`; a `motion` entry carries `reduced_motion`; no block carries more than 2 representations |
| prediction | a concept lesson carries exactly one `prediction`: stem at most 40 words, resolution at most 40 words; `mcq` with 2 to 4 distinct option labels of at most 12 words and exactly one `is_key`, or `short_answer` with a numeric or symbolic key equal to worked example 1's answer or one of its valued steps (a statement key is text only); absent on prerequisite and decision lessons |
| contrast | the first strategy block of a concept lesson carries `contrast` and no other block does: `this.text` and `not_this.text` at most 30 words each and distinct, `not_this.why_not` at most 20 words, `feature` at most 20 words, `this.archetype_id` equal to the block's archetype |
| fade | `fade_from` sits only on a worked example served in the low band alone, is at least 2 and at most the step count, and at least one earlier step carries an expression; every second worked example of a concept lesson carries it |
| fix_prompt | every error block of a concept lesson carries `fix_prompt`, `true` when its `relation` is `distinct` and `false` when `equivalent` |
| figure_presence | a concept lesson with no drawn delivery (figure, table, motion, interactive, model) carries `no_figure_reason` (at most 40 words); one with a drawn block does not |
| served_text | no served text (orientation, key idea text and notation, strategy fields and contrast texts, prediction stem, option labels and resolution, representations, bridges, problem texts, step cues and whys, check stems) carries a `BC-*` id, a `ced:`, `sg-YY:`, `cr-YY:` or `crabbc-YY:` citation, or an evidence tag; a strategy `method` never begins with `First line:` |
| coverage (directory) | every manifest id has a design and every design a manifest id |

Words are whitespace-separated tokens. Inline mathematics sits between `\(` and `\)`, and counts
as words like any other token.

## Sections, in order

The section set depends on the lesson kind. Concept lessons (LSN-CON) carry all fifteen, with
Prediction first. Prerequisite lessons (LSN-PRQ) omit Prediction, Scoring, Representations and
Prerequisite bridge.
Decision lessons (LSN-DEC) carry Orientation, Recognition, Method choice, Stems, Traps, Time,
Checks, Band plan, Sources, Machine record.

### Prediction

New on 2026-09-29. One question the student commits to before any rule is stated, both bands,
served first. It is posed on worked example 1's own numbers (the concrete case), asks for the
concept's core claim, and carries a resolution the key idea screen shows beside the student's
choice. Form: `mcq` with 2 to 4 options and exactly one key, or `short_answer` with a numeric or
symbolic key that equals worked example 1's answer or one of its valued steps, so the blind
re-solve of the example already covers it. Stem at most 40 words, resolution at most 40 words, no
verdict word in the resolution (the prediction activates, it does not assess). Source: the concept
record and the topic section the key idea cites. Delivery: `text`, or a figure or table when the
question is about a picture (rules 4 and 5 of Delivery). The stem says "Predict" or "Before the
rule:" in its own words; it never says the student is wrong.

### Orientation

Plan 15 `orientation`, at most 60 words, both bands. Source: the concept's `description_plain`
and the topic's Assessment behaviour paragraph (research/units, the `### Assessment behaviour`
subsection of the topic), stated as what a response must show. No count, no frequency, no
prediction. Cite the concept id and the topic section.

### Key ideas

Plan 15 `key_ideas`: one block per BC-EK the concept's skills map (through
`skills[].essential_knowledge`), at most 120 words each, `depth` core or extended, at most 2 core.
Source: the topic's Required mathematical knowledge paragraph paraphrased, citing the BC-EK id and
`ced:<page>`; at most one anchor quote of 25 words or fewer per block, found on the cited page;
the notation line from the concept's `notation`. Core blocks serve both bands, extended blocks
the low band only.

### Recognition

Exam-attack part (a), delivered through the strategy cue lines. For each archetype family that
loads a skill of the concept: the stem features and wording that signal this concept, from the
archetype's `typical_wording`, `asked_to_produce` and `common_givens`; the MCQ and FRQ shapes it
appears in, from research/question-analysis/question-archetypes.md (the archetype's `###`
heading) and the `official_examples` BC-FRQ ids in the bundle. Name what a student reads in the
stem that says "this concept", and what in a stem says "not this one".

### Method choice

Exam-attack part (b), delivered as plan 15 `strategy` blocks (at most 3, at most 80 words each,
low and mid bands, the first only in mid). Per archetype: the method, named as the first entry of
`expected_solution_path`; the first written line; the rival method from `wrong_approaches` or
`prohibited_shortcuts`; and the one stem feature that separates them. Where the archetype lacks
`asked_to_produce` and `common_givens`, the block rests on `typical_wording` and carries
`evidence_tag: inferred` (plan 15 Q21). The `method` text names the step itself; it never begins
with a label such as "First line:", because the reader prints that label.

The first strategy block also carries the contrast pair (new on 2026-09-29): `this`, a stem of at
most 30 words that is this concept, drawn from the block's archetype and never equal to a
published item's stem; `not_this`, a stem of at most 30 words that a student could mistake for it
and that calls for the rival method or another concept, with `why_not` (at most 20 words) saying
what it asks for instead; and `feature` (at most 20 words), the one thing in the stem that tells
them apart. The prose of the Recognition section names where the two stems come from (the rival's
archetype, a sibling concept, or the `wrong_approaches` entry).

### Solution path

Exam-attack part (c), plan 15 `worked_examples`: one or two, example 1 for both bands, example 2
for the low band only. Example 2, when present, is faded (new on 2026-09-29): its `fade_from` names
the 1-based step from which the steps are withheld, at least 2 and at most the step count, with at
least one valued step before it; the student reads the shown steps, writes the answer, and then
sees the withheld steps. The prose says which steps are shown and why the fade falls there. Each is a draw from the archetype's `parameter_spec`, never equal to a
published item's `parameter_draw` on the same archetype (search content/items_*). Steps follow
`expected_solution_path`. Every step carries a `cue` (at most 20 words: what in the stem or the
previous line selects this step) and a `why` (at most 25 words). A step with a value carries
`expr` and a `relation` to the previous valued step. State here which steps a fluent solver writes
and which are held in the head (exam-attack part (f)), and the `comparison` gap for a
productive-failure target where one exists.

### Scoring

Exam-attack part (d), plan 15 `what_a_reader_scores`: one checklist per worked example whose
archetype lists `point_types`, at most 6 lines, each line the output of
`app/lessons/source.py reader_checks` for the BC-PT ids the example's steps tag. The design names
the point types and quotes the generated lines; the checker recomputes them. Add the point losses
research/scoring names for this topic, cited by heading (for example
research/scoring/common-point-losses.md#Answer points) and by `sg-YY:page`. An archetype without
`point_types` carries no scoring section and the lesson says nothing about points (plan 15, R14).

### Traps

Exam-attack part (e), plan 15 `common_errors`: one block per active BC-ERR whose skills meet the
concept's, at most 4, in the bundle's order (highest linked BC-MIS severity, then id); the mid band
shows the first 2. Each block copies `observed_behavior` and `scoring_consequence` from the record,
shows the wrong step beside the right step on the worked example's draw, both as SymPy strings with
`relation` distinct or equivalent, and may add `possible_reason` only in words taken from the
linked BC-MIS `description`. The error is never stated as what the student believes.

Each block carries `fix_prompt` (new on 2026-09-29): `true` when the relation is `distinct`, so the
student is shown the wrong step and writes the right one before it appears; `false` when the two
steps share a value and the difference lives in the sentence, so the block keeps the reveal form.
A value the wrong or right text writes as a decimal is written as a decimal expression (`0.52`,
not `13/25`), so the rendered value matches the sentence beside it.

### Representations

Plan 15 `representations`: 0 or 1, low band, from the topic's Representations paragraph, with a
declarative figure spec whose labels sit inside the figure. Write "None." when the topic section
gives nothing figure-shaped.

### Prerequisite bridge

Plan 15 `prerequisite_bridge`: one paragraph of at most 60 words per BC-PRQ in the bundle's
`prerequisites`, from its `description_plain` and `failure_signature`, gated by state, not band.
Write "None." when the bundle lists no BC-PRQ parent.

### Time

Exam-attack part (f). The exam part the archetype's shape lives in and its budget from
research/exam/exam-structure.md: Section I Part A 2.14 minutes per question, Part B 2.92, Section
II 15.0 per question (plan 15, Fluency). Which steps a fluent solver writes and which are skipped,
and where the minutes go. No target, no schedule.

### Stems (decision lessons only)

Plan 15 decision lessons: two to four stems, one per method in the set, drawn from the set's
archetypes with parameters chosen so the stems differ in exactly the feature that selects the
method. Beside each stem, the method it selects and the feature that selects it.

### Checks

Exam-attack part (g), plan 15 `checks`: 2 or 3 item-shaped records. Check 1 is the completion
form of worked example 1 (last step blanked), check 2 an isomorph short answer from the same
archetype on another draw, check 3 a 4-option MCQ whose distractors each carry the `error_path` of
an error block above, derived by making that error on the draw. Low band serves all, mid band
serves 1 and 2. A decision lesson's checks are method-naming MCQs only, with no execution. A
prerequisite lesson carries two checks.

### Delivery

Exam-attack part (j). How each served block reaches the student, chosen per block for the content,
not per lesson. One entry per served block (the orientation, every key idea, every worked example,
every error block, the representations block, the decision stems), each naming a mode from the
vocabulary below, the reason the content needs that mode, its declarative spec where the mode
draws or runs anything, and its fallback. The mode is a teaching decision, so the author never
makes it.

| Mode | What the student meets | When it is selected | Bound by |
|---|---|---|---|
| text | prose with inline mathematics | the default; a rule, a definition, a scoring habit | one new idea per screen (01, Split-attention-free presentation) |
| step_reveal | a worked example shown one step at a time, the why line beside its step | every worked example and every error block's wrong-beside-right pair | 15 UI, `StepMarks.tsx`; 01 split-attention rule |
| figure | a static declarative figure, labels inside | a skill or archetype whose representations include BC-REP-02, 07, 08, 12, 13 or 14, or a topic Representations paragraph naming a graphical conversion | 04 Figures rule 13; at most 2 representations per screen (01) |
| table | a rendered numerical table | BC-REP-03 givens, or a numeric experiment's output | 04 Figures; labels inside |
| motion | a parameter sweep over a declarative figure, rendered as discrete frames the student steps through; auto-advance only when `prefers-reduced-motion` is `no-preference`, else a cross-fade between frames on the student's own key press | a limit or approximation process: a secant closing to a tangent, rectangles refining under a curve, Euler steps, partial sums, a slope field being traced, a polar sweep | 08 Motion rules (replace, do not delete); proposed amendment A-D3 |
| interactive | a manipulable on a declarative figure: one slider or one draggable point, keyboard-operable, with the reading the student takes from it stated as a question | a relationship that varies with one parameter and that the stem tests as a reading: sign of a derivative against monotonicity, concavity against the tangent, accumulated area against the integrand's sign, the parameter that moves a polar or parametric curve | 04 figure spec plus `controls` (amendment A-D2); 08 keyboard rules; one control per screen [inferred] |
| model | a concrete quantitative model the student runs: a deterministic numeric experiment from a spec (difference quotients at shrinking h, Riemann sums at growing n, partial sums, Euler steps), shown as a table and, where a figure exists, a figure | a concept whose meaning is the behaviour of a computed sequence of values, and every productive-failure target (BC-DF-13 and 15 archetypes) | 01 Productive-failure openers; 15 Sequencing within a concept; [inferred] |
| contrast | two to four stems on one screen with the selecting feature marked | decision lessons only | 15 Decision lessons, side by side |

Figure presence (new on 2026-09-29): a concept lesson carries at least one drawn block (figure,
table, motion, interactive or model), or its machine record states `no_figure_reason`, at most 40
words, saying why no figure fits (a symbolic rule with no figure-bearing representation on any of
its skills and no process in its key ideas). A design that adds a figure to a lesson that had none
says in this section which rule chose it.

Selection rules, applied in order and cited in each entry's `reason`:

1. A worked example and an error block are always `step_reveal`.
2. A key idea whose text describes a process (a limit being taken, a partition refining, terms accumulating, a curve being traced) is `motion`, with a `model` on the same concept's example only where a computed sequence of values is the idea.
3. A process idea whose parameter is discrete and chosen by the student (the degree of a Taylor polynomial, the number of terms of a partial sum, the number of subintervals, the centre of a series) may be `interactive` with one stepper control in place of `motion`, so the student picks the value and reads the result; the graph the control drives is the process's own picture, not a representation the stem carries, and the entry says so in its reason.
4. A key idea or orientation whose skill representations include a figure-bearing BC-REP is `figure`, promoted to `interactive` when the archetype's `common_givens` or `difficulty_variables` name a quantity that varies and the stem asks for a reading of the relationship.
5. A block resting on BC-REP-03 givens is `table`.
6. Everything else is `text`.

Every entry beyond `text` and `step_reveal` carries a `spec` (declarative, every label placed inside), a `fallback` (the static form served when the mode cannot render, and under reduced motion for `motion`), and `keyboard` (how the control is operated without a pointer). No block carries more than 2 representations. No evidence in the ledgers separates these modes by effect, so every non-text choice is tagged [inferred] and the settling measurement is the modality A/B in the build plan (skip rate and time to first credited success by mode).

### Band plan

Exam-attack part (h). What the low band serves and what the mid band serves, in the served order
of 2026-09-29, with word and minute totals under the caps (full 900 words and 6 minutes, brief 450
and 3), and the refresher pointer list (core key ideas, error blocks, worked example 1). The totals
must equal the machine record's `word_count`.

The served order, low band: prediction, orientation, bridges when gated, key ideas (core then
extended), strategy blocks with the contrast pair on the first, example 1 and its scoring lines,
check 1, error blocks (at most 4), example 2 faded and its scoring lines, check 2, representations,
check 3. Mid band: prediction, orientation, bridges, core key ideas, the first strategy block,
example 1 and its scoring lines, check 1, the first 2 error blocks, check 2.

### Sources

Exam-attack part (i). Every id and page used, and every research heading cited, one per line.
Every `[inferred]` claim listed with what would settle it.

### Machine record

One fenced block, opened by a line reading exactly three backticks followed by `json` and closed by
three backticks. Its shape:

```text
{
 "id": "LSN-CON-02013",
 "kind": "concept",                       concept | prerequisite | decision
 "target_id": "BC-CON-02013",             BC-CON, BC-PRQ or BC-UNIT id
 "unit": "02",
 "skills": ["BC-SKL-02036", ...],         the concept's skills, or the set's, or the PRQ's dependents used
 "prediction": {"id": "pr-1", "stem": {"text": "...", "command_verb": "predict"}, "format": "mcq",
  "options": [{"id": "A", "label": "...", "is_key": false}, {"id": "B", "label": "...", "is_key": true}],
  "key": {"form": "numeric", "expr": "5"},        short_answer only
  "resolution": "...", "sources": ["BC-CON-02013"]},
 "no_figure_reason": "...",                       only when no delivery entry is drawn
 "orientation": {"text": "...", "sources": ["BC-CON-02013", "research/units/unit-02-....md#2.8 ..."]},
 "key_ideas": [
  {"id": "ki-1", "ek_id": "BC-EK-FUN-3B1", "depth": "core", "text": "...", "notation": "product rule",
   "quote": {"text": "...", "source": "ced:67"} or null, "sources": ["BC-EK-FUN-3B1", "ced:67"]}
 ],
 "strategy": [
  {"id": "st-1", "archetype_id": "BC-QA-02008", "cue": "...", "method": "...", "rival": "...",
   "separating_feature": "...", "sources": ["BC-QA-02008"], "evidence_tag": "verified" | "inferred",
   "contrast": {"this": {"text": "...", "archetype_id": "BC-QA-02008"},
                "not_this": {"text": "...", "why_not": "..."}, "feature": "..."}}
 ],
 "worked_examples": [
  {"id": "ex-1", "archetype_id": "BC-QA-02008", "bands": ["low", "mid"],
   "parameter_draw": {...},                 keys and values in the archetype's parameter_spec terms
   "problem": {"text": "...", "command_verb": "find"},
   "calculator_status": "no_calculator" | "calculator",
   "steps": [
    {"cue": "...", "why": "..."},                                        a step with no value
    {"cue": "...", "why": "...", "expr": "2*x*(x**3-2*x)+(x**2+1)*(3*x**2-2)", "relation": "new",
     "point_type_id": "BC-PT-99022"},
    {"cue": "...", "why": "...", "expr": "5*x**4-3*x**2-2", "relation": "equivalent"}
   ],
   "answer": {"form": "symbolic" | "numeric" | "statement", "expr": "5*x**4-3*x**2-2"}},
  {"id": "ex-2", "bands": ["low"], "fade_from": 3, ...}                 the second example is faded
 ],
 "what_a_reader_scores": [
  {"example_id": "ex-1", "point_type_ids": ["BC-PT-99022"], "lines": [{"point_type_id": "BC-PT-99022", "text": "..."}]}
 ],
 "common_errors": [
  {"error_id": "BC-ERR-02020", "observed_behavior": "...", "scoring_consequence": "...",
   "wrong_step": {"text": "...", "expr": "..."}, "right_step": {"text": "...", "expr": "..."},
   "relation": "distinct" | "equivalent",
   "fix_prompt": true,                             true when distinct, false when equivalent
   "possible_reason": {"misconception_id": "BC-MIS-02011", "text": "..."} or null,
   "sources": ["BC-ERR-02020"]}
 ],
 "representations": {"text": "...", "figure": {...}} or null,
 "prerequisite_bridges": [{"prq_id": "BC-PRQ-06005", "text": "..."}],
 "time": {"exam_part": "I-A", "budget_minutes": 2.14, "source": "research/exam/exam-structure.md#Section and part structure", "written_steps": [2, 3], "skipped_steps": [1]},
 "checks": [
  {"id": "chk-1", "check_kind": "completion" | "isomorph" | "mcq" | "discrimination",
   "format": "short_answer" | "mcq", "bands": ["low", "mid"], "archetype_id": "BC-QA-02008",
   "parameter_draw": {...}, "completes": "ex-1" (completion only),
   "stem": {"text": "...", "command_verb": "write"},
   "key": {"form": "symbolic", "expr": "..."},
   "steps": [{"text": "...", "expr": "...", "relation": "new"}, ...],
   "options": [{"id": "A", "is_key": false, "expr": "9", "error_path": "BC-ERR-02024", "derivation": "..."}, ...],
   "calculator_status": "no_calculator", "skills": ["BC-SKL-02036"]}
 ],
 "decision": {"skills": [...], "selecting_feature": "task",
  "stems": [{"id": "stem-1", "archetype_id": "BC-QA-06012", "method": "...", "parameter_draw": {...}, "text": "..."}]},
 "delivery": [
  {"block": "orientation", "mode": "text", "reason": "rule 5: a symbolic rule with BC-REP-01 givens", "sources": ["BC-SKL-02036"]},
  {"block": "ki-1", "mode": "figure", "reason": "rule 3: BC-REP-02 on BC-SKL-05012", "sources": ["BC-SKL-05012"],
   "spec": {"kind": "graph", "curves": [...], "labels": [{"text": "...", "placement": "inside"}]},
   "fallback": "the same figure at the stated input, static", "keyboard": "none needed"},
  {"block": "ex-1", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-02020", "mode": "step_reveal", "reason": "rule 1", "sources": []}
 ],
 "refresher": ["ki-1", "err-BC-ERR-02020", "ex-1"],
 "read_minutes": {"full": 4.0, "brief": 2.5},
 "word_count": {"full": 563, "brief": 344},
 "research_lines": [{"file": "research/scoring/common-point-losses.md", "line": "an exact sentence from the file"}],
 "inferred": [{"claim": "...", "settles": "..."}],
 "sources": ["BC-CON-02013", "BC-EK-FUN-3B1", "ced:67", "sg-25:20", "research/units/unit-02-differentiation-definition-properties.md#2.8 The Product Rule"]
}
```

Expression strings are SymPy: `**` for powers (`^` is accepted), `*` written explicitly, `exp(x)`,
`log(x)` for the natural logarithm, `sqrt(x)`, `pi`, `e`, `oo`. A string with one `=` is an
equation. A decision check's key has `"form": "statement"` and its options carry `label` instead of
`expr`.

Step relations, each checked against the previous valued step:

| relation | meaning | extra keys |
|---|---|---|
| new | starts a chain; nothing is checked | |
| equivalent | equal as expressions, and not the same string | |
| differentiate | this is the derivative of the previous step | `variable` |
| integrate | this differentiates back to the previous step | `variable` |
| evaluate | the previous step with `subs` applied | `subs`, optional `approx: true` for a 3-place decimal |
| solve | each value here is a root of the previous step, or of its equation | `variable` |
| limit | the limit of the previous step | `variable`, `point`, optional `dir` |

The words served per band, which the checker computes for `word_count`:

- both bands, before everything else: the prediction stem, its option labels and its resolution; the
  first strategy block's contrast texts (this, not this, why not, feature).
- low (full): orientation; every key idea (text, notation and quote); every strategy block; example 1 (problem, cues, whys) and its scoring lines; every error block (observed behaviour, consequence, wrong and right texts, possible reason); every check stem and option label; example 2 and its scoring lines; representations text; the decision stems and methods; the bridges.
- mid (brief): orientation; core key ideas; the first strategy block; example 1 and its scoring lines; the first 2 error blocks; checks 1 and 2 whose `bands` include mid; the decision stems; the bridges.

## Prerequisite lesson form

Short and gap-closing: an orientation from `description_plain`; one key idea block whose text is
the `description_plain` restated with the `failure_signature` as what goes wrong (tag inferred where
the record is inferred; the BC-PRQ has no BC-EK, so `ek_id` is null); a recognition section naming
the dependent skills the bundle's edges give and the archetypes whose `prerequisites` list the
record; one strategy block; one worked example drawn from such an archetype (or, when none lists
it, from an archetype loading a dependent skill, tagged inferred); traps from the
`failure_signature` (no BC-ERR is linked to a BC-PRQ, so distractors on a prerequisite check carry
error paths held by the dependent skills); two checks.

## Decision lesson form

Per plan 15, Decision lessons for confusable sets: stems that differ in exactly `selecting_feature`,
one per method, the strategy blocks of the archetypes side by side, and 2 or 3 method-naming checks
whose options are the set's methods and whose distractors carry the `error_path` of the BC-ERR the
wrong method produces. No check asks for execution.
