---
title: Item Generation
research_date: 2026-09-19
status: draft
purpose: How the 139 active archetypes become generated items with verified keys, controlled difficulty, error-derived distractors, and a copyright and duplicate gate, with every parameter sourced or marked inferred.
---

# Item Generation

This document specifies how the app produces the items it serves. Decision D5 in the decisions memo binds the pipeline shape; D2 and D3 supply the difficulty target that generation must hit; D11 supplies the quality gates. Plan document 03 owns what happens to an item after a student answers it.

Every number below carries its source URL and an evidence tag. Where no source exists the text says unknown.

The pipeline described here starts in P4. Generation, the independent re-solve and the item review queue are all P4 work (R9). P1 items are authored by hand, 10 per P1 archetype, with the archetype record used as the mould exactly as this document uses it for a generated item: the same `invariant_structure` constraint, the same difficulty dials, the same `common_distractors` seeded from named BC-ERR paths, and the same worked solution tagged to the archetype's point types where it has any. A hand-authored item passes the same SymPy equivalence check, the same numeric check and the same distractor checks as a generated one, and it carries a provenance record with `model` set to `"operator"` and the parameter seed recorded as the operator's chosen draw. What P1 does not run is the generator prompt, the independent re-solve and the review queue, because with 130 items of which 100 are hand-audited without the key there is nothing for them to catch that the author has not already seen. P1 ships the SymPy checker, the numeric check and the distractor checks regardless, because plan document 03's grader needs them.

The app never serves an official stem, an official figure, or official rubric text. The released material is read as structure only. College Board's permission instructions define commercial use to include "test-prep settings" (25-word cap respected; https://privacy.collegeboard.org/copyright-trademark/request-instructions [verified]), and the exam booklets carry a stronger notice against unauthorized reproduction or use of any part of the test (https://apcentral.collegeboard.org/media/pdf/ap-hybrid-digital-exams-free-response-booklets-overview.pdf [verified]).

## Archetypes as item models

### The Gierl and Lai frame

