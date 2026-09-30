---
title: The Bluebook Desmos Calculator for AP Calculus BC
research_date: 2026-09-29
status: draft
purpose: Which Desmos calculator Bluebook ships for AP Calculus BC, what it can and cannot do against the CED capability list, how it differs from desmos.com, when it is available, how it is practised, what the cached pages settle among the open calculator questions, and the facts about the Desmos API and its terms that bear on embedding.
---

# The Bluebook Desmos Calculator for AP Calculus BC

Every fact below is cited to a page of the local cache as `doc-id p.N`. Web pages and help articles are one page each. Where a fact rests only on a browser observation or on nothing at all, the section says so.

## Which calculator Bluebook ships for Calculus BC [verified]

Three cached sources agree that AP Calculus BC gets the Desmos graphing calculator and no other Desmos calculator.

The AP Students calculator policy table lists, for Calculus BC, "Built-in Desmos graphing calculator through Bluebook" beside "Graphing calculator" as the type allowed (web-calc-policy p.1). The AP Central version of the same table carries the same row (web-calc-policy-central p.1). The Desmos Assessment Resources FAQ answers which calculator each AP Exam gets and lists "Precalculus, Calculus AB & BC" with "Graphing Calculator" only, while listing two calculators for Chemistry and for the Physics exams (desmos-help-assessment-faq p.1).

The College Board Desmos PDF, a one-page document from Desmos marked "Updated for SY2026-2027", has a "Find Your Testing Calculator" grid with a row for "AP Precalculus, Calculus AB & BC" (desmos-cb-calculators-pdf p.1). In the rendered page that row carries a check only in the Graphing column. The check marks are drawing objects and do not survive into the cached text layer, so this reading of the grid is from the rendered PDF, and the FAQ and the two policy pages are the text-level confirmation.

Because the Calculus row has no Scientific check, the PDF's sentence that exams with both Scientific and Graphing calculators allow toggling between them (desmos-cb-calculators-pdf p.1) does not apply to Calculus BC.

## How the College Board version differs from desmos.com [verified]

The PDF opens by saying the exam calculators "may differ from what's available for free on desmos.com" (desmos-cb-calculators-pdf p.1). For the Graphing Calculator it lists exactly two differences.

| Feature | College Board version | Source |
|---|---|---|
| Images, folders, and notes | "Images, folders, and notes are disabled on your test." | desmos-cb-calculators-pdf p.1 |
| Log mode for regressions | "The calculator on your test automatically checks Log mode when working with applicable exponential, logarithmic, and power regressions." | desmos-cb-calculators-pdf p.1 |

It states that the Four-Function and Scientific calculators do not differ from desmos.com (desmos-cb-calculators-pdf p.1). The PDF names no disabled function categories, no change of default angle mode, and no removed calculus notation for the Graphing Calculator.

The contrast with the Desmos default testing configuration is informative. The default testing PDF, also marked for SY2026-2027, disables named trig, hyperbolic, statistics and geometry functions, disables tone, and sets the default angle mode to degrees (desmos-default-testing-pdf p.1). None of those changes appears in the College Board PDF. The Practice With Testing Calculators article describes the same pattern in general terms: testing calculators often disable images, folders, notes and links, often default to degrees, and often disable groups of functions by category (desmos-help-testing-calculators p.1).

The Assessment Resources FAQ adds that testing calculators in general may exclude features such as importing graphs, adding images, logging in, saving or sharing links, and linking to external resources (desmos-help-assessment-faq p.1). That answer is about testing calculators as a class and does not name the College Board configuration.

On timing, Desmos says test creators typically decide enabled and disabled features once a year in the summer, so desmos.com updates during a school year "don't usually appear on that year's tests" (desmos-help-assessment-faq p.1), and the per-assessment PDFs are usually updated once a year over the summer (desmos-help-testing-calculators p.1).

## What the College Board version showed in a browser [single-source]

Observed in a browser on 2026-09-29, and not in any cached source. The College Board version of the Desmos graphing calculator at https://www.desmos.com/testing/collegeboard/graphing opened with Radians selected in its Graph Settings. Its settings menu offered Radians and Degrees, Grid, Axis Numbers, Minor Gridlines, X-Axis and Y-Axis bounds with Step, Complex Mode, Reverse contrast and Braille Mode. The expression list had no image, folder or note items.

