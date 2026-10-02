---
title: The live tutor draws, build plan
research_date: 2026-09-30
status: draft
purpose: Order the implementation of the tutor's drawing ability into slices with the files, tests, checks and acceptance of each, in the style of docs/agent/build-plan.md.
---

# The live tutor draws, build plan

Each slice below is one Opus 5.5 subagent brief, reviewed and checked by the orchestrator, in the worktree `/Users/mahfujm/dev/growth-drawing` on `agent/drawing`. A slice is done when its named tests were seen red against a broken input and green after, its checks exit 0, and the orchestrator has read the diff. Checks per slice unless the slice narrows them: the affected pytest files, each in its own background process under `timeout 600`; `npm --prefix app/web run test`; `npm --prefix app/web run build`; `tools/cost_model.py --check` over every plan file the slice touches; `tools/agent_eval.py` and `tests/eval/test_agent_golden.py` once slice 6 has landed. Style: Python 3-space indent, double quotes, decomposed conditions, blank lines between logic blocks; TypeScript matches `app/web`; no em dashes, no en dashes as punctuation, no emojis; comments only where a human would write one.

Nothing in any slice loosens a test, a threshold, a cap, a lint or an eval bar. Nothing writes mastery evidence. No tool definition is sent to a model. No model string becomes markup, a URL, a class or a style.

## The render spec contract [inferred]

Slices 2 and 5 are built in parallel against this contract, which `schemas/agent/figure_render.schema.json` (slice 2) encodes and `app/web/src/api/types.ts` `TutorFigureSpec` (slice 5) mirrors. Coordinates are world coordinates; the client maps them with `view` and `window` exactly as the server laid them out.

```json
{
  "id": "figure",
  "kind": "graph",
  "title": "Secant to tangent",
  "description": "The curve y equals x squared ...",
  "window": {"x": [-1, 4], "y": [-1, 9]},
  "view": {"width": 320, "height": 300, "padding": 20},
  "axes": {"x": "x", "y": "y"},
  "grid": true,
  "equal_scale": false,
  "steps": [{"id": "curve", "caption": "The curve y = x^2"}],
  "columns": null,
  "rows": null,
  "primitives": [
    {"type": "path", "step": "curve", "element": "f", "role": "given", "points": [[-1, 1], [-0.97, 0.94]], "closed": false, "fill": "none", "style": "solid", "weight": "regular", "arrow": "none", "highlighter": false, "faded_at": null, "erased_at": null},
    {"type": "dot", "step": "secant", "element": "P", "role": "constructed", "at": [1, 1], "open": false, "faded_at": null, "erased_at": null},
    {"type": "label", "step": "curve", "element": "f", "role": "given", "at": [2.5, 6.25], "offset": [6, -6], "align": "start", "text": "\\(y = x^2\\)", "faded_at": null, "erased_at": null},
    {"type": "cell", "step": "row", "element": "h", "role": "highlight", "row": 2, "column": null, "faded_at": null, "erased_at": null}
  ]
}
```

