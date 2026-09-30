---
title: Desmos Technique for Calculator Tasks
research_date: 2026-09-29
status: draft
purpose: For each calculator task the AP Calculus BC exam asks for, the documented Desmos route with its typed syntax and keystrokes, the pitfalls the cached sources support, and how the College Board version in Bluebook changes it.
---

# Desmos Technique for Calculator Tasks

## Scope and sources [verified]

The exam fact this file serves is the CED's calculator paragraph. A calculator for the exam is expected to plot a function "within an arbitrary viewing window", find zeros, and numerically calculate derivatives and definite integrals, and a free-response result from one of those capabilities needs its setup written beside the result (ced p.13). Use of other built-in features "require the mathematical steps necessary to produce the results" (ced p.13). Which parts allow a calculator is stated in research/exam/exam-structure.md and nowhere here. College Board states that for Calculus BC, Desmos is available only in the calculator-required parts (web-calc-policy p.1).

Tool facts come from Desmos's own documentation in the cache: the help articles, the keyboard shortcuts page, the user guide PDF and the two testing PDFs. Shortcuts below are given as Windows or ChromeOS first and Mac second, as desmos-graphing-shortcuts p.1 lists them. A technique appears here only if a cached page documents it. Where a step is a combination of documented steps, the section says so and carries `[inferred]`.

## What the College Board version changes [verified]

The College Board PDF, marked "Updated for SY2026-2027", lists two changes to the Graphing Calculator for the SAT and AP Exams. "Images, folders, and notes are disabled on your test", and the calculator "automatically checks Log mode when working with applicable exponential, logarithmic, and power regressions" (desmos-cb-calculators-pdf p.1). The same PDF lists AP Calculus AB and BC under the graphing calculator (desmos-cb-calculators-pdf p.1), and the Desmos FAQ lists "Precalculus, Calculus AB & BC" as having the Graphing Calculator (desmos-help-assessment-faq p.1).

The FAQ adds that on testing calculators "you can't import graphs, add images, log into your account, save or share links, or link to external resources" (desmos-help-assessment-faq p.1). The feature set is fixed once a year, so updates to desmos.com during the school year "don't usually appear on that year's tests" (desmos-help-assessment-faq p.1). Bluebook's own page says the Desmos calculator can be dragged anywhere on the screen (web-bluebook-tools p.1).

The FAQ also states the tool's limit, which governs every technique below. Desmos "is not considered a computer algebra system (CAS)", and students "must be able to analyze and interpret the outputs" (desmos-help-assessment-faq p.1). Every result in this file is a numerical value or a picture, never a symbolic answer.

Consequences for the techniques. The folder and note shortcuts (Ctrl+Alt+F, Ctrl+Alt+O) and the image shortcut do nothing useful in the College Board version, and the Save, Open and Share shortcuts are listed by Desmos under "Desmos.com Only" (desmos-graphing-shortcuts p.1). None of the techniques below depends on a disabled feature.

## College Board version as observed [single-source]

Observed in a browser on 2026-09-29: the College Board version of the graphing calculator at https://www.desmos.com/testing/collegeboard/graphing opened with Radians selected in Graph Settings. Its settings menu offered Radians and Degrees, Grid, Axis Numbers, Minor Gridlines, X-Axis and Y-Axis bounds with Step, Complex Mode, Reverse contrast and Braille Mode, and the expression list had no image, folder or note items. This is one observation of the practice page, not of Bluebook on exam day.

## Check the angle mode [verified]

Task: confirm radians before any trigonometric evaluation. The 2025 scoring guidelines carry the instruction "(Note: Your calculator should be in radian mode.)" (sg-25 p.2), and the 2023 guidelines state that an answer obtained in degree mode "does not earn the first point it would have otherwise earned" (sg-23 p.4). The library records this as BC-ERR-06032.

1. Press Ctrl+Alt+G (Mac Ctrl+Cmd+G) to open Graph Settings (desmos-graphing-shortcuts p.1).
2. Read which of Radians and Degrees is selected, and toggle if needed (desmos-help-graph-settings p.1, desmos-help-trigonometry p.1).
3. Alternatively press Alt+D (Mac Ctrl+D), listed as "Toggle Between Degrees and Radians" (desmos-graphing-shortcuts p.1). A toggle flips the state, so step 2's check still has to happen.

