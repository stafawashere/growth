---
title: The live tutor draws, design
research_date: 2026-09-30
status: draft
purpose: Specify the tutor's drawing ability end to end, from the figure language the model writes to what the student sees and hears, with the guardrail, the caps, the events, the renderer, the motion, the accessibility contract, storage, cost and the evals, and record what was rejected and why.
---

# The live tutor draws, design

The tutor can draw. When a figure would teach the moment better than words alone, and when the student asks for one, the tutor writes one figure into its reply, and the panel builds it on the page step by step as the sentences that explain each step appear, the way a teacher adds to a sketch at the board while talking. The research behind every choice is `research/drawing.md`, whose ranked synthesis this file turns into a specification. `drawing-build-plan.md` schedules the work. `design.md` and `architecture.md` carry short sections that point here.

Two operator instructions set the scope, both on 2026-09-30: the tutor draws whatever figure best teaches the moment, built step by step in time with the words; and the vocabulary goes beyond graphs to shapes such as circles, the kinds of triangle, arrows and boxes, free text labels, and different kinds of stroke. Everything else here was decided on the operator's delegation and is recorded with its reason.

## What does not change [verified]

Read from the run brief and `architecture.md` on 2026-09-30. The model has no tools. No student text reaches a system prompt. Every call goes through `app/providers/guard.py` under the `agent` role's caps, which are unchanged, and `MAX_OUTPUT_TOKENS` stays 800. The plan 03 guardrail holds: before an item is checked, no answer, no evaluation of a draft, no key. Nothing writes mastery evidence. Model output is data: the model never writes SVG, HTML, CSS or JavaScript, and nothing it writes becomes a tag, an attribute name, a URL or a style. No study advice, schedule, praise or prediction talk, in the figure's text as in the reply's.

## What the student sees [inferred]

A reply that draws looks like this in the 384 px panel, on an item after it was checked:

```
Tutor said
The left sum uses the height at the start of each subinterval.

  Left sum under f on [0, 2]
  +------------------------------------------+
  |  y                                        |
  |  4 |                        .'            |
  |    |                     .'   f           |
  |  2 |            +-----+'                  |
  |    |   +-----+  |     |                   |
  |  0 +---+-----+--+-----+------------ x     |
  |        0    0.5     1   1.5     2         |
  +------------------------------------------+
  Step 3 of 4: Two left rectangles
  [Previous] [Next] [Show all]   > Steps

Each rectangle's top left corner sits on the curve.
The response used the right endpoints, so its rectangles
were taller and its sum was too large.
```

The figure frame (title, axes, window) appears where the figure sits in the reply. Each step appears together with the sentence that introduces it. A step's lines sweep in from the left over 300 ms and its fills and labels fade in over the same 300 ms; nothing moves once drawn and nothing loops. The panel waits before showing the next step and its sentence until the words since the last step could have been read (238 words a minute, at most 6 seconds a step), so the figure is built at reading pace and not at the speed the model writes. A "Show all" text button under the figure ends the wait and shows every step received.

When the reply has finished, the controls under the figure are "Previous", "Next" and "Show all", with the line "Step k of n: {caption}". Left and Right arrows do the same when the figure has focus, and Home and End go to the first and last step. There is no autoplay replay. A disclosure "Steps" under the controls holds the ordered list of captions, with the current step marked "now".

Roles give meaning without relying on colour:

| Role | Used for | How it looks |
| --- | --- | --- |
| given | what the item or the student already has: the curve, the table, the stated points | `text-secondary` ink, regular weight |
| constructed | what the tutor adds: a secant, a tangent, rectangles, a brace, an arrow | `accent-base` ink, bold weight |
| highlight | the one thing a sentence is about | bold `accent-base` over a highlighter underlay in `accent-tint-3` |
| error | a wrong step drawn for contrast after submission | `state-incorrect`, dashed, and always with a word label such as "right endpoints" |
| ghost | an element the tutor faded, such as the secant a closer secant replaced | `text-muted`, thin, dotted |

Fills sit in accent tints with a hairline edge so neighbouring rectangles stay apart; an area below the axis uses a darker tint than one above it and carries a sign label. The accent is monochrome in the operator's tokens, so these roles ride on lightness, weight, dash and the underlay; `state-incorrect` is used for the error role only and never alone. The model picks a role, never a colour.

Labels sit on the figure next to what they name, typeset as mathematics where they hold `\( \)`. There is no legend and no caption under the figure other than the step line.

