---
title: Desmos fluency, design
research_date: 2026-09-29
status: draft
purpose: The Desmos fluency feature as the student meets it: where it lives, the procedure cards, the drills, the measured view, the layouts, the offline state and the words, decided from docs/calculator/research/synthesis.md and the plan.
---

# Desmos fluency, design

On the two calculator parts the only calculator that counts is the Desmos graphing calculator built into Bluebook (research/exam/calculator-policy.md). This feature teaches the Desmos way to do everything the exam expects of a calculator, drills it against the clock, and carries the habits that ride on calculator work: radian mode checked first, the setup written beside the result, and a result reported to three decimal places, rounded or truncated. Fluency is measured and never credited: nothing here touches mastery, spacing or credit (docs/plan/15-lessons.md, Fluency, measured and never credited). Nothing here is a schedule, quota, target or goal; the student sees their own measured times and accuracy in the words the progress views already use, with denominators. The build follows [architecture.md](architecture.md) and [build-plan.md](build-plan.md); the evidence is in [research/synthesis.md](research/synthesis.md).

## Where it lives [inferred]

A Calculator destination in the top bar, sixth after Assessments, with the graph icon, at `#/calculator`. It has three sections in one page, the first two reached by the same route with a section id: Procedures (the cards), Drill, and Measured. The same destination is reachable from three places inside the work:

- every calculator-part item in a session shows, beside its Open Desmos control, a small text link "Calculator practice" that opens the procedure card for the capability the item's archetype most plausibly uses, or the card list when none is known;
- every calculator part of a timed part drill or a mock shows the same link on the part's setup screen and never inside the running part, because the running part reproduces Bluebook and Bluebook has no such link;
- every lesson whose worked example belongs to a calculator archetype shows the link at the end of that worked example.

Nothing is inserted into a session queue by this feature and nothing on Today mentions it. The student goes there when they want to.

## The procedure cards [inferred]

One card per technique, in this order, each on the evidence in research/desmos-technique.md:

| Card | What it teaches | Exam habit it carries |
|---|---|---|
| Check radians first | Open Graph Settings, read which of Radians and Degrees is selected, and the toggle shortcut | The 2025 stem's radian instruction; a degree-mode answer earns nothing |
| Define f(x) once | Type `f(x)=` once, reuse `f(...)` everywhere, the typing shortcuts for powers, roots, fractions and pi | Parentheses kept when substituting |
| Evaluate at a point | `f(3)` in a new line; a function table for several inputs | The value reported with the setup |
| Derivative at a point | `f'(a)` with the value in place of a; `d/dx` for the graph of the derivative | A calculator derivative shown with its setup |
| Definite integral | `int`, then lower bound, upper bound, integrand, `dx` | The integral written beside the value; three places |
| Average value | The integral divided by the interval length with `frac` | The division written, not only the integral |
| Zeros and f(x)=k | Points of interest in gray, hover and click for coordinates; `y=k` on a second line | A solution read from a point of interest, not a traced estimate |
| Intersection as a bound | The gray intersection point, Export Point to Expression List, the value in a bound | An intermediate value carried at full display precision |
| A window that shows the work | Graph Settings bounds, Zoom to Fit, a curly-bracket restriction | An interior zero or intersection not missed |
| Three places, rounded or truncated | What Desmos shows, what the reader accepts, how to write both the setup and the result | The one rounding point per question |

A card is one screen, top to bottom: the task in one sentence; the exact Desmos steps as a numbered list, each with its typed syntax or shortcut in a monospace span exactly as Desmos documents it; a demonstration, which is one worked instance shown as a step reveal in the lesson reader's own component (the function, each expression typed, what Desmos shows, the written setup, the three-place answer); the exam habit the card carries, in the reader's words from the library's error record, without the record's id; a Bluebook note when the College Board version changes anything; and a "Drill this" button that starts a drill of the card's capability. A card carries no reading time, no completion mark and no checkbox. Cards cite their sources in the record, never on the screen.

## The drills [inferred]

One task at a time. The drill screen has, from 1100px, the task on the left and the real Desmos open on the right; below that width the task, then Desmos, then the answer fields, stacked. Desmos is the College Board version of the graphing calculator (architecture.md, The Desmos frame), opened by the same Open Desmos control the items use, open by default on the drill screen from 1100px and on demand below it. The page never sees inside the frame.

The task is a sentence with the function and the interval or point, drawn fresh each time from a template (architecture.md, Drill templates), and never a stem from any released question. It states the unit when there is one and carries the radian note when the function is trigonometric, in the words the calculator items already use.

Two fields below the task. "Result, to three decimal places" is a plain text field that takes what the student would write on the page, so the three-place rule is checked on what was typed. "Setup, as you would write it on the page" is the math field the items use, so a setup is typed as an integral, a derivative at a point, an equation or a function value, not as Desmos keystrokes. One button, "Check". Enter in the result field also checks.