Pitfalls. The standard Graphing Calculator defaults to radians (desmos-help-faqs p.1), but "The testing calculator's default angle mode is often set to degrees rather than radians" (desmos-help-testing-calculators p.1), and the default testing calculator PDF states that it "defaults to degrees" (desmos-default-testing-pdf p.1). The College Board PDF does not list an angle-mode change (desmos-cb-calculators-pdf p.1), and the browser observation above found Radians. The default testing calculators are also offered in the Desmos Test Mode app (desmos-help-testing-calculators p.1), so a generic practice calculator and the College Board page can open in different modes.

## Define f(x) once and reuse it [verified]

Task: enter a given function once and use it for values, derivatives and integrals.

1. Type `f(x)=` followed by the expression, using `^` for exponents and `sqrt`, `pi`, `theta` and `frac` for their symbols (desmos-graphing-shortcuts p.1, desmos-help-functions p.1).
2. Reference it anywhere as `f(...)`. The Functions article states that once defined, a function can be used "in expressions or within other functions" (desmos-help-functions p.1).
3. Press Enter for a new expression line (desmos-user-guide-pdf p.13) or Ctrl+Alt+X (Mac Ctrl+Cmd+X) for "Add an Expression" (desmos-graphing-shortcuts p.1).

Pitfalls. Functions can use any letter except the special ones, which the user guide names as x, y, r, t and e (desmos-user-guide-pdf p.12). Any free variable prompts for a slider (desmos-help-sliders p.1), so a mistyped name yields a slider prompt. Parentheses matter when an expression is substituted, the error the library records as BC-ERR-99009 from Chief Reader reports (cr-23 p.30).

## Evaluate a function at a point [verified]

1. With `f` defined, type `f(3)` in a new line. The article's example evaluates to a number shown in the expression list (desmos-help-functions p.1, desmos-help-getting-started p.1).
2. For several inputs at once, use a function table (see the table section).

Two-variable functions work the same way, for example `g(10,3)` (desmos-help-functions p.1).

## Derivative at a point [verified]

Task: numerically calculate the derivative of a function at a point, one of the four CED capabilities.

1. Define `f(x)=...`.
2. Type `f'(a)` with the value in place of `a`. The apostrophe is the prime shortcut (desmos-graphing-shortcuts p.1), and the Derivatives article says to "Use prime notation to evaluate the derivative of a function at a given point" (desmos-help-derivatives p.1).
3. To graph the derivative instead, type `f'(x)` or `d/dx(f(x))` (desmos-help-derivatives p.1, desmos-help-supported-functions p.1). Higher derivatives are `f''(x)` and so on (desmos-help-derivatives p.1).
4. For a tangent line, the article gives `y=f'(a)(x-a)+f(a)` (desmos-help-derivatives p.1).

Pitfalls. "If the function is undifferentiable at given points, the result will be undefined" (desmos-help-derivatives p.1). Prime notation "is supported for functions of a single argument" (desmos-help-derivatives p.1). Higher-order derivatives "may be slow to graph or non-existent" for complex functions (desmos-help-derivatives p.1). The free-response setup is still required: the library records a calculator derivative reported without setup as BC-ERR-02031 (sg-25 p.4).

## Definite integral [verified]

Task: numerically calculate a definite integral, one of the four CED capabilities.

1. Type `int` in an expression line (desmos-help-integrals p.1). The shortcuts page lists `int` as the typed form of the integral template (desmos-graphing-shortcuts p.1).
2. Enter, in the order the article gives, "a lower bound, upper bound, integrand, and differential", the differential being `dx` (desmos-help-integrals p.1). The article does not name the key that moves between fields. The shortcuts page lists Tab as "Exit Current Block" and the arrow keys for moving between characters (desmos-graphing-shortcuts p.1).
3. With `f` defined, the integrand can be `f(x)` and the differential `dx`; the article's worked example evaluates the integral of a defined function from 0 to 3 (desmos-help-integrals p.1).
4. For an improper bound, type `infinity` or `infty` in either bound (desmos-help-integrals p.1).
5. To graph an accumulation function, put `x` in the upper bound, `0` in the lower bound, and integrate with respect to another variable (desmos-help-integrals p.1).