The missing image, folder and note items match the PDF's stated difference. The Radians selection matches the PDF's silence on angle mode, since the desmos.com default is radians (desmos-default-testing-pdf p.1 describes its own degrees default as "rather than radians like on desmos.com"). This page is the practice URL for the College Board version. The Desmos Testing page lists a Graphing Calculator labelled College Board Version under the SAT Suite and AP Exams heading (desmos-testing p.1), but the URL string itself is not in the cached page text.

## The four CED capabilities in the Desmos articles [verified]

The CED expects a graphing calculator appropriate for the AP Exam to have four built-in capabilities: plot the graph of a function within an arbitrary viewing window, find the zeros of functions (solve equations numerically), numerically calculate the derivative of a function, and numerically calculate the value of a definite integral (ced p.13). The table maps each to what the Desmos help articles describe for the standard Graphing Calculator.

| CED capability | What the Desmos article describes | Source |
|---|---|---|
| Plot in an arbitrary window | Zoom in and out, a default viewport, and adjusting "the domain and range of the viewport manually" through Graph Settings, plus a Lock Viewport option | desmos-help-graph-settings p.1 |
| Find zeros | No named zero or solve command appears in the cached articles. Selecting a curve shows gray points of interest at intercepts, intersection points, maximums and minimums, and clicking one displays its coordinates. Two graphed functions show their points of intersection | desmos-help-faqs p.1, desmos-help-getting-started p.1 |
| Numerical derivative at a point | "Use prime notation to evaluate the derivative of a function at a given point." A derivative that evaluates to a constant is shown in the expression list. An undifferentiable point gives undefined | desmos-help-derivatives p.1 |
| Numerical definite integral | Type int, enter lower bound, upper bound, integrand and differential. The worked example evaluates to a decimal number. Convergent improper integrals evaluate, divergent ones show as undefined | desmos-help-integrals p.1 |

The derivatives article also opens by saying you can "evaluate numerical derivative values directly" (desmos-help-derivatives p.1). The FAQ adds a limit on points of interest: "Coordinates are not displayed for parametric equations" (desmos-help-faqs p.1). Zero finding in Desmos is therefore a graphical route, reading an x-intercept or the intersection of two curves, and the articles do not describe a typed command that returns a root as a number.

## Other features a Calculus BC student meets [verified]

Points of interest can be exported. Clicking one offers Export Point to Expression List, and the coordinates can be copied (desmos-help-getting-started p.1).

Function definition and evaluation work in the expression list. Defining f(x) and entering f at a number evaluates it, functions of more than one variable evaluate, and a defined function can be used inside other expressions (desmos-help-functions p.1, desmos-help-getting-started p.1).

Tables accept typed or pasted data, can be generated from a function through Create Table, fill a column computed from a function in its header, and can drive a regression through Add Regression (desmos-help-tables p.1). Create Table is not available for implicit, parametric and polar graphs (desmos-help-tables p.1).

Restrictions use curly brackets after an expression to limit the domain or range, and several inequality restrictions can be combined with and or or (desmos-help-restrictions p.1).

Sliders appear whenever an expression has free variables, have an adjustable interval and step, animate, and can move a point along a function as (a, f(a)) (desmos-help-sliders p.1). The letters x, y, θ, r (with θ present), i (in complex mode) and e cannot be sliders (desmos-help-sliders p.1).

Regressions come from templates below a table or as custom models written with a tilde, and fitted parameters are stored in variables for later use (desmos-help-regressions p.1). The College Board version changes one regression behaviour, the automatic Log mode stated in the PDF (desmos-cb-calculators-pdf p.1).

None of these features is named as disabled in the College Board PDF. The CED rule is that use of built-in features beyond the four listed capabilities requires the mathematical steps that produce the results (ced p.13), which bears on how a table, slider or regression result could be reported on a free-response part.

## Degree and radian mode [verified]

Graph Settings toggles between Radians and Degrees (desmos-help-graph-settings p.1, desmos-help-trigonometry p.1). The desmos.com default is radians, as the default testing PDF states when it describes its own degrees default (desmos-default-testing-pdf p.1). The Practice With Testing Calculators article says a testing calculator's default angle mode "is often set to degrees rather than radians" (desmos-help-testing-calculators p.1). The College Board PDF lists no angle mode change (desmos-cb-calculators-pdf p.1), and the browser observation above found Radians selected. The mode remains a user setting in the College Board version on that observation, so the default is a starting state and not a guarantee of the state a student leaves it in.