A clock runs from the moment the task appears, shown as minutes and seconds in the corner the timed drill uses for its timer, and it can be hidden with the same control and stays hidden across drills in this browser. Hidden or shown, the time is recorded. The clock is a measurement, so the screen never says whether the time was good.

After Check, the screen shows three things and nothing else:

- The result line: "Accurate to three places" or the reason it was not, in one sentence: "Give three decimal places" when fewer were typed, "Not the value Desmos gives for this setup" when the number is wrong, "Not a number" otherwise. Under it, both accepted forms: "Rounded 3.901, truncated 3.900", so the student sees that either would have earned the point.
- The setup line: "Setup shown and equivalent", or "Setup shown but not equivalent" with the expected setup rendered beneath, or "No setup shown", with the reader's own sentence for that error from the library record. An expression the check could not read says so and counts as neither.
- The time: "42 seconds" and, once per drill, the exam's own figure for the calculator multiple-choice part from research/exam/exam-structure.md in the words the timed drill uses: "The exam allows N seconds a question on Section I Part B." That is the exam's number, stated once, never a target.

Then two buttons: "Next" (same capability, a fresh draw) and "Change capability". A drill that is left unanswered is recorded as served and unanswered and is never counted in accuracy. There is no streak, no run of correct answers, no badge, no sound and no praise copy.

The capability chooser at the top of the Drill section lists the six drilled capabilities with the count of drills answered beside each in the form "12 answered", or "none yet": plot (a window set so an extreme value can be read from a point of interest), zeros (an x-intercept or f(x)=k), derivative at a point, definite integral, intersection as a bound, and value at a point. A drill can also be started from a card, which preselects its capability.

## The measured view [inferred]

The Measured section says what has been measured, per capability, in the words the progress views use and with the denominator on every figure:

| Capability | Answered | Accurate to three places | Setup shown | Setup equivalent | Median time |
|---|---|---|---|---|---|
| Definite integral | 14 | 12 of 14 | 13 of 14 | 11 of 14 | 38 seconds |
| Derivative at a point | 2 | 2 of 2 | 2 of 2 | 2 of 2 | not measured yet |

Median time reads "not measured yet" under three answered drills, as the progress views say "not measured yet" for retention. Below the table, one line with the exam's per-question figure for the calculator multiple-choice part, as above, and the free-response calculator part's per-question figure, both from exam-structure.md. Below that, the last twenty drills as a list: the capability, the task's function, the result verdict, the setup verdict and the time. No bar, no percent, no trend arrow, no comparison to other students, and no sentence that says whether any of it is enough.

The Progress destination's pace card does not change; it gains one text link, "Calculator", to this section, so the numbers live in one place.

## Keyboard [inferred]

The whole feature works from the keyboard. On a card, the steps are plain text and the demonstration's "Next step" is the lesson reader's button. On the drill screen the tab order is the capability chooser, the clock's hide control, the Open Desmos control, the Desmos frame (which takes focus and keeps it until Escape or Tab out, since it is another origin), the result field, the setup field, Check, and after checking, Next and Change capability. A skip link at the top of the drill screen, "Skip to the result field", jumps past the frame. Every verdict is announced through the same live region the items use for feedback, so a screen reader hears it without moving. Focus lands on the result line after Check and on the task after Next.

## Phone [inferred]

At 600px and below the sections stack, the top bar is the fixed bottom bar it already is, the clock sits in the page header rather than a corner, the frame opens on demand at full width and 60vh tall, and the result field sits directly under the frame so the student reads the value and types it without scrolling past the setup field. No sideways scroll at 375px.

## Reduced motion and dark mode [inferred]

Nothing moves. The step reveal is the lesson reader's, which is already reduced-motion safe, and the clock changes its text once a second, which is not motion. The verdict lines appear without transition. The page uses tokens throughout; the Desmos frame keeps Desmos's own colours, which are light, and the frame carries a hairline border so the light rectangle reads as a tool inside a dark page rather than a defect.

## When Desmos cannot load [inferred]

The frame cannot report a cross-origin failure, so the offline state is decided from the browser's connection state and from the existing offline notice: when the app knows it is offline, the drill screen replaces the frame with one sentence, "Desmos loads from the internet, so it needs a connection. A handheld calculator works for the drill; enter the result and the setup as before." The task, the fields and the checks work exactly as online, because the checks run on the server and the server is local. The drill row records which variant was open or that none was. When the connection returns, the frame comes back on the next drill.

## Words [inferred]

Every string the student reads is listed once in the client's calculator module so the checker and the vitest tests read the same words: "Calculator practice", "Procedures", "Drill", "Measured", "Result, to three decimal places", "Setup, as you would write it on the page", "Check", "Next", "Change capability", "Accurate to three places", "Give three decimal places", "Not the value Desmos gives for this setup", "Not a number", "Setup shown and equivalent", "Setup shown but not equivalent", "No setup shown", "The expression could not be read", "not measured yet", "answered", "none yet", "Hide the clock", "Show the clock", "Skip to the result field". None of them grades the student, promises anything about the exam, or sets a goal.
