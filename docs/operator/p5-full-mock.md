---
title: P5 full mock, driven through the running app
research_date: 2026-09-24
status: measured
purpose: The one full mock 11 P5's exit criterion names, at the documented shape and with the paper capture path, driven in the browser by Claude on the operator's delegation.
---

# P5 full mock through the running app [verified]

Run on 2026-09-24 by claude-opus-5-5 on the operator's delegation, not by a person. The
application was the worktree's (`app/main.py` `build_application` over a fresh scratch database,
the real item bank ingested with every check on first use), served on localhost and driven in the
Claude desktop app's browser pane. The transcriber, grader and diagnostician ran live on the
operator's Claude subscription ($0.00 of API spend). The one double was the passkey verifier.

## What was done

- Registration, then the onboarding diagnostic answered "I have not learned this yet" throughout
  (a scripted click loop on the diagnostic's own button), so home offered the queue.
- Home, Mock exam, "Start the full mock" with paper photographs as the capture mode. The setup
  screen listed the four parts with counts, minutes and calculator status read from
  exam-structure.md and the reference-sheet note.
- Section I Part A, 29 questions under a 62-minute server timer, NO CALCULATOR ALLOWED and the
  absent-calculator note, no graphing panel on the page. Each question was read and answered:
  the first by clicking the option and crossing one out, the rest through the screen's own option
  and Next controls from the page's script; one question was marked for review, the question
  menu showed every question answered and that one marked, and Submit part asked for
  confirmation before closing the part.
- The break screen, then Section I Part B, 13 questions under 38 minutes, CALCULATOR REQUIRED,
  the radian-mode note on the trigonometric calculator items, and the graphing panel. The panel
  was used for three answers: a definite integral (20.639825 on 0 to 3.5), a derivative at a
  point (-1.639803 at 0.4) and a zero in a set window (2.228916 on 0 to 6).
- Section II Part A (2 questions, 30 minutes, calculator, panel present) and Part B (4 questions,
  60 minutes, no calculator, no panel on the page, checked by searching the page). The booklet
  page link served a PNG headed with the part's calculator header and addressed "Answer Question
  1 parts (a), (b), (c), (d) on this page". The page was reloaded mid-mock and the mock resumed
  from the setup screen's Resume list with the server's clock.
- Capture after the last part: for each of the six questions a photograph of a written booklet
  page (rendered with a handwriting font by tools/render_frq_pages.py, since no real handwriting
  exists) was put into the capture screen's file input from the page's script, the image gate
  passed it, "Read my page" ran the live transcriber, the read-back was shown with the places it
  was unsure of, a confidence was chosen, and "Yes, grade it" started live grading.
- "See the result": the band and its assumptions, raw counts, the per-question table against
  2023 to 2025 means, and pacing for each part.

## Result

| Measure | Value |
| --- | --- |
| Multiple choice | 41 of 42 correct (the miss was a figure question; its graph prints no axis numbers, and counting grid lines at the pane's size was not attempted) |
| Free response | 37 points earned, 9 provisional, of 54; per question 9, 4 (3 provisional), 5 (1), 8 (1), 5 (3), 6 (1) |
| Band | 3 to 5, with the seven assumptions on the same screen; no single score anywhere |
| Gradings | 54 point rows, 22 decided by deterministic checks, 9 provisional after split samples |
| Subscription calls | transcriber 8 (two read-backs failed and were retried, see below), grader 99, diagnostician 4 |
| skills_state (618 rows) | `shasum` (SHA-1) prefix of every row, `66f234b2024ef971`, before the mock and after the result |
| Attempts written by the mock | 48 (42 multiple choice, 6 free response) |

The time used per part (3:21, 2:04, 1:52, 0:16) is the model's answering speed, not a student's,
so the pacing figures here show the screen works, not how a student paces.

## Defects the run found, each fixed and tested in this stage

1. Home offered an open mock as "a set in progress", and Resume would have opened it in the
   micro-session screen. `app/session/preview.py` now leaves the assessment modes out
   (`test_an_open_mock_is_not_offered_as_todays_set_in_progress`). The P3 free-response unit check
   had the same exposure.
2. Two captures failed with "database is locked": grading held SQLite's one write lock through the
   diagnostician's model call while the next read-back tried to write. The diagnostician now runs
   before any grading write (`observe_lost_points`, `test_no_write_lock_is_held_while_the_diagnostician_runs`)
   and the driver's busy wait is 30 seconds instead of 5. One further read-back failed once while
   the grader was being paced at 20 calls a minute and read cleanly on retry.
3. The capture list did not refresh after a capture, a confirmed question reopened on the photo
   step, and a grading stopped by a server restart had no way to restart from the screen. The
   list now re-reads and polls; a confirmed question opens on its grading; "Grade it again"
   appears after about five minutes without points.
4. The part header counted within the part ("Question 1 of 13"); it now uses the exam number
   against the section ("Question 30 of 42").
5. Every answered question counted as revisited; a revisit is now a visit that began after the
   first answer. Free-response questions now count as answered once captured.
6. ITM-GEN-01005-04 printed f(x) = x + 3 sin(1/(x + 3)) - 1 for (x + 3) sin(1/(x + 3)) - 1,
   whose limit does not exist as printed. The template now brackets a sum factor; the item was
   retired with a recorded decision (content/generation_review/decisions.json).

Not fixed here, carried in BUILD-LEDGER.md Known defects: the function-graph figures draw a grid
with no numbers on the axes, so a value read off the graph has to be found by counting grid lines.