### When the tutor draws [inferred]

The move the app chose decides whether this turn may draw. The packet carries the answer as a field, `drawing`, with the value `open` or `closed`, and the server drops a figure written on a closed turn.

| Mode | Move | Drawing | Why |
| --- | --- | --- | --- |
| practice | restate, ask_what_tried | closed | The first reply on an item asks before it tells; attempting before instruction beat instruction first, g = 0.36 |
| practice | name_representation | open | A sketch of the representation the givens use |
| practice | next_self_question | open | A generic sketch that prompts the question |
| practice | name_rule | open | A generic illustration of the rule, never the item's answer-bearing element |
| practice | point_to_section | closed | The move points; the section draws |
| after submission | discuss_step | open | The step the response missed, drawn as the worked explanation |
| after submission | name_point | closed | Rubric language, not a picture |
| after submission | self_explanation_question | open | Explaining after a drawing was strongest after dynamic drawings |
| after submission | probe | closed | The probe is a question whose answer a figure would bias |
| browsing | explain, navigate | open | No item and no key on the screen |

On an open turn the tutor draws without being asked when a figure carries a step of the mathematics (the prompt names the moments: a representation the student has not connected, a limit process, an area or accumulation, a sign argument, a geometric set-up, a table row that decides a step), and draws when asked. On a closed turn a request to draw gets a sentence saying the sketch comes after the student has said what they tried (practice) or nothing about drawing at all (other closed moves), and no figure. At most one figure per reply.

Before an item is checked, and on a lesson section that poses a question, a figure shows what the stem gives and generic illustrations, and never the element that carries the answer: no shaded region with the asked-for area, no tangent labelled with the asked-for slope, no solution curve through the given point, no completed sign chart with its conclusion, no marked limit or maximum. The screen enforces the numeric version of that rule (below); the prompt carries the rest.

### States and copy [inferred]

| State | What shows |
| --- | --- |
| The figure is being written | The text so far and, under it, the static muted line "Drawing a figure" until the figure arrives. No spinner |
| A figure the server could not use (malformed, oversized, cut off, a second figure, written on a closed turn, or `GROWTH_AGENT_DRAWING=off`) | The reply's text continues, and where the figure would have been one muted line: "The figure for this reply could not be drawn." |
| A figure that would give away the answer | The whole reply is withheld exactly as a leaking sentence is: the text released so far stays, the fixed decline follows, and nothing after it. The figure never reaches the client |
| Stop pressed while steps wait | Every step and sentence already received is shown at once, and the turn ends stopped |

## The figure language [inferred]

The model writes one fenced block with the info string `figure`, holding one JSON object, on lines of its own, then refers to the figure's steps in the sentences that follow with a marker `[[step:ID]]` placed in the sentence that introduces the step. The server strips the markers from the text.

```figure
{"kind": "graph", "title": "Secant to tangent", "window": {"x": [-1, 4], "y": [-1, 9]},
 "description": "The curve y equals x squared with a point P at x equals 1. A secant from P to a second point Q moves toward P, and the tangent at P is drawn last.",
 "steps": [
  {"id": "curve", "caption": "The curve y = x^2", "add": [{"id": "f", "curve": "x^2", "role": "given", "label": "\\(y = x^2\\)"}]},
  {"id": "secant", "caption": "A secant through P and Q", "add": [
    {"id": "P", "point": {"on": "f", "x": 1}, "label": "P"},
    {"id": "Q", "point": {"on": "f", "x": 3}, "label": "Q"},
    {"id": "s1", "secant": {"on": "f", "x": [1, 3]}}]},
  {"id": "closer", "caption": "Q moves closer to P", "fade": ["s1", "Q"], "add": [
    {"id": "Q2", "point": {"on": "f", "x": 2}, "label": "Q"},
    {"id": "s2", "secant": {"on": "f", "x": [1, 2]}}]},
  {"id": "tangent", "caption": "The tangent at P", "fade": ["s2", "Q2"], "add": [
    {"id": "t", "tangent": {"on": "f", "x": 1}, "role": "highlight", "label": "tangent"}]}]}
```

A sentence then reads, for example, "[[step:secant]] Join P to a second point Q on the curve; that line is a secant."

### Top level

