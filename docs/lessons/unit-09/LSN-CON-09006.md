---
title: LSN-CON-09006 Derivative of a vector-valued function taken component by component
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-09006, differentiating a vector-valued function one component at a time to give the velocity and acceleration vectors at a time, built from authoring_bundle("BC-CON-09006") and the research files it cites, so an author fills plan 15's lesson record without making a teaching decision.
---

# LSN-CON-09006 Derivative of a vector-valued function taken component by component

Concept BC-CON-09006 (skills BC-SKL-09015, 09016, 09017), topic 9.4 of Unit 9, BC only (ced:174), loaded by BC-QA-09004 (family parametric-motion) and, for BC-SKL-09015 and 09016 only, BC-QA-99005 (polar path to vectors, taught with BC-CON-09012). No Unit 9 hard parent beyond BC-CON-09001 (docs/lessons/unit-09/README.md, section 1).

## Prediction

Served first, both bands: an `mcq` on ex-1's own functions. The core claim is that each entry of the acceleration vector is its own derivative of whatever is given for that component, so the entries take different numbers of derivatives. Key A, the \(x\) entry two and the \(y\) entry one. The distractors are one each (the velocity read as the whole task) and two each. It is answerable before any rule from what a derivative of a position and of a velocity give. The resolution states the component form with no verdict word. Source: BC-CON-09006 and the topic section the key idea cites.

## Orientation

Served text, from BC-CON-09006 `description_plain` (differentiate each component separately) and the topic's Assessment behaviour paragraph (research/units/unit-09-parametric-polar-vector.md#9.4 Defining and Differentiating Vector-Valued Functions): the MCQ forms ask for a velocity or acceleration vector at a time, and the free-response opener scores one point per component with its setup (sg-23:5). The orientation states what a response shows. No count, no frequency.

## Key ideas

One BC-EK, BC-EK-CHA-3H1 (ced:174), maps the three skills, so one core block, both bands. ki-1 paraphrases the Required mathematical knowledge paragraphs Vector derivative, Motion vectors and Notation. No anchor quote: the CHA-3.H.1 sentence adds nothing the paraphrase lacks. Notation line: the concept's `notation`.

## Recognition