`kind` is `graph`, `diagram`, `number_line` or `table`. The client draws a frame (axes, gridlines, numbered ticks, axis titles) for `graph` only; for `diagram` and `number_line` the server emits every line, tick and tick label as primitives. `view.height` is the plot height the server chose (the window's aspect clamped between 180 and the plot width, `view.width` less twice the padding, as `FigureView` does; or equal scale when `equal_scale`, for which the server widens the window about its centre) plus twice the padding. A `cell` primitive may carry `text`, a labelled highlight. `offset` is in view units. `role` is `given`, `constructed`, `highlight` or `error`; a primitive whose `faded_at` step has been revealed is drawn in the ghost style, and one whose `erased_at` step has been revealed is not drawn. `cell` primitives appear only in a `table` figure, whose `columns` and `rows` are then set. Caps the client re-checks: at most 200 primitives, 4,000 points in all, 6 steps, finite numbers.

## Slice 1. Expression grammar, schema and validator

Entry: `drawing-design.md`. Scope: the server can read a figure block safely and say exactly why one is refused.

| Path | Change |
|---|---|
| app/agent/drawing/__init__.py | new package |
| app/agent/drawing/expression.py | Python twin of `app/web/src/lessons/expression.ts`: tokenizer and recursive-descent parser with the same tokens, precedence, function table (plus `ln`, less `oo`) and implicit multiplication; caps of 80 characters, 48 tokens and depth 10; one declared variable set per use; `evaluate(tree, scope)` in floats through `math` returning `None` where undefined; `to_sympy(tree)` built node by node. No `eval`, `exec`, `compile`, `sympify`, `parse_expr` or `lambdify` anywhere in the package |
| schemas/agent/figure.schema.json | the model-facing language of `drawing-design.md`, draft 2020-12, `additionalProperties: false` on every object, enums, the numeric and length caps |
| app/agent/drawing/spec.py | `read_figure(text)`: character cap, `json.loads` with `ValueError` and `RecursionError` caught, schema validation, then the semantic checks (unique ids, references to earlier elements of the right shape, `fade` and `erase` of earlier elements only, ordered windows, `on` names a curve, at most 4 added per step and 16 in all); raises `FigureRefused(reason)` with reason `malformed` or `oversized` |
| tests/fixtures/drawing/expressions.json | a shared list of expressions with their values at given points and the strings that must refuse, read by both the pytest and the vitest parity tests |

Tests: `tests/agent/drawing/test_expression.py` (the shared fixture evaluates to the listed values; every refusing string refuses, including `__import__("os")`, attribute access, a name outside the table, 81 characters, depth 11; a source scan of `app/agent/drawing/` finds none of the forbidden calls), `tests/agent/drawing/test_spec.py` (every example block in `drawing-design.md` reads; each cap, each semantic rule and a truncated block refuses with its reason, each seen red by breaking the check). Vitest `app/web/src/lessons/expression.parity.test.ts` evaluates the same fixture with `expression.ts`, so the two grammars cannot drift.

Acceptance: all green; no file outside the new package, schema and fixtures changed.

## Slice 2. Compiler, render spec and figure checks

Entry: slice 1. Scope: every shape compiles to the render spec, and every leak channel is checked.

| Path | Change |
|---|---|
| app/agent/drawing/compile.py | `compile_figure(figure)`: the geometry of every shape in `drawing-design.md` (curves at 161 samples broken where undefined or beyond ten window heights, paths at 241, points on curves, secants, tangents by central difference, clipped lines, areas with below-axis parts, Riemann and trapezoid pieces, slope-field lattice at most 11 by 11, Runge-Kutta solution, Euler steps, sequences and partial sums, vectors with legs, circles and arcs as paths, angle and right-angle marks, boxes, triangles by kind with the right-angle mark and equal-side ticks, polygons, braces, text, callouts with leader arrows, rings, number-line lines, ticks, intervals and sign rows, table cell highlights), label placement beside the element and clamped inside the view, `view` and `equal_scale`, the fade and erase steps, the 4,000-point, 200-primitive and 100 ms caps; returns the render spec and a `FigureFacts` record of every number and text the figure shows, by channel |
| schemas/agent/figure_render.schema.json | the render spec contract above |
| app/evals/figure_checks.py | `figure_texts_pass(facts, packet_facts, forms)` through `agent_checks.SENTENCE_CHECKS`; `no_answer_in_figure(facts, packet_facts, forms)` over the numeric channels of `drawing-design.md` "The screen" with `agent_checks.NUMERIC_TOLERANCE`; `figure_well_formed(block_text)`; `draws_only_when_open(drawing, has_figure)`; `figure_described(figure)`; each returns an `agent_checks.Verdict` |

Tests: `tests/agent/drawing/test_compile.py` (each shape's geometry against a closed form: the secant slope of x^2 on [1, 3] is 4, the tangent slope at 1 is 2, left, right, midpoint and trapezoid totals of x^2 on [0, 2] with n = 4, the area of x^2 on [0, 3] is 9 within 1e-6, a right triangle's vertices and its mark, an isosceles triangle's apex and ticks, an equilateral's sides, a polar window at equal scale, the slope-field cap, Euler values for dy = x + y, partial sums of 1/2^n; every output validates against the render schema; each cap refuses), `tests/agent/drawing/test_figure_checks.py` with red-first tests for a leaking point, a leaking line (slope and intercept), a leaking label, a leaking shaded region, plus a Riemann total, a curve equal to a key expression, a table cell, a multiple-choice key letter label and a key option value; a generic secant sketch passes on an item whose key is not in it; after submission only the text checks run; each test seen red with its channel switched off.

Acceptance: all green; the four named red-first tests recorded red then green in the slice report.

## Slice 3. Splitter, screen, route, storage and switch

Entry: slice 2. Scope: a figure travels from the provider stream to the client events, is screened, stored and logged by the rules.

| Path | Change |
|---|---|
| app/agent/drawing/stream.py | `FigureSplitter`: prose passes through with `[[step:ID]]` markers removed and their offsets recorded; a fence line with info string `figure` buffers to its closing fence; partial openers, closers and markers across deltas are held; nothing inside `\( \)` or `\[ \]` is read as a marker or fence; the 2,000-character cap, an unclosed block at the end, and a second block produce refusals |
| app/agent/screen.py | `SentenceScreen.boundary()` screens and releases the buffered fragment; `withhold(verdict)` releases the decline and stops |
| app/agent/moves.py | `DRAWING_OPEN_MOVES` and `drawing_for(move, enabled)` per the move table in `drawing-design.md` |
| app/agent/context.py | the packet gains `drawing`; `practice_body` gains the item figure summary (kind, window, alt, table columns and rows); `_history_payload` appends "[Figure shown: {title}. {description}]" to an agent turn with a shown figure |
| app/agent/turn.py | `screened_text` runs the splitter before the sentence screen and emits `figure_pending`, `figure`, `figure_refused` and `figure_step` in the order of `drawing-design.md` "Events and order"; a figure on a closed turn or with the switch off is refused; a leaking figure withholds through `withhold` with the check and the part `figure` in the audit detail; the stored agent turn carries the figure column; the log line adds the figure outcome and step count |
| app/agent/conversations.py | `append_turn` takes the figure JSON |
| app/db/models.py, app/db/migrate.py | `agent_turns.figure`, additive, nullable |
| app/main.py, app/api/app.py | `Settings.agent_drawing` from `GROWTH_AGENT_DRAWING` (default on) |
| tests/fixtures/fake_claude/claude | a `stream_script` mode that streams `$HOME/fake_claude_stream_text.txt` in chunks of `$HOME/fake_claude_chunk` characters (default 7) so fences and markers split across deltas |

Tests: `tests/agent/drawing/test_stream.py` (every split position of an opener, a closer and a marker; math spans holding brackets; unclosed, oversized and second blocks; the boundary keeps order), `tests/agent/test_screen.py` extended for `boundary` and `withhold`, `tests/api/test_agent_turn_drawing.py` through the route with the fake CLI (event order with steps before their sentences; unmarked steps sent before `end`; a leaking figure gives the decline, outcome withheld, one audit row naming `no_answer_in_figure` and part `figure`, and no `figure` event; a malformed and an oversized block give `figure_refused` and the text continues; a figure on `ask_what_tried` is refused `closed`; `GROWTH_AGENT_DRAWING=off` refuses `off`; the stored column; a marked label and expression appear in no log record and no audit detail), `tests/agent/test_context.py` extended for the `drawing` field, the item figure summary and the history line, `tests/agent/test_moves.py` for the table, `tests/agent/test_boundary.py` unchanged and green.

Acceptance: all green; `tests/agent` and the agent route tests green; the log-hygiene assertion seen red with the spec logged.

## Slice 4. The drawing template

Entry: slice 2. Scope: the model knows when and how to draw.

| Path | Change |
|---|---|
| prompts/agent/live_v2.md | v1's rules unchanged, plus the drawing rules, the vocabulary in compact form and at least ten example figures with their marked sentences (the list in `drawing-design.md` "The prompt"), and the `drawing` field below the marker |
| app/agent/context.py | `LIVE_TEMPLATE_PATH` points at v2; `render_prompt` fills `drawing` |
| tests/fixtures/prompt_token_counts.json | the v2 prefix count by the 3.1 divisor, marked as an estimate until a live call reports the cached count |

Tests: a new `tests/agent/drawing/test_template_examples.py` extracts every figure block from the template, reads and compiles each with slices 1 and 2, asserts at least ten, every one well formed and described, every marker naming a step of its figure, and no example leaking against its own stated item; `tests/agent/test_prefix.py` for v2 (byte-identical across draws, above 512 tokens); `tests/providers/test_prompts.py` for the new template's front matter.

Acceptance: all green; a broken example seen red.

## Slice 5. The client

Entry: the render spec contract (5a) and slice 3's events (5b). Scope: the panel builds the figure in step with the words, at reading pace, accessibly, in both themes and at phone width.

| Path | Change |
|---|---|
| app/web/src/figures/GraphFrame.tsx, FigureView.tsx | the axes, gridlines, numbered ticks and axis titles factored out of `FigureView` into `GraphFrame`, parameterised by view width; the item figure's output unchanged |
| app/web/src/agent/TutorFigure.tsx | parses and re-checks the render spec; draws the frame for `graph`, each primitive by role, style, weight, arrowheads (SVG markers), highlighter underlay and fill; the ghost style after `faded_at`, nothing after `erased_at`; labels in an HTML layer with `MathText` on the tutor renderer; tables as an HTML table with highlighted cells; the title, description, step line, Previous, Next and Show all, the "Steps" disclosure (open under reduced motion), arrow keys, Home and End; `role="img"`, `aria-labelledby`, `aria-describedby`, the focusable wrapper |
| app/web/src/styles/app.css | the tutor figure classes, tokens only |
| app/web/src/styles/motion.css, motion.ts | `motion-figure-wipe` (transform and opacity, with its reduced-motion rule) and `motion-figure-step` (opacity) |
| app/web/src/api/types.ts, client.ts | `TutorFigureSpec` and the four event types |
| app/web/src/agent/useAgentStream.ts | dispatches `figure_pending`, `figure`, `figure_step`, `figure_refused`; a figure event clears the first-text timer |
| app/web/src/agent/AgentProvider.tsx | per-reply figure state, the display queue with gates at reading pace (238 words a minute, math spans as three words, at most 6 seconds), Show all and Stop open every gate, `end` applied and announced when the queue drains, "Figure: {title}. {description}" in the announcement |
| app/web/src/agent/AgentPanel.tsx, agentCopy.ts | the figure placed at its offset in the reply, "Drawing a figure", the refused line, the copy of `drawing-design.md` |
| app/web/src/testing/screens.tsx | screen entries with a finished figure in each role, so `contrastAllScreens` and `greyscaleStates` cover it |

Tests: `TutorFigure.test.tsx` (primitives appear by step; roles, styles and weights map to classes; arrowheads; a faded and an erased element; labels typeset; a spec over a cap draws nothing; the accessible name and description; keyboard stepping; the disclosure open under a mocked reduced-motion query), `useAgentStream.test.ts` (the four events; a figure clears the timer), `AgentProvider` pacing tests with fake timers (a gate opens at the reading time and not before; Show all and Stop open every gate; `end` waits for the queue), `AgentPanel.test.tsx` (the figure at its offset; the pending and refused lines), `expression.parity.test.ts` from slice 1, and the existing `motion.test.ts`, `noLiteralValues.test.ts`, `contrastAllScreens.test.tsx`, `greyscaleStates.test.tsx` and `FigureView` tests green.

Acceptance: `npm --prefix app/web run test` green apart from failures that fail on `main` too, each named; `npm --prefix app/web run build` exit 0; `npx tsc --noEmit` exit 0.

## Slice 6. Golden drawing cases and the eval

Entry: slices 3 and 4. Scope: the drawing rules are measured by the same code the screen runs.

| Path | Change |
|---|---|
| content/golden/agent.json | at least 14 drawing turns: cases that should draw (a secant sketch on name_rule, a Riemann figure on discuss_step, a slope field and a triangle on explain), cases that must not (a figure on ask_what_tried and on probe), cases whose figure leaks (a point, a tangent slope, a label letter, a shaded area and a Riemann total at the key), a malformed and an oversized block, each labelled on the new checks |
| app/evals/golden.py | the agent role's validation accepts the four new labels; candidate replies are split and compiled with the live splitter and compiler |
| tools/agent_eval.py | reports the figure checks beside the prose checks, with denominators |

Tests: `tests/eval/test_agent_golden.py` (every label agrees with its check; a red-first case: a leaking figure candidate relabelled as acceptable makes the test fail).

Acceptance: `tools/agent_eval.py` exit 0 with 0 disagreements; `tests/eval/test_agent_golden.py` green.

## Slice 7. Cost figures

Entry: slice 4's prefix count. Scope: plan 14 quotes the drawing lines from the model.

| Path | Change |
|---|---|
| tools/cost_model.py | a drawing block: `drawing.prefix_tokens`, `drawing.figure_output_tokens` (300), `drawing.turn_share` (0.3), `drawing.turn_usd`, `drawing.figure_turn_usd`, `drawing.conversation_usd`, `drawing.day_usd`, `drawing.cycle_usd`, `drawing.added_cycle_usd` (against `agent.cycle_usd`); the `agent.*` figures unchanged |
| tests/tools/test_cost_model.py | the new figures present and consistent |

Acceptance: `tools/cost_model.py --check` 0 unknown over plans 03, 08, 09, 12, 13 and 14 after the orchestrator quotes the amounts.

## Slice 8. The walkthrough recorder

Entry: none. Scope: a rerunnable captioned screencast of a browser walk.

| Path | Change |
|---|---|
| tools/record_walkthrough.mjs | drives a headless Brave over the Chrome DevTools Protocol through a JSON script of steps (navigate, click by selector or text, type, press, wait for a selector or a text, set the viewport, emulate reduced motion or a colour scheme, caption, pause), records `Page.startScreencast` frames with their timestamps, burns each step's caption in with ffmpeg's drawtext, and stitches an MP4 at a steady frame rate under a path the caller names |

Tests: a `--dry-run` that validates a script and prints the planned steps, run by the orchestrator.

Acceptance: one recorded walkthrough of the drawing feature under `var/agent/`.

## Slice 9. Marks on the page, server and template

Entry: slices 3 and 4. Scope: the model can mark named anchors on the screen, screened like a figure (`drawing-design.md`, "Marks on the page").

| Path | Change |
|---|---|
| schemas/agent/marks.schema.json | the marks language |
| app/agent/drawing/marks.py | `read_marks`, validation against the turn's anchors (quotes found in the anchor text, coordinates inside the item figure's window, after-checking-only shapes and anchors), `compile_marks` to the render marks and their facts |
| app/agent/context.py | the packet's `anchors`: ids, and for text anchors the text they hold where the packet does not already carry it; the item figure's window for `item_figure` |
| app/agent/drawing/stream.py | the `marks` fence beside the `figure` fence; one block of each per reply |
| app/evals/figure_checks.py | `no_answer_in_marks`: option anchors before checking, the numeric channels on the item's graph, the texts |
| app/agent/turn.py, app/agent/drawing/record.py | the `marks` event, steps through `figure_step`, `figure_refused` with part marks, the stored record's `marks` entry, the log line |
| prompts/agent/live_v2.md | the marks rules, the anchors, and at least four worked examples (underline a phrase of the stem and ring a point on the item's graph; highlight the deciding table row; after checking, strike a worked-solution phrase and note beside it; an arrow from the stem to the item's graph) |

