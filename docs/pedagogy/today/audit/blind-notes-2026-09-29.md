---
title: Blind re-solve notes for the Today audit sample
research_date: 2026-09-29
status: draft
purpose: Stem problems and statement-item choices from a stems-only re-solve of the 72-item sample
---

# Blind re-solve notes

Source read: var/today-redesign/audit-sample-stems.json only. No record, key or worked solution was opened. One exposure to report: while reading content/items_p1_agent/key_formulations.py as the model file, lines 1 to 80 were printed, and line 69 holds the P1 formulation for 01004-02 (a sampled item). That is a formulation, not a key, and ITM-AGT-01004-02 was re-derived by hand (7/8), but it is not strictly blind. Sampled suffixes 01008-06, 01015-04, 02006-04, 02006-09, 02011-06 and 03008-09 also have entries in that file past line 80; those lines were never read.

## Stems that depend on a table or graph the stems file does not carry

- ITM-GEN-01002-09: needs the table of f values; unformulated.
- ITM-GEN-03006-06: needs the table of f and f'; unformulated.
- ITM-GEN-04002-06: needs the table of F; unformulated. Also asks for units, but options are bare numbers.
- ITM-GEN-05005-06, ITM-GEN-05005-07, ITM-GEN-05005-09: need the graph of f'; unformulated. All three stems are word-for-word identical, so a student sees three items that differ only in the figure.
- ITM-GEN-06001-05: needs the table of R; unformulated. Asks for the setup, options are values.
- ITM-GEN-06002-04: needs the table of R; unformulated. Asks for the setup, options are values.
- ITM-GEN-05001-18: refers to a table, but the choice does not depend on it (see statement items).
- ITM-GEN-08009-09: says "the shaded region R shown"; the region is still fixed by the text, so solved (11/12).

## Stems that ask for a form the options do not match

- ITM-GEN-04006-07: asks for "an exact answer with units"; options are bare values (216 pi solved).
- ITM-GEN-08002-11, ITM-GEN-08002-18, ITM-GEN-09003-14, ITM-GEN-09005-12, ITM-GEN-09005-17, ITM-GEN-09006-09, ITM-GEN-09010-11, ITM-GEN-99002-08, ITM-GEN-99006-10: ask to "show the setup"; options are three-decimal values only.
- ITM-GEN-06018-05, ITM-GEN-06019-09: indefinite integrals; no option carries + C.
- ITM-GEN-99001-04: says "A calculator may be used" but asks for an exact value. Premise checked against the curve: theta = 5 pi/4 gives dy/dtheta = -4 sqrt(2) - 1, dx/dtheta = 4 sqrt(2), slope -1 - sqrt(2)/8, so the stated data are consistent.

## Stems with a second defensible choice

- ITM-GEN-05008-09: option A reads "because it is negative there"; if "it" is read as f', A says the same as C. Chose C.
- ITM-GEN-10016-04: A and C list the same four terms; A's general term is C's with n replaced by n + 1, and neither states where n starts. With n from -1, A is also correct. Chose C.
- ITM-GEN-10015-16: A reaches the right verdict by the alternating series test citing only the limit 0; its sentence is incomplete rather than false. Chose C.
- ITM-GEN-07005-16: B's sentence (concave down at the starting point) is true but does not justify the overestimate on the interval. Chose A.

## Copied from an AP question

None recognised. This is a guess from memory, not a check against the cache: the calculator particle-motion stems (09003, 09005, 09006) and the instantaneous-equals-average stems (08002) follow common AP free-response patterns, but the functions and numbers do not match any question I recall.

## Statement items, letter chosen and reason

- ITM-GEN-01004-07: B. Cancelling x - 1 leaves (x - 5)/x, which is -4 at 1.
- ITM-GEN-01006-02: D. Left limit 4, right limit 3, so not continuous.
- ITM-GEN-05001-18: A. The corner at 19/2 is inside (8, 11), so MVT hypotheses fail.
- ITM-GEN-05008-09: C. f' < 0 on (-inf, -3) and (-2, 0); A's reason is ambiguous.
- ITM-GEN-05013-16: A. f'(-1) = 0, f''(-1) = -30 gives a relative maximum; f'(3) = -24, not critical.
- ITM-GEN-06014-03: C. Width 5/n, right endpoints 1 + 5k/n; checked the limit equals the integral.
- ITM-GEN-07005-16: A. y'' = y + 2 < 0 whenever f < -2, so concave down throughout.
- ITM-GEN-07006-08: D. Rate k(60 - P) with k > 0 moves P toward 60.
- ITM-GEN-07012-16: C. 6xy - 24x = 6x(y - 4) separates to dy/(y - 4) = 6x dx.
- ITM-GEN-10015-05: C. At x = -3 the terms are 1/(sqrt(n) + 6); limit comparison with p = 1/2. A's comparison runs the wrong way.
- ITM-GEN-10015-10: B. Radius 3, so x = 6 gives the convergent p-series with p = 3/2.
- ITM-GEN-10015-16: C. At x = 1 the terms are (-1)^n/n^(3/2), alternating and decreasing to 0.
- ITM-GEN-10016-04: C. 6x - 4x^3 + 4x^5/5 - 8x^7/105, general term indexed from n = 0.
- ITM-GEN-99010-13: C. T is the sum of the two integrals with no added constant; 48.6215 + 11 is at most 60.
