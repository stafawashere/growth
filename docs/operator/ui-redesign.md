---
title: Stage 9 UI redesign, from the operator's prototype to the app
research_date: 2026-09-26
status: done
purpose: The record of how the operator's standalone prototype was ported onto the running app, which token values changed to meet a gate, which prototype features were not taken and why, and where the before and after screenshots are.
---

# Stage 9 UI redesign [verified]

On 2026-09-26 the operator attached `growth-standalone-source.zip`, a static design prototype built
by another assistant from screenshots, the plan and this repository at commit 7a677c6. Attaching it
is the operator's instruction to replace the Graphite palette chosen on 2026-09-23. The prototype
was read as a visual and interaction reference only; none of its code, data or vendored libraries
entered the repository.

Every comparison and judgement in this record was made by claude-opus-5-5 on the operator's
delegation, not by a person. The screenshots were taken by that model driving headless Brave
152 over the Chrome DevTools Protocol against the real app, served by `app/main.py` over a
scratch database with the passkey verifier replaced by a double.

## Palette mapping [verified]

The prototype's variables on `:root` (dark) and `:root[data-theme=light]` map onto 08's token roles
as below. Token names are unchanged; only values moved.

| 08 token | Prototype variable | Dark | Light |
| --- | --- | --- | --- |
| `surface-page` | `--bg` | #101012 | #f8f8f8 |
| `surface-raised` | `--panel` | #18181b | #ffffff |
| `surface-sunken` | `--well` | #09090b | #efeff1 |
| `border-hairline` | `--line` | #6b6b72 (changed, see below) | #83838b (changed, see below) |
| `text-primary` | `--text` | #f4f4f5 | #18181b |
| `text-secondary` | `--sub` | #ababb4 | #575762 |
| `text-muted` | `--muted` | #92929d | #666670 |
| `accent-base` | `--white` (the primary fill) | #ffffff | #18181b |
| `text-on-accent` | `--ink` | #09090b | #ffffff |
| `focus-ring` | `--white` (the prototype's outline) | #ffffff | #18181b |
| `state-correct` | `--green` | #34d399 | #087b54 |
| `state-incorrect` | `--red` | #fb918b | #b83c35 |
| `accent-tint-1` to `accent-tint-4` | `--raised` and the steps either side of it | #1c1c20, #242428, #2c2c31, #35353b | #f2f2f4, #e7e7ea, #dedee2, #d4d4d9 |
| `accent-contrast-text` | `--text` on a raised fill | #fafafa | #18181b |

The prototype is monochrome: its one accent is the ink colour itself (a white primary in dark, a
near-black primary in light). That is read as 08's "one restrained accent" with the accent set to
the ink hue, so `accent-contrast-text` is a tint of that same neutral hue and no grey sits on a
coloured ground. The prototype's neutrals are a cool zinc rather than 08's warm ramp; the operator's
choice of design overrides that line of 08, as the Graphite choice did before it.

## Values changed to meet a gate [verified]

Each value below failed a gate at the prototype's setting and was moved until it passed. No gate
was changed.

| What | Prototype | App | Gate and ratio reached |
| --- | --- | --- | --- |
| `border-hairline`, dark | #2b2b30, 1.26:1 on `surface-raised` | #6b6b72 | SC 1.4.11 in `eval_contrast_all_screens`: 3.59:1 page, 3.35:1 raised, 3.76:1 sunken |
| `border-hairline`, light | #d6d6db, 1.26:1 on `surface-sunken` | #83838b | same gate: 3.54:1 page, 3.76:1 raised, 3.27:1 sunken. A first value, #8e8e96, reached only 2.83:1 on sunken and failed |
| An answered question-menu tile's border | the prototype draws answered tiles by fill alone | `text-muted` border | the hairline on `accent-tint-2` is 2.92:1 in dark, under 3:1 |
| The shaded region under a figure's curve | (the app's own figures) | `accent-tint-1` | the gridlines over `accent-tint-3` were 2.63:1 dark and 2.42:1 light |
| A chosen option or confidence tile | border colour change only | border shorthand in `text-primary` | the catalogue's cascade reads the shorthand, and the hairline on `accent-tint-2` fails at 2.92:1 |
| Page title | 28 px, weight 600 | `type-title`, 24 px | 08's type table, pinned by `tests/design/test_fixed_tokens.py` and `app.test.ts` |
| Eyebrow labels | 12 px | `type-caption`, 13 px | no 12 px step exists in 08's table |
| Navigation links | 15 px | `type-label`, 14 px | same |
| Button text | 15 px | `type-body`, 16 px | same |
| Math input | 24 px | `type-math-display`, 21 px (`type-math-inline` under 600 px) | same |
| Primary hover `filter: brightness(.88)` and disabled `opacity: .4` | literal factors | not taken; disabled keeps the dashed outline | `test_no_literal_values` allows no literal factor, and the greyscale gate needs disabled to read without colour |
| Section rules under every `h2` | 1 px `--line` | none; headings are separated by space | at 3:1 a rule under every heading reads heavy, and 08 prefers space over borders |