Tests: `tests/agent/drawing/test_marks.py` (every shape reads and compiles; a quote not in the anchor, an unlisted anchor, a coordinate outside the window and an after-checking shape before checking each refuse), red-first screen tests for a mark on an option before checking, a ring at the key's point on the item's graph, a tangent with the key's slope and a note stating the key; route tests for the event order with a figure and marks in one reply; the template example test extended to marks.

## Slice 10. Marks on the page, client

Entry: slice 9's events. Scope: marks drawn over the real elements, in step with the words.

| Path | Change |
|---|---|
| app/web/src/session/Item.tsx, ElaboratedPanel.tsx and the worked-solution and option components, app/web/src/figures/FigureView.tsx, app/web/src/lessons/LessonSection.tsx | `data-agent-anchor` attributes on the anchored elements; the item figure's SVG carries its window and plot box so a mark maps its coordinates |
| app/web/src/agent/PageMarks.tsx | the overlay: finds anchors, measures them (quotes through a text range), follows scroll, resize and layout changes, draws marks by role and stroke with the figure's classes, reveals by step, never takes pointer events or focus |
| app/web/src/agent/AgentProvider.tsx, AgentPanel.tsx | the `marks` event through the same gate queue; marks kept per screen key for the conversation, hidden when the screen changes and drawn again, finished and without motion, when the student returns; a new reply's marks replace the same screen's earlier set; "Marked on the page" with the captions; "Clear marks" for the current screen; the announcement clause |