| Field | Required | Values |
| --- | --- | --- |
| `kind` | yes | `graph` (axes and a window), `diagram` (no axes, equal scale), `number_line`, `table` |
| `title` | yes | at most 60 characters, shown above the figure and used as its accessible name |
| `description` | yes | at most 400 characters, what the finished figure shows in plain sentences, for assistive technology |
| `window` | graph, diagram, number_line | `{"x": [low, high], "y": [low, high]}`; a number line has `x` only |
| `axes` | no | graph only, `{"x": "t", "y": "v(t)"}`, axis titles of at most 12 characters |
| `grid` | no | graph only, default `true`; gridlines and numbered ticks |
| `columns`, `rows` | table | at most 6 columns and 10 rows of cells of at most 24 characters, inline `\( \)` allowed |
| `steps` | yes | 1 to 6 steps |

A step is `{"id", "caption", "add": [elements], "fade": [ids], "erase": [ids]}`. `caption` is at most 100 characters. `add` holds at most 4 elements, one idea's worth. `fade` turns earlier elements into ghosts; `erase` removes them, for the rare case where a construction must be replaced, and the prompt asks for fading instead. The first step only adds.

### Elements

Every element has `id` (letters, digits and underscore, at most 16 characters, unique in the figure), one shape key from the table below, and optionally `role` (`given`, `constructed`, `highlight`, `error`; default `constructed`), `label` (at most 40 characters, inline `\( \)` allowed, placed next to the element) and `stroke`:

| `stroke` field | Values | Default |
| --- | --- | --- |
| `style` | `solid`, `dashed`, `dotted` | by role: error dashed, otherwise solid |
| `weight` | `thin`, `regular`, `bold` (the `stroke-hairline`, `stroke-mark` and `stroke-curve` tokens) | by role: given regular, constructed and highlight bold, error regular |
| `arrow` | `none`, `end`, `start`, `both` | `none`, except `vector`, `callout` and parametric curves, which default to `end` |
| `highlighter` | `true`, `false` | `true` for highlight, otherwise `false` |

Numbers are finite, at most 1,000 in absolute value. Expressions are strings in one variable (`x` for curves and fields, `t` for parametric, `theta` for polar, `n` for sequences, `x` and `y` for a slope field) over numbers, `+ - * / ^`, parentheses, the constants `pi` and `e`, and the functions `sqrt exp ln log sin cos tan sec csc cot asin acos atan sinh cosh tanh abs`, at most 80 characters. A point may be written as `[x, y]`, as the id of a point element, or as `{"on": "CURVE_ID", "x": a}`, which the server computes.

Graph and diagram shapes:

| Shape key | Value | Draws |
| --- | --- | --- |
| `curve` | `"EXPR"` or `{"y": "EXPR", "domain": [a, b]}` | y = f(x), broken at discontinuities and where it leaves the window |
| `parametric` | `{"x": "EXPR", "y": "EXPR", "t": [a, b]}` | a path with an arrowhead showing the direction of travel |
| `polar` | `{"r": "EXPR", "theta": [a, b]}` | a polar curve; the window is kept at equal scale |
| `point` | point, plus `"open": true` for a hole | a filled or open dot |
| `line` | `{"through": [P1, P2]}` or `{"point": P, "slope": m}` | a line across the window |
| `segment` | `[P1, P2]` | a segment, with arrowheads through `stroke.arrow` |
| `secant` | `{"on": "CURVE_ID", "x": [a, b]}` | the secant line through the two curve points |
| `tangent` | `{"on": "CURVE_ID", "x": a}`, optional `"length"` | the tangent line at x = a, or a segment of that length |
| `vline`, `hline` | a number | a vertical or horizontal guide, dashed by default, for asymptotes and levels |
| `area` | `{"under": "CURVE_ID", "from": a, "to": b}` or `{"between": ["CURVE_ID", "CURVE_ID"], "from": a, "to": b}` | a filled region with an edge; below-axis parts in the darker tint |
| `riemann` | `{"on": "CURVE_ID", "from": a, "to": b, "n": k, "rule": "left" \| "right" \| "midpoint" \| "trapezoid"}` | k stroked rectangles or trapezoids, n at most 12 |
| `slope_field` | `{"dy": "EXPR in x and y"}` | short segments on a lattice the server chooses, at most 15 by 15 |
| `solution` | `{"dy": "EXPR", "through": P}` | the solution curve through P, traced by the server |
| `euler` | `{"dy": "EXPR", "start": P, "h": step, "n": k}` | k Euler steps as a polyline with dots, k at most 10 |
| `sequence` | `{"a": "EXPR in n", "n": [first, last]}`, optional `"sums": true` | dots at (n, a_n), or at (n, S_n) with `sums`, at most 30 |
| `vector` | `{"from": P, "to": P}` or `{"from": P, "components": [dx, dy]}`, optional `"legs": true` | an arrow, with dashed component legs |
| `circle` | `{"center": P, "radius": r}` | a circle |
| `arc` | `{"center": P, "radius": r, "from": degrees, "to": degrees}` | an arc, counterclockwise |
| `angle` | `{"at": P, "from": P, "to": P}` | an angle mark at a vertex |
| `right_angle` | `{"at": P, "from": P, "to": P}` | a small square mark |
| `box` | `{"at": P, "width": w, "height": h}`, optional `"text"` | a rectangle from its lower left corner, with centred text |
| `triangle` | `{"kind": "right", "at": P, "base": b, "height": h}`, `{"kind": "isosceles", "at": P, "base": b, "height": h}`, `{"kind": "equilateral", "at": P, "side": s}` or `{"kind": "scalene", "vertices": [P, P, P]}`; optional `"rotate"` in degrees, `"names"` (three vertex names) and `"sides"` (three side labels) | the triangle, with the right-angle mark or the equal-side ticks drawn by the server |
| `polygon` | `[P, P, ...]`, 3 to 8 points | a closed polygon |
| `brace` | `{"from": P, "to": P}`, optional `"text"` and `"side": "left" \| "right"` | a bracket beside a length, such as Δx or h |
| `text` | `{"at": P, "text": "..."}` | a free label of at most 60 characters |
| `callout` | `{"target": P or ID, "at": P, "text": "..."}` | text at `at` with a leader arrow to the target |
| `ring` | `{"target": P or ID}` | a ring around a point, the board's circling gesture |