Pitfalls. "Divergent integrals will show as undefined" (desmos-help-integrals p.1). On paper the scoring guidelines award the setup point "with or without the differential" (sg-25 p.3), but the Desmos template asks for one (desmos-help-integrals p.1). A numerical answer with no integral written is BC-ERR-99021 and BC-ERR-08045 in the library (sg-25 p.3, crabbc-25 p.30).

## Average value [inferred]

Composite of documented steps. Type `int`, fill bounds, integrand and differential as above, then divide by the interval length, using `frac` for the fraction template (desmos-graphing-shortcuts p.1). The library's BC-ERR-06016 is the integral reported without that division (sg-25 p.3). No cached Desmos page describes average value as such.

## Find zeros and solve f(x)=k numerically [inferred]

No cached Desmos page documents a solve command. The documented mechanism is points of interest.

1. Graph `f(x)` and, for an equation `f(x)=k`, graph `y=k` in another line.
2. Select the curve on the graph or on its expression line. Points of interest appear in gray at intercepts, intersections, maximums and minimums (desmos-help-getting-started p.1, desmos-help-faqs p.1).
3. Hover to reveal the labeled coordinates, or click to keep the label on screen (desmos-help-getting-started p.1).
4. A zero is the x-coordinate of an x-intercept point of interest (desmos-help-getting-started p.1).

Pitfalls. The FAQ says coordinates are best seen when the expression is entered explicitly and "Coordinates are not displayed for parametric equations or in the 3D Calculator" (desmos-help-faqs p.1), which matters for BC parametric and polar tasks. A Chief Reader report notes responses that used a TRACE function and got "a solution that was not correct to three digits after the decimal" (cr-23 p.27); that report does not name Desmos, but the point of interest, not a dragged estimate, is the documented source of exact coordinates. The library records a missed interior intersection as BC-ERR-08025 (ced p.157).

## Intersection as a bound [inferred]

Composite of documented steps.

1. Graph both curves and find the intersection as a gray point of interest (desmos-help-getting-started p.1).
2. Click the point, then Export Point to Expression List, which adds it as a new expression line (desmos-help-getting-started p.1). Alternatively highlight the coordinate and copy and paste it with the keyboard (desmos-help-getting-started p.1).
3. Type `int` and enter the x-coordinate as a bound.

Pitfalls. Desmos states it shows "at least 5 decimal places for intersection points" (desmos-help-whats-new p.1). No cached page states how to reference the x-coordinate of an exported point inside another expression, so the documented route is copying or retyping the value, which carries the displayed digits only. Whether five or more displayed decimals are always enough to keep a later integral accurate to three places is not stated by any source. Rounding an intermediate value too early is BC-ERR-08005 in the library (sg-25 p.2, crabbc-25 p.30).

## Copy a point of interest into the expression list [verified]

1. Click the gray point of interest (desmos-help-getting-started p.1).
2. Choose Export Point to Expression List (desmos-help-getting-started p.1). Desmos introduced this for "intercepts, maximum and minimum values, or intersections" (desmos-help-whats-new p.1).
3. Or highlight the coordinate and copy with the keyboard (desmos-help-getting-started p.1).

Extreme values found this way are maximum and minimum points of interest (desmos-help-faqs p.1).

## Read and build a table of values [verified]

Task: tabulate a function, or enter a given table.

1. Add a table with Ctrl+Alt+T (Mac Ctrl+Cmd+T), by typing `table` in an expression line, or with Add Item then Table (desmos-graphing-shortcuts p.1, desmos-help-tables p.1, desmos-help-faqs p.1).
2. Type values into the cells and move with the arrow keys or Tab (desmos-help-tables p.1, desmos-graphing-shortcuts p.1).
3. For a function table, put a function of the first column in the second header, such as `f(x_1)`, and the column fills from the first (desmos-help-tables p.1). Subscripts use `_` (desmos-graphing-shortcuts p.1).
4. From an existing function line, open Edit List (Ctrl+Alt+D, Mac Ctrl+Option+D) and click Create Table (desmos-help-tables p.1, desmos-graphing-shortcuts p.1). The default inputs run from -2 to 2, and Return adds a row (desmos-help-getting-started p.1).
5. Use Zoom Fit to fit the view to the data (desmos-help-tables p.1).