Automatic item generation as Gierl and Lai describe it is three steps: develop a cognitive model with subject-matter experts specifying the content and the reasoning required, develop an item model that is "like a mould or rendering that highlights the features in an assessment task that must be manipulated", then assemble by algorithm, with a claimed yield of hundreds or thousands of items per model (https://ncme.org/wp-content/uploads/2025/10/Module-34-Automated-Item-Generation-Gierl-Lai.pdf and https://onlinelibrary.wiley.com/doi/abs/10.1111/emip.12018 [verified]). Automatic item generation is also argued as a test-security mechanism, because generating from a model rather than reusing a fixed item limits exposure of any single item (https://www.frontiersin.org/journals/education/articles/10.3389/feduc.2022.853578/full [single-source]).

`data/archetypes.json` already holds item models in that sense: 139 active BC-QA records in 77 families with 395 BC-QV variants (computed 2026-09-19 from `data/archetypes.json` [verified]). Track 3 records that the archetype schema is a closer match to Gierl and Lai's item-model construct than the library's own documentation claims for it, and that the library does not currently cite that literature. This plan adopts the frame explicitly: the archetype record is the item model, `research/question-analysis/question-archetypes.md` is the human-readable view of it, and generation is parameter substitution into a validated mould rather than a free-form request to write a question like a named released item. Free-form generation from a released item is both the legally riskier path and the one that drifts off the construct (track 3's recommendation).

### Field-by-field mapping to generation inputs

| Archetype field | Role in generation |
| --- | --- |
| `invariant_structure` | A hard constraint stated in the prompt and re-asserted as a Monte Carlo assertion. For BC-QA-06001 it fixes that the rate is tabulated at unevenly spaced inputs, that the number of subintervals equals the number of gaps, and that widths are differences of consecutive table inputs. A draw that violates it is rejected, not repaired. |
| `safe_variables` | The features that may vary without changing what is measured. For BC-QA-06001 these include the quantity being accumulated. Today this is prose, which is the gap named below. |
| `difficulty_variables` | The features that change how hard the item is. For BC-QA-06001: uniform versus nonuniform widths, left versus right endpoint, whether an over or under estimate justification is demanded, whether an interpretation with units is demanded, whether the table is monotone. These become the dials. |
| `difficulty_factors` | The BC-DF ids the archetype is allowed to move. BC-QA-06001 carries BC-DF-01, 03, 05, 10, 14, 15, 16. A dial outside this list is not available on this archetype. |
| `common_distractors` | The seed list for MCQ option generation, each to be rewritten as a named error path. BC-QA-06001 lists using a single uniform width for unevenly spaced data, using the opposite endpoint, summing rate values without multiplying by widths, and dividing by the number of subintervals. |
| `expected_solution_path` | The ordered steps the worked solution must contain, which is also the tagging spine for BC-PT ids. |
| `calculator_status` | Passed to the generator and asserted by the verifier. The distribution over 139 active archetypes is no_calculator 75, either 37, calculator 27 (computed 2026-09-19 from `data/archetypes.json` [verified]). |
| `representations` | The BC-REP codes the archetype may present. The library defines 14, BC-REP-01 through BC-REP-14. |
| `point_types` | The BC-PT ids the item's worked solution steps are tagged to, and the rubric the grader in plan document 03 will run. |
| `typical_wording` | Phrasing patterns, used as style guidance only. Never copied from an official stem; the archetype record's wording is already a paraphrase written for the library. |
| `skills`, `prerequisites`, `misconceptions` | Metadata carried onto the item so the engine and the diagnostician can use it without re-deriving it. |
| `scoring_pattern`, `multipart_structure` | Shape constraints for free-response variants: how many points, how the parts divide. |

### The missing parameter spec

`safe_variables` and `difficulty_variables` are prose lists today, on all 139 active archetypes (computed 2026-09-19 from `data/archetypes.json` [verified]). D5 and D13(c) both name this as the library gap generation depends on. A generator handed "the quantity being accumulated" has to invent both the domain and its bounds, and two independent draws will disagree about what is legal.

What the spec must contain per archetype, per parameter:

- `name`, `type` (integer, rational, real, symbol, function_form, interval, label, unit), and `role` (`safe` or `difficulty`). A `safe` parameter is a declared incidental in Bejar's sense and a `difficulty` parameter a declared radical; the declaration is checked rather than trusted, by varying each `safe` parameter alone and requiring the structure of every solution step and of the key to stay fixed (`13-ai-engineering.md`, Radicals and incidentals). Distractor composition is always a radical.
- `domain`: an explicit set or range, for integers a list or a bounded range with a step, for symbols an allowed alphabet, for function forms an enumerated list of shapes rather than free text.
- `constraints`: predicates over the whole draw, written so a checker can evaluate them. For BC-QA-06001 these include that consecutive table inputs are strictly increasing, that at least two gap widths differ, and that no width is zero.
- `derived`: values computed from the draw rather than drawn, with the expression that computes them.
- `invariants`: the assertions the Monte Carlo pass checks, restating `invariant_structure` in evaluable form.
- `dial_bindings`: which BC-DF id each difficulty parameter moves, and which setting of that dial each value of the parameter corresponds to.
- `calculator_guard`: the predicate that decides whether the drawn instance is closed-form solvable, required on every archetype whose `calculator_status` is `no_calculator` or `either`.
- `representation_bindings`: which BC-REP codes the parameter set can render into, and what additional parameters each rendering needs (a graph needs a window, a table needs row count).

Corrected 2026-09-24: the spec exists for all 139 active archetypes as `parameter_spec` on each archetype record, with its schema at `schemas/archetypes.schema.json` `$defs/parameter_spec`. A `difficulty` binding to a two-state dial uses `off` and `low`. Each spec was authored with its template (`app/generation/templates/`) and merged through `data/staging/parameter-spec-p4.json`, a fields-only staging file, and `tests/generation/test_parameter_specs.py` keeps the two identical. See docs/operator/p4-generation.md.

Until that spec exists in the library, generation runs archetype by archetype from a spec authored alongside the first generated items for that archetype, held in the app repository and proposed back to the library as a staging file. That is the D12 phase ordering: P1 covers SymPy-verifiable no-calculator archetypes in Units 1 to 3, so the first specs written are for those. 56 active archetypes carry no `point_types` at all, listed in the repo-facts sheet, so their free-response variants cannot be point-graded and they are generated as multiple-choice or short-answer only until the library fills the field.

Alternative rejected: letting the generator infer the parameter domain from `safe_variables` prose on each call. It needs no library work and it is what a first prototype does. Rejected on learning impact, because an item whose parameters drifted outside the archetype's construct is measuring something the engine will credit to the wrong skill, and rejected on cost, because every Monte Carlo family check would have to re-derive the domain it is testing against.

## Generation contract

### Input schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "GenerationRequest",
  "type": "object",
  "required": [
    "archetype_id", "variant_id", "format", "calculator_status",
    "representation", "difficulty_settings", "parameter_draw",
    "point_types", "prompt_version"
  ],
  "properties": {
    "archetype_id": { "type": "string" },
    "variant_id": { "type": "string", "description": "BC-QV id" },
    "format": { "enum": ["mcq", "free_response_part", "short_answer"] },
    "option_count": {
      "type": "integer",
      "description": "Required when format is mcq. See the distractor section: the current framework uses 4."
    },
    "calculator_status": { "enum": ["no_calculator", "calculator", "either"] },
    "representation": { "type": "string", "description": "BC-REP id" },
    "target_success_probability": {
      "type": "number",
      "description": "Guessing-corrected p_A requested by plan document 02's Item selection algorithm."
    },
    "difficulty_settings": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["difficulty_factor_id", "setting"],
        "properties": {
          "difficulty_factor_id": { "type": "string" },
          "setting": { "enum": ["off", "low", "medium", "high"] }
        }
      }
    },
    "parameter_draw": {
      "type": "object",
      "description": "Concrete values for every parameter in the archetype's parameter spec. Drawn by the backend, never by the model."
    },
    "invariant_structure": { "type": "string" },
    "expected_solution_path": { "type": "array", "items": { "type": "string" } },
    "point_types": { "type": "array", "items": { "type": "string" } },
    "distractor_error_paths": {
      "type": "array",
      "items": { "type": "string", "description": "BC-ERR ids, one per required distractor" }
    },
    "typical_wording": { "type": "array", "items": { "type": "string" } },
    "forbidden_text": {
      "type": "array",
      "items": { "type": "string" },
      "description": "Empty by design. The generator is never given official stem text."
    },
    "prompt_version": { "type": "string" }
  }
}
```

The parameter draw is made by the backend from the archetype's parameter spec, not by the model. That keeps the family reproducible, keeps the Monte Carlo pass and the runtime draw using one code path, and makes provenance a record of a seed rather than a record of a conversation.

### Output schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "GeneratedItem",
  "type": "object",
  "required": ["stem", "key", "worked_solution"],
  "properties": {
    "stem": {
      "type": "object",
      "required": ["text"],
      "properties": {
        "text": { "type": "string", "description": "Plain text with inline LaTeX. No official wording." },
        "command_verb": { "type": "string" },
        "setup_required": {
          "type": "boolean",
          "description": "True on calculator items, which must ask for the setup. See the difficulty section."
        },
        "radian_mode_note": { "type": "boolean" }
      }
    },
    "figure": {
      "type": "object",
      "description": "Declarative spec. Never an image emitted by the model.",
      "properties": {
        "kind": {
          "enum": ["function_graph", "slope_field", "table", "region",
                   "parametric_curve", "polar_curve", "vector_diagram",
                   "number_line", "geometric_diagram"]
        },
        "domain": { "type": "array", "items": { "type": "number" } },
        "range": { "type": "array", "items": { "type": "number" } },
        "curves": { "type": "array", "items": { "type": "object" } },
        "marks": { "type": "array", "items": { "type": "object" } },
        "labels": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "text": { "type": "string" },
              "anchor": { "type": "array", "items": { "type": "number" } },
              "placement": { "enum": ["inside"] }
            }
          },
          "description": "Placement is always inside the figure. See the figures section."
        },
        "gridlines": { "type": "boolean" },
        "axis_titles": { "type": "array", "items": { "type": "string" } }
      }
    },
    "options": {
      "type": "array",
      "description": "Present when format is mcq.",
      "items": {
        "type": "object",
        "required": ["id", "text", "is_key"],
        "properties": {
          "id": { "type": "string" },
          "text": { "type": "string" },
          "is_key": { "type": "boolean" },
          "generating_error_path": {
            "type": "string",
            "description": "BC-ERR id. Required on every option where is_key is false."
          },
          "distractor_mechanism": {
            "enum": ["conceptual_confusion", "algebra_slip", "sign_error",
                     "wrong_limits", "reversed_quantities", "chain_rule_omitted",
                     "product_rule_omitted", "theorem_condition_ignored",
                     "forgot_constant", "compound"],
            "description": "Category from research/question-analysis/distractor-taxonomy.md"
          },
          "candidate_misconceptions": {
            "type": "array", "items": { "type": "string" }
          }
        }
      }
    },
    "key": {
      "type": "object",
      "required": ["form"],
      "properties": {
        "form": { "enum": ["symbolic", "numeric", "interval", "statement", "option_id"] },
        "latex": { "type": "string" },
        "sympy": { "type": "string", "description": "Parseable expression for the verifier." },
        "numeric": { "type": "number" },
        "decimals": { "type": "integer", "description": "3 on reported-value calculator items." },
        "units": { "type": "string" }
      }
    },
    "worked_solution": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["step", "text"],
        "properties": {
          "step": { "type": "integer" },
          "text": { "type": "string" },
          "point_type_id": {
            "type": "string",
            "description": "BC-PT id this step earns, or absent for a step that earns nothing."
          },
          "rule_named": { "type": "string" },
          "sympy": { "type": "string" }
        }
      }
    },
    "metadata": {
      "type": "object",
      "required": ["archetype_id", "variant_id", "difficulty_settings",
                   "representation", "calculator_status", "provenance"],
      "properties": {
        "archetype_id": { "type": "string" },
        "variant_id": { "type": "string" },
        "skills": { "type": "array", "items": { "type": "string" } },
        "prerequisites": { "type": "array", "items": { "type": "string" } },
        "point_types": { "type": "array", "items": { "type": "string" } },
        "difficulty_settings": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "difficulty_factor_id": { "type": "string" },
              "setting": { "enum": ["off", "low", "medium", "high"] }
            }
          }
        },
        "representation": { "type": "string" },
        "calculator_status": { "enum": ["no_calculator", "calculator", "either"] },
        "predicted_success_probability": { "type": "number" },
        "provenance": {
          "type": "object",
          "required": ["parameter_seed", "model", "prompt_version", "generated_at"],
          "properties": {
            "parameter_seed": { "type": "string" },
            "parameter_draw": { "type": "object" },
            "model": { "type": "string", "description": "Provider model id, or \"operator\" on a hand-authored item." },
            "prompt_version": { "type": "string" },
            "generated_at": { "type": "string" },
            "spec_version": { "type": "string" },
            "content_snapshot": { "type": "string" }
          }
        }
      }
    }
  }
}
```