Number line shapes: `point` (a number, with `open`), `interval` (`{"from": a, "to": b, "open": [bool, bool]}`, where `null` for an end means unbounded and draws an arrow), `signs` (`{"name": "f'(x)", "at": [c1, c2], "signs": ["+", "-", "+"]}`, one sign per interval, at most 3 rows a figure; a critical value where the function is undefined is written in `undefined`), `text`, `brace`, `callout`, `ring`, `segment`.

Table shapes: `highlight` with `{"row": i}`, `{"column": j}` or `{"cell": [i, j]}` (0-based over the body rows), in role highlight or error, and `callout` pointing at a cell.

### Caps

The block is at most 2,000 characters, one per reply, 1 to 6 steps, at most 16 elements in all and 4 added per step, at most 3 sign rows, at most 12 Riemann pieces, 15 by 15 slope-field segments, 10 Euler steps, 30 sequence terms and 8 polygon vertices; window spans are above 0 and at most 200; a parametric or polar parameter spans at most 8 pi; every curve is sampled at 161 points and every path at 241, and the compiled figure holds at most 4,000 points and 200 primitives. Expressions are at most 80 characters, 48 tokens and nesting depth 10. The server stops compiling a figure after 100 ms and drops it. JSON is read with `json.loads` under the character cap, and a `RecursionError` is caught with the `ValueError`.

## From block to screen [inferred]

### The splitter

`app/agent/drawing/stream.py` `FigureSplitter` sits in `screened_text` (`app/agent/turn.py`) between the provider's text deltas and `SentenceScreen.feed`. It passes prose through, recognises a line that opens a fence with the info string `figure` and buffers until the closing fence, and removes every `[[step:ID]]` marker from the prose, recording the marker's offset in the marker-free text. A partial opener, closer or marker split across deltas is held until it is certain. Text inside `\( \)` and `\[ \]` is never read as a marker or a fence. At an opening fence it calls `SentenceScreen.boundary()`, which screens and releases whatever sentence fragment is buffered, so text and figure keep their order. A block that grows past 2,000 characters is dropped at the cap, and the text after its closing fence continues. A block still open when the stream ends is dropped. A second block is dropped.

### The compiler

`app/agent/drawing/spec.py` validates the parsed block against `schemas/agent/figure.schema.json` (draft 2020-12, `additionalProperties: false` throughout, enums for every kind, role, style and rule, the numeric and length caps) with `Draft202012Validator`, then checks what a schema cannot: ids unique, references resolve to earlier elements of the right shape, a `fade` or `erase` names an element added in an earlier step, windows ordered, `on` names a curve.

