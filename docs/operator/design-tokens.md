---
title: The design token file
research_date: 2026-09-20
status: in_progress
purpose: What the operator fills into the design token file, and how to check it before the PR.
---

# The design token file

Entry criterion 5, remaining implementer decision 6 and gate 26 (`test_contrast_floors`) need a
filled design token file. 08-design-brief.md fixes the token names and their roles and
deliberately fixes no hex values; the operator authors every hex value in this pull request. This
document authors no hex value and suggests none.

## What to do

1. Copy `docs/operator/design-tokens.template.json`. It carries every token name the vocabulary
   in `app/design/tokens.py` names, the 17 colour tokens and the 9 type-scale tokens, under both
   `light` and `dark`, each value `null`.
2. Fill every colour token with a hex colour and every type token with a type-scale value, as
   described under "Type-scale values" below.
3. Run the checker (below) and fix anything it reports.
4. Paste the checker's output into the pull request, alongside the output of a named WCAG 2.2
   contrast checker (see "The pull request" below), per remaining implementer decision 6.

## Token names by group

Read from `app/design/tokens.py`, `COLOUR_TOKENS`. 08's role for each is the comment attached to
it there:

Neutral ramp, so far as 08 names its steps: `surface-page`, `surface-raised`, `surface-sunken`,
`border-hairline`, `text-primary`, `text-secondary`, `text-muted`, `text-on-accent`,
`focus-ring`.

Accent: `accent-base` and its tint ramp `accent-tint-1` through `accent-tint-4`, plus
`accent-contrast-text`.

Semantic: `state-correct`, `state-incorrect`. 08 names a tint ramp for each without enumerating
steps, so no semantic tint token is in the vocabulary; only these two base tokens are checked.

Both `light` and `dark` carry the full set. `THEMES` in the same module is `("light", "dark")`.

Type tokens are a separate table and carry no colour of their own; see "The two floors" below for
which ones are checked at which floor once a screen binds a colour pair to them, and "Type-scale
values" for what goes in the slot.

## Type-scale values

Read from `app/design/tokens.py`, `TYPE_TOKENS`: `type-display`, `type-title`, `type-heading`,
`type-body`, `type-math-inline`, `type-math-display`, `type-label`, `type-caption`, `type-mono`.
Entry criterion 5 calls them the nine type-scale steps and hands their values to the operator the
same way it hands over the hex values.

A filled value is the right-hand side of a CSS declaration: whatever string the operator wants
`font-size: var(--growth-type-body)` to resolve to. 08-design-brief.md fixes no type-scale value,
so no unit, no step ratio and no range is prescribed here, and none is enforced. `1rem`,
`1.125rem`, `18px` and `clamp(1rem, 2.5vw, 1.5rem)` are all accepted, and the choice of ramp is
the operator's, to be recorded in the pull request alongside the contrast evidence.

What `app/design/css.py` does enforce is that the value can be emitted at all. A type token the
token file omits is refused, exactly as a missing colour is, because a silently dropped type
token resolves to an empty custom property in the client and the browser falls back to its own
default with nothing failing. A value that is not a string, is `null`, or is empty once trimmed
is refused. A value carrying `;`, `{`, `}`, `<`, `>`, a backslash, a quote character, `/*`, `*/`
or a control character is refused, because each of those can end the declaration, end the rule
block, close the surrounding element or open a comment, and a browser drops the broken
declaration while parsing the rest of the sheet, so nothing would surface.

## The two floors

From `app/design/contrast.py`: `TEXT_CONTRAST_FLOOR = 4.5`, `LARGE_TEXT_CONTRAST_FLOOR = 3.0`.

`app/design/tokens.py`, `TYPE_TOKENS`, marks `type-display` and `type-title` as `"large"`; the
other seven type tokens (`type-heading`, `type-body`, `type-math-inline`, `type-math-display`,
`type-label`, `type-caption`, `type-mono`) are `"normal"`. The large-text floor is 3:1; every
other type token's floor is 4.5:1.

The colour-pair checker itself (`token_violations`, what `check_tokens.py` runs) checks every
pair it enforces against the 4.5:1 floor, since 08 never states that a specific colour pair
renders only at `type-display` or `type-title` size. It checks: every text role
(`text-primary`, `text-secondary`, `text-muted`) against every surface (`surface-page`,
`surface-raised`, `surface-sunken`); `text-on-accent` against `accent-base`;
`accent-contrast-text` against each of the five accent backgrounds; `state-correct` and
`state-incorrect` against every surface; `focus-ring` against every surface.

## Both themes checked independently

`token_violations` runs the full check over `light` and again over `dark`. A pair that clears the
floor in one theme is not assumed to clear it in the other; both are computed.

## The check

```
python3 tools/check_tokens.py <path>
```

Its vocabulary is `COLOUR_TOKENS`, so it checks colour values and contrast pairs only; the
type-scale values are checked by `app/design/css.py` when the stylesheet is generated. Because
the template now also offers the nine type tokens and `token_violations` does not yet know them,
the tool reports each of them as an unknown token. That is a gap in the checker, not a fault in
the template, and it is recorded in the pull request.

Run on 2026-09-21 against the unfilled `docs/operator/design-tokens.template.json`, this printed
52 lines: 34 for the missing colours (17 tokens times 2 themes), each shaped like:

```
light: surface-page is not a valid hex colour, got None
```

and 18 for the type tokens the checker does not yet know (9 tokens times 2 themes), and exited 1,
as expected for an all-null file. Once every value is a valid hex colour, the tool
instead prints, for every checked pair in each theme, a line like
`light: text-primary on surface-page is 4.83:1`, so the operator sees the margin, not only a
pass or fail; any pair still below its floor is reported as a violation and the tool exits 1.
Exit 0 with no violation lines means every checked pair clears 4.5:1 in both themes.

## The pull request

08's own decision 6 is that the pull request carries the output of a named WCAG 2.2 contrast
checker, by tool name and version, with each measured ratio recorded, alongside this tool's own
output. `test_contrast_floors` reads the hex values out of the token file and computes the
ratios itself; the external checker's output is the manual cross-check named in gate 26, not a
substitute for running `check_tokens.py`.