Corrected 2026-09-20: `metadata` left the `required` list and is no longer model output. Every field in it is an echo of the generation request, so the backend writes it and a model that restates one of them wrongly can no longer corrupt an item's provenance. Measured on a full-schema record, `metadata` was 32.0 percent of the emitted characters against the worked solution's 26.0 percent. The `metadata` schema below stays as the definition of the block the backend writes. See `13-ai-engineering.md`.

Two properties of this contract matter more than the field list. First, the figure is a declarative spec rather than an image or an SVG string, so the renderer controls label placement and the same spec can be re-rendered at another size, in dark theme, or as a table. Second, every worked-solution step carries the BC-PT id it earns, which is what lets the grader in plan document 03 run per-point calls against a generated item with no extra authoring.

## Difficulty control

The library defines 17 difficulty factors, BC-DF-01 through BC-DF-17 (computed 2026-09-19 from `data/taxonomies.json` [verified]). Each is treated as a dial with a small set of settings, and an archetype may only move the dials its own `difficulty_factors` list carries. Every allowed-setting definition below is [inferred]: the library records the factors but attaches no numeric weights to them, which is gap D13(i), so none of these settings is sourced.

| Dial | Allowed settings |
| --- | --- |
| BC-DF-01 Number of concepts combined | low: one concept. medium: two. high: three or more. |
| BC-DF-02 Prerequisite depth | low: prerequisites are one hop from the primary skill. medium: two hops. high: three or more, over hard_prerequisite edges in `data/prereq_edges.csv`. |
| BC-DF-03 Unusual representation | off: the archetype's modal representation. on: any other BC-REP the archetype allows. |
| BC-DF-04 Notation complexity | low: single notation system. medium: mixed prime and Leibniz, or sigma notation. high: nested or inverse-function notation. |
| BC-DF-05 Contextual interpretation | off: bare mathematics. low: a named context with no interpretation demanded. high: an interpretation sentence demanded. |
| BC-DF-06 Algebraic burden | low: at most two manipulation steps after the calculus step. medium: three to four. high: five or more. |
| BC-DF-07 Calculator workflow | off: no calculator. low: one stored computation. high: two or more chained calculator results. Only available when `calculator_status` permits. |
| BC-DF-08 Multi-step dependency | low: parts independent. medium: one part consumes an earlier result. high: a chain of three. |
| BC-DF-09 Theorem recognition | off: the theorem is named in the stem. on: the student must select it. |
| BC-DF-10 Required justification | off: none. low: a conclusion sentence. high: hypotheses stated, verified, and concluded. |
| BC-DF-11 Unfamiliar surface presentation | off: standard presentation. on: an unusual but legal surface, for example an implicitly defined function where an explicit one is usual. |
| BC-DF-12 Sign and direction handling | low: all quantities positive. medium: one sign change. high: signed quantities on both sides of a comparison. |
| BC-DF-13 Reversed reasoning direction | off: forward. on: the answer is given and a condition must be recovered. |
| BC-DF-14 Missing or implicit given | off: everything stated. on: one given must be inferred from the figure, table, or context. |
| BC-DF-15 Unsignposted procedure selection | off: the method is named. on: the student selects among confusable methods. |
| BC-DF-16 Units and labelling demand | off: none. low: units on the final answer. high: units plus a labelled interpretation. |
| BC-DF-17 Case splitting at a boundary | off: single case. on: a piecewise or boundary case must be split. |