`app/agent/drawing/expression.py` is a Python twin of `app/web/src/lessons/expression.ts`: a tokenizer and recursive-descent parser over the same tokens, precedence and function table, with `**` read as `^`, implicit multiplication after a number or a closing bracket, and the length, token and depth caps. It builds a small tree that evaluates in floats through `math` and converts to a SymPy expression by construction, node by node, for the one check that needs symbols. It never calls `eval`, `exec`, `sympify`, `parse_expr` or `lambdify`, and a name outside the table is a refusal.

`app/agent/drawing/compile.py` turns the validated figure into the render spec: it samples curves (161 points, broken where undefined or beyond 10 window heights), paths (241 points), computes points on curves, tangent slopes by a central difference, secant and tangent lines clipped to the window, region polygons, Riemann and trapezoid pieces with their sample points, slope-field segments on the lattice, the solution curve by fourth-order Runge-Kutta, Euler steps, sequence dots, circles and arcs as sampled paths, triangle vertices with the right-angle mark and equal-side ticks, braces, callout leaders and rings. It also collects, for the screen, every number the figure shows (below).

### The render spec

The client receives only this, in a `figure` event: `{"id", "kind", "title", "description", "window", "axes", "grid", "view": {"width", "height"}, "columns", "rows", "steps": [{"id", "caption"}], "primitives": [...]}`. Each primitive has `step` (the step id that adds it), `role`, `element` (the source element id), `faded_at` and `erased_at` (step ids or null), and one of three shapes:

- `path`: `points` (world coordinates), `closed`, `fill` (`none`, `region`, `region_below`), `style`, `weight`, `arrow`, `highlighter`
- `dot`: `at`, `open`
- `label`: `at` (world coordinates), `text`, `align` (`start`, `middle`, `end`), `baseline`, and `boxed` for a table callout

A table figure's primitives are `cell` highlights `{"row", "column"}` with a role. Everything the client draws is a number or a string it typesets; no field names a colour, a class or a URL.

### The screen

`app/evals/figure_checks.py` holds the figure checks, shared by the live screen and the eval as `app/evals/agent_checks.py` is for prose. `no_answer_in_figure` applies when the turn's mode is practice and key forms exist (an unchecked item, or a lesson section that poses a question), and compares with the key forms `key_forms_for` already computes:

1. The title, the description, every caption, label, box text, callout and free text, and every table cell run the existing sentence checks (`agent_checks.SENTENCE_CHECKS`: the key and its letter, praise, advice, prediction, dashes, ids outside the packet). This part applies in every mode.
2. Every marked coordinate: points, segment ends, vector ends, polygon and triangle vertices, circle centres and radii, box corners and sizes, sequence dots, Euler points, interval ends, sign-chart critical values, callout and ring targets, the touching point of a tangent and the two points of a secant. Each coordinate is compared with the key's numeric value within `NUMERIC_TOLERANCE` (0.0005). Integers are compared, as a math span's are.
3. Every line, secant and tangent: slope, y-intercept and x-intercept.
4. Every area: signed integral and absolute area; every Riemann or trapezoid set: its total.
5. Every curve: a constant curve's value; and when the key is an expression in a variable, each curve converted to SymPy and compared with the key at 16 sample points in the window.
6. On a multiple-choice item, the key letter patterns and the key option's value, through part 1 and part 2.

Window bounds, tick positions and expression literals are not compared. A failing figure withholds the whole reply exactly as a failing sentence does: `SentenceScreen.withhold(verdict)` releases the fixed decline, nothing after it is released, the turn ends `withheld`, the stored reply is the decline, and `agent_reply_withheld` is written with the check `no_answer_in_figure` (or the sentence check that fired on a figure text) and the part `figure`, never the value.

### Events and order

Three events join `start`, `text`, `end` and `error` on `POST /agent/turns`:

| Event | Data | When |
| --- | --- | --- |
| `figure_pending` | `{}` | the opening fence was seen; the panel shows "Drawing a figure" |
| `figure` | the render spec | the figure compiled and passed the screen |
| `figure_refused` | `{"reason": "malformed" \| "oversized" \| "unclosed" \| "extra" \| "closed" \| "off", "copy": "..."}` | a figure was dropped; the reply continues |
| `figure_step` | `{"figure": id, "step": id}` | sent immediately before the `text` event of the sentence that carries the step's marker, after that sentence has passed the screen |