## Precision and display of results [verified]

The cached Desmos pages say the following about how numbers are shown.

| Topic | Statement | Source |
|---|---|---|
| Intersection points | Since July 2024, Desmos shows "at least 5 decimal places for intersection points" | desmos-help-whats-new p.1 |
| Regression constants | Since November 2024, template constants are rounded to at least the lesser of 5 figures after the decimal point or 9 significant figures | desmos-help-whats-new p.1 |
| Decimal and fraction | An answer can be converted from decimal to fraction, and a keyboard shortcut toggles "Show Answer as Decimal or Fraction" | desmos-help-faqs p.1, desmos-graphing-shortcuts p.1 |
| Rounding function | round(value, places) rounds to a given place value | desmos-help-supported-functions p.1 |

The API documentation describes the decimal and fraction toggle as available when Desmos "detects a good rational approximation" (desmos-api-docs p.1). The scoring guidelines require decimal approximations accurate to three places after the decimal point (sg-25 p.2), and the CED names rounding as a practice skill (ced p.17). A display of at least five decimals for intersections exceeds three, so the reported digits are the student's rounding or truncation step. How many digits a general evaluation line (a derivative or integral value) displays is not stated in any cached page.

## Desmos is not a CAS [verified]

The Assessment Resources FAQ answers the question directly. "Desmos is not considered a computer algebra system (CAS)", which it describes as "recognized by its ability to solve equations algebraically, simplify expressions, and perform exact arithmetic without rounding or truncating decimals" (desmos-help-assessment-faq p.1). The same answer adds that students must analyze and interpret the outputs. The approved handheld list, by contrast, includes CAS models such as the TI-Nspire CX II CAS marked with the asterisk for the expected Calculus capabilities (web-calc-policy p.1).

## When the calculator is available [verified]

The student calculator policy page says "For Calculus AB, Calculus BC, and Precalculus, Desmos calculators will only be available in the calculator-required parts of the exam" (web-calc-policy p.1). The AP Central page carries the same sentence as a note (web-calc-policy-central p.1). The free-response booklet overview says the built-in Desmos graphing calculator in Bluebook "is only available for questions that allow calculator use" (hybrid-booklets-2026 p.6).

Per research/exam/exam-structure.md, the calculator-required parts are Section I Part B (13 questions, 38 minutes) and Section II Part A (2 questions, 30 minutes), and the no-calculator parts are Section I Part A and Section II Part B. The policy table marks the graphing calculator "Required for Part B" of Section I and "Required for Part A" of Section II for Calculus BC (web-calc-policy p.1).

## The handheld allowance and the built-in calculator [verified]

Both College Board policy pages state that the built-in calculator sits outside the count of two. The student page reads "In addition to the Desmos built-in calculator through Bluebook, you can bring up to 2 permitted handheld calculators to the exam" (web-calc-policy p.1). The AP Central page uses the same construction for students (web-calc-policy-central p.1). Both pages open by saying students can use "an approved handheld calculator and/or the Desmos built-in calculator" (web-calc-policy p.1, web-calc-policy-central p.1).

Both pages also restrict which Desmos counts. "Only the built-in Desmos calculator through Bluebook can be used during an AP Exam, not the web-based or app-based calculator" (web-calc-policy p.1, web-calc-policy-central p.1). The Desmos FAQ agrees that handhelds may be used "instead of or in addition to Desmos calculators" (desmos-help-assessment-faq p.1).

## The Bluebook tools page [verified]

The Bluebook testing tools page describes the calculator in two sentences. On the SAT, PSAT-related assessments and certain AP Exams "you'll have access to a Desmos calculator", and "You can drag it anywhere on the screen" (web-bluebook-tools p.1). The page does not name the variant per exam and does not describe calculator features.

## Practice routes [verified]