### Mapping a requested success probability to dial settings

Plan document 02's Item selection algorithm asks for an archetype whose predicted success probability is near a target: 0.8 on the guessing-corrected scale in learning mode, 0.5 in diagnostic mode for free response and 0.625 raw for four-option multiple choice (D3 as corrected in 02-adaptive-engine.md; Math Academy tunes to about 80 percent, https://www.mathacademy.com/how-our-ai-works [single-source, vendor-published]; Wilson et al derive about 85 percent for a narrow formal class and state it does not yet generalise to multi-choice tasks or other learning algorithms, https://www.nature.com/articles/s41467-019-12552-4 [verified]; ALEKS uses 0.5 for open response, https://www.aleks.com/about_aleks/Science_Behind_ALEKS.pdf [verified]).

The mapping from a requested probability to a dial vector is [inferred] in full. The rule:

```
choose_settings(archetype, target_p, skill_state):
    base = beta_prior(archetype)          # D2 as amended by R1:
                                          #   -0.35 * (mean BC-DF count - 2)
    gap  = logit(target_p) - predicted_logit(archetype at all dials off,
                                             skill_state)

    # each dial at "on" or "low" costs 0.35 logits, "medium" 0.7, "high" 1.05
    budget = -gap                          # logits of difficulty to spend
    dials  = archetype.difficulty_factors
    rank   = order dials by (skill_state.weakest_related_skill first,
                             then representation_gap,
                             then lowest observation_count)

    settings = {d: "off" for d in dials}
    for d in rank:
        while budget >= cost(next_setting(settings[d])) :
            settings[d] = next_setting(settings[d])
            budget -= cost(settings[d])
            if budget < 0.35: break
    return settings
```

The 0.35 logits per dial step is the same constant D2 uses for the beta prior. Per R1 that prior is centred rather than raw: `beta_k = -0.35 * (mean BC-DF count over the archetypes that list k in their skills array - 2)` (R25), where 2 is the median BC-DF count across the 139 active archetypes (distribution 1:32, 2:40, 3:34, 4:23, 5:6, 6:3, 7:1, computed 2026-09-19 from `data/archetypes.json` [inferred; the 0.35 coefficient stays tunable in D2]). The dial arithmetic reuses that centred form, so a median-difficulty archetype at all dials off starts at p = 0.5 and each dial step costs 0.35 logits from there. Using one constant in both places keeps the prior and the dial arithmetic consistent, so a generated item's predicted difficulty equals what the engine already believed about an archetype carrying that many factors. It is a modelling convenience, and it is the parameter most likely to be wrong.