`python3 tools/check_tokens.py app/design/growth-tokens.json` exits 0. Its lowest text pairs are
light `state-correct` on `surface-sunken` at 4.60:1, light `state-incorrect` on `surface-sunken`
at 4.90:1 and light `text-muted` on `surface-sunken` at 4.94:1.

## Type, space and layout [verified]

- Inter at 400, 500 and 600 is self-hosted from `@fontsource/inter` 5.3.0 (the package's own files,
  not the prototype's, whose hashes differ), with the SIL Open Font License kept beside them in
  `app/web/src/fonts/OFL.txt`. Each weight file is its own family in `app/web/src/styles/fonts.css`
  ("Inter", "Inter Medium", "Inter SemiBold"), so a rule picks a weight by family and no numeric
  weight appears in any stylesheet.
- Tracking follows the prototype, written as fractions of the 4 px step: titles at -0.5 px,
  headings at -0.25 px, eyebrows and the calculator label at +0.8 px, the brand at +0.33 px.
- The page column is the prototype's 820 px (205 steps of 4 px); every paragraph and list item
  inside a screen still stops at 08's 68 characters.
- Breakpoints are the prototype's 900 px and 600 px. Under 600 px the gutter is 16 px, as 08 fixes,
  and the primary action stretches to the column.

## Chrome and screens [verified]

- Header: the brand "Calculus BC" (moved from each screen's eyebrow into the bar), Home, and
  Settings at the right, over a full-width hairline. The current destination carries
  `aria-current="page"` and an underline. The bar still holds exactly Home and Settings, as
  `App.test.tsx` and 08's information architecture require.
- Footer: a hairline and "AP Calculus BC". The prototype's tagline and preview links are not taken.
- A screen is drawn flat on the page. Its title carries the rule beneath it.
- Home: "Today" as the title, the minute forecast as the lead line, the queue counts as large
  tabular numbers, one primary action, the four links in a ruled row, the exam line in monospace.
- Session: a stage badge above the item (08's wireframe shows "stage: completion" in the item
  header), the item and its feedback in a raised panel, "Worked so far" over the steps (08's
  wireframe copy) in a sunken well, the confidence rating as three tiles, and the primary action
  at the right of a ruled submit row.
- Multiple choice: options as bordered rows; the chosen row takes a raised fill and a
  `text-primary` border while its radio stays drawn, so the choice reads without colour.
- Onboarding: the title as the page heading, "I have not learned this yet" and "Check my answer" in
  one submit row, the unit results as ruled rows.
- Progress: the legend above the map, each unit a ruled row with its name above its marks, the
  calibration curve directly beneath the map as 08 requires.
- Mock exam and timed parts: the free-response capture choice as tiles, drills and unit checks as
  ruled rows, a tool bar (mark for review, question menu, zoom) above the question, the question
  menu opening as a block of tiles beneath it, and Back, Next and Submit part in a ruled bottom row.
- Settings: tables and lists as ruled rows, inputs capped at 288 px.
- The constant e in a multiple-choice option now renders. MathLive with compute-engine 0.24.1 wrote
  it as `\exponentialE`, which KaTeX showed as raw LaTeX; `mathJsonToLatex` rewrites it to
  `\mathrm{e}`. This was a defect present before the stage, fixed because it showed on the
  redesigned option rows; `src/math/mathjson.test.ts` went red on the old code and green after.

## Prototype features not taken [verified]

| Feature | Why |
| --- | --- |
| Sample questions (`data.js`), curriculum copy (`curriculum.js`), seeded mastery, calibration and history, localStorage state | every screen reads the real API; `data.js` was not copied or quoted anywhere |
| The "if-then study plan" in placement | no study plans or schedules anywhere |
| Provider and model choice, non-Anthropic providers | ruled out for one student in P6; settings shows the chain read-only |
| Simulated sign-in, named devices, the recovery flow | authentication stays passkey-only as built, with the app's own recovery code path |
| A single predicted score | the result shows the band with its assumptions only |
| "Reset preview", "Design preview", "All views", "illustrative" and sample-record labels | they describe the prototype, not the app |
| Simulated OCR, grading and scheduling | the app does these for real |
| Session, Review and Progress on the top bar, and the account icon | 08's information architecture and `App.test.tsx`: the bar holds Home and Settings; the rest is reached from home |
| Tabs on progress | 08 puts the calibration curve directly beneath the map on one screen |
| A skill count beside each unit on the map | `MasteryMap.test.tsx` "prints no count and no percentage anywhere on the map" failed when it was added, which is 08's anti-bar rule |
| 21 px map squares with 5 px gaps | the 16 px marks with 8 px gaps keep the 24 px target spacing ruled for WCAG 2.5.8 |
| The session progress segments and "Set 1 of 3, item 1" | the client has no set position to show; showing a total would be a count of remaining work the queue does not fix |
| "I want to stop here" | the client has no stop route; leaving through Home keeps the set resumable from home's Resume |
| "Press Enter to check your answer" | no Enter binding is verified on every item type, so the hint would be a claim |
| The theorem reference panel, "the idea to keep", and the "you wrote / the rule gives" block | the item and feedback payloads carry none of that content; feedback keeps the step marks and the elaborated panel |
| A theme switch and a reduced-motion switch in settings | the app follows the system setting for both; the operator can switch the system |
| Vendored KaTeX, MathLive and Compute Engine | the app's own npm copies are kept, with MathML exposure from P8 |
| The amber flag marker | no amber token exists, and a flagged question already says "marked for review" in words |

## Screenshot pairs [verified]

Taken on 2026-09-26 by claude-opus-5-5 in headless Brave 152, not by a person. Both apps were
served from the same database snapshot (the item bank ingested, one registered student), the before
app from a detached worktree at 54898ee and the after app from the `ui` branch, and walked through
the same 22 states by one script. A part drill draws its questions afresh, so the timed-part pairs
show different questions. The files are in the session scratchpad, not the repository:

`/private/tmp/claude-502/-Users-mahfujm-dev-growth/f2920e88-e8bd-434f-a3f9-1b20be9fa70f/scratchpad/shots/`

- `before/`: the old client, every state at 1280 px in both themes (44 files).
- `after/`: the new client, every state at 1280, 900 and 375 px in both themes (132 files).
- `pairs/`: one image per state and theme with before on the left and after on the right (44 files).

| Screen | Pair |
| --- | --- |
| Onboarding, the diagnostic introduction | `pairs/onboarding-intro-1280-dark.png`, `pairs/onboarding-intro-1280-light.png` |
| Onboarding, a diagnostic question | `pairs/diagnostic-question-1280-dark.png`, `pairs/diagnostic-question-1280-light.png` |
| Onboarding, the unit results | `pairs/diagnostic-result-1280-dark.png`, `pairs/diagnostic-result-1280-light.png` |
| Home, the queue ready | `pairs/home-ready-1280-dark.png`, `pairs/home-ready-1280-light.png` |
| Session, an item at the example stage | `pairs/session-item-1280-dark.png`, `pairs/session-item-1280-light.png` |
| Session, the item answered with a confidence chosen | `pairs/session-item-answered-1280-dark.png`, `pairs/session-item-answered-1280-light.png` |
| Session, step-mark feedback with the self-explanation and the error note | `pairs/session-feedback-1280-dark.png`, `pairs/session-feedback-1280-light.png` |
| Home, a set in progress | `pairs/home-in-progress-1280-dark.png`, `pairs/home-in-progress-1280-light.png` |
| Progress, the map, the curve, representations and histories | `pairs/progress-1280-dark.png`, `pairs/progress-1280-light.png` |
| Review | `pairs/review-1280-dark.png`, `pairs/review-1280-light.png` |
| Free response, the unit list | `pairs/frq-units-1280-dark.png`, `pairs/frq-units-1280-light.png` |
| Free response, a question and its capture choice | `pairs/frq-question-1280-dark.png`, `pairs/frq-question-1280-light.png` |
| Mock exam setup, with the capture tiles, drills and unit checks | `pairs/mock-setup-1280-dark.png`, `pairs/mock-setup-1280-light.png` |
| Unit check, a question with option rows and confidence tiles | `pairs/unit-check-1280-dark.png`, `pairs/unit-check-1280-light.png` |
| Part drill, the start screen | `pairs/part-start-1280-dark.png`, `pairs/part-start-1280-light.png` |
| Timed part, a calculator question | `pairs/part-runner-1280-dark.png`, `pairs/part-runner-1280-light.png` |
| Timed part, the question menu open and the graphing panel plotting | `pairs/part-tools-1280-dark.png`, `pairs/part-tools-1280-light.png` |
| Timed part, the closed-part boundary | `pairs/part-closed-1280-dark.png`, `pairs/part-closed-1280-light.png` |
| Part drill result, raw counts and pacing | `pairs/part-result-1280-dark.png`, `pairs/part-result-1280-light.png` |
| Settings | `pairs/settings-1280-dark.png`, `pairs/settings-1280-light.png` |
| Evidence of learning, from settings | `pairs/evidence-1280-dark.png`, `pairs/evidence-1280-light.png` |
| Account, signed out | `pairs/account-signed-out-1280-dark.png`, `pairs/account-signed-out-1280-light.png` |

The prototype's own views, for side-by-side reading, are in `proto/` (17 routes at the three
widths in both themes) and `proto-flow/` (its session, feedback and part setup).

At 375 px no state scrolls the page sideways: `scrollWidth` equalled `clientWidth` (375) on all 22.
The only elements past the edge were inside a horizontally scrolling table or KaTeX's clipped
MathML layer, which also shows the probe was reading real elements.