Desmos names three places to practise with a testing configuration. The Testing page carries per-assessment calculators and lists College Board versions of the four-function, scientific and graphing calculators under the SAT Suite and AP Exams, with a link to the College Board PDF (desmos-testing p.1). The Desmos Test Mode app, on Chromebooks in Kiosk Mode, Android and iOS, offers Choose Assessment to select "the exact calculator you'll encounter on your exam", and the assessment must be selected each time the app opens (desmos-help-testing-calculators p.1). The FAQ says the app allows offline practice (desmos-help-assessment-faq p.1), and the Chromebook route has moved to a progressive web app (desmos-help-whats-new p.1, desmos-help-in-class-assessments p.1). The FAQ also points to practising in Bluebook itself (desmos-help-assessment-faq p.1), and the January 2025 What's New entry says the Graphing Calculator is built into practice tests in Bluebook (desmos-help-whats-new p.1).

## The four capabilities in the Bluebook variant, as an inference [inferred]

No cached page says in one sentence that the Bluebook graphing calculator meets the four CED capabilities. The chain that supports that conclusion is this.

1. Calculus BC gets the Desmos Graphing Calculator (web-calc-policy p.1, desmos-help-assessment-faq p.1, desmos-cb-calculators-pdf p.1).
2. The College Board PDF, for SY2026-2027, lists the only Graphing Calculator differences from desmos.com as disabled images, folders and notes and automatic Log mode for certain regressions (desmos-cb-calculators-pdf p.1).
3. On desmos.com, the definite integral evaluates to a number (desmos-help-integrals p.1), prime notation evaluates a derivative at a point (desmos-help-derivatives p.1), the viewport's domain and range can be set manually (desmos-help-graph-settings p.1), and points of interest give coordinates of intercepts and intersections (desmos-help-faqs p.1, desmos-help-getting-started p.1).
4. None of the features in step 3 is on the list in step 2, so they are present in the College Board version.

The weakest link is step 4, because it reads a list of differences as exhaustive. The PDF presents its table as the differences and does not say "only", and the default testing PDF shows Desmos naming disabled function categories explicitly when it disables them (desmos-default-testing-pdf p.1), which supports the exhaustive reading. The browser observation of X-Axis and Y-Axis bounds in the College Board version is direct but single-source support for the window capability. A second qualification concerns zeros. Desmos meets "find the zeros" through points of interest on a graph, not through a solve command, and whether the CED's "solve equations numerically" is satisfied in the form the CED means is a reading of the CED that no cached page makes. The step 4 conclusion also holds for SY2026-2027 only. That the May 2027 administration falls in that school year is an inference from the date in research/exam/exam-structure.md.

## What this settles [inferred]

| Open question | Settled by the cache? | Citation | What remains open |
|---|---|---|---|
| docs/plan/12-open-questions.md: which Desmos variant Bluebook ships for Calculus | Yes | web-calc-policy p.1, web-calc-policy-central p.1, desmos-help-assessment-faq p.1, desmos-cb-calculators-pdf p.1 | Nothing for SY2026-2027. A later PDF could change the configuration |
| docs/plan/12-open-questions.md: whether it satisfies all four CED capabilities | Supported by inference, not stated | chain above | A College Board or Desmos sentence saying so, or a Bluebook AP Calculus practice test showing integral, derivative and zero evaluation in the calculator part |
| calculator-policy.md Unresolved: current approved model list | Yes at the page level. The list is now cached with asterisks marking models with the expected Calculus capabilities | web-calc-policy p.1, web-calc-policy-central p.1 | Both pages say the list will be updated, so a re-fetch before May 2027 is the check |
| calculator-policy.md Unresolved: whether Bluebook Desmos satisfies the four capabilities | As the second row | as above | as above |
| calculator-policy.md Unresolved: whether the two-handheld allowance counts the built-in Desmos | Yes. It sits outside the two | web-calc-policy p.1, web-calc-policy-central p.1 | Nothing |

The plan's product decision, a panel of its own with the four capabilities and a mode indicator, is described in docs/plan/12-open-questions.md and is not revisited here. The facts above bear on it in two places. The Bluebook variant is a full graphing Desmos apart from the listed differences, which is the case the plan describes as the panel being under-featured (no sliders, tables or regressions). And the College Board version starts in radians on the browser observation.

## The Desmos API and its terms [verified]

These are the facts for the embedding decision. No decision is made here.