Tests: overlay placement against measured anchor rectangles (mocked `getBoundingClientRect` and ranges), step reveal, marks hidden on a screen change and restored on return, replaced by the next reply's marks on the same screen, clearing, the item-figure coordinate mapping, no pointer events, reduced motion, the captions list and announcement, contrast and greyscale screens.

## The marks contract [inferred]

Slices 9 and 10 are built in parallel against this contract, encoded by `schemas/agent/marks_render.schema.json` (slice 9) and mirrored by `TutorMarksSpec` in `app/web/src/api/types.ts` (slice 10).

The `marks` event carries `{"id", "description", "steps": [{"id", "caption"}], "marks": [...]}`. Each mark has `step`, `element`, `role`, `stroke` (`style`, `weight`, `arrow`, `highlighter`), `faded_at`, `erased_at` and `kind`, one of `ring`, `underline`, `highlight`, `strike`, `bracket`, `note`, `arrow`, `point`, `segment`, `line`, `vline`, `hline`, with:

- `target` for ring, underline, highlight, strike, bracket and note; `from` and `to` for arrow. A target is `{"anchor", "quote", "at", "row", "column", "cell"}` with the unused fields null: `quote` a phrase of a text anchor, `at` a point in the item figure's coordinates, `row`, `column` or `cell` in the item's table.
- `text` and `side` (`left`, `right`, `above`, `below`) for note.
- `at` and `open` for point; `points` (two world points on the item's graph, lines and guides already clipped to its window by the server) for segment, line, vline and hline.

In the page, an anchored element carries `data-agent-anchor="<id>"`. The item figure's SVG carries `data-agent-window="xmin xmax ymin ymax"` and `data-agent-plot="left top right bottom"` in its view units, so the overlay maps a point through the plot box and the SVG's screen matrix. The item table's body rows are the anchor's `tbody tr` elements in order.

The packet's `anchors` is a list of `{"id", "kind"}` with `kind` one of `text`, `graph`, `table`, `element`, plus `window` for a graph and `rows` and `columns` for a table. Text anchors' text is the text the packet already carries for them (the stem, the section text, the feedback fields, the worked solution steps).