Pitfalls. Create Table "isn't available for implicit expressions, parametric, and polar graphs" (desmos-help-tables p.1). Computed cells cannot be edited and show a gray background (desmos-help-tables p.1). Summing table values for a Riemann or trapezoidal sum is not one of the four CED capabilities, so its steps must be written out on paper (ced p.13). Regressions run from a table (desmos-help-tables p.1, desmos-help-regressions p.1) are also outside the four capabilities (ced p.13), and in the College Board version log mode is automatically checked for applicable regressions (desmos-cb-calculators-pdf p.1).

## Set a window with Graph Settings [verified]

Task: plot within an arbitrary viewing window, one of the four CED capabilities.

1. Press Ctrl+Alt+G (Mac Ctrl+Cmd+G) to open Graph Settings (desmos-graphing-shortcuts p.1).
2. Enter lower and upper bounds for the x- and y-axes (desmos-help-getting-started p.1, desmos-help-graph-settings p.1).
3. For trigonometric graphs, set Step to `pi` to label the axis in multiples of pi (desmos-help-graph-settings p.1, desmos-help-trigonometry p.1, desmos-user-guide-pdf p.7).
4. Shortcuts for the view: Zoom In Alt++ (Mac Ctrl++), Zoom Out Alt+- (Mac Ctrl+-), Restore Default Viewport Alt+0 (Mac Ctrl+0), Zoom to Fit Shift+Alt+Z (Mac Shift+Option+Z) (desmos-graphing-shortcuts p.1, desmos-help-graph-settings p.1).

The default viewport "is pre-defined depending on the size of your screen" (desmos-help-graph-settings p.1), so the default view differs between devices.

## Restrict a domain [verified]

1. Add curly brackets at the end of an expression, for example `y=x{-2<x<2}` (desmos-help-restrictions p.1, desmos-user-guide-pdf p.5).
2. Combine conditions with `and` or `or` inside the brackets (desmos-help-restrictions p.1).
3. For a piecewise function use the `{condition: value, default}` format (desmos-user-guide-pdf p.5).

Typing `<=` and `>=` gives the non-strict symbols (desmos-graphing-shortcuts p.1).

## Sliders [verified]

Sliders appear whenever an expression has a free variable (desmos-help-sliders p.1). The default interval is -10 to 10 in the Graphing Calculator, the ends are edited by clicking them, and a numerical step limits the values (desmos-help-sliders p.1). The point `(a,f(a))` with a slider moves along the curve (desmos-help-functions p.1, desmos-help-sliders p.1). Letters x, y, theta, r (when theta is present), i (in complex mode) and e cannot be sliders (desmos-help-sliders p.1). Slider values are keyboard-adjustable with the arrow keys, Page Up and Page Down, Home and End (desmos-graphing-shortcuts p.1). None of the four CED capabilities needs a slider; the use here is exploration and a moving point for reading values.

## Read a result to three decimals [verified]

Exam requirement: a decimal answer "should be accurate to three places after the decimal point" and may be "rounded or truncated" (sg-25 p.2, sg-25 p.3), with at most one point per question lost to rounding (sg-25 p.2). Chief Reader reports record answers given to too few places (crabbc-25 p.8, cr-22 p.3, cr-24 p.10), which the library holds as BC-ERR-99019 and BC-ERR-02032.

What Desmos documents about display.

1. Show Answer as Decimal or Fraction is Alt+Shift+A (Mac Cmd+Shift+A) (desmos-graphing-shortcuts p.1). The FAQ also describes a Convert button for turning a decimal answer into a fraction (desmos-help-faqs p.1).
2. Intersection points show at least 5 decimal places (desmos-help-whats-new p.1).
3. Regression template constants are rounded "to at least the lesser of 5 figures after the decimal point or 9 significant figures" (desmos-help-whats-new p.1).
4. A `round` function exists, with the example `round(1.3254, 2)` (desmos-help-supported-functions p.1).

The user guide PDF does not describe how a numeric result in the expression list is displayed or offer a precision setting (desmos-user-guide-pdf pp.1 to 13).

