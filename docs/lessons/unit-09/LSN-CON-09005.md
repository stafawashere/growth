---
title: LSN-CON-09005 Vector-valued function as a pair of component functions
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-09005, a vector-valued function as a pair of component functions written with the horizontal entry first and labelled, built from authoring_bundle("BC-CON-09005") and the research files it cites, so an author fills plan 15's lesson record without making a teaching decision.
---

# LSN-CON-09005 Vector-valued function as a pair of component functions

Concept BC-CON-09005 (skill BC-SKL-09018), topic 9.4 of Unit 9, BC only (ced:174), loaded by BC-QA-09004 and BC-QA-09005 (family parametric-motion). The skill is not independently assessable, so the lesson works inside the acceleration shape of BC-QA-09004 and stresses this concept's own move: the pair of component functions written as one vector, horizontal entry first and labelled.

## Prediction

Served first, both bands: an `mcq` on ex-1's own functions. The core claim is that a vector-valued function is its two components in a fixed order, horizontal first. Key A, the pair \(\langle x''(2), y''(2)\rangle\). The distractors are the pair with the position component first (the swapped conversion, BC-SIG-09222) and a single summed number. The convention of an ordered pair answers it before any rule is taught. The resolution states the pair form with no verdict word. Source: BC-CON-09005 and the topic section the key idea cites.

## Orientation

Served text, from BC-CON-09005 `description_plain` (a vector function is just two ordinary functions written together) and the topic's Assessment behaviour paragraph (research/units/unit-09-parametric-polar-vector.md#9.4 Defining and Differentiating Vector-Valued Functions): MCQ forms ask for a vector at a time, and the free-response opener scores one point per component with its setup (sg-23:5). The orientation states what a response shows: the pair, in order, with each derivative visible. No count, no frequency.

## Key ideas

One BC-EK, BC-EK-CHA-3H1 (ced:174), maps the one skill, so one core block, both bands. ki-1 paraphrases the Required mathematical knowledge paragraphs Vector derivative and Notation (the components must be identifiable) and the concept's `description_formal`. Horizontal first is from the skill's `mastered_if`. No anchor quote: the CHA-3.H.1 sentence on ced:174 is about derivatives and adds nothing the paraphrase lacks. Notation line: the concept's `notation`.

## Recognition

