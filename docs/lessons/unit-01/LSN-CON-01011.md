---
title: LSN-CON-01011 Connecting limit representations
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-01011, connecting graphical, numerical, analytical and verbal limit statements, built from authoring_bundle("BC-CON-01011") and the research files it cites, so an author fills plan 15's lesson record without making a teaching decision.
---

# LSN-CON-01011 Connecting limit representations

Concept BC-CON-01011 (skills BC-SKL-01036, BC-SKL-01037, BC-SKL-01038), topic 1.9 of Unit 1, loaded by BC-QA-01013 (primary). The unit attack map places it eleventh, after BC-CON-01006, with figure delivery.

## Prediction

Served first, both bands, on ex-1's own limit fact \(\lim_{x\to3^-}g(x)=\infty\). Form: `mcq`, three options, key B. The question asks for the concept's core claim before any rule is stated: what the infinity symbol in the value slot says about the graph. Distractor A reads the 3 as a value the outputs settle to, distractor C moves the infinity under the arrow. The resolution names the vertical asymptote and the other position of the symbol, in the record's words. Sources: BC-CON-01011 and the topic section the key idea cites. Delivery: text.

## Orientation

Served text, from BC-CON-01011 `description_plain` and the topic's Assessment behaviour paragraph (research/units/unit-01-limits-continuity.md#1.9 Connecting Multiple Representations of Limits): MCQ forms ask which representation matches; FRQ forms ask for the behaviour in words. Stated as what a response shows. No count, no frequency. Delivered as a figure.

## Key ideas

No skill of BC-CON-01011 lists `essential_knowledge` and ced:46 prints no essential knowledge statement for topic 1.9, so the one core block carries `ek_id` null, tagged [inferred].

