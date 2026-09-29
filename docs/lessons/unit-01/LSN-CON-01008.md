---
title: LSN-CON-01008 Indeterminate form handled by rewriting
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-01008, the indeterminate form zero over zero handled by rewriting, built from authoring_bundle("BC-CON-01008") and the research files it cites, so an author fills plan 15's lesson record without making a teaching decision.
---

# LSN-CON-01008 Indeterminate form handled by rewriting

Concept BC-CON-01008 (skills BC-SKL-01024 to BC-SKL-01028), topics 1.6 and 1.7 of Unit 1, loaded by BC-QA-01004 (primary). The unit attack map (docs/lessons/unit-01/README.md) places it eighth, a root concept, with text delivery.

## Prediction

Served first, both bands. Pose on ex-1's own quotient: substitution at \(x=2\) gives zero over zero, and the student writes the limit. Form `short_answer`, key \(-\frac{5}{2}\), which is ex-1's answer. The resolution says that zero over zero carries no value and that the rewritten quotient gives the limit, from BC-CON-01008 and the topic 1.6 paragraph. It carries no verdict word.

## Orientation

Served text, from BC-CON-01008 `description_plain` and the topic's Assessment behaviour paragraph (research/units/unit-01-limits-continuity.md#1.6 Determining Limits Using Algebraic Manipulation): a response shows zero over zero with the two limits written separately, rewrites, and evaluates. The sg-23:14 rule on a limit written equal to zero over zero is the one scoring statement in the paragraph, stated as what a response shows. No count, no frequency.

## Key ideas

All five skills map to one BC-EK, BC-EK-LIM-1E1 (ced:43), so one core block, both bands.

- ki-1 (core). Paraphrase of the topic's Required mathematical knowledge paragraph (Rewriting, Equivalence): zero over zero carries no value, the expression is rearranged into an equivalent form, the three CED routes, and the equivalence holding at every input near but not at the target. Anchor quote (16 words) from ced:43. Notation line from the concept record: indeterminate form zero over zero.

## Recognition