BC-QA-09004 (research/question-analysis/question-archetypes.md#BC-QA-09004 Acceleration vector of a particle in planar motion) is the archetype that fixes the notation demand; BC-QA-09005 also lists the skill and is taught under BC-CON-09008.

- `common_givens`: a velocity vector or a pair of component rates, and a time. `asked_to_produce`: two derivative expressions and a labelled vector of two values. `typical_wording`: find the acceleration vector of the particle at the given time and show the setup for the calculations.
- The signal in the stem: the words acceleration vector, or two components asked for by name. The difficulty variable is whether the notation must be a vector or may be two labelled numbers.
- Shapes: the opening part of the calculator active free response, BC-FRQ-2013-Q2-C, BC-FRQ-2022-Q2-B, BC-FRQ-2023-Q2-A.

The near miss of the contrast pair is the speed stem, from BC-QA-09006 (outside the block's archetype), which shares the velocity components and the time and differs in asking for one magnitude. The `common_distractors` entry "the magnitude of the acceleration" is the same confusion.

## Method choice

- st-1, BC-QA-09004. Cue from `common_givens` and `asked_to_produce`. Method, `expected_solution_path` in order: differentiate each component, evaluate at the time, present the pair as a vector. Rival: `wrong_approaches` "reporting an unsupported vector" and the `common_distractors` "components in the wrong order". Separating feature: the request names a vector. Both cue fields exist, so the block is not inferred. The block carries the contrast pair, a vector stem beside a speed stem. No served field opens with a label.

## Solution path

- ex-1, BC-QA-09004, both bands, calculator. Draw: amplitude 2, growth 1/3, log_scale 2, linear -1, time 2, position_axis y, notation vector. \(x'(t)=2e^{t/3}\sin t\), \(y(t)=2\ln(1+t^2)-t\); the acceleration is \(\langle -0.440, -0.480\rangle\), computed with SymPy, \(y''(2)=-12/25\) exactly. No published item on BC-QA-09004 carries this draw (content/items_gen_unit09, ITM-GEN-09004-00 to 21).
- No second worked example: the concept's one skill is a notation conversion, and the second example would repeat the derivative steps that BC-CON-09006 teaches. The lesson carries no faded example.
- Steps follow `expected_solution_path`: both component derivatives with their evaluations, then the pair. A fluent solver writes the derivatives, the values and the labelled vector, and holds the given rates and the recognition step.
- No productive-failure comparison: BC-CON-09005 is not in `PRODUCTIVE_FAILURE_TARGETS`.

## Scoring

BC-QA-09004 lists BC-PT-99064, 99052, 99050, 99005. ex-1 tags BC-PT-99064 only, the labelled values point, which is this concept's own point; BC-PT-99052 (component setup) and BC-PT-99005 belong to BC-CON-09006 and are left untagged to keep the brief band inside its cap. The line is `reader_checks` output.

Point losses from research: an unsupported correct vector earns one of two points and reversed components lose both (BC-PT-99052 `not_earned_by`, sg-22:7); unlabelled pairs are read left to right and top to bottom (sg-22:10) (research/scoring/common-point-losses.md#Precision and presentation points).

## Traps

One error meets the skill, BC-ERR-09017, linked to BC-MIS-09009 and BC-MIS-99011. Low and mid band both show it. The wrong step is the pair with the two values exchanged, the right step the horizontal value first, both on ex-1's draw; `fix_prompt` true, since the pairs are distinct. Possible reason from BC-MIS-09009. The other errors on BC-QA-09004 (BC-ERR-99029, 99002, 99019, 99021) attach to BC-SKL-09016, 09017 and 09028 and are taught in BC-CON-09006 and BC-CON-09009.

## Representations

None. The topic's Representations paragraph names the conversion from a parametric pair to a vector-valued function; the drawn blocks (orientation, ki-1) already carry it, and a third figure would exceed the band caps.

## Prerequisite bridge

- BC-PRQ-09001, from its `description_plain` and `failure_signature`, gated by state.

## Time

BC-QA-09004 is an MCQ in Section I Part B, 2.92 minutes (research/exam/exam-structure.md#Section and part layout); as the opening free response part it scores 2 points, 3.33 minutes (docs/lessons/unit-09/README.md, section 5). A fluent solver writes the two derivatives, the two values and the labelled pair; the given rates and the recognition step are held [inferred]. No target.

## Checks

- chk-1, completion of ex-1, both bands: the two values given, the pair asked. Key the labelled vector.
- chk-2, isomorph, both bands, calculator. Draw: amplitude 4, growth 1/2, log_scale 1, linear 2, time 3/2, position_axis x, notation components. \(x(t)=2t+\ln(1+t^2)\), \(y'(t)=4e^{t/2}\sin t\); the acceleration is \(x''=-0.237\), \(y''=4.822\), each labelled.
- No chk-3: one error meets the skill, so three distractors each anchored to an error block cannot be built without stretching BC-ERR-09017 (inferred array). Checks stay at the minimum of two.

## Delivery

- orientation, ki-1: figure. Unit README section 6 names CHA-3H1 as a figure for BC-CON-09005; rule 4 of the TEMPLATE selection (the README's rule 3): BC-REP-12 and BC-REP-14 on BC-SKL-09018. Not promoted to interactive: the skill is a notation conversion and the stem asks for a written form, not a reading. The orientation shows the path with its point, ki-1 the vector with its two legs.
- ex-1, err-BC-ERR-09017: step_reveal. Rule 1.

## Band plan

- Low (full): prediction, orientation, bridge, ki-1, st-1 with the contrast pair, ex-1 and its line, chk-1, err-BC-ERR-09017, chk-2. 420 words, 2.8 minutes.
- Mid (brief): prediction, orientation, bridge, ki-1, st-1 with the contrast pair, ex-1 and its line, chk-1, err-BC-ERR-09017, chk-2. Every block is served in both bands, since the lesson has one example and one error. 420 words, 2.8 minutes.
- Refresher: ki-1, err-BC-ERR-09017, ex-1.

## Sources

- BC-CON-09005; BC-SKL-09018; BC-EK-CHA-3H1; ced:174
- BC-QA-09004, BC-QA-09005; BC-PT-99064
- BC-ERR-09017; BC-MIS-09009
- BC-PRQ-09001
- sg-23:5, sg-23:6, sg-22:7, sg-22:10, sg-25:18
- research/units/unit-09-parametric-polar-vector.md#9.4 Defining and Differentiating Vector-Valued Functions
- research/question-analysis/question-archetypes.md#BC-QA-09004 Acceleration vector of a particle in planar motion
- research/scoring/common-point-losses.md#Precision and presentation points
- research/exam/exam-structure.md#Section and part layout
- [inferred] The figure modes, the held steps and the two-check shape, each settled as the inferred array states.

## Machine record

```json
{
 "id": "LSN-CON-09005",
 "kind": "concept",
 "target_id": "BC-CON-09005",
 "unit": "09",
 "skills": [
  "BC-SKL-09018"
 ],
 "prediction": {
  "id": "pr-1",
  "stem": {
   "text": "A particle has \\(x'(t)=2e^{t/3}\\sin t\\) and \\(y(t)=2\\ln(1+t^2)-t\\). Predict how its acceleration at \\(t=2\\) is written.",
   "command_verb": "predict"
  },
  "format": "mcq",
  "options": [
   {
    "id": "A",
    "label": "\\(\\langle x''(2), y''(2)\\rangle\\)",
    "is_key": true
   },
   {
    "id": "B",
    "label": "\\(\\langle y''(2), x''(2)\\rangle\\)",
    "is_key": false
   },
   {
    "id": "C",
    "label": "\\(x''(2)+y''(2)\\)",
    "is_key": false
   }
  ],
  "resolution": "A vector-valued function is a pair of component functions, horizontal first, so \\(\\mathbf{a}(t)=\\langle x''(t), y''(t)\\rangle\\) and its value at \\(t=2\\) is an ordered pair.",
  "sources": [
   "BC-CON-09005",
   "research/units/unit-09-parametric-polar-vector.md#9.4 Defining and Differentiating Vector-Valued Functions"
  ]
 },
 "orientation": {
  "text": "A vector-valued function is two component functions written together, \\(\\langle x(t), y(t)\\rangle\\). A response gives its value at a time as an ordered pair or labelled components, with each derivative shown first.",
  "sources": [
   "BC-CON-09005",
   "research/units/unit-09-parametric-polar-vector.md#9.4 Defining and Differentiating Vector-Valued Functions"
  ]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-CHA-3H1",
   "depth": "core",
   "text": "A vector-valued function is a pair of functions, \\(\\mathbf{r}(t)=\\langle x(t), y(t)\\rangle\\), the parametric equations \\(x=x(t)\\), \\(y=y(t)\\) in one symbol. Derivatives act on each component. The components must be identifiable: horizontal first, or each labelled.",
   "notation": "ordered pair or angle bracket notation",
   "quote": null,
   "sources": [
    "BC-EK-CHA-3H1",
    "ced:174",
    "research/units/unit-09-parametric-polar-vector.md#9.4 Defining and Differentiating Vector-Valued Functions"
   ]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-09004",
   "cue": "Two component rates, a time, a labelled vector requested.",
   "method": "Differentiate each component, evaluate, write the pair horizontal first.",
   "rival": "Two unlabelled numbers in the order computed.",
   "separating_feature": "A vector request makes order and labels part of the answer.",
   "sources": [
    "BC-QA-09004"
   ],
   "evidence_tag": "verified",
   "contrast": {
    "this": {
     "text": "A particle has \\(x'(t)=3e^{t/2}\\sin t\\) and \\(y(t)=\\ln(1+t^2)+2t\\). Find its acceleration vector at \\(t=2\\).",
     "archetype_id": "BC-QA-09004"
    },
    "not_this": {
     "text": "A particle has \\(x'(t)=3e^{t/2}\\sin t\\) and \\(y'(t)=2\\sqrt{t}\\). Find its speed at \\(t=2\\).",
     "why_not": "Speed is one number, the magnitude, so no ordered pair is written."
    },
    "feature": "A vector request needs an ordered pair; a speed request needs one number."
   }
  }
 ],
 "worked_examples": [
  {
   "id": "ex-1",
   "archetype_id": "BC-QA-09004",
   "bands": [
    "low",
    "mid"
   ],
   "parameter_draw": {
    "amplitude": "2",
    "growth": "1/3",
    "log_scale": "2",
    "linear": "-1",
    "time": "2",
    "position_axis": "y",
    "notation": "vector"
   },
   "problem": {
    "text": "A particle has \\(x'(t)=2e^{t/3}\\sin t\\) and \\(y(t)=2\\ln(1+t^2)-t\\). Find its acceleration vector at \\(t=2\\), showing the setup.",
    "command_verb": "find"
   },
   "calculator_status": "calculator",
   "steps": [
    {
     "cue": "\\(x'\\) is given.",
     "why": "One derivative gives \\(x''\\).",
     "expr": "2*exp(t/3)*sin(t)",
     "relation": "new"
    },
    {
     "cue": "Differentiate.",
     "why": "Product and chain rules.",
     "expr": "2*exp(t/3)*sin(t)/3 + 2*exp(t/3)*cos(t)",
     "relation": "differentiate",
     "variable": "t"
    },
    {
     "cue": "Evaluate at \\(t=2\\).",
     "why": "Radian mode.",
     "expr": "-0.440",
     "relation": "evaluate",
     "subs": {
      "t": "2"
     },
     "approx": true
    },
    {
     "cue": "\\(y\\) is a position.",
     "why": "Two derivatives give \\(y''\\).",
     "expr": "-t + 2*log(t**2 + 1)",
     "relation": "new"
    },
    {
     "cue": "Differentiate.",
     "why": "Chain rule.",
     "expr": "4*t/(t**2 + 1) - 1",
     "relation": "differentiate",
     "variable": "t"
    },
    {
     "cue": "Again.",
     "why": "Quotient rule.",
     "expr": "-8*t**2/(t**2 + 1)**2 + 4/(t**2 + 1)",
     "relation": "differentiate",
     "variable": "t"
    },
    {
     "cue": "Evaluate at \\(t=2\\).",
     "why": "Exact here.",
     "expr": "-0.480",
     "relation": "evaluate",
     "subs": {
      "t": "2"
     },
     "approx": true
    },
    {
     "cue": "Write the pair.",
     "why": "Horizontal first, labelled.",
     "point_type_id": "BC-PT-99064"
    }
   ],
   "answer": {
    "form": "statement",
    "expr": "<-0.440, -0.480>",
    "text": "The acceleration at t = 2 is \\(\\langle -0.440, -0.480\\rangle\\)."
   }
  }
 ],
 "what_a_reader_scores": [
  {
   "example_id": "ex-1",
   "point_type_ids": [
    "BC-PT-99064"
   ],
   "lines": [
    {
     "point_type_id": "BC-PT-99064",
     "text": "Labelled values. Earned by: Each requested value presented with the label that identifies which quantity it is (sg-25:18, sg-22:10). Not earned by: Unlabelled values, which sg-25:18 states earn neither point; a single unlabelled value, which sg-22:10 states earns nothing. Notation: sg-25:18 treats incorrect communication between a label and its value as scratch work with no effect on scoring; sg-22:10 reads unlabelled pairs left to right and top to bottom."
    }
   ]
  }
 ],
 "common_errors": [
  {
   "error_id": "BC-ERR-09017",
   "observed_behavior": "Two correct numbers appear with no indication of which is the horizontal and which the vertical component.",
   "scoring_consequence": "The guideline accepts separate components only when they are labelled, so an unlabelled pair can lose a point (sg-23:6).",
   "wrong_step": {
    "text": "\\(\\langle -0.480, -0.440\\rangle\\).",
    "expr": "Matrix([-0.480, -0.440])"
   },
   "right_step": {
    "text": "\\(\\langle -0.440, -0.480\\rangle\\).",
    "expr": "Matrix([-0.440, -0.480])"
   },
   "relation": "distinct",
   "fix_prompt": true,
   "possible_reason": {
    "misconception_id": "BC-MIS-09009",
    "text": "reports two values without treating them as components of one object"
   },
   "sources": [
    "BC-ERR-09017",
    "BC-MIS-09009"
   ]
  }
 ],
 "representations": null,
 "prerequisite_bridges": [
  {
   "prq_id": "BC-PRQ-09001",
   "text": "The horizontal entry comes first. Components listed apart need labels."
  }
 ],
 "time": {
  "exam_part": "I-B",
  "budget_minutes": 2.92,
  "source": "research/exam/exam-structure.md#Section and part layout",
  "written_steps": {
   "ex-1": [
    2,
    3,
    5,
    6,
    7,
    8
   ]
  },
  "skipped_steps": {
   "ex-1": [
    1,
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
   "archetype_id": "BC-QA-09004",
   "parameter_draw": {
    "amplitude": "2",
    "growth": "1/3",
    "log_scale": "2",
    "linear": "-1",
    "time": "2",
    "position_axis": "y",
    "notation": "vector"
   },
   "completes": "ex-1",
   "stem": {
    "text": "\\(x''(2)\\approx -0.440\\) and \\(y''(2)=-0.480\\). Write the acceleration vector.",
    "command_verb": "write"
   },
   "key": {
    "form": "statement",
    "expr": "<-0.440, -0.480>",
    "label": "\\(\\langle -0.440, -0.480\\rangle\\)"
   },
   "steps": [
    {
     "text": "Horizontal value first, both inside one pair.",
     "expr": "-0.440",
     "relation": "new"
    }
   ],
   "calculator_status": "calculator",
   "skills": [
    "BC-SKL-09018"
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
   "archetype_id": "BC-QA-09004",
   "parameter_draw": {
    "amplitude": "4",
    "growth": "1/2",
    "log_scale": "1",
    "linear": "2",
    "time": "3/2",
    "position_axis": "x",
    "notation": "components"
   },
   "stem": {
    "text": "A particle has \\(x(t)=2t+\\ln(1+t^2)\\) and \\(y'(t)=4e^{t/2}\\sin t\\). Find its acceleration at \\(t=\\frac32\\), each component labelled, to three decimals.",
    "command_verb": "find"
   },
   "key": {
    "form": "statement",
    "expr": "x''(3/2)=-0.237, y''(3/2)=4.822",
    "label": "\\(x''(\\tfrac32)=-0.237\\), \\(y''(\\tfrac32)=4.822\\)"
   },
   "steps": [
    {
     "text": "x is the position, so two derivatives.",
     "expr": "2*(1 - t**2)/(t**4 + 2*t**2 + 1)",
     "relation": "new"
    },
    {
     "text": "Evaluate.",
     "expr": "-0.237",
     "relation": "evaluate",
     "subs": {
      "t": "3/2"
     },
     "approx": true
    }
   ],
   "calculator_status": "calculator",
   "skills": [
    "BC-SKL-09018"
   ]
  }
 ],
 "delivery": [
  {
   "block": "orientation",
   "mode": "figure",
   "reason": "rule 4 (unit README rule 3): BC-REP-12 and BC-REP-14 on BC-SKL-09018; not promoted, the skill is a notation conversion",
   "sources": [
    "BC-SKL-09018"
   ],
   "spec": {
    "kind": "parametric_path",
    "x": "x(t)",
    "y": "y(t)",
    "t_range": [
     0,
     3
    ],
    "points": [
     {
      "t": 2,
      "style": "filled"
     }
    ],
    "labels": [
     {
      "text": "x = x(t), y = y(t)",
      "placement": "inside"
     },
     {
      "text": "r(t) = < x(t), y(t) >",
      "placement": "inside"
     }
    ]
   },
   "fallback": "the same path static with both labels",
   "keyboard": "no control; the figure description is reached with Tab"
  },
  {
   "block": "ki-1",
   "mode": "figure",
   "reason": "rule 4 (unit README rule 3): BC-REP-14 on BC-SKL-09018; not promoted, a notation conversion with no reading to take",
   "sources": [
    "BC-SKL-09018"
   ],
   "spec": {
    "kind": "vector_diagram",
    "tail": [
     0,
     0
    ],
    "head": [
     3,
     2
    ],
    "legs": [
     {
      "axis": "x",
      "value": "x(t), first entry"
     },
     {
      "axis": "y",
      "value": "y(t), second entry"
     }
    ],
    "labels": [
     {
      "text": "r(t) = < x(t), y(t) >",
      "placement": "inside"
     },
     {
      "text": "horizontal entry first",
      "placement": "inside"
     }
    ]
   },
   "fallback": "the static vector with its two legs labelled",
   "keyboard": "no control"
  },
  {
   "block": "ex-1",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-09017",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  }
 ],
 "refresher": [
  "ki-1",
  "err-BC-ERR-09017",
  "ex-1"
 ],
 "research_lines": [
  {
   "file": "research/units/unit-09-parametric-polar-vector.md",
   "line": "Ordered pair, angle bracket, and bracket notation are all acceptable, and the two components must be identifiable."
  }
 ],
 "inferred": [
  {
   "claim": "Only BC-ERR-09017 meets the concept's one skill, so the lesson carries two checks and no MCQ: a check 3 needs three distractors that each anchor to an error block.",
   "settles": "A second error record for BC-SKL-09018, for example a swapped conversion between the parametric pair and the vector."
  },
  {
   "claim": "The figure modes serve this concept better than text.",
   "settles": "The modality A/B in the build plan: skip rate and time to first credited success by mode."
  },
  {
   "claim": "A fluent solver writes the derivatives and the labelled vector and holds the given rates.",
   "settles": "Timing data per step once the fluency telemetry exists."
  }
 ],
 "sources": [
  "BC-CON-09005",
  "BC-SKL-09018",
  "BC-EK-CHA-3H1",
  "ced:174",
  "BC-QA-09004",
  "BC-QA-09005",
  "BC-PT-99064",
  "sg-23:6",
  "sg-25:18",
  "sg-22:10",
  "BC-ERR-09017",
  "BC-MIS-09009",
  "BC-PRQ-09001",
  "research/units/unit-09-parametric-polar-vector.md#9.4 Defining and Differentiating Vector-Valued Functions",
  "research/question-analysis/question-archetypes.md#BC-QA-09004 Acceleration vector of a particle in planar motion",
  "research/scoring/common-point-losses.md#Precision and presentation points",
  "research/exam/exam-structure.md#Section and part layout"
 ],
 "word_count": {
  "full": 420,
  "brief": 420
 },
 "read_minutes": {
  "full": 2.8,
  "brief": 2.8
 }
}
```
