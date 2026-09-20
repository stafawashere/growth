---
title: Design brief for the adaptive AP Calculus BC tutor
research_date: 2026-09-19
status: draft
purpose: The interface contract for the app. Fixes the point of view, the type and colour systems, spacing, motion, interface writing, the anti-pattern list, the information architecture, one ASCII wireframe per screen, and the accessibility floor, so that 11-phased-delivery.md can name screens by name and an implementer never has to invent a visual decision.
---

# Design brief

This document is binding on every screen the app renders. It follows decision D9 of the decisions memo and draws its evidence from track 4 Part A (design sources and educational UX), track 1 (session shape, feedback, calibration), and track 3 sections 1 and 2 (Bluebook tools, the paper booklet, the capture flow). Numbers carry their source URL and an evidence tag: [verified] means a primary page was loaded and the claim is read off it, [single-source] means one secondary page supports it, [inferred] means it follows from loaded material without being stated there. Where a value is not known it says unknown rather than guessing.

Ordering rule for every justification below: learning impact first, cost second, convenience third, and the rejected alternative named. A design choice that only saves the builder time does not survive contact with a student who has eighteen months and one exam.

## Point of view

The app is a quiet textbook that knows what the student got wrong last Tuesday [inferred, decisions memo D9]. A student who opens it daily for eighteen months will stop seeing the interface by about week three, so the design's job is to be invisible and fast rather than impressive on first load [inferred, track 4 design point of view draft]. Every screen presents exactly one next action, because a dashboard of options forces a decision before any mathematics happens, and that decision is the most common point of abandonment [inferred, track 4, following Chimero's argument that the designer's job is framing and articulation rather than subtraction, https://frankchimero.com/blog/2015/the-webs-grain/]. Typography carries the entire product, because the content is prose, symbols and numbers and there is almost nothing else on screen to design [inferred, track 4 relevance note on Refactoring UI, https://www.refactoringui.com/]. Hierarchy comes from weight, colour and space rather than from size, since size is the crudest lever and the correct move is usually to de-emphasise the surroundings instead of enlarging the focus [single-source, a commercial book landing page rather than a study, https://www.refactoringui.com/]. Colour is one restrained accent over a warm neutral scale, reserved for the current focus and for correctness state and never used decoratively, which is Kennedy's black-and-white-first rule with a single accent introduced afterwards [verified, https://www.learnui.design/blog/7-rules-for-creating-gorgeous-ui-part-1.html]. Motion exists only to explain a state change, runs under roughly 300 ms, is interruptible, and degrades to an opacity cross-fade under reduced-motion [verified, https://emilkowal.ski/ui/great-animations and https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion]. Feedback is informational and process-directed, naming what the student can now do and what specifically failed, because positive verbal feedback enhanced free-choice behaviour at d = 0.33 and self-reported interest at d = 0.31 while completion-contingent tangible reward ran at d = -0.36 [single-source, Deci, Koestner and Ryan 1999, https://home.ubalt.edu/tmitch/642/articles%20syllabus/Deci%20Koestner%20Ryan%20meta%20IM%20psy%20bull%2099.pdf]. There is no chat box beside an unsolved problem, because in a field experiment with nearly 1,000 Turkish high-school mathematics students the unguarded chat condition beat control by 48 percent during assisted practice and then scored 17 percent below control on the unassisted exam, while the guardrailed tutor recovered only to parity [single-source, Bastani et al, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4895486 and https://pubmed.ncbi.nlm.nih.gov/40560616/]. Progress is shown as coverage and durability of the syllabus, a map that fills in and fades where retention is decaying, rather than as a bar or a streak that can be lost, because retention decays and a bar implies a finish line that does not exist [inferred, track 4 anti-pattern list]. Reference material and the thing the student is doing sit on screen together rather than one behind a navigation jump, so the worked reference for a technique appears beside the problem instead of replacing it [inferred, track 4 Stripe section]. The daily commitment is expressed in minutes of focused work rather than in items, because a hard implicit-differentiation problem and an easy power-rule derivative are not the same unit and minutes are honest about cost in a way item counts are not [inferred from Math Academy's XP unit of roughly one minute of focused effort, https://www.mathacademy.com/how-it-works].

## Type system

The prose and interface face is Inter at its text optical size. Inter ships two optical sizes: the text cut has a deliberately tall x-height for lowercase legibility and carries contrast-enhancing details the site calls ink traps and bridges, while the display cut drops those in favour of cleaner lines and finer detail at large settings [verified, https://rsms.me/inter/]. The switch to the display optical size happens only above roughly 28 px, which is a threshold chosen for this app and not stated on the typeface's site [inferred]. Tabular figures are an explicit documented feature of Inter, intended for columns of numbers that must align across rows [verified, same URL], and they are enabled globally for every score, timer, accuracy percentage, question counter, point total and mastery count, so a number does not jitter horizontally as it changes [inferred]. Contextual alternates are left on, because they adjust punctuation shapes depending on surrounding glyphs, which matters in an interface where punctuation sits next to mixed-case and numeric strings [verified, same URL]. Inter's own site does not carry an optical-size-to-tracking table, so the specific tracking values per optical size are unknown here and must be set by eye and recorded in the token file rather than cited.

Mathematics is set in the fonts KaTeX ships. KaTeX's font documentation describes the formats it ships, namely ttf, woff and woff2, and how to configure them, and the app loads the woff2 files only [verified, https://katex.org/docs/font]. The specific KaTeX family names and their derivation from Computer Modern were not on the page that loaded, so that lineage is unknown as a sourced claim and must be read out of the installed package before anyone asserts it in code comments or documentation. Latin Modern, STIX Two and Libertinus were not loaded either, so their metrics and glyph coverage are unknown and none of them is adopted as a reading face without a measurement pass.

The math and prose seam is accepted rather than hidden. The prose typeface and the mathematics typeface will never match, and pretending otherwise produces a worse result than designing around the mismatch, which is Chimero's point that some tensions in the medium are intrinsic and should be designed around rather than solved, his own example being that text and images do not scale the same way [verified, the principle, https://frankchimero.com/blog/2015/the-webs-grain/; the application to math type is inferred]. The practical rule is that inline and display mathematics is set one step above the surrounding prose on the type scale so that perceived x-heights read as equal [inferred, track 4]. Baseline alignment of inline KaTeX against Inter is checked per size step and corrected with a per-step vertical offset token; the required offsets are unknown until measured and belong in the token file, not in this document.

The type scale is fixed up front rather than picked per screen, which is Refactoring UI's instruction to define a scale in advance and to set line-height proportionally to size rather than as a constant [single-source, https://www.refactoringui.com/]. The specific numbers below are this project's choices and are not in any source.

| Token | Size | Line height | Optical size | Use |
|---|---|---|---|---|
| `type-display` | 32 px | 38 px | Inter Display | Screen title on onboarding and mock exam start only [inferred] |
| `type-title` | 24 px | 32 px | Inter Text | Page title, one per screen [inferred] |
| `type-heading` | 19 px | 28 px | Inter Text | Section heading inside a screen [inferred] |
| `type-body` | 16 px | 26 px | Inter Text | Prose, item stems, feedback [inferred] |
| `type-math-inline` | 18 px | 26 px | KaTeX | Mathematics inside body prose, one step up [inferred] |
| `type-math-display` | 21 px | 34 px | KaTeX | Displayed equations and the item's principal expression [inferred] |
| `type-label` | 14 px | 20 px | Inter Text | Field labels, metadata, part headers [inferred] |
| `type-caption` | 13 px | 18 px | Inter Text | Provenance, evidence tags, timestamps [inferred] |
| `type-mono` | 14 px | 22 px | system monospace | The raw LaTeX inspector and nothing else [inferred] |

Two sizes cross the WCAG large-text boundary and two do not, which is the only reason the table matters for contrast. WCAG 2.2 success criterion 1.4.3 requires 4.5:1 for normal text and 3:1 for large-scale text at Level AA, where large scale means at least 18 point or 14 point bold, which the Understanding document converts to roughly 24 px and 18.5 px using 1 pt = 1.333 px [verified, https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html]. So `type-display` and `type-title` may sit at 3:1 and everything else must hold 4.5:1, including `type-math-inline` at 18 px, which is below the 24 px threshold and is therefore normal text for contrast purposes even though it is larger than the body.

Measure is capped at 68 characters for prose and the reading column is a fixed width that simply stops rather than stretching, following the instruction to keep measure in a readable range and the observation that a fixed-width element that stops is often correct [single-source, both instructions, https://www.refactoringui.com/; the 68-character number is inferred]. Displayed mathematics is allowed to exceed the prose measure and scrolls horizontally inside its own container rather than forcing the page to scroll, because a long integrand must not shrink the prose column around it.

Every element except the page title mixes one emphasising property with one de-emphasising property, so large size pairs with light weight or bold weight pairs with small size and muted colour, and only the page title is loud on every axis at once [verified, Kennedy rule 5, https://www.learnui.design/blog/7-rules-for-creating-gorgeous-ui-part-2.html]. Kennedy names Satoshi, Metropolis, Source Sans and Figtree as safe free choices [verified, same URL]; none is adopted here, because Inter's optical sizes and tabular figures are documented features rather than guesses and this app's content is numeric and dense. That is the alternative rejected.

## Colour system

The palette is built in HSL with every shade predefined before any screen is designed, because the project will need far more greys and far more tints of the accent than seems reasonable at the start, and because washing colour out into near-white to chase a contrast ratio is a named failure mode rather than a solution [single-source, https://www.refactoringui.com/]. Token names and roles are fixed here; concrete values are not, with two exceptions noted below, because a hex value asserted in a planning document and never measured against a contrast checker is worse than no value at all.

Neutral ramp, nine steps, warm rather than pure grey, on a warm near-white ground rather than pure white [inferred, track 4 Anthropic-interface section, where the specific off-white value used by any existing product is unknown]:

- `surface-page`, the page ground. Warm near-white in the light theme.
- `surface-raised`, cards and the item container, one step from `surface-page`.
- `surface-sunken`, input wells and the answer field.
- `border-hairline`, used sparingly. Where a border would separate two regions, prefer a background-colour shift, a shadow, or more space, because using fewer borders is the stated rule [single-source, https://www.refactoringui.com/].
- `text-primary`, `text-secondary`, `text-muted`, `text-on-accent`.
- `focus-ring`, a single ring colour used for every keyboard focus outline.

Accent, one hue only, with the full tint ramp predefined:

- `accent-base`, the current focus, the primary button, the active queue item.
- `accent-tint-1` through `accent-tint-4`, backgrounds and accent borders. An accent border on an otherwise plain element is the cheap way to introduce colour [single-source, same URL].
- `accent-contrast-text`, a tint of the accent's own hue, never grey. Grey text on a coloured background goes muddy, and the correct move is a tint of the background hue itself [single-source, same URL]. This rule is absolute in this app: no grey on colour, anywhere, including on the correct and incorrect states below.

Semantic, exactly two beyond the accent:

- `state-correct` and its tint ramp.
- `state-incorrect` and its tint ramp.

Neither semantic colour is ever the only channel carrying its meaning. A correct answer also carries a check glyph and the word "Correct" in text; an incorrect answer also carries a cross glyph and the word "Not yet" in text. A colour-blind student must be able to read every state with the colour channel removed entirely, and the quickest test is to render the screen in greyscale and confirm nothing is lost [inferred, track 4 type and colour direction].

The dark theme is a separate set of HSL shades, not an inversion, with saturation reduced slightly at low lightness so colours do not vibrate [inferred from Refactoring UI's colour chapter, https://www.refactoringui.com/]. Token names are identical across themes; only the values differ. Both themes are checked independently against the contrast floors, because a ratio that passes in light does not pass in dark by construction.

Contrast floors, treated as floors rather than targets: 4.5:1 for anything at `type-body` and below, and 3:1 for `type-title` and `type-display`, per WCAG 2.2 SC 1.4.3 [verified, https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html]. Non-text contrast is handled by success criterion 1.4.11, referenced from that same page and applying to charts, diagrams and control boundaries; the specific ratio for 1.4.11 was not stated on the page that loaded, so it is unknown here and must be fetched before the mastery map's node borders and the calibration curve's axes are specified [verified that 1.4.11 is referenced, same URL]. Until it is fetched, the map and the curve hold 3:1 against their adjacent background as a working floor [inferred].

Two values are justified concretely rather than left open. First, elevation follows a single overhead light source, so inset controls such as text fields and the answer well get a darker top edge and outset controls such as raised buttons and popovers get a brighter top edge, because light from below reads as wrong to the eye [verified, Kennedy rule 1, https://www.learnui.design/blog/7-rules-for-creating-gorgeous-ui-part-1.html]. Second, no gradient appears anywhere, decorative or otherwise, because a gradient adds a visual variable that carries no information and wrecks text contrast at the ends of the ramp [inferred, track 4 anti-pattern list].

Monospace and colour intersect in exactly one place: the raw LaTeX inspector, which shows the student what they typed. It uses `text-secondary` on `surface-sunken` and no syntax colouring, because a calculus app has almost no code and a coloured token stream competes with mathematical symbols for the same visual channel [inferred, track 4].

## Spacing and layout

The spacing scale is fixed, with noticeably distinct steps so that any two adjacent values are obviously different, and it is used everywhere: 4, 8, 12, 16, 24, 32, 48, 64, 96 px. The instruction to use a fixed scale with distinct steps is stated; these nine values are this project's choice [single-source, the instruction, https://www.refactoringui.com/; the values are inferred].

Whitespace is started at too much and removed, rather than started tight and added [verified, same URL]. Kennedy's concrete calibrations are adopted directly and are the only spacing numbers in this document with a source: a 12 px label carries roughly its own height in padding above and below, roughly 15 px separates a title from its rule, roughly 25 px separates sections, and navigation text occupies roughly 20 percent of the bar height so that 80 percent is air [verified, https://www.learnui.design/blog/7-rules-for-creating-gorgeous-ui-part-1.html]. Those map onto the scale as 12 px label padding, 16 px title-to-rule, 24 px between sections and a 56 px top bar carrying 14 px text. Where Kennedy's number and the scale disagree, the scale wins and the deviation is recorded.

The reading column is fixed-width and simply stops. Grids are overrated and a fixed-width element that stops is often correct [single-source, https://www.refactoringui.com/], and the web's defining material property is edgelessness, so a layout that presumes a rectangle is fighting the material [verified, https://frankchimero.com/blog/2015/the-webs-grain/]. Practically the app has one column of content, centred, at the measure fixed in the type section, with a 16 px side gutter at phone width and no horizontal page scroll at any width.

One next action per screen. The primary action is the only `accent-base` button on the screen. Secondary actions are text buttons in `text-secondary`. Destructive actions are text buttons in `state-incorrect` and always carry a typed confirmation, never a single click.

There are no dashboards. A dashboard is a set of numbers that asks the student to decide what to do, which is the decision the app exists to make for them. The progress screen is not a dashboard: it is a single map with a single curve beneath it, reachable from home, and it never appears as the landing screen. The alternative rejected is the familiar tile grid of streak, accuracy, minutes and rank, which is rejected on learning impact (it converts study into a metric-optimisation game), not on cost.

Figures carry their labels and the relevant algebraic step inside the figure, never in a caption or a separate panel, and never requiring scrolling between the figure and the question, because integrated presentation beat split presentation at g = 0.63 across 58 independent comparisons with n = 2426 [verified, Schroeder and Cenkci 2018, https://link.springer.com/article/10.1007/s10648-018-9435-9]. This is a layout constraint before it is an illustration constraint: the item container must be tall enough to hold figure and stem together at the smallest supported viewport, and an item whose figure and stem cannot both fit is a content bug, not a rendering one.

Split attention also bounds feedback. Feedback appears in the representation of the item first, then at most one translation into a second representation, and never more than two representations on one feedback screen [decisions memo D4, inferred].

## Motion rules

Every animation runs under roughly 300 ms and uses ease-out, because ease-out starts fast and settles, which reads as the interface responding rather than the interface performing [verified, https://emilkowal.ski/ui/great-animations]. Only `transform` and `opacity` are animated, so the compositor can hold 60 fps on a school laptop [verified, same URL]. Every animation is interruptible: if the student submits the next answer while the previous result is still animating in, the new state takes over from wherever the old one is rather than queueing [verified, same URL].

Nothing triggered by a repeated keystroke is animated, because the animation becomes the bottleneck on frequently repeated keyboard-initiated actions [verified, same URL]. In this app that means symbol insertion in the MathLive field, moving between blanks in a completion problem, moving between questions in a timed part, marking for review, eliminating an option, and submitting an answer. All of those are instant. A student doing forty problems a day will not tolerate a palette click per symbol, so entry is keyboard-first, and every animation on that path is removed for the same reason [inferred, track 4 math input section].

Under `@media (prefers-reduced-motion: reduce)`, any translation or scale is replaced by an opacity cross-fade and the feedback itself is kept. The media feature has two values, `no-preference` and `reduce`, and the bare query `@media (prefers-reduced-motion)` is equivalent to the reduce case; MDN is explicit that the intent is to replace motion that can trigger vestibular symptoms, typically scaling or panning of large objects, with muted alternatives such as opacity cross-fades, while keeping animation that carries necessary UI feedback [verified, https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion]. Reduce means replace, not delete, and an implementation that ships `animation: none` under that query is wrong.

There is no entrance animation on page load, no staggered list reveal, no skeleton shimmer, and no number count-up on any score, accuracy, point total or mastery count [inferred, track 4 motion rules]. A count-up is a small celebration attached to a number, which is the completion-contingent reward pattern in miniature, and it also fights the tabular-figures decision by animating the exact horizontal jitter that tabular figures exist to prevent.

Material 3's numeric duration and easing tokens could not be loaded, so specific millisecond values and cubic-bezier curves from that system are unknown here and must be fetched rather than assumed if a token system is wanted. Apple's HIG motion page returned only a title, so Apple's specific wording is unknown too.

## Interface writing

Copy uses plain verbs in the student's voice rather than system voice. The app says "Start today's set", not "Initiate session"; "Check my answer", not "Submit response"; "Show me the next step", not "Request hint"; "I want to stop here", not "Terminate session" [inferred, track 4 Things and Craft section, where the specific copy conventions of those products are unknown as sourced claims].

Feedback is informational and never praise. What the screen after a correct answer says is what was demonstrated and what it unlocks; it awards nothing. The evidence is that positive verbal feedback ran at d = 0.33 on free-choice behaviour and d = 0.31 on self-reported interest, while engagement-contingent, completion-contingent and performance-contingent tangible rewards ran at d = -0.40, -0.36 and -0.28 on free-choice intrinsic motivation, with tangible rewards more damaging for children than for college students [single-source, Deci, Koestner and Ryan 1999, 128 experiments, https://home.ubalt.edu/tmitch/642/articles%20syllabus/Deci%20Koestner%20Ryan%20meta%20IM%20psy%20bull%2099.pdf]. A badge for completing a set is a completion-contingent tangible reward, which is the exact category at d = -0.36; informational feedback about what the student can now do is the category at d = +0.33. Those are opposite interventions that look similar on a screen, and the writing is where they are told apart.

Feedback on an error names the specific error and the rule violated, not just the right answer, because specific elaborated feedback beats verification-only feedback and feedback helps only when it provides correct-answer information the learner cannot already anticipate [verified, the elaborated-over-verification conclusion, Shute 2008, https://journals.sagepub.com/doi/10.3102/0034654307313795; single-source for the anticipation condition, Bangert-Drowns et al 1991, https://journals.sagepub.com/doi/10.3102/00346543061002213]. Feedback also names the scoring consequence, because the criterion task is an exam with a rubric.

No copy anywhere labels the output as machine-generated. No "AI-powered", no sparkle glyph, no robot icon. "AI-powered" describes the implementation rather than the benefit, and the student does not choose this product from a feature list; sparkle and robot iconography labels the output as machine-generated, which invites the student to trust or discount it wholesale rather than check it [inferred, track 4 anti-pattern list]. Where a score is provisional because two grading samples disagreed, the copy says so in plain words and offers the dispute path, which is a statement about confidence, not about provenance.

Good and bad copy, by screen:

| Context | Good | Bad |
|---|---|---|
| Home primary action | "Start today's set. About {queue.minutes} minutes in today's queue." | "Continue your learning journey" |
| Empty queue | "Nothing is due today. You can add a 15 minute practice set if you want one." | "Great job! You're all caught up! Come back tomorrow" |
| Correct answer | "Correct. That is the product rule applied with the factors kept in order. This was your third unaided success on three separate days, so this skill is now counted as mastered." | "Awesome work! +25 XP" |
| Incorrect answer | "Not yet. The numerator terms were reversed. The quotient rule is low times the derivative of high, minus high times the derivative of low. On an AP rubric a reversed numerator loses the quotient rule point even if the algebra afterwards is clean." | "Oops! That's not quite right. Try again!" |
| Confidence prompt | "Before you see the answer: guess, unsure, or confident?" | "Rate your confidence level" |
| Error note prompt | "In one line, what went wrong?" | "Reflect on your mistake to unlock your review card" |
| Mastery map node fading | "Chain rule with three layers. Last correct 11 days ago. Due for review." | "Chain rule: 67% complete" |
| Mock score | "Position against published distributions, with assumptions. Cut points are not published, so this is a band, not a score." | "Your predicted AP score: 4" |
| Provisional grade | "This point is provisional. Two gradings disagreed on whether the justification named the hypothesis. You can ask for it to be re-read." | "AI grading confidence: 78%" |
| Settings, claudebox | "Single operator only. Enabling this routes requests through your personal Claude subscription, which the consumer terms do not permit you to share or to reach by automated means. You alone carry that risk." | "Save money with subscription mode!" |

The tutor never produces the final answer during practice. That is a copy rule as much as a routing rule: the tutor's refusal is written as a next step the student can take, not as a refusal notice.

## Anti-pattern list

Each entry is banned outright. The reason is one line and the citation is the evidence it rests on.

- Gradients used as decoration. They add a second visual variable carrying no information and wreck text contrast at the ends of the ramp [inferred, track 4].
- Glassmorphism cards. Backdrop blur puts variable-luminance content behind text, which makes the WCAG 1.4.3 ratio unverifiable and non-deterministic [inferred from https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html].
- Icon feature grids. Marketing-page furniture that fills a daily tool with reminders of things the student already knows it does [inferred, track 4].
- Sparkle and robot iconography. It labels output as machine-generated, inviting wholesale trust or wholesale discount instead of checking [inferred, track 4].
- "AI-powered" copy. It describes the implementation rather than the benefit [inferred, track 4].
- Emoji in the interface. Rendering varies by platform, they carry unintended tone, and they compete with mathematical symbols for the same visual channel [inferred, track 4].
- Chat-first layout for tutoring. The unguarded chat condition scored 17 percent below control on the unassisted exam despite a 48 percent gain during assisted practice [single-source, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4895486].
- Confetti on a correct answer. A completion-contingent reward, the category at d = -0.36 for free-choice intrinsic motivation [single-source, https://home.ubalt.edu/tmitch/642/articles%20syllabus/Deci%20Koestner%20Ryan%20meta%20IM%20psy%20bull%2099.pdf].
- Streak-loss guilt notifications. Loss framing turns study into avoidance of punishment, and the day the streak breaks the reason to open the app goes with it [inferred, track 4; the compatible sourced finding is the undermining effect above].
- Infinite scroll. It removes the end of the session, and a study session needs a defined end so the student can stop having finished rather than stop having given up [inferred, track 4].
- Leaderboards and leagues. A 16-week two-course comparison with the same curriculum found lower motivation, satisfaction and empowerment over time in the gamified condition carrying a leaderboard and badges [single-source, Hanus and Fox 2015, https://www.researchgate.net/publication/265644737_Assessing_the_effects_of_gamification_in_the_classroom_A_longitudinal_study_on_intrinsic_motivation_social_comparison_satisfaction_effort_and_academic_performance]. Math Academy's leagues are exactly this mechanic, which is why that product is copied selectively rather than wholesale [verified that they run leagues, https://www.mathacademy.com/how-it-works].
- Percentage-complete bars on the mastery graph. A bar implies a finish line; retention decays, so the correct visual is a map that fades rather than a bar that fills [inferred, track 4].
- Text over photography. There should be no text over images anywhere in a mathematics tutor, which makes Kennedy's six named techniques for that problem irrelevant here [inferred; the six techniques are verified at https://www.learnui.design/blog/7-rules-for-creating-gorgeous-ui-part-2.html].
- Grey text on a coloured background. It goes muddy; the fix is a tint of the background's own hue [single-source, https://www.refactoringui.com/].
- Auto-generated review cards with no student input. Most of the value of spaced repetition in mathematics is in constructing the card, and decks shared without their construction context lose their meaning, so an app that generates cards from errors without the student is doing the low-value half [verified, the position, Nielsen, https://cognitivemedium.com/srs-mathematics; the product consequence is inferred].

## Information architecture

Six screens plus settings. The tree below lists each screen and its states.

```
app
├── onboarding
│   ├── account (passkey registration)
│   ├── implementation intention (one if-then plan, fixed time and place)
│   ├── diagnostic intro (what it is, why it stops early, no score at the end)
│   ├── diagnostic item (states: unanswered, answered, submitted)
│   └── diagnostic result (unit-level states, never a percentage)
├── home  [the daily landing screen]
│   ├── queue ready (due count in minutes, one primary action)
│   ├── queue empty (no due work; optional extra set offered, not pushed)
│   ├── session in progress (resume)
│   └── long gap (over 21 days: offers a re-diagnostic instead of the queue)
├── session  [the four blocks of 02's Session assembly, in order]
│   ├── block 1, due reviews (at most 5 items or 5 minutes of forecast)
│   ├── block 2, fringe learning (until 25 minutes of forecast, or the fringe empties)
│   │   └── item states: example | completion | unsupported
│   ├── block 3, interleaved mixed review (10 to 15 minutes of forecast)
│   ├── block 4, calibration prompts and one-line error notes
│   ├── item states: reading, working, confidence rating, submitted,
│   │                feedback (verification | elaborated), self-explanation prompt
│   ├── error note (one line, student-authored, before the retry is scheduled)
│   ├── no photo capture on this screen; capture lives in unit check,
│   │   part drill, mock and checkpoint only [R10]
│   └── session end (what was demonstrated, what is scheduled next, no score)
├── review
│   ├── queue (items requeued after correction, at a 1 to 2 day gap)
│   ├── hypercorrection lane (high-confidence errors, 1 day gap, served first)
│   ├── error notes (the student's own sentences, searchable, editable)
│   └── grading disputes (provisional points awaiting re-read)
├── progress
│   ├── mastery map (fading nodes over the prerequisite graph)
│   │   └── node states: not attempted, in progress, mastered, fading, gap
│   ├── calibration curve (confidence against accuracy, monthly)
│   ├── representation matrix (source representation by target representation)
│   └── checkpoint history (6-week released-material results)
├── mock
│   ├── setup (which form, which parts, paper or typed capture)
│   ├── part I-A ({part.count} questions, {part.minutes} minutes, calculator absent)
│   ├── part I-B ({part.count} questions, {part.minutes} minutes, calculator present)
│   ├── part II-A ({part.count} questions, {part.minutes} minutes, calculator present)
│   ├── part II-B ({part.count} questions, {part.minutes} minutes, calculator absent)
│   ├── capture (booklet print, photo upload, read-back confirm or correct)
│   ├── grading (per point, provisional where samples disagreed)
│   └── result (per-question means against published 2023 to 2025 means, band)
└── settings
    ├── providers (per role, with the claudebox guard)
    ├── budgets (per role, per day)
    ├── queue settings (daily minute target, exam date, desired retention)
    ├── accessibility (reduced motion, theme, math speech)
    └── data (export, purge, image retention)
```

Every `{part.count}`, `{part.minutes}` and `{days_to_exam}` above and in the wireframes below is a placeholder, not a value. The renderer reads part counts, part durations and the exam date from `research/exam/exam-structure.md`, which is the only file that owns them, and this brief never restates them [R22].

The daily loop is: home shows the due queue as a minute forecast and one primary action; the session runs the four blocks of 02's Session assembly, which are block 1 due reviews at at most 5 items or 5 minutes of forecast, block 2 fringe learning until 25 minutes of forecast are assembled or the fringe is exhausted, block 3 interleaved mixed review at 10 to 15 minutes of forecast, and block 4 calibration prompts with the one-line error notes; the session ends when all four blocks are empty, not when a timer expires [inferred throughout, R5 and track 1 session-length section, where the internal split and the 40 to 60 minute total are explicitly unsourced]. The minute figure is a forecast of the queue that has been assembled, never a schedule the student is held to, and the copy says so. Progress, review and mock are all reachable from home and none of them is ever the landing screen, because the landing screen's job is to remove a decision, not to offer one.

The mastery map lives on progress and nowhere else, because a map that also appears on home converts the landing screen into a dashboard. The calibration curve lives directly beneath the map on the same screen, since calibration is a property of the same mastery states the map draws. Error notes live on review, because they are working material the student returns to, not a record they admire. The review queue lives on review and is also the source of the session's block 1 due reviews, so the same items appear in two places by design and the count is stated once, in minutes, on home. Mock history lives on progress under checkpoint history, together with the 6-week released-material results, because both answer the same question, which is whether the internal numbers mean anything against the criterion. Settings is a single screen with five sections and is reachable only from the top bar.

## Wireframes

Each wireframe is followed by exactly one rationale sentence.

### Onboarding diagnostic

```
+--------------------------------------------------------------+
|  Calculus BC                                    [settings]    |
+--------------------------------------------------------------+
|                                                              |
|  Question 7 of at most 30                                    |
|  ------------------------------------------------            |
|                                                              |
|     lim   ( x^2 - 9 ) / ( x - 3 )                            |
|    x->3                                                      |
|                                                              |
|  Your answer                                                 |
|  +--------------------------------------------------+        |
|  |  [ MathLive field ]                              |        |
|  +--------------------------------------------------+        |
|  raw LaTeX: \frac{x^2-9}{x-3}                                |
|                                                              |
|  I have not learned this yet                                 |
|                                                              |
|                                   [ Check my answer ]        |
|                                                              |
|  This stops early once it has enough to place you.           |
|  There is no score at the end.                               |
+--------------------------------------------------------------+
```

The item count is capped and the copy promises early stopping because ALEKS caps its diagnostic at 30 questions and its measures barely move after question 10, so a longer diagnostic buys nothing and costs the student's first session [verified, https://www.aleks.com/about_aleks/Science_Behind_ALEKS.pdf].

### Home, today's queue

```
+--------------------------------------------------------------+
|  Calculus BC                                    [settings]    |
+--------------------------------------------------------------+
|                                                              |
|  Today                                                       |
|  ------------------------------------------------            |
|                                                              |
|  About {queue.minutes} minutes of work is in today's queue.  |
|                                                              |
|      12 skills due for review                                |
|       4 skills at your current frontier                      |
|       2 corrected items coming back                          |
|                                                              |
|                  [ Start today's set ]                       |
|                                                              |
|  ------------------------------------------------            |
|  Progress        Review        Mock exam                     |
|                                                              |
|  Exam: {exam.date}, {days_to_exam} days away                 |
+--------------------------------------------------------------+
```

The commitment is stated in minutes rather than items because a hard related-rates problem and an easy power-rule derivative are not the same unit, and Math Academy's own effort unit is roughly one minute of focused work [verified that their XP unit is about one minute, https://www.mathacademy.com/how-it-works]. `{queue.minutes}`, `{exam.date}` and `{days_to_exam}` are computed by the renderer, the last two from `research/exam/exam-structure.md` [single-source, research/exam/exam-structure.md], and the minute figure is a forecast of the assembled queue rather than a schedule, which is what the copy has to say: the queue ends when it ends [R5, R22].

### Session, item with fading stage

```
+--------------------------------------------------------------+
|  Set 1 of 3   *  item 4          stage: completion    [stop]  |
+--------------------------------------------------------------+
|                                                              |
|  Differentiate  f(x) = x^2 sin(x)                            |
|                                                              |
|  Worked so far                                                |
|   1. Name the factors:  u = x^2 ,  v = sin(x)   [given]      |
|   2. u' = 2x ,  v' = cos(x)                     [given]      |
|   3. Product rule:  f' = u'v + uv'              [given]      |
|   4. f'(x) = ______________________             [you]        |
|                                                              |
|  +--------------------------------------------------+        |
|  |  [ MathLive field, focused ]                     |        |
|  +--------------------------------------------------+        |
|                                                              |
|  Before you see the answer:                                  |
|     ( ) guess    ( ) unsure    ( ) confident                 |
|                                                              |
|                                   [ Check my answer ]        |
+--------------------------------------------------------------+
```

The last step is the blank and the earlier steps are given because backward fading, removing the last solution step first and earlier steps later, outperformed an abrupt switch from examples to problems [single-source, Renkl and Atkinson, https://link.springer.com/article/10.1023/B:TRUC.0000021815.74806.f6].

### Session, feedback state

```
+--------------------------------------------------------------+
|  Set 1 of 3   *  item 4          stage: completion    [stop]  |
+--------------------------------------------------------------+
|                                                              |
|  x  Not yet.                                                 |
|                                                              |
|  You wrote      f'(x) = 2x cos(x)                            |
|  The rule says  f'(x) = 2x sin(x) + x^2 cos(x)               |
|                                                              |
|  Each factor was differentiated separately and the two       |
|  derivatives were multiplied. The product rule differentiates|
|  one factor at a time and keeps the other whole, then adds   |
|  the two terms.                                              |
|                                                              |
|  On an AP rubric this loses the product rule point, and the  |
|  answer point with it.                                       |
|                                                              |
|  Which rule justifies step 3, and why does it apply here?    |
|  +--------------------------------------------------+        |
|  |                                                  |        |
|  +--------------------------------------------------+        |
|                                                              |
|  In one line, what went wrong?                               |
|  +--------------------------------------------------+        |
|  |                                                  |        |
|  +--------------------------------------------------+        |
|                                                              |
|  Coming back in 1 day.               [ Next item ]           |
+--------------------------------------------------------------+
```

Feedback names the rule violated and the scoring consequence rather than only the right answer because specific elaborated feedback beats verification-only feedback [verified, Shute 2008, https://journals.sagepub.com/doi/10.3102/0034654307313795].

### Review

```
+--------------------------------------------------------------+
|  Review                                         [settings]    |
+--------------------------------------------------------------+
|                                                              |
|  Coming back to you                                          |
|  ------------------------------------------------            |
|  today    Quotient rule, numerator order    (was confident)  |
|  today    Chain rule, three layers          (was confident)  |
|  tomorrow Implicit differentiation, dy/dx   (was unsure)     |
|  in 2 d   Limit by conjugate                (was unsure)     |
|                                                              |
|  My error notes                                              |
|  ------------------------------------------------            |
|  "I keep multiplying the two derivatives instead of          |
|   using the product rule."            2026-09-14   [edit]    |
|  "I forget the inner derivative when the inner function      |
|   is linear."                         2026-09-11   [edit]    |
|                                                              |
|  Provisional points                                          |
|  ------------------------------------------------            |
|  2026 Q3 part b, justification point   [ ask for re-read ]   |
+--------------------------------------------------------------+
```

High-confidence errors are listed first and scheduled at a 1 day gap because they are both the most persistent and the most correctable once corrected, which is the hypercorrection finding [single-source, Butterfield and Metcalfe, https://www.columbia.edu/cu/psychology/metcalfe/PDFs/ButterfieldMetcalfe2001.pdf; the effect size is unknown].

### Progress

```
+--------------------------------------------------------------+
|  Progress                                       [settings]    |
+--------------------------------------------------------------+
|                                                              |
|  What you can do, and how well it is holding                 |
|  ------------------------------------------------            |
|                                                              |
|   U1 limits        [##][##][##][# ][# ][  ][  ]              |
|   U2 derivatives   [##][##][# ][# ][  ][  ][  ]              |
|   U3 composites    [##][# ][  ][  ][  ][  ][  ]              |
|   U4 to U10        [  ][  ][  ][  ][  ][  ][  ]              |
|                                                              |
|   ## solid = mastered and fresh                              |
|   #  faded = mastered, retrievability falling, review due    |
|      empty = not yet demonstrated                            |
|      /     = prerequisite gap diagnosed below this node      |
|                                                              |
|  Calibration, last 30 days                                   |
|  ------------------------------------------------            |
|   accuracy                                                   |
|    1.0 |                          . ideal                    |
|        |                    .   o                            |
|    0.5 |              .   o                                  |
|        |        .  o                                         |
|    0.0 +----------------------------  confidence             |
|         guess     unsure    confident                        |
|   You are overconfident on "confident" by 18 points.         |
+--------------------------------------------------------------+
```

The map fades rather than filling a bar because retention decays and a bar implies a finish line, and the calibration curve sits beneath it because greater monitoring accuracy was associated with higher retention while overconfident learners stopped studying prematurely and retained less [verified, Dunlosky and Rawson 2012, https://www.sciencedirect.com/science/article/pii/S0959475211000685].

### Mock exam

```
+--------------------------------------------------------------+
|  Section I  Part B   {part.count} questions  [hide timer]     |
|  Question {item.index} of {section.count}   {time.remaining}  |
+--------------------------------------------------------------+
|                                                              |
|  CALCULATOR REQUIRED            [ graphing panel ]           |
|                                                              |
|  [stem, with highlight and notes available on selection]     |
|                                                              |
|   (A)  ...                                      [x]          |
|   (B)  ...                                      [x]          |
|   (C)  ...                                      [ ]          |
|   (D)  ...                                      [ ]          |
|                                                              |
|  [ ] mark for review        [ question menu ]  [ zoom ]      |
|                                                              |
|              [ back ]                    [ next ]            |
+--------------------------------------------------------------+
```

The tool set is a hideable timer with a five-minute alert, highlight and notes, mark for review, option eliminator, a question menu showing skipped and flagged questions, and zoom, with the graphing panel present only on calculator parts, because those are exactly the tools Bluebook documents and the built-in Desmos is available only for questions that allow calculator use [verified, https://bluebook.collegeboard.org/students/tools and https://apcentral.collegeboard.org/media/pdf/ap-hybrid-digital-exams-free-response-booklets-overview.pdf].

### Mock exam, no-calculator lockout and part boundary

```
+--------------------------------------------------------------+
|  Section II  Part B  {part.count} questions  [hide timer]     |
|  Question {item.index} of {section.count}   {time.remaining}  |
+--------------------------------------------------------------+
|                                                              |
|  NO CALCULATOR ALLOWED                                       |
|  There is no calculator on this part. It is not hidden.      |
|  It is not there.                                            |
|                                                              |
|  ------------------------------------------------            |
|  Part A is closed. You cannot return to its questions.       |
|  ------------------------------------------------            |
|                                                              |
|  [stem]                                                      |
|                                                              |
|  Write your answer in the booklet, {question.label}.         |
|                                                              |
|  [ print booklet page ]                                      |
|                                                              |
|              [ back to Q2 of this part ]      [ next ]       |
+--------------------------------------------------------------+
```

The calculator control is removed rather than merely disabled and the previous part is closed because every fidelity cue College Board documents is attached to a part boundary, and the no-calculator header is printed in the paper booklet as well as shown in Bluebook [verified, https://apcentral.collegeboard.org/media/pdf/ap-hybrid-digital-exams-free-response-booklets-overview.pdf].

### Mock exam, FRQ booklet and photo read-back

```
+--------------------------------------------------------------+
|  Free response capture              Question 3, parts a, b    |
+--------------------------------------------------------------+
|                                                              |
|  Your page                        What I read                |
|  +----------------------+         +------------------------+ |
|  |                      |         | (a)                    | |
|  |  [photo of the       |         |   dy/dx = (2x - y)     | |
|  |   booklet page,      |         |           / (x + 2y)   | |
|  |   boxed, unlined]    |         |                        | |
|  |                      |         | (b) At (1, 1):         | |
|  |                      |         |   dy/dx = 1/3          | |
|  +----------------------+         +------------------------+ |
|                                                              |
|  image check: sharp, page markers found, contrast ok         |
|                                                              |
|  Is this what you wrote?                                     |
|         [ yes, grade it ]      [ no, let me fix it ]         |
|                                                              |
|  Nothing is scored until you confirm this.                   |
+--------------------------------------------------------------+
```

The transcription is shown as a rendered read-back the student confirms or corrects before any point is graded because in the 2026 AIED handwriting study roughly 87 percent of the best model's remaining errors were transcription failures rather than rubric misapplication [single-source, https://arxiv.org/abs/2605.19043].

### Settings

```
+--------------------------------------------------------------+
|  Settings                                                     |
+--------------------------------------------------------------+
|  Providers                                                   |
|  ------------------------------------------------            |
|   tutor          Anthropic  claude-sonnet-5      [change]    |
|   generator      Anthropic  claude-opus-5        [change]    |
|   verifier       Anthropic  claude-opus-5        [change]    |
|   grader         Anthropic  claude-sonnet-5      [change]    |
|   diagnostician  Anthropic  claude-opus-5        [change]    |
|   transcriber    Anthropic  claude-haiku-4-5     [change]    |
|                                                              |
|   claudebox   [ off ]                                        |
|   Single operator only. Enabling this routes requests        |
|   through your personal Claude subscription. The consumer     |
|   terms say you may not share account credentials or make    |
|   your account available to anyone else, and may not reach   |
|   the Services by automated means except with an API key.    |
|   No streaming, so the tutor cannot run on it. Localhost     |
|   only. Refuses to start with more than one user record.     |
|   To enable, set CLAUDEBOX_SINGLE_OPERATOR=1 and type        |
|   ENABLE CLAUDEBOX SINGLE OPERATOR below.                    |
|   +----------------------------------------+                 |
|   |                                        |                 |
|   +----------------------------------------+                 |
|                                                              |
|  Budgets                                                     |
|  ------------------------------------------------            |
|   daily cap, all roles          $ [    ]                     |
|   per role caps                 [ open ]                     |
|   this month so far             $ 0.00                       |
|                                                              |
|  Data                                                        |
|  ------------------------------------------------            |
|   Export everything (JSON)               [ export ]          |
|   Delete my FRQ photos                   [ delete ]          |
|   Purge everything                       [ purge  ]          |
|   Default retention: until 30 days after 10 May 2027.        |
+--------------------------------------------------------------+
```

The acknowledgement string is "ENABLE CLAUDEBOX SINGLE OPERATOR" and 07-ai-provider-layer.md owns that copy; this brief shows where it appears and does not define it [R19]. The claudebox warning is typed rather than clicked and states the consumer-terms constraint in full because Anthropic's consumer terms say you may not share account login information, API key or account credentials with anyone else or make your account available to anyone else, and prohibit accessing the Services through automated or non-human means except via an API key [verified, https://www.anthropic.com/legal/consumer-terms].

## Accessibility

Keyboard-first is the primary interaction model, not a fallback. Every primary action has a keyboard binding, because a student doing forty problems a day will not tolerate a palette click per symbol and a daily user should stop reaching for the mouse by about week three [inferred, track 4 Linear and math-input sections]. The session path in particular is fully operable from the keyboard: enter the answer, rate confidence, submit, read feedback, write the error note, advance. Focus order follows reading order, focus is never trapped except inside a modal that can be dismissed with Escape, and the `focus-ring` token is visible against every surface in both themes.

Mathematics is exposed to screen readers rather than rendered as an image or as an opaque span. MathLive is described as screen-reader friendly with math-to-speech and ARIA labels, exports to LaTeX, MathML, ASCIIMath, Typst and MathJSON, and carries mobile virtual keyboards and physical keyboard shortcuts [verified, https://www.npmjs.com/package/mathlive and https://mathlive.io/mathfield/]. Note the conflict in the ledgers: track 4 records that the documentation site redirected and returned empty content in that session, so its feature list and licence were unknown there, while track 3 loaded the npm page and the mathfield page successfully. The npm and mathfield sources are the ones relied on here, and the licence must still be confirmed from the package before implementation. Rendered output uses KaTeX with MathML output enabled so that assistive technology reads structure rather than glyph soup; whether the installed KaTeX version emits MathML by default is unknown here and must be checked in the package.

Colour independence is enforced, not requested. Every state that uses `state-correct` or `state-incorrect` also carries a glyph and a word, and the greyscale render is part of the design review for every screen.

Reduced motion follows the rule in the motion section: replace, do not delete. A student who sets `prefers-reduced-motion: reduce` still sees the feedback state change, as a cross-fade.

Contrast holds 4.5:1 for body and below and 3:1 for the two large steps in both themes [verified, https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html]. The 1.4.11 non-text ratio is unknown here and must be fetched before the mastery map and calibration curve are finalised.

One accessibility fact about the exam itself constrains nothing in the app but belongs on the record: the CED states that accessible technology with the capabilities expected for AP Calculus is available for students who are blind or visually impaired, and that its use requires an accommodation request through College Board Services for Students with Disabilities [verified, research/exam/exam-structure.md, CED p.198].

## Traceability to 01 and 05

To 01-learning-model.md. Interleaving appears in the interface as the session's mixed review block and as the constraint that no more than 2 consecutive items share a primary skill, which is what the d = 0.83 classroom RCT tested [verified, Rohrer et al 2020, http://uweb.cas.usf.edu/~drohrer/pdfs/Rohrer_et_al_2020JEdPsych.pdf]. Spaced retrieval appears as the finite due-today queue on home, assembled as block 1 by 02's Session assembly, and as the fading mastery map on progress, which is the mechanic that replaces the streak [verified, the spacing basis, Adesope et al 2017 g = 0.51, https://journals.sagepub.com/doi/abs/10.3102/0034654316689306]. Mastery gating appears as the map's four node states and as the copy that never lets the student self-declare a skill done. Adaptive fading appears as the session item's three stages, example, completion and unsupported, shown in the item header. Feedback timing appears as two distinct feedback states, step-level verification in the example and completion stages and withheld elaborated feedback on unsupported and exam-shaped items. Confidence rating appears as the three-point control before feedback, and its consequence appears as the hypercorrection lane on review and as the calibration curve on progress. Self-explanation appears as exactly one structured prompt, attached to worked examples and corrected errors only and never to a routine correct answer in the unsupported stage, because the marginal problem is worth more than the prompt at that point [verified, Bisra et al 2018 g = 0.55, https://link.springer.com/article/10.1007/s10648-018-9434-x]. Split-attention-free figures appear as the layout constraint that a figure carries its labels and the relevant algebraic step inside itself [verified, g = 0.63, https://link.springer.com/article/10.1007/s10648-018-9435-9]. The implementation intention appears once, in onboarding [verified, d = 0.65, https://www.sciencedirect.com/science/chapter/bookseries/abs/pii/S0065260106380021].

To 05-assessment-modes.md. The mock screen implements the four part shapes exactly: 29 questions in 62 minutes with no calculator, 13 in 38 minutes with a calculator, 2 in 30 minutes with a calculator, 4 in 60 minutes with no calculator, 42 multiple-choice and 6 free-response questions in total, 9 points per free-response question, Section I and Section II each carrying 50 percent [verified, research/exam/exam-structure.md]. The part boundary is a hard boundary in the interface because calculator availability, the on-screen direction, the printed booklet header and the timer all attach to it. The FRQ capture screen implements the paper-first default, the booklet-shaped printable page, the photo capture, the image quality gate and the confirmed read-back. The result screen never shows a single predicted score: it shows per-question means against published 2023 to 2025 means and a band with its assumptions stated, because section weights are published while cut points are not and the 2027 form is new. Typed MathLive entry with MathJSON export is the secondary capture mode and the mode for short answers, and MathJSON rather than a LaTeX string is what the verifier consumes.

Open items this brief could not settle, carried to 12-open-questions.md: the Inter optical-size-to-tracking table, the KaTeX family names and their lineage, whether the installed KaTeX emits MathML by default, MathLive's licence, the WCAG 1.4.11 non-text contrast ratio, the specific inline-math baseline offsets per size step, whether AP Calculus BC receives a Bluebook reference sheet, and whether the Bluebook Desmos variant satisfies all four CED calculator capabilities.
