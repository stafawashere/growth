---
title: LSN-CON-01003 Limit notation and its reading
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-01003, reading and writing limit notation with its one sided arrows and infinity symbols, built from authoring_bundle("BC-CON-01003") and the research files it cites, so an author fills plan 15's lesson record without making a teaching decision.
---

# LSN-CON-01003 Limit notation and its reading

Concept BC-CON-01003 (skills BC-SKL-01005, BC-SKL-01007), topics 1.2 and 1.9 of Unit 1, loaded by one archetype, BC-QA-01013 (family representation-consistency). It is a root of the unit's concept order (docs/lessons/unit-01/README.md, section 1). The concept holds no active error, so the lesson has no error blocks and two checks.

## Prediction

Served first in both bands. Multiple choice on ex-1's own statement: the limit of \(g(x)\) as \(x\) approaches \(-3\) from the right is negative infinity, and the student picks what the graph does near \(x=-3\) from a vertical asymptote falling on the right (key), a horizontal asymptote at \(y=-3\) and a lowest point at \(x=-3\). The resolution states that infinity as the value claims outputs unbounded near a vertical line. Sources: BC-CON-01003 and the topic 1.9 section that ki-1 cites. Delivery: text.

## Orientation

Served text (27 words), from BC-CON-01003 `description_plain` and the Assessment behaviour paragraphs of topics 1.2 and 1.9, which ask which notation records a described behaviour, what a written statement claims, and which representation matches a stated limit behaviour (research/units/unit-01-limits-continuity.md#1.2 Defining Limits and Using Limit Notation; research/units/unit-01-limits-continuity.md#1.9 Connecting Multiple Representations of Limits). No count, no frequency.

## Key ideas

Both skills map one BC-EK, BC-EK-LIM-1A1 (ced:39; BC-SKL-01007 also cites ced:40), so one core block, both bands.

- ki-1 (core, BC-EK-LIM-1A1). A limit statement names the input approached, the side (a minus superscript for the left, a plus for the right, none for both) and the value; infinity as the value and infinity under the arrow make different claims. Paraphrased from the topic 1.2 Notation paragraph and the topic 1.9 paragraph "What conversion must not lose". No quote. Notation from the concept record: lim as x approaches c from the left; lim as x approaches c from the right.

## Recognition

- BC-QA-01013 (research/question-analysis/question-archetypes.md#BC-QA-01013 Limit claim matched across graphical, numerical, and analytic representations): `typical_wording` "Which of the given representations is consistent with the stated limit behaviour of f at the named input?"; `common_givens` a limit fact in one representation and candidate graphical, numerical or analytic representations; `asked_to_produce` the representation that matches. The signal is a written limit, often with an infinity symbol or a superscript sign, and options that restate it in another form. MCQ only (`multipart_structure`); the topic 1.2 paragraph adds FRQ parts where a limit expression must be written inside a larger argument, with a separate point for presenting it (sg-25:4).

The contrast pair on st-1 takes its near miss from the wrong approach in BC-ERR-01033 and the unit README's neighbour table (BC-MIS-01018 probe): the same statement written once with infinity as the value at a finite input and once with infinity under the arrow. The separating feature is where the infinity symbol sits.

What says "not this concept": a stem that asks for the value of a limit from a graph or rule, not for what a statement claims, belongs to BC-CON-01002, 01004 or 01006.

## Method choice

One strategy block, both bands.

- st-1, BC-QA-01013. Cue from `common_givens`. Method, `expected_solution_path[0]`: read the limit behaviour from the supplied representation; the first written line names input, side and value, served without a label. Rival, `wrong_approaches`: reading a vertical asymptote statement as end behaviour or the reverse (BC-ERR-01033). Separating feature: where the infinity symbol sits, in the value or under the arrow (the unit README's neighbour table, BC-MIS-01018 probe).

The archetype carries `asked_to_produce` and `common_givens` in the snapshot, so the block is verified.

## Solution path

- ex-1, BC-QA-01013, both bands, no calculator. Draw: number -3, side right, growth down, direction negative, letter g, statement infinite_limit, giving the statement that the limit of \(g(x)\) as \(x\) approaches \(-3\) from the right is negative infinity. Steps follow `expected_solution_path`: read the side (no value), read the value (no value), test the candidates (no value), select the match (valued, the line \(x=-3\), new). The answer is a statement, a vertical asymptote at \(x=-3\) with \(g\) falling to its right, carrying the invariant "'asymptote' in key".

On an MCQ a fluent solver writes nothing: the neutral statement of the behaviour is held in the head (docs/lessons/unit-01/README.md, section 5) [inferred].

## Scoring

None. BC-QA-01013 lists no `point_types`, so the lesson carries no scoring entry and says nothing about points (plan 15, R14).

## Traps

None. BC-CON-01003 holds no active error: no BC-ERR record's skills meet BC-SKL-01005 or BC-SKL-01007, so `common_errors` is empty and no check carries a distractor. The concept's misconception BC-MIS-01018 is linked only to errors of other concepts (BC-ERR-01021, BC-ERR-01033), whose blocks sit in the lessons on BC-CON-01011 and BC-CON-01017.

## Representations

None. The topic 1.9 Representations paragraph lists conversions among four representations, but both skills carry BC-REP-01 and BC-REP-04 only, and the lesson reads symbols into words.

## Prerequisite bridge

One bridge, BC-PRQ-06005 (supporting parent of both skills), gated by state.

## Time

BC-QA-01013 is `no_calculator` and a single MCQ, so the part is Section I Part A, 2.14 minutes (research/exam/exam-structure.md#Section and part layout). The reading of input, side and value is done without writing; the minutes go to testing each option against the three.

## Checks

- chk-1, completion of ex-1, both bands: the side and the value are given, the student names the line. Key the statement \(x=-3\), a vertical asymptote, equal to ex-1's answer.
- chk-2, isomorph on BC-QA-01013, both bands: number 5/2, side left, statement limit_at_infinity, the limit of \(h(x)\) as \(x\) decreases without bound is 5/2. Key the statement \(y=5/2\), a horizontal asymptote on the left end.

Two checks: with no error block, a 4-option MCQ has no error paths to carry.

## Delivery

- orientation, ki-1: text. Rule 5; BC-SKL-01005 and BC-SKL-01007 carry BC-REP-01 and BC-REP-04 only, and the unit README's delivery map picks text.
- ex-1: step_reveal, rule 1.

No non-text mode applies: notation read into words has no process to watch and no figure-bearing representation on the skills. Figure presence: the record carries `no_figure_reason`, since none of rules 2 to 5 selects a drawn block for this concept.

## Band plan

- Low (full), served order: prediction, orientation, bridge when gated, ki-1, st-1 with its contrast pair, ex-1, chk-1, chk-2. No error blocks, no second example, no representations block.
- Mid (brief): the same blocks; with one core key idea, one strategy block, one example, no error blocks and two checks, the two bands serve the same words.
- Totals: full 436 words, 2.95 minutes (cap 900 and 6); brief 436 words, 2.95 minutes (cap 450 and 3).
- Refresher: ki-1, ex-1.

## Sources

- BC-CON-01003; BC-SKL-01005, BC-SKL-01007; BC-EK-LIM-1A1; ced:39, ced:40
- BC-QA-01013; BC-MIS-01018; BC-ERR-01033, BC-ERR-01021
- Prediction pr-1 and the contrast pair: BC-CON-01003, BC-ERR-01033
- BC-PRQ-06005
- sg-25:4
- research/units/unit-01-limits-continuity.md#1.2 Defining Limits and Using Limit Notation
- research/units/unit-01-limits-continuity.md#1.9 Connecting Multiple Representations of Limits
- research/question-analysis/question-archetypes.md#BC-QA-01013 Limit claim matched across graphical, numerical, and analytic representations
- research/exam/exam-structure.md#Section and part layout
- [inferred] The spec parameter side read as the end of the axis for a limit at infinity statement (left for x decreasing without bound). Settled by the generation template for BC-QA-01013.
- [inferred] Nothing is written on the MCQ. Settled by timing in the modality A/B.
- Library gap: no active BC-ERR meets BC-SKL-01005 or BC-SKL-01007, so the lesson carries no error block and two checks.

## Machine record

```json
{
 "id": "LSN-CON-01003",
 "kind": "concept",
 "target_id": "BC-CON-01003",
 "unit": "01",
 "skills": [
  "BC-SKL-01005",
  "BC-SKL-01007"
 ],
 "prediction": {
  "id": "pr-1",
  "stem": {
   "text": "Predict. The limit of g(x) as x approaches -3 from the right is negative infinity. What does the graph of g do near x = -3?",
   "command_verb": "predict"
  },
  "format": "mcq",
  "options": [
   {
    "id": "A",
    "label": "A vertical asymptote at x = -3, falling on the right",
    "is_key": true
   },
   {
    "id": "B",
    "label": "A horizontal asymptote at y = -3",
    "is_key": false
   },
   {
    "id": "C",
    "label": "A lowest point at x = -3",
    "is_key": false
   }
  ],
  "resolution": "Infinity as the value claims outputs unbounded near a vertical line, so g falls without bound beside x = -3.",
  "sources": [
   "BC-CON-01003",
   "research/units/unit-01-limits-continuity.md#1.9 Connecting Multiple Representations of Limits"
  ]
 },
 "no_figure_reason": "Neither skill carries a figure-bearing representation, and the key idea is a reading rule for symbols with no process in it, so no drawn block fits.",
 "orientation": {
  "text": "A response turns a described approach into limit symbols, or a written limit into words, keeping the input, the side the arrow names and the claimed value.",
  "sources": [
   "BC-CON-01003",
   "research/units/unit-01-limits-continuity.md#1.2 Defining Limits and Using Limit Notation",
   "research/units/unit-01-limits-continuity.md#1.9 Connecting Multiple Representations of Limits"
  ]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-LIM-1A1",
   "depth": "core",
   "text": "A limit statement names three things: the input x approaches, the side (a minus superscript for the left, a plus for the right, none for both) and the claimed value. Infinity as the value claims outputs unbounded near a vertical line; infinity under the arrow claims end behaviour.",
   "notation": "lim as x approaches c from the left; lim as x approaches c from the right",
   "quote": null,
   "sources": [
    "BC-EK-LIM-1A1",
    "ced:39",
    "research/units/unit-01-limits-continuity.md#1.9 Connecting Multiple Representations of Limits"
   ]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-01013",
   "cue": "A limit fact in one form, with candidate sentences, graphs or tables to match against it.",
   "method": "Read the statement as input, side and value.",
   "rival": "Reading a vertical asymptote statement as end behaviour, or the reverse.",
   "separating_feature": "Where the infinity symbol sits: in the value, or under the arrow.",
   "sources": [
    "BC-QA-01013",
    "BC-ERR-01033"
   ],
   "evidence_tag": "verified",
   "contrast": {
    "this": {
     "text": "The limit of h(x) as x approaches 4 from the left is infinity. Which statement describes the graph of h?",
     "archetype_id": "BC-QA-01013"
    },
    "not_this": {
     "text": "The limit of h(x) as x approaches infinity is 4. Which statement describes the graph of h?",
     "why_not": "Infinity sits under the arrow, so it claims end behaviour, not a vertical line."
    },
    "feature": "Where the infinity symbol sits: in the value or under the arrow."
   }
  }
 ],
 "worked_examples": [
  {
   "id": "ex-1",
   "archetype_id": "BC-QA-01013",
   "bands": [
    "low",
    "mid"
   ],
   "parameter_draw": {
    "number": -3,
    "side": "right",
    "growth": "down",
    "direction": "negative",
    "letter": "g",
    "statement": "infinite_limit"
   },
   "problem": {
    "text": "The limit of g(x) as x approaches -3 from the right is negative infinity. Which statement describes the graph of g?",
    "command_verb": "identify"
   },
   "calculator_status": "no_calculator",
   "steps": [
    {
     "cue": "The arrow carries a plus superscript.",
     "why": "Only inputs just above -3 are claimed about."
    },
    {
     "cue": "The value is negative infinity.",
     "why": "Outputs decrease without bound; infinity in the value signals a vertical line."
    },
    {
     "cue": "Test each option against input -3, right side, unbounded below.",
     "why": "An option putting infinity under the arrow describes end behaviour and fails."
    },
    {
     "cue": "One option keeps all three.",
     "why": "The line x = -3 is a vertical asymptote, with g falling on its right.",
     "expr": "x = -3",
     "relation": "new"
    }
   ],
   "answer": {
    "form": "statement",
    "expr": "x = -3",
    "text": "The line x = -3 is a vertical asymptote of the graph of g, which decreases without bound as x approaches -3 from the right."
   }
  }
 ],
 "what_a_reader_scores": [],
 "common_errors": [],
 "representations": null,
 "prerequisite_bridges": [
  {
   "prq_id": "BC-PRQ-06005",
   "text": "Reading a limit statement rests on reading function notation: which letter is the function and which number is the input. The failure: a value taken for the wrong input."
  }
 ],
 "time": {
  "exam_part": "I-A",
  "budget_minutes": 2.14,
  "source": "research/exam/exam-structure.md#Section and part layout",
  "written_steps": {
   "ex-1": []
  },
  "skipped_steps": {
   "ex-1": [
    1,
    2,
    3,
    4
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
   "archetype_id": "BC-QA-01013",
   "parameter_draw": {
    "number": -3,
    "side": "right",
    "growth": "down",
    "direction": "negative",
    "letter": "g",
    "statement": "infinite_limit"
   },
   "completes": "ex-1",
   "stem": {
    "text": "The limit of g(x) as x approaches -3 from the right is negative infinity. Name the asymptote of the graph of g.",
    "command_verb": "name"
   },
   "key": {
    "form": "statement",
    "expr": "x = -3",
    "text": "x = -3, a vertical asymptote"
   },
   "steps": [
    {
     "text": "Infinity is the value and -3 is the input, so the line is vertical at -3.",
     "expr": "x = -3",
     "relation": "new"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-01007"
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
   "archetype_id": "BC-QA-01013",
   "parameter_draw": {
    "number": "5/2",
    "side": "left",
    "growth": "up",
    "direction": "positive",
    "letter": "h",
    "statement": "limit_at_infinity"
   },
   "stem": {
    "text": "The limit of h(x) as x decreases without bound is 5/2. Name the asymptote of the graph of h.",
    "command_verb": "name"
   },
   "key": {
    "form": "statement",
    "expr": "y = 5/2",
    "text": "y = 5/2, a horizontal asymptote at the left end"
   },
   "steps": [
    {
     "text": "Infinity sits under the arrow and 5/2 is the value, so the line is horizontal at 5/2.",
     "expr": "y = 5/2",
     "relation": "new"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-01005"
   ]
  }
 ],
 "delivery": [
  {
   "block": "orientation",
   "mode": "text",
   "reason": "rule 5: BC-SKL-01005 carries BC-REP-01 and BC-REP-04 only; unit README delivery map",
   "sources": [
    "BC-SKL-01005"
   ]
  },
  {
   "block": "ki-1",
   "mode": "text",
   "reason": "rule 5: notation read into words, BC-REP-01 and BC-REP-04 only",
   "sources": [
    "BC-SKL-01005",
    "BC-SKL-01007"
   ]
  },
  {
   "block": "ex-1",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  }
 ],
 "refresher": [
  "ki-1",
  "ex-1"
 ],
 "read_minutes": {
  "full": 2.95,
  "brief": 2.95
 },
 "word_count": {
  "full": 436,
  "brief": 436
 },
 "research_lines": [
  {
   "file": "research/units/unit-01-limits-continuity.md",
   "line": "the distinction between an infinite limit and a limit at infinity"
  }
 ],
 "inferred": [
  {
   "claim": "The parameter side is read as the end of the axis for a limit at infinity statement, left meaning x decreases without bound.",
   "settles": "The generation template for BC-QA-01013 under app/generation/templates."
  },
  {
   "claim": "On the MCQ a fluent solver writes no step.",
   "settles": "Timing of written against held steps in the modality A/B."
  },
  {
   "claim": "Two checks, because the concept holds no active error to anchor MCQ distractors.",
   "settles": "A BC-ERR record whose skills include BC-SKL-01005 or BC-SKL-01007."
  }
 ],
 "sources": [
  "BC-CON-01003",
  "BC-SKL-01005",
  "BC-SKL-01007",
  "BC-EK-LIM-1A1",
  "ced:39",
  "ced:40",
  "BC-QA-01013",
  "BC-MIS-01018",
  "BC-ERR-01033",
  "BC-PRQ-06005",
  "sg-25:4",
  "research/units/unit-01-limits-continuity.md#1.2 Defining Limits and Using Limit Notation",
  "research/units/unit-01-limits-continuity.md#1.9 Connecting Multiple Representations of Limits",
  "research/exam/exam-structure.md#Section and part layout"
 ]
}
```
