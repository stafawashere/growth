---
title: Figures as declarative specs
version: v1
role: generator
model: offline Claude Code session, claude-opus-5-5
purpose: How a template emits a figure as a declarative spec the client renders, never as an image, with every label inside the figure.
---

# Figures are data

A figure is a dictionary built with the helpers in `app/generation/kit.py`. The client draws it; a
model never draws a picture and never writes SVG.

- `figure(kind, domain, range_, curves, marks, labels, axis_titles, gridlines, alt, fills)` for
  `function_graph`, `region`, `parametric_curve`, `polar_curve`, `vector_diagram`, `number_line`,
  `slope_field` and `geometric_diagram`. A curve is a list of polyline segments; build them with
  `sample_curve`, `sample_parametric` or `sample_polar`, which break at asymptotes and at the window
  edge so the renderer never joins across a gap. Straight pieces may be written as two-point
  segments. `fills` are polygons (a region's boundary as a closed list of points).
- `marks` are `point_mark` (filled or open, for holes and endpoints), `segment_mark` (solid or
  dashed, for asymptotes, tangent lines and slope-field ticks; `slope_segments` builds a whole
  field) and nothing else.
- `labels` come from `label(text, x, y)` and always sit inside the window with placement `inside`.
  Put the curve's name and any value the student must read from the figure beside the thing it
  names, never in a caption or a legend. Choose the window so every label fits.
- `table_figure(columns, rows)` for a numerical table. The first column is the input. Cells are
  short strings; inline LaTeX between `\(` and `\)` is allowed.
- `alt` is one or two plain sentences stating what the figure shows, including every value the
  student needs, so the item can be read without seeing it.

Every value the solution uses must be readable from the figure: vertices on grid points, values
at labelled points, a slope field on a lattice the stem names. The stem says "shown" or names
"the table" when it relies on the figure, and never repeats the figure's data in prose.