A marker before the figure arrived, for an unknown step or repeated, is ignored. Steps no sentence marked are sent as `figure_step` events after the last sentence, before `end`, so the figure is always complete. A `figure` or `figure_pending` event clears the client's 15-second first-text timer.

### The client

`useAgentStream.ts` dispatches the new events to `onFigurePending`, `onFigure`, `onFigureStep` and `onFigureRefused`. `AgentProvider.tsx` keeps, per reply, the figure, its offset in the reply's text (the length of the text shown when the figure arrived), the steps revealed, and a display queue: while a figure is building, a `figure_step` event is a gate, and the text after it waits with it. A gate opens at `previous_gate_time + reading_time(words shown since the previous gate)` at 238 words a minute (math spans count as three words), capped at 6 seconds; the first gate counts from the first text shown in the reply. "Show all" and Stop open every gate at once. The `end` event is applied, and the reply announced, when the queue has drained. Under reduced motion the pacing is the same.

`app/web/src/agent/TutorFigure.tsx` renders the figure frame at once and each primitive when its step is revealed, in an SVG with a 320-unit view width, so ticks and strokes render near 1:1 in the 320 to 384 px panel. It reuses the graph frame from `app/web/src/figures/FigureView.tsx` (layout, axes, gridlines, numbered ticks), which is factored into a shared component with the item figure's output unchanged. Labels are an HTML layer over the SVG, positioned in percentages of the view box and typeset with `MathText` on the tutor renderer, clamped inside the figure. The client re-validates the render spec (types, finite numbers, the point and primitive caps) and draws nothing from a spec that fails, showing the refused line instead.

Placement: the reply renders its text up to the figure's offset, the figure, then the rest, so the figure sits where the model put it, under the sentence that introduces it.

## Motion [inferred]

Each step's primitives enter together. Paths enter by a wipe: the step's paths are clipped by a rectangle whose `transform: scaleX()` goes from 0 to 1 from the left edge of the plot over 300 ms ease-out (`motion-figure-wipe`), and dots, fills and labels fade in over the same 300 ms (`motion-figure-step`). Under `prefers-reduced-motion: reduce` the wipe's transform is dropped and only the opacity cross-fade runs, as plan 08 prescribes; the build keeps its order and its reading pace, and the "Steps" disclosure is open. No `stroke-dashoffset`, no second duration, no stagger inside a step, no loop, no motion after a step has entered. A step interrupted by the next (a fast "Next") jumps to its end state. Both classes live in `motion.css` and are listed in `motion.ts`, so `motion.test.ts` holds them to 300 ms ease-out, transform and opacity only, and the reduced-motion rule.

## Accessibility [inferred]

- The SVG is `role="img"` with `aria-labelledby` naming the visible title and `aria-describedby` naming the description and the step list, both outside the SVG, because an `img`'s children are presentational. The label layer is `aria-hidden`, since the description and the captions carry what it says.
- The figure's wrapper is in the tab order (`tabindex="0"`, `role="group"`, `aria-roledescription` not used) with the title as its name, so a keyboard user reaches it and hears the title and description; the step controls follow it in the tab order. Nothing takes focus when a figure or a step appears.
- While the reply streams the reply is `aria-busy`, so steps are not announced one by one. When it ends, the one status announcement adds "Figure: {title}. {description}" after the reply's words.
- The step list is an ordered list of captions; the revealed step count and the current step carry `aria-current="step"` and the word "now".
- Every mark holds 3:1 against its ground in both themes and every role differs from the others with colour removed; `contrastAllScreens.test.tsx` and `greyscaleStates.test.tsx` cover the figure through a screen entry in `app/web/src/testing/screens.tsx`.
- The figure scales to the panel's width at phone width, keeps its height at most the view width, and never scrolls sideways.

## The prompt [inferred]

`prompts/agent/live_v2.md` replaces `live_v1.md` for the agent role. Its prefix keeps every rule of v1 and adds, above the marker so it is cached: the drawing rules (when to draw, the practice rule on answer-bearing elements, one figure, the block and marker syntax, steps of one idea, labels short and on the figure, roles not colours, fade rather than erase, describe the figure in the description, never mention the markers or the block in prose), the vocabulary table in compact form, and at least ten example figures with the sentences that mark their steps: secant to tangent (practice, generic curve), left Riemann rectangles against right (after submission), area between curves, slope field with a solution, a sign chart for f prime, a table with a highlighted row, a related-rates right triangle, a parametric path with a velocity vector, a polar curve with rays, partial sums approaching a limit line, an interval of convergence, a box-and-arrow picture of rate in and rate out, and a hole with one-sided approach. Below the marker it gains one app-composed field, `drawing`, with `open` or `closed`. The prefix stays byte-identical across turns.