BC-QA-09004 is the archetype (research/question-analysis/question-archetypes.md#BC-QA-09004 Acceleration vector of a particle in planar motion). BC-QA-99005 loads BC-SKL-09015 and 09016 on a polar path and is taught with the polar concepts.

- `common_givens`: a velocity vector or a pair of component rates, and a time. `asked_to_produce`: two derivative expressions and a labelled vector of two values. `typical_wording`: find the acceleration vector of the particle at the given time and show the setup.
- The signal in the stem: acceleration vector, with a position given for one component and a velocity for the other. Shapes: the opening part of the calculator active free response, BC-FRQ-2013-Q2-C, BC-FRQ-2022-Q2-B, BC-FRQ-2023-Q2-A.

The near miss of the contrast pair is the coordinate stem from BC-QA-09005 (outside the block's archetype): the same rate vector, but a known start and a later coordinate, so the rates integrate. The `common_distractors` entry "the velocity vector" is a second near miss.

## Method choice

- st-1, BC-QA-09004. Cue from `common_givens` and `asked_to_produce`. Method, `expected_solution_path`: differentiate each velocity component, evaluate both at the time, present the pair. Rival: `common_distractors` "the velocity vector" and the wrong-order pair. Separating feature: acceleration is the derivative of what is given as velocity. Both cue fields exist, so the block is not inferred. The block carries the contrast pair, an acceleration stem beside a coordinate stem.

## Solution path

- ex-1, BC-QA-09004, both bands, calculator. Draw: amplitude 3, growth 1/2, log_scale 1, linear 2, time 2, position_axis x, notation components. \(x(t)=\ln(1+t^2)+2t\), \(y'(t)=3e^{t/2}\sin t\); acceleration \(\langle -0.240, 0.314\rangle\), velocity \(\langle 2.800, 7.415\rangle\) (SymPy). No published item on BC-QA-09004 carries this draw (ITM-GEN-09004-00 to 21).
- ex-2, low band, calculator. Draw: amplitude 5, growth 1/3, log_scale 2, linear -1, time 3/2, position_axis y, notation components. \(x'(t)=5e^{t/3}\sin t\), \(y(t)=2\ln(1+t^2)-t\); acceleration \(\langle 3.324, -0.473\rangle\).
- ex-2 is faded from step 4: steps 1 to 3 (the horizontal entry, from a velocity) are shown, the student writes the vertical entry, where the given component is a position and two derivatives are needed, and steps 4 to 8 then reveal.
- Steps follow `expected_solution_path`. A fluent solver writes the derivatives, the values and the labelled pair, and holds the given rates.
- No productive-failure comparison: BC-CON-09006 is not in `PRODUCTIVE_FAILURE_TARGETS`.

## Scoring

BC-QA-09004 lists BC-PT-99064, 99052, 99050, 99005. ex-1 tags no point type, because its reader line would take 83 words of the brief band's 450; ex-2 tags BC-PT-99052 and BC-PT-99064 (the labelled pair). BC-PT-99005 and BC-PT-99050 are untagged: 99005 keeps the brief band inside its cap, 99050 is the speed point and belongs to BC-CON-09009. The lines are `reader_checks` output.

Point losses from research: components in reversed order lose both component points (sg-22:7), an unsupported vector earns one of two (sg-23:6), and a variable expression equated to a value loses one (research/scoring/common-point-losses.md#Precision and presentation points).

## Traps

Four errors meet the skills, in bundle order: BC-ERR-99029, BC-ERR-09017, BC-ERR-99002, BC-ERR-99019. BC-ERR-99021 falls past the cap of 4. Low band all four, mid band the first two. All on ex-1's draw.

- err-BC-ERR-99029: the velocity \(y'(2)\) in the acceleration's place. Distinct, `fix_prompt` true. No possible reason line.
- err-BC-ERR-09017: the pair exchanged. Distinct, `fix_prompt` true. Possible reason, BC-MIS-09009.
- err-BC-ERR-99002: \(x''(t)\) set equal to a number. The values are the same and the difference lives in the sentence, so `relation` equivalent and `fix_prompt` false. Possible reason, BC-MIS-99011.
- err-BC-ERR-99019: \(y''(2)\) reported as 0.31, fewer than three places. Distinct, `fix_prompt` true.

## Representations

None. The topic's Representations paragraph names the conversion of a vector expression to a pair of numerical components, which ki-1 and the orientation already draw.

## Prerequisite bridge

- BC-PRQ-09001, from its `description_plain` and `failure_signature`, gated by state.

## Time

BC-QA-09004 is an MCQ in Section I Part B, 2.92 minutes (research/exam/exam-structure.md#Section and part layout); as the free response opener it scores 2 points, 3.33 minutes (docs/lessons/unit-09/README.md, section 5). A fluent solver writes the derivatives, the values and the labelled pair; the given rates are held [inferred]. No target.

## Checks

- chk-1, completion of ex-1, both bands: the two second derivatives given, the labelled pair at t = 2 asked. Key \(\langle -0.240, 0.314\rangle\).
- chk-2, isomorph, both bands, calculator. Draw: amplitude 4, growth 1/3, log_scale 2, linear 3, time 3/2, position_axis x, notation components. Key \(\langle -0.473, 2.659\rangle\).
- chk-3, MCQ, low band, calculator. Draw: amplitude 2, growth 1/4, log_scale 3, linear -2, time 3/2, position_axis x, notation components. Key \(\langle -0.710, 0.932\rangle\). Distractors: the reversed pair (BC-ERR-09017); the velocity vector (BC-ERR-99029); the position component differentiated once (BC-ERR-99029, the second form the record lists). Keys are statements, so the checker recomputes none of them; each was computed with SymPy.

## Delivery

- orientation: figure. Unit README section 6 names CHA-3H1 for BC-CON-09006. Rule 3 of the README: BC-REP-14 on BC-SKL-09015 to 09017. Static path with both vectors at t = 2.
- ki-1: interactive. Rule 3 promoted (TEMPLATE rule 4): BC-QA-09004 `common_givens` names a time and the stem asks for the vector at that time. One slider, the time. The path is the process's own picture, not a representation the stem carries.
- ex-1, ex-2, the four error blocks: step_reveal. Rule 1.

## Band plan

- Low (full): prediction, orientation, bridge, ki-1, st-1 with the contrast pair, ex-1 and its line, chk-1, the four error blocks, ex-2 (faded from step 4) and its lines, chk-2, chk-3. 793 words, 5.3 minutes.
- Mid (brief): prediction, orientation, bridge, ki-1, st-1 with the contrast pair, ex-1 and its line, chk-1, err-BC-ERR-99029, err-BC-ERR-09017, chk-2. 435 words, 2.9 minutes.
- Refresher: ki-1, the four error blocks, ex-1.

## Sources

- BC-CON-09006; BC-SKL-09015, BC-SKL-09016, BC-SKL-09017; BC-EK-CHA-3H1; ced:174
- BC-QA-09004, BC-QA-99005; BC-PT-99052, BC-PT-99064
- BC-ERR-99029, BC-ERR-09017, BC-ERR-99002, BC-ERR-99019; BC-MIS-09009, BC-MIS-99011
- BC-PRQ-09001
- sg-23:5, sg-23:6, sg-22:7, sg-25:18, sg-22:10
- research/units/unit-09-parametric-polar-vector.md#9.4 Defining and Differentiating Vector-Valued Functions
- research/question-analysis/question-archetypes.md#BC-QA-09004 Acceleration vector of a particle in planar motion
- research/exam/exam-structure.md#Section and part layout
- [inferred] The interactive mode, the held steps and the untagged BC-PT-99005, each settled as the inferred array states.

## Machine record

```json
{
 "id": "LSN-CON-09006",
 "kind": "concept",
 "target_id": "BC-CON-09006",
 "unit": "09",
 "skills": [
  "BC-SKL-09015",
  "BC-SKL-09016",
  "BC-SKL-09017"
 ],
 "prediction": {
  "id": "pr-1",
  "stem": {
   "text": "A particle has \\(x(t)=\\ln(1+t^2)+2t\\) and \\(y'(t)=3e^{t/2}\\sin t\\). Predict how many derivatives each entry of its acceleration vector takes.",
   "command_verb": "predict"
  },
  "format": "mcq",
  "options": [
   {
    "id": "A",
    "label": "\\(x\\) entry two, \\(y\\) entry one",
    "is_key": true
   },
   {
    "id": "B",
    "label": "Each entry one",
    "is_key": false
   },
   {
    "id": "C",
    "label": "Each entry two",
    "is_key": false
   }
  ],
  "resolution": "Acceleration is the derivative of velocity on each component: the position \\(x\\) needs two derivatives, the velocity \\(y'\\) one, giving \\(\\langle x''(t), y''(t)\\rangle\\).",
  "sources": [
   "BC-CON-09006",
   "research/units/unit-09-parametric-polar-vector.md#9.4 Defining and Differentiating Vector-Valued Functions"
  ]
 },
 "orientation": {
  "text": "Differentiate each component on its own: the derivative of position is the velocity vector, the derivative of velocity the acceleration vector. A response shows each component's derivative, then the labelled values at the time.",
  "sources": [
   "BC-CON-09006",
   "research/units/unit-09-parametric-polar-vector.md#9.4 Defining and Differentiating Vector-Valued Functions"
  ]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-CHA-3H1",
   "depth": "core",
   "text": "Derivatives of vector-valued functions are taken one component at a time. The derivative of the position vector is the velocity vector, and the derivative of the velocity vector is the acceleration vector. At a time, each is an ordered pair of numbers with the components identifiable.",
   "notation": "velocity vector; acceleration vector",
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
   "cue": "Component rates, a time, a labelled vector requested.",
   "method": "Differentiate each component, evaluate at the time.",
   "rival": "The velocity vector reported as the acceleration.",
   "separating_feature": "Acceleration differentiates what is given as velocity.",
   "sources": [
    "BC-QA-09004"
   ],
   "evidence_tag": "verified",
   "contrast": {
    "this": {
     "text": "A particle has \\(x'(t)=2\\cos t\\) and \\(y'(t)=t^2\\). Find its acceleration vector at \\(t=1\\).",
     "archetype_id": "BC-QA-09004"
    },
    "not_this": {
     "text": "A particle has \\(x'(t)=2\\cos t\\) and \\(y'(t)=t^2\\), with \\(x(0)=1\\). Find \\(x(2)\\).",
     "why_not": "It asks for a coordinate, which accumulates the rate."
    },
    "feature": "A vector at a time differentiates; a later coordinate integrates."
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
    "amplitude": "3",
    "growth": "1/2",
    "log_scale": "1",
    "linear": "2",
    "time": "2",
    "position_axis": "x",
    "notation": "components"
   },
   "problem": {
    "text": "A particle has \\(x(t)=\\ln(1+t^2)+2t\\) and \\(y'(t)=3e^{t/2}\\sin t\\). Find its acceleration vector at \\(t=2\\), showing the setup.",
    "command_verb": "find"
   },
   "calculator_status": "calculator",
   "steps": [
    {
     "cue": "\\(x\\) is a position.",
     "why": "Two derivatives give \\(x''\\).",
     "expr": "2*t + log(t**2 + 1)",
     "relation": "new"
    },
    {
     "cue": "Differentiate.",
     "why": "Chain rule.",
     "expr": "2*t/(t**2 + 1) + 2",
     "relation": "differentiate",
     "variable": "t"
    },
    {
     "cue": "Again.",
     "why": "Quotient rule.",
     "expr": "2*(-2*t**2/(t**2 + 1) + 1)/(t**2 + 1)",
     "relation": "differentiate",
     "variable": "t"
    },
    {
     "cue": "Evaluate at \\(t=2\\).",
     "why": "Exact here.",
     "expr": "-0.240",
     "relation": "evaluate",
     "subs": {
      "t": "2"
     },
     "approx": true
    },
    {
     "cue": "\\(y'\\) is a velocity.",
     "why": "One derivative gives \\(y''\\).",
     "expr": "3*exp(t/2)*sin(t)",
     "relation": "new"
    },
    {
     "cue": "Differentiate.",
     "why": "Product and chain rules.",
     "expr": "3*exp(t/2)*sin(t)/2 + 3*exp(t/2)*cos(t)",
     "relation": "differentiate",
     "variable": "t"
    },
    {
     "cue": "Evaluate at \\(t=2\\).",
     "why": "Radian mode.",
     "expr": "0.314",
     "relation": "evaluate",
     "subs": {
      "t": "2"
     },
     "approx": true
    },
    {
     "cue": "Write the pair.",
     "why": "Horizontal first, labelled."
    }
   ],
   "answer": {
    "form": "statement",
    "expr": "<-0.240, 0.314>",
    "text": "The acceleration at t = 2 is \\(\\langle -0.240, 0.314\\rangle\\)."
   }
  },
  {
   "id": "ex-2",
   "archetype_id": "BC-QA-09004",
   "bands": [
    "low"
   ],
   "parameter_draw": {
    "amplitude": "5",
    "growth": "1/3",
    "log_scale": "2",
    "linear": "-1",
    "time": "3/2",
    "position_axis": "y",
    "notation": "components"
   },
   "fade_from": 4,
   "problem": {
    "text": "A particle has \\(x'(t)=5e^{t/3}\\sin t\\) and \\(y(t)=2\\ln(1+t^2)-t\\). Find its acceleration vector at \\(t=\\frac32\\), showing the setup.",
    "command_verb": "find"
   },
   "calculator_status": "calculator",
   "steps": [
    {
     "cue": "\\(x'\\) is a velocity.",
     "why": "One derivative gives \\(x''\\).",
     "expr": "5*exp(t/3)*sin(t)",
     "relation": "new"
    },
    {
     "cue": "Differentiate.",
     "why": "Product and chain rules.",
     "expr": "5*exp(t/3)*sin(t)/3 + 5*exp(t/3)*cos(t)",
     "relation": "differentiate",
     "variable": "t"
    },
    {
     "cue": "Evaluate at \\(t=\\frac32\\).",
     "why": "Radian mode.",
     "expr": "3.324",
     "relation": "evaluate",
     "subs": {
      "t": "3/2"
     },
     "approx": true,
     "point_type_id": "BC-PT-99052"
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
     "cue": "Evaluate at \\(t=\\frac32\\).",
     "why": "Three places.",
     "expr": "-0.473",
     "relation": "evaluate",
     "subs": {
      "t": "3/2"
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
    "expr": "<3.324, -0.473>",
    "text": "The acceleration at t = 3/2 is \\(\\langle 3.324, -0.473\\rangle\\)."
   }
  }
 ],
 "what_a_reader_scores": [
  {
   "example_id": "ex-1",
   "point_type_ids": [],
   "lines": []
  },
  {
   "example_id": "ex-2",
   "point_type_ids": [
    "BC-PT-99052",
    "BC-PT-99064"
   ],
   "lines": [
    {
     "point_type_id": "BC-PT-99052",
     "text": "Acceleration vector components. Earned by: Each component of the acceleration vector obtained by differentiating the matching velocity component and evaluating at the requested time; the rubrics award one point per component (sg-22:7, sg-23:5). Not earned by: Components presented in reversed order, which sg-22:7 states loses both points; an unsupported vector, which earns only one of the two (sg-22:7, sg-23:6). Notation: sg-23:6 accepts several bracket styles and allows components listed separately provided they are labelled; sg-22:7 requires labels when no ordered pair is used."
    },
    {
     "point_type_id": "BC-PT-99064",
     "text": "Labelled values. Earned by: Each requested value presented with the label that identifies which quantity it is (sg-25:18, sg-22:10). Not earned by: Unlabelled values, which sg-25:18 states earn neither point; a single unlabelled value, which sg-22:10 states earns nothing. Notation: sg-25:18 treats incorrect communication between a label and its value as scratch work with no effect on scoring; sg-22:10 reads unlabelled pairs left to right and top to bottom."
    }
   ]
  }
 ],
 "common_errors": [
  {
   "error_id": "BC-ERR-99029",
   "observed_behavior": "Responses invert the quotient for the slope of the path, report a velocity vector where an acceleration vector was asked or reverse its components, compute a one-dimensional arc length or a Pythagorean combination of two separate integrals for total distance, or reason from dy/dx where dy/dt determines the direction of motion.",
   "scoring_consequence": "The setup point for the requested quantity is lost, and the answer point follows it.",
   "wrong_step": {
    "text": "The velocity \\(y'(2)=7.415\\) written as the second entry.",
    "expr": "3*exp(1)*sin(2)"
   },
   "right_step": {
    "text": "The acceleration \\(y''(2)=0.314\\).",
    "expr": "3*exp(1)*(sin(2)/2 + cos(2))"
   },
   "relation": "distinct",
   "fix_prompt": true,
   "possible_reason": null,
   "sources": [
    "BC-ERR-99029"
   ]
  },
  {
   "error_id": "BC-ERR-09017",
   "observed_behavior": "Two correct numbers appear with no indication of which is the horizontal and which the vertical component.",
   "scoring_consequence": "The guideline accepts separate components only when they are labelled, so an unlabelled pair can lose a point (sg-23:6).",
   "wrong_step": {
    "text": "\\(\\langle 0.314, -0.240\\rangle\\).",
    "expr": "(0.314, -0.240)"
   },
   "right_step": {
    "text": "\\(\\langle -0.240, 0.314\\rangle\\).",
    "expr": "(-0.240, 0.314)"
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
  },
  {
   "error_id": "BC-ERR-99002",
   "observed_behavior": "Responses join unequal objects with an equals sign, for example writing a general expression in t equal to the value of that expression at one instant, or stringing several lines of work together with equals signs.",
   "scoring_consequence": "The presentation point or the setup point is lost, and in some parts the response becomes ineligible for later points in that part.",
   "wrong_step": {
    "text": "\\(x''(t)=-0.240\\).",
    "expr": "-0.240"
   },
   "right_step": {
    "text": "\\(x''(2)=-0.240\\).",
    "expr": "-0.240"
   },
   "relation": "equivalent",
   "fix_prompt": false,
   "possible_reason": {
    "misconception_id": "BC-MIS-99011",
    "text": "uses the equals sign to join successive lines of work"
   },
   "sources": [
    "BC-ERR-99002",
    "BC-MIS-99011"
   ]
  },
  {
   "error_id": "BC-ERR-99019",
   "observed_behavior": "Responses report fewer than three digits after the decimal point, round an intermediate value before it is used again, or read a value off a trace rather than solving for it.",
   "scoring_consequence": "The answer point is not earned; the report notes this recurs across several parts of the same response.",
   "wrong_step": {
    "text": "\\(y''(2)\\approx0.31\\).",
    "expr": "0.31"
   },
   "right_step": {
    "text": "\\(y''(2)\\approx0.314\\).",
    "expr": "0.314"
   },
   "relation": "distinct",
   "fix_prompt": true,
   "possible_reason": null,
   "sources": [
    "BC-ERR-99019"
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
    3,
    4,
    6,
    7
   ],
   "ex-2": [
    2,
    3,
    5,
    6,
    7
   ]
  },
  "skipped_steps": {
   "ex-1": [
    1,
    5
   ],
   "ex-2": [
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
    "amplitude": "3",
    "growth": "1/2",
    "log_scale": "1",
    "linear": "2",
    "time": "2",
    "position_axis": "x",
    "notation": "components"
   },
   "completes": "ex-1",
   "stem": {
    "text": "\\(x''(t)=\\frac{2(1-t^2)}{(1+t^2)^2}\\) and \\(y''(t)=3e^{t/2}\\left(\\frac{\\sin t}{2}+\\cos t\\right)\\). Write the acceleration vector at \\(t=2\\).",
    "command_verb": "write"
   },
   "key": {
    "form": "statement",
    "expr": "<-0.240, 0.314>",
    "label": "\\(\\langle -0.240, 0.314\\rangle\\)"
   },
   "steps": [
    {
     "text": "Evaluate both at 2.",
     "expr": "-0.240",
     "relation": "new"
    }
   ],
   "calculator_status": "calculator",
   "skills": [
    "BC-SKL-09017"
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
    "growth": "1/3",
    "log_scale": "2",
    "linear": "3",
    "time": "3/2",
    "position_axis": "x",
    "notation": "components"
   },
   "stem": {
    "text": "A particle has \\(x(t)=2\\ln(1+t^2)+3t\\) and \\(y'(t)=4e^{t/3}\\sin t\\). Find its acceleration vector at \\(t=\\frac32\\), to three decimals.",
    "command_verb": "find"
   },
   "key": {
    "form": "statement",
    "expr": "<-0.473, 2.659>",
    "label": "\\(\\langle -0.473, 2.659\\rangle\\)"
   },
   "steps": [
    {
     "text": "x twice, y' once.",
     "expr": "4*(1 - t**2)/(t**2 + 1)**2",
     "relation": "new"
    }
   ],
   "calculator_status": "calculator",
   "skills": [
    "BC-SKL-09017"
   ]
  },
  {
   "id": "chk-3",
   "check_kind": "mcq",
   "format": "mcq",
   "bands": [
    "low"
   ],
   "archetype_id": "BC-QA-09004",
   "parameter_draw": {
    "amplitude": "2",
    "growth": "1/4",
    "log_scale": "3",
    "linear": "-2",
    "time": "3/2",
    "position_axis": "x",
    "notation": "components"
   },
   "stem": {
    "text": "A particle has \\(x(t)=3\\ln(1+t^2)-2t\\) and \\(y'(t)=2e^{t/4}\\sin t\\). Its acceleration vector at \\(t=\\frac32\\) is",
    "command_verb": "identify"
   },
   "key": {
    "form": "statement",
    "expr": "<-0.710, 0.932>",
    "label": "\\(\\langle -0.710, 0.932\\rangle\\)"
   },
   "steps": [
    {
     "text": "x twice, y' once.",
     "expr": "6*(1 - t**2)/(t**2 + 1)**2",
     "relation": "new"
    }
   ],
   "options": [
    {
     "id": "A",
     "is_key": false,
     "label": "\\(\\langle 0.932, -0.710\\rangle\\)",
     "error_path": "BC-ERR-09017",
     "derivation": "the two components written in the wrong order"
    },
    {
     "id": "B",
     "is_key": false,
     "label": "\\(\\langle 0.769, 2.903\\rangle\\)",
     "error_path": "BC-ERR-99029",
     "derivation": "the velocity vector at the time reported as the acceleration"
    },
    {
     "id": "C",
     "is_key": true,
     "label": "\\(\\langle -0.710, 0.932\\rangle\\)",
     "error_path": null
    },
    {
     "id": "D",
     "is_key": false,
     "label": "\\(\\langle 0.769, 0.932\\rangle\\)",
     "error_path": "BC-ERR-99029",
     "derivation": "the position component differentiated once, so it gives its velocity, not its acceleration"
    }
   ],
   "calculator_status": "calculator",
   "skills": [
    "BC-SKL-09017"
   ]
  }
 ],
 "delivery": [
  {
   "block": "orientation",
   "mode": "figure",
   "reason": "rule 4 (unit README rule 3): BC-REP-14 on BC-SKL-09015 to 09017",
   "sources": [
    "BC-SKL-09015"
   ],
   "spec": {
    "kind": "parametric_path",
    "x": "ln(1+t^2)+2t",
    "y": "integral of 3*exp(t/2)*sin(t)",
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
      "text": "velocity vector at t = 2",
      "placement": "inside"
     },
     {
      "text": "acceleration vector at t = 2",
      "placement": "inside"
     }
    ]
   },
   "fallback": "the same path static with both vectors drawn at t = 2 and labelled",
   "keyboard": "no control; the figure description is reached with Tab"
  },
  {
   "block": "ki-1",
   "mode": "interactive",
   "reason": "rule 3 promoted: BC-REP-14 on BC-SKL-09015 to 09017; BC-QA-09004 common_givens a time, and the stem asks for the vector at that time. The path is the process's own picture, and the control drives the time",
   "sources": [
    "BC-SKL-09015",
    "BC-SKL-09016",
    "BC-SKL-09017",
    "BC-QA-09004"
   ],
   "spec": {
    "kind": "parametric_path",
    "x": "ln(1+t^2)+2t",
    "y": "integral of 3*exp(t/2)*sin(t)",
    "t_range": [
     0,
     3
    ],
    "vectors": [
     "velocity",
     "acceleration"
    ],
    "controls": [
     {
      "type": "slider",
      "parameter": "t",
      "range": [
       0,
       3
      ],
      "step": 0.5,
      "start": 2
     }
    ],
    "labels": [
     {
      "text": "velocity: x', y'",
      "placement": "inside"
     },
     {
      "text": "acceleration: x'', y''",
      "placement": "inside"
     }
    ],
    "question": "What are the horizontal and vertical components of each vector at this time?"
   },
   "fallback": "three static copies of the path at t = 1, 2 and 3 with both vectors and components labelled inside",
   "keyboard": "Tab focuses the slider; left and right arrow keys change t by 0.5; the components are announced"
  },
  {
   "block": "ex-1",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "ex-2",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-99029",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-09017",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-99002",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-99019",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  }
 ],
 "refresher": [
  "ki-1",
  "err-BC-ERR-99029",
  "err-BC-ERR-09017",
  "err-BC-ERR-99002",
  "err-BC-ERR-99019",
  "ex-1"
 ],
 "research_lines": [
  {
   "file": "research/units/unit-09-parametric-polar-vector.md",
   "line": "The derivative of the position vector is the velocity vector and the derivative of the velocity vector is the acceleration vector."
  }
 ],
 "inferred": [
  {
   "claim": "The interactive mode on ki-1 serves this concept better than text or a static figure.",
   "settles": "The modality A/B in the build plan: skip rate and time to first credited success by mode."
  },
  {
   "claim": "A fluent solver writes the derivatives, the two values and the labelled pair and holds the given rates.",
   "settles": "Timing data per step once the fluency telemetry exists."
  },
  {
   "claim": "BC-PT-99005 (setup with the value) is untagged in both examples, and ex-1 carries no tag, to keep the brief band inside its cap.",
   "settles": "A brief cap that admits its reader line."
  }
 ],
 "sources": [
  "BC-CON-09006",
  "BC-SKL-09015",
  "BC-SKL-09016",
  "BC-SKL-09017",
  "BC-EK-CHA-3H1",
  "ced:174",
  "BC-QA-09004",
  "BC-QA-09005",
  "BC-PT-99052",
  "BC-PT-99064",
  "sg-23:5",
  "sg-23:6",
  "sg-22:7",
  "sg-25:18",
  "sg-22:10",
  "BC-ERR-99029",
  "BC-ERR-09017",
  "BC-ERR-99002",
  "BC-ERR-99019",
  "BC-MIS-09009",
  "BC-MIS-99011",
  "BC-PRQ-09001",
  "research/units/unit-09-parametric-polar-vector.md#9.4 Defining and Differentiating Vector-Valued Functions",
  "research/question-analysis/question-archetypes.md#BC-QA-09004 Acceleration vector of a particle in planar motion",
  "research/exam/exam-structure.md#Section and part layout"
 ],
 "word_count": {
  "full": 793,
  "brief": 435
 },
 "read_minutes": {
  "full": 5.3,
  "brief": 2.9
 }
}
```