- ki-1 (core). Paraphrase of the topic's Required mathematical knowledge paragraph (Equivalence across representations; What conversion must not lose), with the infinity distinction from the unit-01 README (Infinite limit against limit at infinity, BC-MIS-01018 probe). Anchor quote (8 words) from ced:46. Notation line from the topic's Notation line (the concept's `notation` field is empty).

## Recognition

- BC-QA-01013 (family representation-consistency, single MCQ, no calculator; research/question-analysis/question-archetypes.md#BC-QA-01013 Limit claim matched across graphical, numerical, and analytic representations). `typical_wording`: "Which of the given representations is consistent with the stated limit behaviour of f at the named input?" `common_givens`: a limit fact in one representation; candidate graphical, numerical or analytic representations. `asked_to_produce`: the representation that matches. No official example. The signal is one limit fact and several candidate forms, or a request to put a limit statement into words.

What says "not this concept": a stem that asks for the value of a limit from a formula (BC-CON-01007, 01008), or reads only notation without a second representation (BC-CON-01003).

The near miss for st-1 comes from the "not this concept" stems above: a formula asking for the value of a limit (BC-CON-01007 and 01008). It shares the limit notation but gives no second representation to convert into.

## Method choice

- st-1, BC-QA-01013, verified (`asked_to_produce` and `common_givens` present). Method, `expected_solution_path[0]`: read the limit behaviour from the supplied representation. Rival, `wrong_approaches`: reading a vertical asymptote statement as end behaviour (BC-ERR-01033). Separating feature: where the infinity symbol sits (the unit-01 README row, Infinite limit against limit at infinity).

## Solution path

- ex-1, BC-QA-01013, both bands: statement infinite_limit, number 3, side left, growth up, letter g, direction positive; \(\lim_{x\to3^-}g(x)=\infty\). Steps follow `expected_solution_path`: read the behaviour (side, value slot), state it neutrally, test against the forms, produce the match. Answer form statement.
- ex-2, BC-QA-01013, low band: statement limit_at_infinity, number \(-2\), direction positive, letter k; \(\lim_{x\to\infty}k(x)=-2\). Two steps. Answer form statement.

The notes of the `parameter_spec` fix what each statement kind means. No published BC-QA-01013 draw matches either. ex-1 carries no valued chain: the answer is a verbal description, so the checker confirms the draw, not a value. ex-2 carries two valued lines, the limit statement and the asymptote equation, so the fade has a valued step before it. Fade: `fade_from` 2. Step 1 (the infinity under the arrow, read as end behaviour) is shown and the student writes the description; step 2, the horizontal asymptote, is then revealed. The fade falls there because step 1 holds the only reading the concept needs and step 2 is its statement. On the MCQ shape nothing is written [inferred].

## Scoring

None. BC-QA-01013 lists no `point_types`, so no `what_a_reader_scores` entry and no point tag. The topic notes a separate point can attach to presenting a limit expression rather than only a value (sg-25:4; research/scoring/notation-requirements.md#Limit notation); that point sits on BC-QA-01010 and is not served here.

## Traps

Four active errors meet the skills, in the bundle's order. Low band all four, mid band the first two. The first two sit on ex-1's draw, the last two on ex-2's, since each shows on the statement kind it concerns.

- err-BC-ERR-01002 (ex-1). Wrong: the two sided limit at 3. Right: the left limit only. Distinct. Reason, words from BC-MIS-01002.
- err-BC-ERR-01020 (ex-1). Wrong: \(L=\infty\) as an existing limit. Right: the asymptote \(x=3\), no real limit. Distinct. Reason, words from BC-MIS-01012.
- err-BC-ERR-01033 (ex-2). Wrong: \(x=-2\). Right: \(y=-2\). Distinct. Reason, words from BC-MIS-01018.
- err-BC-ERR-01021 (ex-2). Wrong: \(k(\infty)=-2\). Right: the limit kept. Distinct. Reason, words from BC-MIS-99008.

All four blocks are distinct, so all four carry `fix_prompt` true.

## Representations

None as a separate block. The topic's Representations paragraph names graph to table, analytic statement to words and stated conditions to a sketch; the orientation figure and the ki-1 figure with its table carry these, at the cap of two representations per screen.

## Prerequisite bridge

Two BC-PRQ parents, supporting edges, gated by state: BC-PRQ-01003 (piecewise rule) and BC-PRQ-06005 (function notation and evaluation). Each is one short line from `description_plain`, with the `failure_signature` kept, to stay under the brief cap.

## Time

BC-QA-01013 is `no_calculator`, "Typically a single multiple choice item", so Section I Part A, 2.14 minutes (research/exam/exam-structure.md#Section and part layout). A fluent solver writes nothing and reads three features (side, slot of the infinity symbol, value) before scanning the options [inferred].

## Checks

- chk-1, completion of ex-1, both bands: the side and the value are read, the student writes the description. Key form statement, the asymptote \(x=3\).
- chk-2, isomorph, both bands: \(\lim_{x\to-1^+}f(x)=-\infty\). Key: vertical asymptote \(x=-1\), downward from the right.
- chk-3, MCQ, low band: \(\lim_{x\to2^+}h(x)=-\infty\). Key: right of 2, decreasing without bound, asymptote \(x=2\). Distractors carry BC-ERR-01033 (horizontal asymptote \(y=2\)), BC-ERR-01002 (both sides), BC-ERR-01020 (an existing limit).

All three keys are statements; each check carries the asymptote equation as its valued line.

## Delivery

- orientation: figure. Rule 3, BC-REP-02 on BC-SKL-01036 and 01038 (README: figure).
- ki-1: figure with a table beside it, two representations, the cap. Rules 3 and 4 (README). Labels inside; keyboard Tab and arrows; fallback the table with the two statements in words.
- ex-1, ex-2 and the four error blocks: step_reveal. Rule 1.

Non-text choices are [inferred], settled by the modality A/B.

## Band plan

- Low (full), in the served order of 2026-09-29: prediction, orientation, bridges when gated in, ki-1, st-1 (contrast pair on st-1), ex-1 and its scoring lines (none), chk-1, err-BC-ERR-01002, err-BC-ERR-01020, err-BC-ERR-01033, err-BC-ERR-01021 (each a fix prompt), ex-2 faded from step 2, chk-2, representations (none), chk-3. 628 words, 4.19 minutes (cap 900 and 6).
- Mid (brief): prediction, orientation, bridges when gated in, ki-1, st-1 with its contrast pair, ex-1, chk-1, err-BC-ERR-01002, err-BC-ERR-01020, chk-2. 448 words, 2.99 minutes (cap 450 and 3).
- Refresher: ki-1, the four error blocks, ex-1.

## Sources

- BC-CON-01011; BC-SKL-01036, BC-SKL-01037, BC-SKL-01038; ced:46; sg-25:4
- BC-QA-01013
- BC-ERR-01002, BC-ERR-01020, BC-ERR-01033, BC-ERR-01021; BC-MIS-01002, BC-MIS-01012, BC-MIS-01018, BC-MIS-99008
- BC-PRQ-01003, BC-PRQ-06005
- research/units/unit-01-limits-continuity.md#1.9 Connecting Multiple Representations of Limits
- research/question-analysis/question-archetypes.md#BC-QA-01013 Limit claim matched across graphical, numerical, and analytic representations
- research/exam/exam-structure.md#Section and part layout
- research/scoring/notation-requirements.md#Limit notation
- [inferred] Non-text delivery modes. Settled by the modality A/B.
- [inferred] ki-1 has no BC-EK. Settled by a library pass mapping the skills.
- [inferred] The representative functions in the figures. Settled by a figure_kind on BC-QA-01013.
- [inferred] Nothing written on the MCQ shape. Settled by timed response logs.
- BC-CON-01011 lists no misconceptions (unit-01 README, Library gaps); the possible reasons come from the misconceptions the error records link.
- Prediction and contrast stems: written for this lesson, no published item shares them (content/items_* searched). Citations sit in each block's `sources` array, never in served text.

## Machine record

```json
{
 "id": "LSN-CON-01011",
 "kind": "concept",
 "target_id": "BC-CON-01011",
 "unit": "01",
 "skills": [
  "BC-SKL-01036",
  "BC-SKL-01037",
  "BC-SKL-01038"
 ],
 "prediction": {
  "id": "pr-1",
  "stem": {
   "text": "Before the rule: \\(\\lim_{x\\to3^-}g(x)=\\infty\\). What do the outputs of \\(g\\) do as \\(x\\) nears 3 from the left?",
   "command_verb": "predict"
  },
  "format": "mcq",
  "options": [
   {
    "id": "A",
    "label": "They settle near 3.",
    "is_key": false
   },
   {
    "id": "B",
    "label": "They grow without bound.",
    "is_key": true
   },
   {
    "id": "C",
    "label": "They level off as \\(x\\) grows.",
    "is_key": false
   }
  ],
  "resolution": "Infinity in the value slot means the outputs grow without bound: a vertical asymptote at \\(x=3\\).",
  "sources": [
   "BC-CON-01011",
   "research/units/unit-01-limits-continuity.md#1.9 Connecting Multiple Representations of Limits"
  ]
 },
 "orientation": {
  "text": "One limit fact can be a graph, a table, a formula or a sentence. A response converts between them, keeping input, side and value.",
  "sources": [
   "BC-CON-01011",
   "research/units/unit-01-limits-continuity.md#1.9 Connecting Multiple Representations of Limits"
  ]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": null,
   "depth": "core",
   "text": "A conversion keeps the input approached, the side and the claimed value, and must not swap the limit for the function value, one sided for two sided, or an infinite limit for a limit at infinity. Infinity in the value slot says vertical asymptote; under the arrow, end behaviour.",
   "notation": "limit notation with its infinite forms",
   "quote": {
    "text": "This topic is intended to focus on connecting representations.",
    "source": "ced:46"
   },
   "sources": [
    "ced:46",
    "research/units/unit-01-limits-continuity.md#1.9 Connecting Multiple Representations of Limits"
   ]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-01013",
   "cue": "A limit fact in one form; which candidate matches?",
   "method": "Read the limit behaviour from the supplied representation.",
   "rival": "Swapping vertical asymptote and end behaviour.",
   "separating_feature": "Infinity in the value, or under the arrow.",
   "sources": [
    "BC-QA-01013"
   ],
   "evidence_tag": "verified",
   "contrast": {
    "this": {
     "text": "Given \\(\\lim_{x\\to5^+}p(x)=-\\infty\\), describe the graph of \\(p\\) near \\(x=5\\).",
     "archetype_id": "BC-QA-01013"
    },
    "not_this": {
     "text": "Find \\(\\lim_{x\\to5}\\frac{x^2-25}{x-5}\\).",
     "why_not": "It asks for a computed value, not a conversion."
    },
    "feature": "One limit fact given, asked for in another form."
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
    "number": 3,
    "side": "left",
    "growth": "up",
    "direction": "positive",
    "letter": "g",
    "statement": "infinite_limit"
   },
   "problem": {
    "text": "Given \\(\\lim_{x\\to3^-}g(x)=\\infty\\), describe the graph of \\(g\\) near \\(x=3\\).",
    "command_verb": "describe"
   },
   "calculator_status": "no_calculator",
   "steps": [
    {
     "cue": "The arrow points to 3 with a minus sign.",
     "why": "The input approaches 3 from the left only; the right side is not given."
    },
    {
     "cue": "The value slot holds \\(\\infty\\), not a number.",
     "why": "Outputs grow without bound, so no real limit exists."
    },
    {
     "cue": "Infinity sits in the value, not under the arrow.",
     "why": "That is a vertical asymptote at \\(x=3\\), not end behaviour."
    },
    {
     "cue": "The stem asks for the behaviour in words.",
     "why": "Left of 3, \\(g(x)\\) increases without bound: vertical asymptote \\(x=3\\)."
    }
   ],
   "answer": {
    "form": "statement",
    "expr": "x = 3"
   }
  },
  {
   "id": "ex-2",
   "archetype_id": "BC-QA-01013",
   "bands": [
    "low"
   ],
   "parameter_draw": {
    "number": -2,
    "side": "left",
    "growth": "up",
    "direction": "positive",
    "letter": "k",
    "statement": "limit_at_infinity"
   },
   "problem": {
    "text": "Given \\(\\lim_{x\\to\\infty}k(x)=-2\\), describe the graph of \\(k\\).",
    "command_verb": "describe"
   },
   "calculator_status": "no_calculator",
   "steps": [
    {
     "cue": "Infinity sits under the arrow: \\(x\\) grows without bound.",
     "why": "This is end behaviour on the right, not behaviour near a finite input.",
     "expr": "Limit(k(x), x, oo) = -2",
     "relation": "new"
    },
    {
     "cue": "The value is the number \\(-2\\).",
     "why": "As \\(x\\) grows, \\(k(x)\\) approaches \\(-2\\): horizontal asymptote \\(y=-2\\) on the right.",
     "expr": "y = -2",
     "relation": "new"
    }
   ],
   "answer": {
    "form": "statement",
    "expr": "y = -2"
   },
   "fade_from": 2
  }
 ],
 "what_a_reader_scores": [],
 "common_errors": [
  {
   "error_id": "BC-ERR-01002",
   "observed_behavior": "The response reports the value approached from one side as the limit although the two sides differ.",
   "scoring_consequence": "The value point is lost because the correct response is that the limit does not exist.",
   "wrong_step": {
    "text": "The left side is written as the two sided claim \\(\\lim_{x\\to3}g(x)=\\infty\\).",
    "expr": "Limit(g(x), x, 3, '+-')"
   },
   "right_step": {
    "text": "Only \\(\\lim_{x\\to3^-}g(x)=\\infty\\) is given.",
    "expr": "Limit(g(x), x, 3, '-')"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-01002",
    "text": "treats a single one sided approach as sufficient"
   },
   "sources": [
    "BC-ERR-01002",
    "BC-MIS-01002"
   ],
   "fix_prompt": true
  },
  {
   "error_id": "BC-ERR-01020",
   "observed_behavior": "The response writes that the limit equals infinity and then treats that statement as an existence claim for a real limit.",
   "scoring_consequence": "A point requiring a statement about existence is lost.",
   "wrong_step": {
    "text": "The limit is recorded as \\(L=\\infty\\) and said to exist.",
    "expr": "L = oo"
   },
   "right_step": {
    "text": "No real limit exists; the graph has the vertical asymptote \\(x=3\\).",
    "expr": "x = 3"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-01012",
    "text": "reads the infinity symbol as a real value"
   },
   "sources": [
    "BC-ERR-01020",
    "BC-MIS-01012"
   ],
   "fix_prompt": true
  },
  {
   "error_id": "BC-ERR-01033",
   "observed_behavior": "The response treats a vertical asymptote statement as an end behaviour statement or the reverse.",
   "scoring_consequence": "The conversion point is lost.",
   "wrong_step": {
    "text": "From \\(\\lim_{x\\to\\infty}k(x)=-2\\): a vertical asymptote \\(x=-2\\).",
    "expr": "x = -2"
   },
   "right_step": {
    "text": "A horizontal asymptote \\(y=-2\\) on the right.",
    "expr": "y = -2"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-01018",
    "text": "vertical and horizontal asymptote statements are exchanged"
   },
   "sources": [
    "BC-ERR-01033",
    "BC-MIS-01018"
   ],
   "fix_prompt": true
  },
  {
   "error_id": "BC-ERR-01021",
   "observed_behavior": "The response substitutes the infinity symbol into the expression and performs arithmetic with it.",
   "scoring_consequence": "Arithmetic performed with the infinity symbol is treated as scratch work and does not earn the value point (sg-25:4).",
   "wrong_step": {
    "text": "The statement is rewritten as \\(k(\\infty)=-2\\).",
    "expr": "k(oo) = -2"
   },
   "right_step": {
    "text": "It stays a limit: \\(\\lim_{x\\to\\infty}k(x)=-2\\).",
    "expr": "Limit(k(x), x, oo) = -2"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-99008",
    "text": "substitutes the infinity symbol for the variable"
   },
   "sources": [
    "BC-ERR-01021",
    "BC-MIS-99008"
   ],
   "fix_prompt": true
  }
 ],
 "representations": null,
 "prerequisite_bridges": [
  {
   "prq_id": "BC-PRQ-01003",
   "text": "Pick the piecewise branch for an input; a wrong branch marks this gap."
  },
  {
   "prq_id": "BC-PRQ-06005",
   "text": "Read \\(f(t)\\) at a stated input; the wrong input marks this gap."
  }
 ],
 "time": {
  "exam_part": "I-A",
  "budget_minutes": 2.14,
  "source": "research/exam/exam-structure.md#Section and part layout",
  "written_steps": {
   "ex-1": [],
   "ex-2": []
  },
  "skipped_steps": {
   "ex-1": [
    1,
    2,
    3,
    4
   ],
   "ex-2": [
    1,
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
   "archetype_id": "BC-QA-01013",
   "parameter_draw": {
    "number": 3,
    "side": "left",
    "growth": "up",
    "direction": "positive",
    "letter": "g",
    "statement": "infinite_limit"
   },
   "completes": "ex-1",
   "stem": {
    "text": "In \\(\\lim_{x\\to3^-}g(x)=\\infty\\) the side is left and the value is infinite. Describe the graph near \\(x=3\\).",
    "command_verb": "describe"
   },
   "key": {
    "form": "statement",
    "expr": "x = 3"
   },
   "steps": [
    {
     "text": "Vertical asymptote \\(x=3\\), approached upward from the left.",
     "expr": "x = 3",
     "relation": "new"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-01037"
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
    "number": -1,
    "side": "right",
    "growth": "down",
    "direction": "negative",
    "letter": "f",
    "statement": "infinite_limit"
   },
   "stem": {
    "text": "Given \\(\\lim_{x\\to-1^+}f(x)=-\\infty\\), describe the graph of \\(f\\) near \\(x=-1\\).",
    "command_verb": "describe"
   },
   "key": {
    "form": "statement",
    "expr": "x = -1"
   },
   "steps": [
    {
     "text": "Right of \\(-1\\), \\(f(x)\\) decreases without bound: vertical asymptote \\(x=-1\\).",
     "expr": "x = -1",
     "relation": "new"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-01037"
   ]
  },
  {
   "id": "chk-3",
   "check_kind": "mcq",
   "format": "mcq",
   "bands": [
    "low"
   ],
   "archetype_id": "BC-QA-01013",
   "parameter_draw": {
    "number": 2,
    "side": "right",
    "growth": "down",
    "direction": "positive",
    "letter": "h",
    "statement": "infinite_limit"
   },
   "stem": {
    "text": "Which description matches \\(\\lim_{x\\to2^+}h(x)=-\\infty\\)?",
    "command_verb": "identify"
   },
   "key": {
    "form": "statement",
    "expr": "x = 2"
   },
   "steps": [
    {
     "text": "Vertical asymptote \\(x=2\\), approached downward from the right.",
     "expr": "x = 2",
     "relation": "new"
    }
   ],
   "options": [
    {
     "id": "A",
     "is_key": true,
     "label": "Right of 2, \\(h(x)\\) decreases without bound; vertical asymptote \\(x=2\\).",
     "error_path": null
    },
    {
     "id": "B",
     "is_key": false,
     "label": "As \\(x\\) grows, \\(h(x)\\) approaches 2; horizontal asymptote \\(y=2\\).",
     "error_path": "BC-ERR-01033",
     "derivation": "infinite limit read as end behaviour"
    },
    {
     "id": "C",
     "is_key": false,
     "label": "\\(h(x)\\) decreases without bound on both sides of 2.",
     "error_path": "BC-ERR-01002",
     "derivation": "one side read as both"
    },
    {
     "id": "D",
     "is_key": false,
     "label": "The limit of \\(h\\) at 2 exists and equals \\(-\\infty\\).",
     "error_path": "BC-ERR-01020",
     "derivation": "infinite limit read as an existing limit"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-01036",
    "BC-SKL-01037"
   ]
  }
 ],
 "delivery": [
  {
   "block": "orientation",
   "mode": "figure",
   "reason": "rule 3: BC-REP-02 on BC-SKL-01036 and BC-SKL-01038 (unit-01 README delivery map)",
   "sources": [
    "BC-SKL-01036",
    "BC-SKL-01038"
   ],
   "spec": {
    "kind": "graph",
    "window": {
     "x": [
      0,
      5
     ],
     "y": [
      -4,
      10
     ]
    },
    "curves": [
     {
      "expr": "1/(3-x)",
      "domain": [
       0,
       2.9
      ],
      "label": {
       "text": "g",
       "placement": "inside"
      }
     }
    ],
    "asymptotes": [
     {
      "x": 3,
      "style": "dashed",
      "label": {
       "text": "x = 3",
       "placement": "inside"
      }
     }
    ],
    "labels": [
     {
      "text": "one fact, four forms: graph, table, symbols, words",
      "placement": "inside"
     }
    ],
    "representations": [
     "graph"
    ]
   },
   "fallback": "Alt text: the curve rises without bound as \\(x\\) approaches 3 from the left, beside a dashed line \\(x=3\\).",
   "keyboard": "none needed: a static figure"
  },
  {
   "block": "ki-1",
   "mode": "figure",
   "reason": "rule 3: BC-REP-02 on BC-SKL-01036 and BC-SKL-01038, with rule 4 for BC-REP-03 on BC-SKL-01036: a figure with a table beside it, two representations, the cap",
   "sources": [
    "BC-SKL-01036"
   ],
   "spec": {
    "kind": "graph_with_table",
    "curves": [
     {
      "expr": "1/(3-x)",
      "domain": [
       0,
       2.9
      ],
      "label": {
       "text": "value slot: infinity",
       "placement": "inside"
      }
     },
     {
      "expr": "-2 + 1/x",
      "domain": [
       1,
       20
      ],
      "label": {
       "text": "under the arrow: infinity",
       "placement": "inside"
      }
     }
    ],
    "table": {
     "columns": [
      "x",
      "g(x)"
     ],
     "rows": [
      [
       "2.9",
       "10"
      ],
      [
       "2.99",
       "100"
      ],
      [
       "2.999",
       "1000"
      ]
     ],
     "label": {
      "text": "x approaching 3 from the left",
      "placement": "inside"
     }
    },
    "labels": [
     {
      "text": "x = 3",
      "placement": "inside"
     },
     {
      "text": "y = -2",
      "placement": "inside"
     }
    ],
    "representations": [
     "graph",
     "table"
    ]
   },
   "fallback": "The table alone with the two statements in words beneath it.",
   "keyboard": "Tab moves between the graph and the table; arrow keys move through table rows."
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
   "block": "err-BC-ERR-01002",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-01020",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-01033",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-01021",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  }
 ],
 "refresher": [
  "ki-1",
  "err-BC-ERR-01002",
  "err-BC-ERR-01020",
  "err-BC-ERR-01033",
  "err-BC-ERR-01021",
  "ex-1"
 ],
 "research_lines": [
  {
   "file": "research/units/unit-01-limits-continuity.md",
   "line": "MCQ forms ask which of several representations matches a stated limit behaviour."
  }
 ],
 "inferred": [
  {
   "claim": "The non-text delivery modes chosen here serve the content better than text and step reveal.",
   "settles": "The modality A/B in the build plan: skip rate and time to first credited success by mode."
  },
  {
   "claim": "No skill of BC-CON-01011 lists essential_knowledge, so ki-1 carries ek_id null and paraphrases the topic's Required mathematical knowledge paragraph.",
   "settles": "A library pass mapping BC-SKL-01036 to 01038 to a BC-EK (ced:46 prints none for topic 1.9)."
  },
  {
   "claim": "The figure and table use the representative functions 1/(3 - x) and -2 + 1/x; the archetype states the limit fact only.",
   "settles": "A figure_kind in the BC-QA-01013 representation_bindings, which is null today."
  },
  {
   "claim": "On the MCQ shape a fluent solver writes nothing and reads the side, the slot of the infinity symbol and the value in the head.",
   "settles": "Timed response logs on BC-QA-01013 items."
  }
 ],
 "sources": [
  "BC-CON-01011",
  "BC-SKL-01036",
  "BC-SKL-01037",
  "BC-SKL-01038",
  "ced:46",
  "sg-25:4",
  "BC-QA-01013",
  "BC-ERR-01002",
  "BC-ERR-01020",
  "BC-ERR-01033",
  "BC-ERR-01021",
  "BC-MIS-01002",
  "BC-MIS-01012",
  "BC-MIS-01018",
  "BC-MIS-99008",
  "BC-PRQ-01003",
  "BC-PRQ-06005",
  "research/units/unit-01-limits-continuity.md#1.9 Connecting Multiple Representations of Limits",
  "research/question-analysis/question-archetypes.md#BC-QA-01013 Limit claim matched across graphical, numerical, and analytic representations",
  "research/exam/exam-structure.md#Section and part layout",
  "research/scoring/notation-requirements.md#Limit notation"
 ],
 "read_minutes": {
  "full": 4.19,
  "brief": 2.99
 },
 "word_count": {
  "full": 627,
  "brief": 447
 }
}
```