## The item's own figure in the packet [inferred]

`practice_body` gains `figure`, a summary of the item figure the student sees: its kind, window, alt text, and for a table its columns and rows. The alt text of a generated figure states every value the student needs (`prompts/generator/figure_spec_v1.md`), so the tutor can refer to what is on screen and draw about it. The summary carries no key; its numbers are the item's givens, and the screen compares the reply with the key as before.

## Storage, privacy and logs [inferred]

`agent_turns` gains one additive nullable column, `figure`, a JSON object on the agent's turn: the validated source spec, the outcome (`shown`, `refused:{reason}` or `withheld`) and the number of steps revealed. A withheld figure's spec is not stored. The column rides the turns' 30-day retention, deletion per conversation and in full, export and purge, because the table already carries `user_id`. The Settings conversation view shows "Figure: {title}" under the turn. The history sent to the model on later turns appends one line to the agent turn, "[Figure shown: {title}. {description}]", and never the spec. Log lines add the figure outcome and the step count to the turn line, and never a spec, an expression, a label or a value.

## The switch [inferred]

`GROWTH_AGENT_DRAWING` (default `on`). With `off`, `drawing` is `closed` on every turn and any figure is dropped with the reason `off`. It is a kill switch for the feature, not an experiment arm; there is no randomisation between drawing and not drawing in this build, because the outcome the experiment would need (later unaided correctness) is already the `tutor_profile` readout and a second arm on the same turns would halve both.

## Cost [inferred]

Priced by `tools/cost_model.py` under the names in brackets and quoted in plan 14's amendment. The v2 prefix is about 5,500 tokens against 2,500 for v1, read from the cache on every turn after the first of a conversation. A figure is about 300 output tokens and about 3 seconds of generation. On the subscription the lines are notional and count against pacing only, one call a turn as before.

## Evals [inferred]

`content/golden/agent.json` gains drawing cases, each a turn whose candidate reply may carry a figure block: cases that should draw (a secant sketch on name_rule, a Riemann figure on discuss_step, a slope field on explain, a triangle on a related-rates lesson), cases that must not (a figure on ask_what_tried, on probe, on navigate is allowed but not needed), cases whose figure leaks (a point at the key, a tangent with the key's slope, a label naming the key letter, a shaded region with the key's area, a Riemann total equal to the key), and a malformed and an oversized block. New labels: `figure_well_formed`, `draws_only_when_open`, `no_answer_in_figure`, `figure_described`. `app/evals/golden.py` compiles each candidate figure with the live compiler, and `tests/eval/test_agent_golden.py` asserts every label agrees with its check. `tools/agent_eval.py` reports the figure checks with denominators beside the prose checks.

## Rejected [inferred]

- Model-written SVG, HTML, CSS or JavaScript, even in a sandboxed frame: plan 09's rule, the SVG record, one origin with no `unsafe-eval`.
- Vega-Lite, Mermaid, Plotly, Desmos state, GeoGebra commands, TikZ or Manim as the language: expression-language XSS, opaque state, embedded scripts, executable code.
- The model writing point lists or colours: models place coordinates badly and colour must carry no meaning alone.
- Evaluating the model's expressions in the browser: what the screen checks and what the student sees must be the same numbers.
- Tool calls for drawing: the no-tools rule, the CLI path, and no gain over a fenced block the server parses.
- One block per step between sentences: a leak that appears only in combination could not be caught.
- Revealing at generation speed: the figure would finish before its first sentence was read.
- A continuous morph, a stroke drawn by dash offset, a visible hand or pen: no learning value in the evidence and outside plan 08's motion rules.
- Autoplay replay: full learner control did not help and its timing would have no source.
- Colouring the matching words of the reply: the reply is plain text by rule, and markup in it would be a second rendering path.
- The finished figure only under reduced motion, the brief's provisional choice: reduced motion asks for movement to be replaced, plan 08 says replace and not delete, and the benefit rides on segmenting and contiguity; the finished figure with its step list stays as the end state.
- Raising `MAX_OUTPUT_TOKENS`: a figure is about 300 tokens of the 800, and the cap is raised only if the evals show replies cut off.