## Keyboard shortcuts for these techniques [verified]

All from desmos-graphing-shortcuts p.1.

| Action | Windows or ChromeOS | Mac |
|---|---|---|
| Toggle Between Degrees and Radians | Alt+D | Ctrl+D |
| Open or Close the Graph Settings Menu | Ctrl+Alt+G | Ctrl+Cmd+G |
| Zoom to Fit | Shift+Alt+Z | Shift+Option+Z |
| Restore Default Viewport | Alt+0 | Ctrl+0 |
| Show Answer as Decimal or Fraction | Alt+Shift+A | Cmd+Shift+A |
| Add an Expression | Ctrl+Alt+X | Ctrl+Cmd+X |
| Delete the Expression that has Keyboard Focus | Ctrl+Shift+D | Ctrl+Shift+D |
| Focus the Expression List | Ctrl+Alt+E | Ctrl+Cmd+E |
| Turn Edit List Mode On or Off | Ctrl+Alt+D | Ctrl+Option+D |
| Add a Table | Ctrl+Alt+T | Ctrl+Cmd+T |
| Undo | Ctrl+Z | Cmd+Z |

Typing shortcuts, identical on both systems: `^` superscript, `_` subscript, `'` prime, `sqrt`, `frac`, `pi`, `theta`, `int`, `sum`, `<=`, `>=`. The user guide PDF lists Ctrl+Y for redo (desmos-user-guide-pdf p.13) where the shortcuts page lists Ctrl+Shift+Z (desmos-graphing-shortcuts p.1). The two sources disagree and neither states which applies to the College Board version.

## Unresolved [uncertain]

- How many decimal places Desmos displays for an ordinary evaluation such as `f(3)`, `f'(a)` or an integral in the expression list. No cached page states it. Settled by a documented statement from Desmos, or by recording the display for a set of known values in the College Board version.
- Whether the keyboard shortcuts work identically inside Bluebook. The shortcuts page separates a "Desmos.com Only" group, which implies the rest apply elsewhere, but no cached source states it for Bluebook. Settled by testing each shortcut in the Bluebook practice app.
- How to reference the coordinates of an exported point inside another expression, which would remove retyping from the intersection-as-bound route. Not in any cached article.
- Whether the College Board version disables any functions by category, as the default testing calculator disables csc, sec, cot and others (desmos-default-testing-pdf p.1). The College Board PDF lists no such change (desmos-cb-calculators-pdf p.1), which suggests none, but absence from a list is not a statement. Settled by typing the functions in the College Board version.
- The angle mode Bluebook itself opens in on exam day. The only evidence is one browser observation of the practice page. Settled by the Bluebook practice app for Calculus BC.
- Whether points of interest outside the current viewing window are shown or listed, and whether a domain restriction limits which ones appear. No cached page states either.
- What log mode does to a regression. The Regressions article lists it only as a link (desmos-help-regressions p.1).
- Which key moves between the fields of the integral template. The Integrals article gives the order but not the key.

## Technique to exam task [inferred]

The right-hand column uses the generic kinds of calculator work named in exam-calculator-work.md. The mapping is a research judgment.

| Technique | Exam calculator work it serves |
|---|---|
| Define f(x) once and reuse it | every kind below that reuses a given function |
| Evaluate a function at a point | evaluate a function at a point |
| Derivative at a point, `f'(a)` | derivative at a point; tangent line value |
| Definite integral, `int` | definite integral of a rate; net change and accumulation; area, volume and arc length setups entered as integrals |
| Accumulation function graph | solve f(x)=k numerically when f is defined by an integral |
| Average value | average value |
| Points of interest (zeros, intersections, extrema) | solve f(x)=k numerically; find zeros; locate extrema candidates |
| Intersection as a bound | intersection as a bound |
| Copy a point of interest | intersection as a bound; reuse of a solved value |
| Table of values | read or extend a table of values; checking values of a defined function |
| Window with Graph Settings | plot in a window, and a prerequisite for seeing any point of interest |
| Restrict a domain | graph on a stated interval; isolate one branch or region |
| Angle mode check | any trigonometric evaluation, derivative or integral |
| Read a result to three decimals | every numerical free-response answer |
