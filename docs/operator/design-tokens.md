---
title: The design token file
research_date: 2026-09-23
status: in_progress
purpose: Where the design token file lives, who authored it, which palette was chosen, and how it is checked.
---

# The design token file

The file is `app/design/growth-tokens.json`. Entry criterion 5 and remaining implementer decision
6 of `docs/plan/11-phased-delivery.md` have the implementer author it in the P1 pull request from
the roles in `docs/plan/08-design-brief.md`, which fixes token names and roles and no hex values.
The implementer authored it and the operator chose the palette. Gate 26
(`test_contrast_floors`, in `tests/design/test_contrast_floors.py`) reads the hex values out of
this file and computes every ratio itself.

`GET /growth-tokens.css` serves the file `GROWTH_TOKENS_PATH` names and answers 404 while it is
unset, so a deployment sets `GROWTH_TOKENS_PATH=app/design/growth-tokens.json`; see `app/main.py`.

## The palette chosen

The operator chose Graphite, revised, on 2026-09-23. The file holds that palette unchanged: 17
colour tokens and 9 type tokens under each of `light` and `dark`. The type values are 08's own
sizes from its type scale table (`type-display` 32px down to `type-caption` 13px), and a test
checks the file against that table.

## Token names by group

Read from `app/design/tokens.py`, `COLOUR_TOKENS`:

Neutral ramp, so far as 08 names its steps: `surface-page`, `surface-raised`, `surface-sunken`,
`border-hairline`, `text-primary`, `text-secondary`, `text-muted`, `text-on-accent`,
`focus-ring`.

Accent: `accent-base` and its tint ramp `accent-tint-1` through `accent-tint-4`, plus
`accent-contrast-text`.

Semantic: `state-correct`, `state-incorrect`. 08 names a tint ramp for each without enumerating
steps, so no semantic tint token is in the vocabulary; only these two base tokens are checked.

Type: `TYPE_TOKENS`, the nine rows of 08's type scale table. Each value is the right-hand side of
a CSS declaration. `app/design/css.py` refuses a missing, empty or unsafe type value when it
builds the stylesheet.

`docs/operator/design-tokens.template.json` is the blank shape of the file, every value `null`.

## The two floors and the pairs checked

From `app/design/contrast.py`: `TEXT_CONTRAST_FLOOR = 4.5`, `LARGE_TEXT_CONTRAST_FLOOR = 3.0`.
`TYPE_TOKENS` marks `type-display` and `type-title` as large (3:1); the other seven are normal
(4.5:1).

The pairs are `CONTRAST_PAIRS` in `app/design/tokens.py`, used by `token_violations`,
`tools/check_tokens.py` and gate 26 alike: every text role (`text-primary`, `text-secondary`,
`text-muted`) on every surface; `text-on-accent` on `accent-base`; `accent-contrast-text` on each
of `accent-tint-1` through `accent-tint-4`; `state-correct` and `state-incorrect` on every
surface; `focus-ring` on every surface. `token_violations` holds every pair to 4.5:1, because 08
never says a specific colour pair renders only at a large size. Gate 26 checks every pair at the
floor of every type step, so in practice every pair must clear 4.5:1. Both themes are checked
independently.

## The approved checker change

`accent-contrast-text` is no longer checked against `accent-base`. The operator approved this on
2026-09-23 when choosing the palette. The reason is that 08 gives the text on an `accent-base`
fill, the primary button, its own token, `text-on-accent`, and that pair is still checked.
`accent-contrast-text` is the tint-hue text 08 describes for the accent tint backgrounds, and it
is still checked on all four tints. Every other check is unchanged.

## The check

```
python3 tools/check_tokens.py app/design/growth-tokens.json
```

It prints every violation, one per line, then the computed ratio for every pair in
`CONTRAST_PAIRS` in each theme, and exits 0 only when there are no violations. The nine type
tokens are known to the checker and are not reported as unknown.

Run on 2026-09-23 against `app/design/growth-tokens.json`, it printed no violations and 46 ratio
lines (23 pairs in each of two themes), and exited 0. The lowest ratios were `focus-ring` on
`surface-sunken` at 4.91:1 (light) and `focus-ring` on `surface-raised` at 4.92:1 (dark). The
lowest text-role ratio was `text-muted` on `surface-raised` at 5.71:1 (dark).

## The named checker cross-check

Implementer decision 6 and gate 26 also ask for the output of a WCAG 2.2 contrast checker named by
tool and version, with each measured ratio, in the pull request. That cross-check is recorded
separately by the integrator, not in this document. It stands beside `test_contrast_floors` as a
manual cross-check and does not replace it.