Two hard rules override the budget. A calculator-part item always sets BC-DF-16 to at least `low` and sets `setup_required`, because the setup requirement is carried in the question stem on the real exam and not only in the rubric: the 2025 Question 1 calculator part ends by asking the student to show the setup for the calculations (https://apcentral.collegeboard.org/media/pdf/ap25-sg-calculus-bc.pdf [verified]). And a no-calculator item always sets BC-DF-07 to `off`, enforced by the verifier rather than trusted to the generator.

Alternative rejected: predicting difficulty from response data. Pelanek states the system needs at least 100 students to get good estimates of item difficulty (https://www.fi.muni.cz/~xpelanek/publications/CAE-elo.pdf [verified]), and this app has one student, so declared difficulty from the BC-DF dials is the only option available. The consequence is recorded in D2: beta_k is not learned.

## Distractor mechanisms

### Option count

`research/question-analysis/mcq-analysis.md` states that the 2012 released BC practice exam is the only source with five options and that both current-framework sources, the course and exam description sample set and the standalone sample set, use four (https://apcentral.collegeboard.org, cached as BC-SRC-ced and BC-SRC-sample-questions; the counts are recorded per source in that file [verified]). The per-source table gives 22 questions at four options, 24 questions at four options, and 45 questions at five options.

So the app generates four options for current-framework multiple choice. Whether the 2027 administration's 42-question Section I uses four options is unknown; no source in the corpus states it, and the 2027 sample material is not yet published (track 3 records that full-length 2027 sample booklets were promised for early 2027 and are not yet available).

The decisions memo and plan document 02 agree with that choice and there is no conflict between them: both use four options, a 3PL guessing floor of 0.25, MCQ success credited at 0.75, and a diagnostic raw target of 0.5 * 0.75 + 0.25 = 0.625 (R19). The app stores the option count per item, so a future form with a different count changes the stored value rather than the credit rule. The 2027 option count stays unknown, as stated above, and is listed in 12-open-questions.md.

### Each distractor comes from a named error path

Every non-key option is generated from a named BC-ERR record, carried in `generating_error_path`, and categorised against the mechanism taxonomy in `research/question-analysis/distractor-taxonomy.md`. That file's categories and their sizes across 91 records and 318 option entries are conceptual confusion 164 entries over 74 records, algebra slip 44 over 31, not determined 28 over 15, sign error 23 over 19, chain rule omitted 12 over 8, wrong limits 12 over 6, reversed quantities 10 over 9, theorem condition ignored 7 over 7, forgot constant 6 over 6, product rule omitted 5 over 5, and compound 4 over 4 (all from that file [inferred, as the file itself records: 287 entries carry `inferred`, 31 carry `uncertain`, none `verified`, and no official rationale exists for any option in any source document]).

Generating from an error path rather than from "plausible wrong answers" is what makes option choice a diagnostic signal instead of noise. Plan document 03 passes the selected option to the diagnostician, which reads `generating_error_path` and enters the error into `observed_errors[]` with the same machinery an FRQ error uses. An option generated without a named path would produce an observation the diagnostician cannot interpret, which throws away most of the value of asking a multiple-choice question at all.

**Where the BC-ERR id is stored (R26).** The machine-readable link is a field on the item, not on the archetype: each entry of `items.options` carries `error_path`, a BC-ERR id or null. The key's is null and every distractor's is a BC-ERR id. From P4 the generator emits it as `generating_error_path` and it is written straight to `error_path`. In P1 there is no generator, so the operator records it by hand on each of the 130 items while authoring them, choosing the BC-ERR record from the 40 that the P1 skills carry. `archetypes.common_distractors` is prose in every case, an authoring guide for a human, and no component ever parses it.

The archetype's `common_distractors` prose is the seed. For BC-QA-06001 the four entries map onto BC-ERR records in the unit 06 block describing a uniform width applied to unevenly spaced data, the opposite endpoint selected, rate values summed without widths, and a division by the number of subintervals. Where an archetype's `common_distractors` entry has no matching BC-ERR record, the generator may still produce the option but the item is flagged for review and the missing error is proposed back to the library as a staging record, exactly as plan document 03 proposes a new error from a student response.

### Checks on the option set

Every generated option set is checked before the item can be published:

- Each distractor is not equal to the key symbolically, via SymPy.
- Each distractor is not equal to the key numerically, evaluated at several points for expression-valued keys and directly for numeric keys.
- The distractors are pairwise distinct, symbolically and numerically.
- Each non-key option carries a `generating_error_path` that resolves to an active BC-ERR id.
- No distractor is an alternative correct form of the key, which the symbolic check catches only when SymPy settles the comparison; an unsettled comparison sends the item to review rather than publishing it.

Track 3 states the reason for the strictness: a distractor that accidentally equals the key is the single worst failure an MCQ bank can ship. Both the symbolic and the numeric check are required because algebraically inequivalent forms can look similar and because SymPy equivalence is undecidable in general and returns unevaluated results on some expressions, so the fraction of BC-relevant expressions it can settle is unknown until measured (track 3 [inferred]).

## Independent key verification

The generating model's own answer is a hypothesis, not a key. The pipeline is five checks and publication requires unanimous agreement.

**Independent re-solve.** A second model, on a different provider where the routing allows it, receives the stem, the figure spec, and nothing else. It does not see the key, the worked solution, or the generating model's output. Its answer is compared to the candidate key symbolically and numerically. D8 as corrected on 2026-09-20 routes the verifier role to `gemini-3.5-flash-lite` on batch at the paid tier, with `gemini-3.8-flash` on batch as the second deployment and `claude-sonnet-5` on batch as the third, so that the verifier is never the generator's own model; the tier within Gemini was chosen on cost in `14-token-economy.md` and is defended by this section's own structure, since the re-solve's answer is never trusted and is compared under SymPy against a key the free checks already agree on; the constraint that the verifier must not see the key is a property of the prompt, not of the model choice, and the constraint that the verifier be decorrelated from the generator is a property of the routing. See `13-ai-engineering.md`.

**SymPy equivalence.** For closed-form keys, meaning derivatives, antiderivatives, limits, series coefficients, and equation solutions, the two answers are compared by symbolic simplification. An unsettled comparison is not a pass.

**Numeric evaluation at several points.** Both candidate answers are evaluated at several parameter values in the legal domain. This catches algebraically inequivalent forms that look similar, which the symbolic check can miss when it does not settle.

**Monte Carlo over the parameter family.** This check is a property of the parameter spec rather than of an item, so it runs once per archetype per spec version before any item is generated, not once per item; the full cheapest-first ordering of the five checks is in `13-ai-engineering.md`. A few hundred parameter tuples are drawn from the archetype's parameter spec, the solution path is run symbolically on each, and the `invariants` from the spec are asserted throughout: the integral converges, the denominator does not vanish on the interval, the series radius is finite and positive, the answer stays in a reportable range, the three-decimal answer is not degenerate. Track 3's argument for this is that these are parametrised families, which is a verification advantage nobody grading a one-off problem has, and that a family failing on 2 percent of draws is a family with a latent bad item. A family whose failure rate exceeds a threshold is quarantined rather than having the failing draws filtered out, because filtering hides a spec defect. The threshold is [inferred] and starts at zero failures on 300 draws for P1 archetypes.

**Calculator-boundary assertion.** A no-calculator item's verified solution path must be closed-form solvable with no numeric root-finding step. A calculator item's answer must be stated to three decimals, per the published general scoring note that decimal approximations should be accurate to three places after the decimal point (https://apcentral.collegeboard.org/media/pdf/ap25-sg-calculus-bc.pdf [verified]). Track 3's framing is that a Section I Part A item whose verified answer requires numeric root-finding is a mis-filed item, not a hard item.

**Publication rule.** Unanimous agreement publishes. Any disagreement routes to the item review queue and is never averaged.

Unanimity is conditional on one measurement that P1 makes (R9). SymPy equivalence is undecidable in general and the fraction of BC-relevant expressions it can settle is unknown, so P1 measures the settle rate on the 40-pair `answers_equiv/` fixture and publishes it before P4 commits to unanimity as the publication rule. If the settle rate is high, unanimity across the independent re-solve, the symbolic check and the numeric check stands as written. If it is low, unanimity would send a large share of the bank to a queue with one reviewer in it, so the rule degrades instead: numeric agreement between the independent re-solve and the candidate key at several points in the legal domain publishes the item, and only the expressions SymPy leaves unsettled go to operator review. The threshold that separates high from low is set when the settle rate is known and is not guessed here.

**Fail-closed.** An archetype with no published item is excluded from selection entirely and logged as a coverage gap for the operator (R18). The engine never relaxes the fringe or substitutes a neighbouring archetype to fill a hole in the bank, because a substituted item credits the wrong skills. P1 cannot hit this case, since its items are hand-authored and every P1 archetype is authored to the same count.

The supporting evidence is thinner than the pipeline's confidence suggests, which is why the pipeline is this heavy. Self-consistency, sampling several reasoning chains and taking the majority, gave large absolute gains on arithmetic reasoning: GSM8K +17.9 percent, SVAMP +11.0, AQuA +12.2 over plain chain of thought (https://arxiv.org/pdf/2203.11171 [verified]). Process supervision, giving feedback on each intermediate step rather than the final answer, outperformed outcome supervision, and the released PRM800K dataset contains 800,000 step-level labels over 75,000 solutions to 12,000 MATH problems (https://arxiv.org/abs/2305.20050 and https://github.com/openai/prm800k [verified]). Solver-assisted architectures beat direct prediction: a systematic comparison on engineering equations found that pairing LLM reasoning with symbolic or numeric solvers substantially outperforms direct prediction (https://arxiv.org/pdf/2601.01774 [single-source]).

The confident-wrong caveat is the part that governs the design. Nothing found in track 3 reports a confident-wrong rate for frontier models on AP-Calculus-level problems specifically. The frontier AIME figures collated there rest on secondary aggregation of vendor claims and should not be repeated in user-facing material, and a 90-plus percent AIME score implies nothing directly about a per-item error rate on a bank of thousands of generated BC items, where even a 0.5 percent silent key error is a serious product defect (track 3 [inferred]). A 2025 paper argues that final-answer benchmarks are saturated enough to be misleading about grading ability and introduces a proof-grading benchmark on the premise that judging an argument is a harder and less-measured skill than producing a correct final answer (https://arxiv.org/pdf/2511.01846 [single-source]).

So the pipeline does not rely on benchmark scores as a proxy for bank quality. The app measures its own key error rate on a hand-audited sample and publishes it internally as a gate. D12 sets that gate at P1 exit: key error rate measured on a 100-item audited sample.

## Rejection rules

An item that trips any rule below is not published. Rules 1 through 8 send it back to the generator with the failing rule named; rules 9 through 14 send it to the item review queue for a human decision.

1. The parameter draw violates a `constraints` predicate in the archetype's parameter spec.
2. A Monte Carlo invariant from `invariant_structure` fails on any drawn tuple in the family pass.
3. The independent re-solve disagrees with the candidate key symbolically and numerically.
4. A SymPy equivalence check returns unevaluated and no numeric check settles the comparison.
5. A distractor equals the key symbolically or numerically.
6. Two distractors are equal to each other.
7. A non-key option carries no `generating_error_path`, or carries an id that does not resolve to an active BC-ERR record.
8. A no-calculator item's verified solution path requires numeric root-finding, or a calculator item's reported answer is not stated to three decimals.
9. A worked-solution step carries a `point_type_id` that is not in the archetype's `point_types` list, or a listed point type has no step tagged to it. This rule applies only when the archetype's `point_types` is non-empty (R14). The 56 active archetypes with an empty `point_types` list are exempt from it, are served only as multiple choice or short answer, and their worked-solution steps carry no point type at all until the library fills the field.
10. The MinHash near-duplicate check trips against the official corpus text cache or the generated bank at the configured Jaccard threshold.
11. The embedding cosine check trips at the configured threshold.
12. The stem contains a span matching cached official text above the duplicate threshold, at any length.
13. The figure spec places a label outside the figure, or the stem refers to a figure the spec does not contain.
14. The item's predicted success probability, recomputed from the realised dial settings, differs from the requested target by more than 0.15 [inferred threshold].
15. A worked-solution step carrying a `sympy` expression does not follow from the previous step's under the rule the step names, checked with `app/items/verify.py` `equivalence`, or a step is an identity under the drawn parameters and therefore vacuous. Added 2026-09-20: none of rules 1 to 14 checks that a worked-solution step is mathematically correct, so the key was verified three ways while the worked solution a student reads on the feedback screen was unverified model output. See `13-ai-engineering.md`.

## Review queue

The item review queue arrives in P4 with the generator and the independent re-solve (R9). P1 has no item review queue for generated items, because P1 authors every item by hand and audits 100 of them by re-solving without the key. The states, the reviewer screen and the rejection-to-prompt-fix path below all describe P4 onward.

### States

An item moves through `generated`, `verifying`, `verified`, `needs_review`, `published`, `rejected`, and `retired`. A `needs_review` item carries the rule number that put it there. A `rejected` item is kept with its provenance rather than deleted, because a rejected item is the evidence a prompt fix is tested against.

### Who reviews

The operator, meaning the single person running the app. There is no second reviewer at single-user scale, and the plan does not pretend otherwise. The review queue's job at this scale is to make one person's attention cheap to spend, not to simulate a panel.

### What a reviewer sees

One screen per item, containing: the rendered stem and figure exactly as a student would see them; the key and the worked solution with each step's BC-PT tag; every option with its `generating_error_path` and mechanism category; the independent re-solve's answer beside the candidate key; the Monte Carlo pass result with the failure count and one failing draw if any; the duplicate-gate scores with the nearest neighbour from each corpus and its identifier; the realised difficulty dial vector against the requested one; and the provenance block, meaning archetype, variant, parameter seed, model, prompt version, and spec version. The failing rule number is at the top, and the three actions are approve, reject with a reason, and edit the parameter spec.

### How a rejection feeds a prompt fix

Every rejection records the rule number, the archetype, the prompt version, and the operator's reason. Rejections group by (rule number, prompt version) and a group crossing a threshold is a prompt defect rather than a draw defect. The fix path is: add the failing item to the prompt's golden test set as a case that must not recur, change the prompt, bump `prompt_version`, run the golden tests, and regenerate the affected archetype's queue. Prompt templates are versioned in the repository with golden tests (D8), so a prompt change is a reviewable diff and not a settings edit.

Two rules have a different fix path. A rule 1 or rule 2 rejection is a parameter-spec defect, not a prompt defect, and it is fixed by editing the spec and re-running the Monte Carlo pass. A rule 10, 11, or 12 rejection is a duplicate-gate hit, which is fixed by re-drawing parameters, and a repeated hit on the same archetype means the safe-variable domain is too narrow to produce distinguishable items.

## Duplicate and copyright gate

### The two stages

Stage one is an n-gram check. The standard large-corpus practice deduplicates with MinHash over n-grams, with published configurations using 5-grams at a Jaccard threshold of 0.8 and 256 hashes per document, and the canonical study shows that removing high n-gram-overlap examples measurably improves downstream models (https://arxiv.org/pdf/2107.06499 and https://aclanthology.org/2022.acl-long.577.pdf [verified]). This catches verbatim and lightly edited reuse.

Stage two is an embedding cosine check at 0.85, which is the commonly cited operating point for high-precision near-duplicates, with 0.88 cited as strict, 0.75 as a balanced semantic-equivalence baseline and 0.60 for high recall (https://futureagi.com/glossary/cosine-similarity/ [single-source]). This catches paraphrase.

A hit on either stage blocks the item and requires regeneration.

### Validation on a labelled sample

Both thresholds are adopted from outside this domain and must be validated before they are trusted. The cosine operating points are practitioner rules of thumb with no validation on math item text, where notation and boilerplate inflate similarity regardless of construct, and whether n-gram deduplication tuned for web corpora transfers to short, formulaic item stems is untested (track 3 [inferred] on both points).

The validation procedure: the operator labels a sample of pairs drawn from the generated bank and from generated-against-official pairs, marking each as duplicate, near-duplicate, or distinct. The thresholds are then set to the operating point that holds false negatives at zero on that sample, accepting whatever false-positive rate that implies, because a false positive costs one regeneration and a false negative costs a copyright exposure. The sample size is unknown until the bank exists; the rule is that the thresholds ship at the published values and are only ever tightened, never loosened, until the labelled sample says otherwise.

Corrected 2026-09-24: the labelled samples now exist (docs/operator/duplicate-gate/, four samples of 220 pairs) and moved both stage-two operating points. Against official text the cosine threshold is 0.70, tightened from 0.85: every lightly edited official passage scored at least 0.758 and the 786 signed-off items written without sight of official text peak at 0.628. The zero-false-negative point for heavy paraphrase, about 0.28, would have blocked 488 of those 786 items at 0.30, so it was not adopted; heavy paraphrase is caught on 40 to 55 percent of the labelled pairs and the rest of that risk rests on construction and on rule 12. Within the generated bank the word vector is replaced by a comparison of the problem itself, the stem and figure without the options: ordered math-token pairs at Jaccard 0.80 and numbers at 0.95, because siblings of one template with other numbers reached cosine 0.985. Stage one stays at 0.8. Stage two is a local TF-IDF vector, not an embedding, because no embedding provider is allowed. On the final sample the adopted gate has precision 1.000 and recall 0.891 against 0.879 and 0.527 at the published points.

### What the gate runs against

Two corpora. First, the official text cache under `cache/text/<doc>/page-NNN.txt` and `.ocr.txt`, which is the project's local copy of the released material and the only place official text lives. Second, the generated bank itself, so the app does not serve the same item twice under two ids.

### Copyright position

The app never serves an official stem, an official figure, or official rubric text. The released material is structure only.

The governing language is College Board's permission instructions, which define commercial use to include "test-prep settings" (https://privacy.collegeboard.org/copyright-trademark/request-instructions [verified]). That removes the noncommercial classroom exception from any monetised or publicly offered app, and the exception is narrow anyway: copies distributed directly to students only, pages copied exactly as they appear and not altered so the copyright notice remains intact, one test per student, and distributed as a stand-alone document rather than incorporated into another handout (same source and https://apstudents.collegeboard.org/exam-policies-guidelines/terms-conditions [single-source]). An app that embeds questions in its own interface violates every one of those conditions. The booklets themselves carry the stronger notice quoted at the top of this document.

The library is already positioned correctly: its 25-word anchor-quote cap, checked by `qa/07_quotes.py`, keeps the research corpus on the right side of the line. What the library does not carry anywhere is the downstream constraint, which track 3 names as a risk: a product built on the library inherits the test-prep clause that the research files do not mention.

One question this design rests on is unanswered by any source found: whether College Board considers a structural description of a question type, as opposed to the question text, to be protected. Nothing in the cited pages answers it. The mitigations are that the generator never sees official stem text, that `forbidden_text` is empty by construction rather than by filtering, and that provenance is a parameter trail.

### Provenance logging

Every published item carries `provenance`: archetype id, variant id, parameter seed and the drawn values, model, prompt version, parameter-spec version, content snapshot id, and generation timestamp. Track 3's argument is that if a copyright question is ever raised, the defensible answer is a parameter trail from a structural description, not a chat transcript. The provenance record is immutable and survives item retirement.

## Figures

Figures are declarative specs rendered client-side, never images emitted by a model. The `figure` object in the output schema names the kind, the domain and range, the curves, the marks, the labels with their anchors, and the axis titles. The renderer draws it.

Three reasons, in order. Learning impact: the renderer can place every label inside the figure, which is the split-attention rule. The spatial contiguity and split-attention meta-analysis reports overall g = 0.63 favouring integrated over split presentation across 58 independent comparisons with n = 2426 (https://link.springer.com/article/10.1007/s10648-018-9435-9 [verified]), so a caption-only label or a legend in a side panel is a measurable cost, and a model emitting an image cannot be held to that rule. Cost: a spec is a few hundred tokens where an image is not generable by the text models in the routing at all. Convenience: a spec re-renders at any size, in the dark theme, and into an accessible table without regeneration.

The `placement` enum on a label has one value, `inside`. A figure whose spec cannot place a label inside is a figure that needs a different window or a different mark set, and rejection rule 13 sends it back.

Figure-bearing archetypes are P4 work in D12, after the SymPy-verifiable no-calculator archetypes in Units 1 to 3 that P1 covers.

## Cost and caching

The numbers below are from track 4 Part B and all carry [verified] from that ledger's Anthropic Messages API table.

**Prompt caching.** The cache read multiplier is 0.1x base input, the 5-minute write is 1.25x and the 1-hour write is 2x, with the 1-hour TTL set by `cache_control: {type: "ephemeral", ttl: "1h"}`, up to 4 explicit breakpoints, and automatic caching consuming one slot (https://platform.claude.com/docs/en/build-with-claude/prompt-caching [verified]). The minimum cacheable prefix is 512 tokens for `claude-opus-5` and 1,024 for `claude-sonnet-5`; below the minimum the prompt is silently processed uncached with no error (same URL [verified]). Concretely on Opus 5, whose base rate is $5 in and $25 out per MTok, that is $6.25 per MTok for a 5-minute write, $10 per MTok for a 1-hour write, and $0.50 per MTok for a read (https://platform.claude.com/docs/en/about-claude/pricing [verified]). Cache reads do not count toward the input-tokens-per-minute rate limit on current models (https://platform.claude.com/docs/en/build-with-claude/prompt-caching [verified]).

What that buys generation specifically: the cached prefix is the archetype record, the parameter spec, the BC-PT definitions the item's points reference, and the generation instructions. That block is identical across every draw from the same archetype, it sits well above the 512-token minimum, and a generation batch for one archetype reads it once per item at 0.1x. The 1-hour TTL is worth its 2x write only when the generation run for that archetype spans more than one 5-minute gap, which a queued batch will. Changing the structured-output format invalidates the prompt cache, and changing `budget_tokens` invalidates cache breakpoints (https://platform.claude.com/docs/en/build-with-claude/structured-outputs and https://platform.claude.com/docs/en/build-with-claude/extended-thinking [verified]), so a prompt-version bump is also a cache-warming event and should be batched rather than trickled.

**Batch API.** 50 percent off both input and output, up to 100,000 requests or 256 MB per batch, most batches finishing under 1 hour with all expiring at 24 hours, results retained 29 days, oversized batches returning 413 `request_too_large`, and `max_tokens: 0` rejected inside a batch (https://platform.claude.com/docs/en/build-with-claude/batch-processing [verified]). Generation, independent verification, and the Monte Carlo family pass are all off the interactive path, so all three run as batches. That is the whole cost argument for keeping the bank pre-generated rather than generating on demand: the interactive path pays list price and the queue does not.

**What the unit of generation does to all of the above, corrected 2026-09-20.** Under the template architecture the model is called once per archetype rather than once per item, so the prefix that caches is the authoring instruction block shared by every request in the pass rather than an archetype record shared by 56 draws, the whole authoring pass is one batch rather than one batch per archetype, and the bank's generation cost falls from $177.62 to $17.37 over the cycle. Instantiation is deterministic backend code and costs nothing. Verification does not follow: the independent re-solve stays per published item, because the floor is that an unverified item is never served. See `14-token-economy.md`.

**Second tier.** D8 routes bulk grading and batch verification to Gemini 3.8 Flash as the cost-controlled second tier, at $0.75 in and $3.75 out per 1M through 31 December 2026, then $1.50 and $7.50 (https://ai.google.dev/gemini-api/docs/pricing [verified]), with implicit context caching on by default above a 4,096-token minimum on the 3.x Flash models and cache reads at $0.075 per 1M through the same date (https://ai.google.dev/gemini-api/docs/caching and the pricing page [verified]). Gemini's structured output supports recursive `$ref`, `minimum` and `maximum`, which Anthropic's does not (https://ai.google.dev/gemini-api/docs/structured-output [verified]); the schemas in this document avoid those keywords so one schema serves both providers.

**Structured outputs everywhere.** Both generation schemas above are passed as `output_config.format` with `{"type": "json_schema", ...}`, supported on Opus 5 and Sonnet 5 among others, with the first use paying a grammar-compilation latency cached for 24 hours (https://platform.claude.com/docs/en/build-with-claude/structured-outputs [verified]).

**Budget control.** D7 sets per-role daily budget caps and D8 sets fallback chains with cooldowns. Generation is the role most able to absorb a cap, because a pre-generated bank means a hit cap delays the queue rather than stopping a session. Track 4's cost position is adopted directly: the honest levers are prompt caching at 0.1x reads plus the 50 percent batch discount for anything off the interactive path.

**Rate limits.** The Start tier is 1,000 requests per minute, 2,000,000 input tokens per minute and 400,000 output tokens per minute for the Opus 5 and Sonnet 5 bucket, with a $500 monthly spend cap (https://platform.claude.com/docs/en/api/rate-limits [verified]). A full-bank generation pass over 139 archetypes with several variants each is the only workload in this app that approaches those numbers, and it runs as a batch for that reason.

## Traceability to 01, 02, 03

| Element of this document | Serves |
| --- | --- |
| Archetypes as item models, generation by parameter substitution | 01's criterion alignment: practice items must measure the construct the released material measures, which is what an item model preserves and a free-form imitation does not |
| The parameter spec with explicit domains and constraints | 02 Update rules and their centred beta prior, which is computed from the archetype's BC-DF count and is only meaningful if every draw from that archetype sits in the same construct |
| Difficulty dials mapped from a requested success probability | 02 Item selection algorithm, which uses the target as a fading-stage filter and needs an item that actually sits at the requested probability |
| Calculator-boundary assertion in the verifier | 02 Prerequisite gating and the outer fringe, and 05's part-shaped drills, both of which assume an item's calculator status is true |
| Distractors from named BC-ERR paths | 03's diagnostician, which reads `generating_error_path` from the selected option and enters it into `observed_errors[]` |
| Worked-solution steps tagged to BC-PT ids | 03's grader, which issues one structured call per BC-PT and needs the item to declare which points it carries |
| `setup_required` and the three-decimal rule on calculator items | 03's deterministic pre-checks, which decide reported-value points numerically |
| Declarative figure specs with labels inside | 03's feedback policy, which re-renders the item's figure on the feedback screen under the same split-attention rule |
| Representation binding per item | 02 Item selection algorithm and its 20 percent translation floor, and 03's one-translation rule |
| Monte Carlo family pass, the SymPy settle-rate measurement and the key error-rate gate | 10's engine invariants and the P1 exit criterion in D12 |
| Hand-authored P1 items carrying a provenance record with model "operator" | 02 Prerequisite gating and the outer fringe, which excludes any archetype with no published item and logs it as a coverage gap |
| Duplicate and copyright gate, provenance logging | 09's data rules and the project's non-negotiable rule that no official stem, figure, or rubric text is served |
| Batch generation and prompt caching | 07's cost controls and 06's job table, which consumes generation and verification as background work |