Embedding. The API documentation's first step is a script tag loading calculator.js from www.desmos.com with an apiKey parameter, and "To obtain your own API key, visit desmos.com/my-api" (desmos-api-docs p.1). The API Keys section says "you must supply an API key as a URL parameter" (desmos-api-docs p.1). Partners may self-host or load from desmos.com (desmos-api-docs p.1).

State and events. getState "Returns a javascript object representing the current state of the calculator", for use with setState to save and restore, and it may be serialized with JSON.stringify (desmos-api-docs p.1). The documentation warns "Calculator states should be treated as opaque values" (desmos-api-docs p.1). setState resets the calculator to a saved state, with an options object (desmos-api-docs p.1). observeEvent('change') fires on any change that affects the persisted state, whether from the user or an API call, and passes an event with a boolean isUserInitiated (desmos-api-docs p.1). The documentation also describes expressionAnalysis, an observable object giving per expression whether it errors and its numeric evaluation, and HelperExpression objects whose numericValue updates as the expression changes (desmos-api-docs p.1). Configuration options include images, folders, notes, links and degreeMode (desmos-api-docs p.1), which are the settings a College Board style configuration would touch.

Plans. The API Plans article says Basic integration "includes the functionality to match the calculator versions used on the digital SAT, ACT, and AP Exams", and that Basic "doesn't include saving and loading graphs, generating screenshots, or lower-level API methods for programmatically generating graphs" (desmos-help-api-plans p.1). The Starter plan is Desmos-hosted only (desmos-help-api-plans p.1).

API terms, operative clauses (API Terms of Service version 1.0, updated July 11, 2025, desmos-api-terms p.1):

| Clause | Quote |
|---|---|
| Trial Tier limit 2(a) | "solely for (a) personal, non-commercial use or (b) a 90 day trial for internal testing to evaluate in preparation for commercial use" |
| Commercial use defined, 2(a) | "Commercial use includes any use of the API in an Application that is accessed by End Users in production" |
| Before leaving the Trial Tier, 3(a) | upgrade to a paid plan or enter a written Commercial Addendum, described in the clause |
| Branding, 5(b)(iii) | "remove, alter, or obscure any branding (including copyright and trademark notices) of Desmos Studio" is prohibited |
| Trademarks | "You may not use the Marks in marketing or promotional materials without our express prior written consent." |
| Trial termination, 9(a) | Desmos may terminate or discontinue Trial Tier access "for any reason and at any time without liability" |

desmos.com Terms of Service, last modified July 15, 2026 (desmos-terms p.1). The Desmos Tools include the web-based Desmos Graphing Calculator. Section 5 reads "You agree to use the Desmos Tools only (a) as an end user, for your personal, non-commercial use" or, as a School, for academic use in individual classes, and "You may not frame or mirror the Desmos Tools without our prior consent" (desmos-terms p.1). The same section says Desmos permits commercial integration "pursuant to a separate written agreement" (desmos-terms p.1).

## Not established by any cached source [uncertain]

- How many digits a derivative or integral evaluation line displays, and whether that differs from intersection points. Settled by a Desmos article on evaluation display, or by the College Board practice calculator.
- The numerical method and error behaviour behind Desmos derivative and integral values, and whether an evaluation can silently lose accuracy near a singularity. Settled by Desmos documentation of its numerical methods.
- Whether points of interest are shown for every function a Calculus item uses, apart from the stated parametric exclusion. Settled by a Desmos statement or the practice calculator.
- Whether the College Board configuration disables anything the PDF does not list. Settled by a statement that the PDF list is complete, or by feature-by-feature use of the practice calculator.
- Whether the angle mode a student sets persists between questions or between the two calculator parts in Bluebook. Settled by a Bluebook AP Calculus practice test.
- Whether the Bluebook calculator keeps expressions across questions within a part. Settled by a Bluebook AP Calculus practice test.
- Whether the College Board practice URL is the same build Bluebook embeds. The Practice With Testing Calculators article says the Testing page and Test Mode app calculators are "configured to match what test takers will encounter on their exams" (desmos-help-testing-calculators p.1), but no College Board page says so.
- Which terms govern an unkeyed embedding or framing of the College Board testing page as opposed to the API. The terms quoted above address the Desmos Tools and the API, and neither names the testing pages.