- BC-QA-01004 (family limit-algebraic-rewrite, MCQ or one part of a larger question, no calculator; research/question-analysis/question-archetypes.md#BC-QA-01004 Indeterminate limit resolved by algebraic rewriting). `typical_wording`: "Find the value of the given limit, or show that it does not exist." `common_givens`: a quotient that gives zero over zero under substitution; a trigonometric quotient at zero. `asked_to_produce`: separate limits of the numerator and denominator; the value of the limit. Official examples: BC-MCQ-CED-001, BC-MCQ-SAMPLE-002. The signal is a quotient whose top and bottom both vanish at the target.

What says "not this concept": substitution gives a defined value, so substitution settles the limit (BC-SKL-01031, BC-CON-01009); substitution gives a nonzero number over zero, which calls for one sided sign analysis and points to BC-CON-01016 (unit-01 README, Recognition features between neighbouring concepts); the variable grows without bound (BC-CON-01017). The contrast pair on st-1 takes its near miss from the nonzero over zero neighbour: `this` is a quotient whose top and bottom both vanish at the target, `not_this` is a quotient whose top does not vanish (BC-CON-01016), and the feature is that both vanish. L'Hospital's rule is not available in Unit 1 (research/units/unit-01-limits-continuity.md#1.6 Determining Limits Using Algebraic Manipulation).

## Method choice

One strategy block (one archetype family), low and mid bands.

- st-1, BC-QA-01004. Cue from `asked_to_produce` and `common_givens`. Method, `expected_solution_path[0]`: substitute and observe the indeterminate form. Written first: the numerator limit and the denominator limit on separate lines (sg-23:14). Rival, `wrong_approaches`: declaring the limit nonexistent on seeing zero over zero (BC-ERR-01009). Separating feature: zero over zero signals a rewrite; a nonzero number over zero does not. The archetype carries `asked_to_produce` and `common_givens`, so the block is verified.

## Solution path

- ex-1, BC-QA-01004, both bands, no calculator. Draw: target 2, top_root \(-3\), bottom_root 4, state_form stated, giving \(\frac{(x-2)(x+3)}{(x-2)(x-4)}\) expanded as \(\frac{x^2+x-6}{x^2-6x+8}\) (the shape the `parameter_spec` notes fix). The value \(-\frac{5}{2}\) meets the invariants (not 0, not 1). No published BC-QA-01004 draw has these values (content/items_gen_unit01, content/items_unit01_agent). Steps follow `expected_solution_path`: substitute and observe the form (the quotient, `new`, with both limits in the why line), rewrite by factoring (`equivalent`), divide out \(x-2\) (`equivalent`), evaluate at the target (`limit`, x to 2).

A fluent solver writes the two separate limits, the cancelled quotient and the value, and holds the factoring in the head [inferred]. No productive-failure target sits in this concept, so no comparison callout.

## Scoring

None. BC-QA-01004 lists no `point_types`, so the lesson carries no `what_a_reader_scores` entry, no step carries a `point_type_id`, and the served text says nothing about points beyond the record text of the error blocks. For the author: the scoring statement the topic rests on is sg-23:14 (the form is established by two separate limits), cited in research/question-analysis/question-archetypes.md#BC-QA-01004 Indeterminate limit resolved by algebraic rewriting.

## Traps

Four active errors meet the skills, in the bundle's order; all linked BC-MIS are severity high. Low band all four, mid band the first two. Every wrong and right step sits on ex-1's draw.

- err-BC-ERR-01008. Wrong: 0 from the numerator alone. Right: \(-\frac{5}{2}\). Distinct. Possible reason, words from BC-MIS-01006.
- err-BC-ERR-01009. Wrong: no limit (SymPy `nan`). Right: \(-\frac{5}{2}\). Distinct. Possible reason, words from BC-MIS-01006.
- err-BC-ERR-01010. Wrong: the \(x^2\) terms cancelled, \(\frac{x-6}{-6x+8}\), which gives 1 at 2 (the `parameter_spec` notes). Right: \(\frac{x+3}{x-4}\). Distinct. Possible reason, words from BC-MIS-01007.
- err-BC-ERR-01011. Wrong: one line equal to \(\frac{0}{0}\). Right: two separate limits, each 0. Distinct. Possible reason, words from BC-MIS-99011.

## Representations

None. The topic's Representations paragraph names BC-REP-01 only, with the conversion expression to equivalent expression; nothing is figure-shaped.

## Prerequisite bridge

Four BC-PRQ parents, each a supporting edge, gated by state: BC-PRQ-01001 (factoring), BC-PRQ-01002 (conjugate), BC-PRQ-01005 (bounds on sine and cosine), BC-PRQ-01007 (complex fraction). Each bridge restates `description_plain` and names the `failure_signature` as the observable gap.

## Time

BC-QA-01004 is `no_calculator` and "Typically a single multiple choice item or one part of a larger question", so the part is Section I Part A, 29 questions in 62 minutes, 2.14 minutes per question (research/exam/exam-structure.md#Section and part layout). A fluent solver writes three lines (the separate limits, the cancelled quotient, the value) and holds the factoring (step 2) in the head [inferred]. The separate limits are written even under time pressure inside a free response part, since a single line equal to zero over zero does not establish the form (sg-23:14).

## Checks

- chk-1, completion of ex-1, both bands: the cancelled quotient is given, the student evaluates. Key \(-\frac{5}{2}\), ex-1's answer.
- chk-2, isomorph, both bands: target \(-1\), top_root 3, bottom_root 2, state_form silent, \(\lim_{x\to-1}\frac{x^2-2x-3}{x^2-x-2}\). Key \(\frac{4}{3}\).
- chk-3, MCQ, low band: target 3, top_root 1, bottom_root \(-2\), \(\lim_{x\to3}\frac{x^2-4x+3}{x^2-x-6}\). Key \(\frac{2}{5}\). Distractors: 0 (BC-ERR-01008), 1 (BC-ERR-01010, the \(x^2\) terms cancelled), does not exist (BC-ERR-01009).

No check draw equals a published BC-QA-01004 `parameter_draw`.

## Delivery

- orientation: text. Rule 5; the unit-01 README delivery map gives text for BC-CON-01008 because its skills carry BC-REP-01 and BC-REP-04 only.
- ki-1: text. Rule 5; the rewriting is shown in the step reveal of ex-1.
- ex-1 and the four error blocks: step_reveal. Rule 1.

No figure, motion, interactive or model entry, and the machine record states `no_figure_reason`: no figure-bearing BC-REP on any skill and no process in the key idea to watch.

## Band plan

- Low (full): pr-1, orientation, the four bridges when gated in, ki-1, st-1 with its contrast, ex-1, chk-1, err-BC-ERR-01008, err-BC-ERR-01009, err-BC-ERR-01010, err-BC-ERR-01011, chk-2, chk-3. There is no second example, so nothing fades. 569 words, 3.8 minutes (cap 900 and 6).
- Mid (brief): pr-1, orientation, the bridges when gated in, ki-1, st-1 with its contrast, ex-1, chk-1, err-BC-ERR-01008, err-BC-ERR-01009, chk-2. 435 words, 2.9 minutes (cap 450 and 3).
- Refresher: ki-1, the four error blocks, ex-1.

## Sources

- BC-CON-01008; BC-SKL-01024, BC-SKL-01025, BC-SKL-01026, BC-SKL-01027, BC-SKL-01028; BC-EK-LIM-1E1; ced:43; sg-23:14
- BC-QA-01004; BC-MCQ-CED-001, BC-MCQ-SAMPLE-002
- BC-ERR-01008, BC-ERR-01009, BC-ERR-01010, BC-ERR-01011; BC-MIS-01006, BC-MIS-01007, BC-MIS-99011
- BC-PRQ-01001, BC-PRQ-01002, BC-PRQ-01005, BC-PRQ-01007
- research/units/unit-01-limits-continuity.md#1.6 Determining Limits Using Algebraic Manipulation
- research/question-analysis/question-archetypes.md#BC-QA-01004 Indeterminate limit resolved by algebraic rewriting
- research/exam/exam-structure.md#Section and part layout
- [inferred] A fluent solver holds the factor search in the head. Settled by timed response logs on BC-QA-01004 items.
- [inferred] The expanded quotient shape of the draws follows the `parameter_spec` notes. Settled by the BC-QA-01004 item template.

## Machine record

```json
{
 "id": "LSN-CON-01008",
 "kind": "concept",
 "target_id": "BC-CON-01008",
 "unit": "01",
 "skills": [
  "BC-SKL-01024",
  "BC-SKL-01025",
  "BC-SKL-01026",
  "BC-SKL-01027",
  "BC-SKL-01028"
 ],
 "prediction": {
  "id": "pr-1",
  "stem": {
   "text": "Substituting x = 2 into \\(\\frac{x^2+x-6}{x^2-6x+8}\\) gives zero over zero. What is \\(\\lim_{x\\to2}\\frac{x^2+x-6}{x^2-6x+8}\\)?",
   "command_verb": "predict"
  },
  "format": "short_answer",
  "key": {
   "form": "numeric",
   "expr": "-5/2"
  },
  "resolution": "Zero over zero carries no value. Rewritten as \\(\\frac{x+3}{x-4}\\), the quotient gives \\(-\\frac{5}{2}\\) at 2.",
  "sources": [
   "BC-CON-01008",
   "research/units/unit-01-limits-continuity.md#1.6 Determining Limits Using Algebraic Manipulation"
  ]
 },
 "no_figure_reason": "A symbolic rewriting rule. No skill carries a figure-bearing representation and the key idea describes no process to watch, so text and the step reveal serve.",
 "orientation": {
  "text": "A response shows substitution giving zero over zero, the numerator limit and denominator limit written separately, then rewrites the quotient into an equivalent form and evaluates it at the target.",
  "sources": [
   "BC-CON-01008",
   "research/units/unit-01-limits-continuity.md#1.6 Determining Limits Using Algebraic Manipulation",
   "sg-23:14"
  ]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-LIM-1E1",
   "depth": "core",
   "text": "Zero over zero carries no value, so the expression is rewritten as an equivalent form: factor out a common factor, use a conjugate, or use an alternate trigonometric form. The rewrite agrees with the original near the target, which is all the limit uses.",
   "notation": "indeterminate form zero over zero",
   "quote": null,
   "sources": [
    "BC-EK-LIM-1E1",
    "ced:43",
    "research/units/unit-01-limits-continuity.md#1.6 Determining Limits Using Algebraic Manipulation"
   ]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-01004",
   "cue": "A quotient that gives zero over zero.",
   "method": "Substitute, writing both limits separately.",
   "rival": "Declaring no limit on seeing zero over zero.",
   "separating_feature": "Zero over zero signals a rewrite; nonzero over zero does not.",
   "sources": [
    "BC-QA-01004",
    "BC-ERR-01009"
   ],
   "evidence_tag": "verified",
   "contrast": {
    "this": {
     "text": "Find \\(\\lim_{x\\to3}\\frac{x^2-9}{x-3}\\).",
     "archetype_id": "BC-QA-01004"
    },
    "not_this": {
     "text": "Find \\(\\lim_{x\\to3}\\frac{x^2+1}{x-3}\\).",
     "why_not": "Substitution gives 10 over 0, not zero over zero."
    },
    "feature": "Both top and bottom vanish at the target."
   }
  }
 ],
 "worked_examples": [
  {
   "id": "ex-1",
   "archetype_id": "BC-QA-01004",
   "bands": [
    "low",
    "mid"
   ],
   "parameter_draw": {
    "target": 2,
    "top_root": -3,
    "bottom_root": 4,
    "state_form": "stated"
   },
   "problem": {
    "text": "Find \\(\\lim_{x\\to2}\\frac{x^2+x-6}{x^2-6x+8}\\), showing the indeterminate form.",
    "command_verb": "find"
   },
   "calculator_status": "no_calculator",
   "steps": [
    {
     "cue": "The stem gives a quotient at \\(x=2\\): substitute into top and bottom separately.",
     "why": "\\(\\lim_{x\\to2}(x^2+x-6)=0\\) and \\(\\lim_{x\\to2}(x^2-6x+8)=0\\): zero over zero, so rewrite.",
     "expr": "(x**2+x-6)/(x**2-6*x+8)",
     "relation": "new"
    },
    {
     "cue": "Both polynomials vanish at 2, so each carries the factor \\(x-2\\).",
     "why": "Factoring exposes the common factor that produced zero over zero.",
     "expr": "(x-2)*(x+3)/((x-2)*(x-4))",
     "relation": "equivalent"
    },
    {
     "cue": "The same factor \\(x-2\\) multiplies top and bottom.",
     "why": "Dividing it out is valid for \\(x\\ne2\\), which is every input the limit uses.",
     "expr": "(x+3)/(x-4)",
     "relation": "equivalent"
    },
    {
     "cue": "The simplified quotient is defined at 2, so substitute.",
     "why": "\\(\\frac{5}{-2}\\) is the limit of the original quotient.",
     "expr": "-5/2",
     "relation": "limit",
     "variable": "x",
     "point": "2"
    }
   ],
   "answer": {
    "form": "numeric",
    "expr": "-5/2"
   }
  }
 ],
 "what_a_reader_scores": [],
 "common_errors": [
  {
   "error_id": "BC-ERR-01008",
   "observed_behavior": "The response reports zero because the numerator tends to zero, without attending to the denominator.",
   "scoring_consequence": "The value point is lost and the rewriting step is absent.",
   "wrong_step": {
    "text": "The numerator tends to 0, so the limit is reported as 0.",
    "expr": "0"
   },
   "right_step": {
    "text": "The denominator also tends to 0; the rewritten form gives \\(-\\frac{5}{2}\\).",
    "expr": "-5/2"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-01006",
    "text": "the symbol zero over zero as an answer, reading it as zero"
   },
   "sources": [
    "BC-ERR-01008",
    "BC-MIS-01006"
   ],
   "fix_prompt": true
  },
  {
   "error_id": "BC-ERR-01009",
   "observed_behavior": "The response states that the limit does not exist because substitution gives zero over zero.",
   "scoring_consequence": "The value point and the rewriting point are lost.",
   "wrong_step": {
    "text": "Substitution gives zero over zero, so the limit is reported not to exist.",
    "expr": "nan"
   },
   "right_step": {
    "text": "Zero over zero calls for rewriting; the limit is \\(-\\frac{5}{2}\\).",
    "expr": "-5/2"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-01006",
    "text": "a nonexistence verdict rather than as a signal to rewrite"
   },
   "sources": [
    "BC-ERR-01009",
    "BC-MIS-01006"
   ],
   "fix_prompt": true
  },
  {
   "error_id": "BC-ERR-01010",
   "observed_behavior": "The response divides out a summand common to numerator and denominator rather than a factor.",
   "scoring_consequence": "The rewriting point and the value point are both lost because the expressions are not equivalent.",
   "wrong_step": {
    "text": "The \\(x^2\\) terms are cancelled, leaving \\(\\frac{x-6}{-6x+8}\\), which gives 1 at 2.",
    "expr": "(x-6)/(-6*x+8)"
   },
   "right_step": {
    "text": "The factor \\(x-2\\) is divided out, leaving \\(\\frac{x+3}{x-4}\\).",
    "expr": "(x+3)/(x-4)"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-01007",
    "text": "terms are cancelled like factors"
   },
   "sources": [
    "BC-ERR-01010",
    "BC-MIS-01007"
   ],
   "fix_prompt": true
  },
  {
   "error_id": "BC-ERR-01011",
   "observed_behavior": "The response presents the limit explicitly set equal to the symbol zero over zero rather than presenting the limits of numerator and denominator separately.",
   "scoring_consequence": "The point for establishing the form is not earned by a limit presented as equal to zero over zero; two separate limits are required (sg-23:14).",
   "wrong_step": {
    "text": "One line: \\(\\lim_{x\\to2}\\frac{x^2+x-6}{x^2-6x+8}=\\frac{0}{0}\\).",
    "expr": "0/0"
   },
   "right_step": {
    "text": "Two lines: \\(\\lim_{x\\to2}(x^2+x-6)=0\\) and \\(\\lim_{x\\to2}(x^2-6x+8)=0\\).",
    "expr": "0"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-99011",
    "text": "uses the equals sign to join successive lines of work"
   },
   "sources": [
    "BC-ERR-01011",
    "BC-MIS-99011"
   ],
   "fix_prompt": true
  }
 ],
 "representations": null,
 "prerequisite_bridges": [
  {
   "prq_id": "BC-PRQ-01001",
   "text": "Factor, then cancel a common factor. Stopping at zero over zero unfactored marks this gap."
  },
  {
   "prq_id": "BC-PRQ-01002",
   "text": "A conjugate clears a radical difference. Leaving the radical and reporting no limit marks this gap."
  },
  {
   "prq_id": "BC-PRQ-01005",
   "text": "Sine and cosine stay between \\(-1\\) and 1. Treating them as unbounded marks this gap."
  },
  {
   "prq_id": "BC-PRQ-01007",
   "text": "Clear nested fractions with a common denominator. Leaving them nested marks this gap."
  }
 ],
 "time": {
  "exam_part": "I-A",
  "budget_minutes": 2.14,
  "source": "research/exam/exam-structure.md#Section and part layout",
  "written_steps": {
   "ex-1": [
    1,
    3,
    4
   ]
  },
  "skipped_steps": {
   "ex-1": [
    2
   ]
  }
 },
 "checks": [
  {
   "id": "chk-1",
   "check_kind": "completion",
   "format": "short_answer",
   "bands": [
    "low",
    "mid"
   ],
   "archetype_id": "BC-QA-01004",
   "parameter_draw": {
    "target": 2,
    "top_root": -3,
    "bottom_root": 4,
    "state_form": "stated"
   },
   "completes": "ex-1",
   "stem": {
    "text": "Dividing out \\(x-2\\) leaves \\(\\frac{x+3}{x-4}\\) for \\(x\\ne2\\). Find \\(\\lim_{x\\to2}\\frac{x^2+x-6}{x^2-6x+8}\\).",
    "command_verb": "find"
   },
   "key": {
    "form": "numeric",
    "expr": "-5/2"
   },
   "steps": [
    {
     "text": "The simplified quotient \\(\\frac{x+3}{x-4}\\).",
     "expr": "(x+3)/(x-4)",
     "relation": "new"
    },
    {
     "text": "Substituting 2 gives \\(-\\frac{5}{2}\\).",
     "expr": "-5/2",
     "relation": "limit",
     "variable": "x",
     "point": "2"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-01024"
   ]
  },
  {
   "id": "chk-2",
   "check_kind": "isomorph",
   "format": "short_answer",
   "bands": [
    "low",
    "mid"
   ],
   "archetype_id": "BC-QA-01004",
   "parameter_draw": {
    "target": -1,
    "top_root": 3,
    "bottom_root": 2,
    "state_form": "silent"
   },
   "stem": {
    "text": "Find \\(\\lim_{x\\to-1}\\frac{x^2-2x-3}{x^2-x-2}\\).",
    "command_verb": "find"
   },
   "key": {
    "form": "numeric",
    "expr": "4/3"
   },
   "steps": [
    {
     "text": "Substitution gives zero over zero.",
     "expr": "(x**2-2*x-3)/(x**2-x-2)",
     "relation": "new"
    },
    {
     "text": "Factor top and bottom.",
     "expr": "(x+1)*(x-3)/((x+1)*(x-2))",
     "relation": "equivalent"
    },
    {
     "text": "Divide out \\(x+1\\).",
     "expr": "(x-3)/(x-2)",
     "relation": "equivalent"
    },
    {
     "text": "Substitute \\(-1\\).",
     "expr": "4/3",
     "relation": "limit",
     "variable": "x",
     "point": "-1"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-01024",
    "BC-SKL-01028"
   ]
  },
  {
   "id": "chk-3",
   "check_kind": "mcq",
   "format": "mcq",
   "bands": [
    "low"
   ],
   "archetype_id": "BC-QA-01004",
   "parameter_draw": {
    "target": 3,
    "top_root": 1,
    "bottom_root": -2,
    "state_form": "stated"
   },
   "stem": {
    "text": "What is \\(\\lim_{x\\to3}\\frac{x^2-4x+3}{x^2-x-6}\\)?",
    "command_verb": "find"
   },
   "key": {
    "form": "numeric",
    "expr": "2/5"
   },
   "steps": [
    {
     "text": "Substitution gives zero over zero.",
     "expr": "(x**2-4*x+3)/(x**2-x-6)",
     "relation": "new"
    },
    {
     "text": "Divide out \\(x-3\\).",
     "expr": "(x-1)/(x+2)",
     "relation": "equivalent"
    },
    {
     "text": "Substitute 3.",
     "expr": "2/5",
     "relation": "limit",
     "variable": "x",
     "point": "3"
    }
   ],
   "options": [
    {
     "id": "A",
     "is_key": false,
     "expr": "0",
     "label": "0",
     "error_path": "BC-ERR-01008",
     "derivation": "the numerator limit alone"
    },
    {
     "id": "B",
     "is_key": true,
     "expr": "2/5",
     "label": "\\(\\frac{2}{5}\\)",
     "error_path": null
    },
    {
     "id": "C",
     "is_key": false,
     "expr": "1",
     "label": "1",
     "error_path": "BC-ERR-01010",
     "derivation": "x squared terms cancelled: (-4x+3)/(-x-6) at 3"
    },
    {
     "id": "D",
     "is_key": false,
     "expr": "nan",
     "label": "The limit does not exist",
     "error_path": "BC-ERR-01009",
     "derivation": "zero over zero read as nonexistence"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-01024"
   ]
  }
 ],
 "delivery": [
  {
   "block": "orientation",
   "mode": "text",
   "reason": "rule 5: BC-SKL-01024 to 01028 carry BC-REP-01 and BC-REP-04 only (unit-01 README delivery map)",
   "sources": [
    "BC-SKL-01028"
   ]
  },
  {
   "block": "ki-1",
   "mode": "text",
   "reason": "rule 5: an algebraic equivalence with no figure-bearing BC-REP on the skills; the rewriting lives in the step_reveal example",
   "sources": [
    "BC-SKL-01024"
   ]
  },
  {
   "block": "ex-1",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-01008",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-01009",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-01010",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-01011",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  }
 ],
 "refresher": [
  "ki-1",
  "err-BC-ERR-01008",
  "err-BC-ERR-01009",
  "err-BC-ERR-01010",
  "err-BC-ERR-01011",
  "ex-1"
 ],
 "research_lines": [
  {
   "file": "research/units/unit-01-limits-continuity.md",
   "line": "MCQ forms present a quotient that is indeterminate under substitution and ask for its value."
  },
  {
   "file": "research/question-analysis/question-archetypes.md",
   "line": "the form is established by presenting the two limits separately (sg-23:14)"
  }
 ],
 "inferred": [
  {
   "claim": "A fluent solver holds the factor search in the head and writes the separate limits, the cancelled form and the value.",
   "settles": "Timed think-aloud or response logs on BC-QA-01004 items showing which lines are written."
  },
  {
   "claim": "The parameter_spec notes fix the quotient shape as (x - target)(x - top_root) over (x - target)(x - bottom_root), both expanded; the check draws follow that shape.",
   "settles": "The item template under app/generation/templates for BC-QA-01004 confirming the expanded form."
  }
 ],
 "sources": [
  "BC-CON-01008",
  "BC-SKL-01024",
  "BC-SKL-01025",
  "BC-SKL-01026",
  "BC-SKL-01027",
  "BC-SKL-01028",
  "BC-EK-LIM-1E1",
  "ced:43",
  "sg-23:14",
  "BC-QA-01004",
  "BC-MCQ-CED-001",
  "BC-MCQ-SAMPLE-002",
  "BC-ERR-01008",
  "BC-ERR-01009",
  "BC-ERR-01010",
  "BC-ERR-01011",
  "BC-MIS-01006",
  "BC-MIS-01007",
  "BC-MIS-99011",
  "BC-PRQ-01001",
  "BC-PRQ-01002",
  "BC-PRQ-01005",
  "BC-PRQ-01007",
  "research/units/unit-01-limits-continuity.md#1.6 Determining Limits Using Algebraic Manipulation",
  "research/question-analysis/question-archetypes.md#BC-QA-01004 Indeterminate limit resolved by algebraic rewriting",
  "research/exam/exam-structure.md#Section and part layout"
 ],
 "read_minutes": {
  "full": 3.8,
  "brief": 2.9
 },
 "word_count": {
  "full": 568,
  "brief": 434
 }
}
```
