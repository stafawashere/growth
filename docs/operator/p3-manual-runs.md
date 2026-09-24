---
title: P3 read-back gate, 20 manual runs
research_date: 2026-09-24
status: measured
purpose: The 20 manual runs 11 P3's exit criterion names, showing no point was committed without a confirmed read-back, run by Claude on the operator's delegation.
---

# P3 read-back gate: 20 manual runs [verified]

Run on 2026-09-24 by claude-opus-5-5 on the operator's delegation, not by a person. The application
was the real one (`app/main.py` `build_application` over a scratch database), served on
localhost and driven from the Claude desktop app's browser pane, with the transcriber, grader and
diagnostician live on the operator's Claude subscription ($0.00 of API spend). The one double was
the passkey verifier. Run 1 was clicked through the capture screen; runs 2 to 20 were driven from
the same page through the routes the screen calls, because the pane cannot pick a file from disk,
and each run's photograph was fetched from the page's own origin and uploaded as the screen
uploads it. The photographs are the rendered fixture pages in `tests/fixtures/frq_pages`, a
handwriting font on the app's booklet page photographed in software; no real handwriting exists.
The runs ran on the tree before the evidence-quote fix recorded in BUILD-LEDGER.md.

The gate: a gradings row may exist only after the attempt's read-back is confirmed. Checked from
the database after the runs: for every attempt, every gradings row's created_at is at or after the
attempt's confirmation time, and an attempt never confirmed has no gradings row.

| run | question | mode | what the student did | photographs through the gate | confirmed | points | rows before confirmation |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | FRQ-AGT-05007-01 | photo | clicked through the screen: blurred photo rejected, clean photo read, confirmed as read | accepted 1, rejected 1 | yes | 4 earned of 4, 0 provisional | 0 |
| 2 | FRQ-AGT-05007-01 | photo | sign-change page read, part (b) corrected to the page's own words, confirmed | accepted 1, rejected 0 | yes | 2 earned of 4, 2 provisional | 0 |
| 3 | FRQ-AGT-05007-01 | photo | angled photo read, confirmed as read | accepted 1, rejected 0 | yes | 4 earned of 4, 0 provisional | 0 |
| 4 | FRQ-AGT-05007-01 | photo | low-light photo rejected, retake read, confirmed as read | accepted 1, rejected 1 | yes | 4 earned of 4, 0 provisional | 0 |
| 5 | FRQ-AGT-05007-01 | photo | cropped and far photos rejected, read-back refused (409), abandoned | accepted 0, rejected 2 | no | no points | 0 |
| 6 | FRQ-AGT-07003-01 | photo | separation page read, confirmed as read | accepted 1, rejected 0 | yes | 5 earned of 5, 0 provisional | 0 |
| 7 | FRQ-AGT-07003-01 | photo | blurred photo rejected, retake read, final answer corrected, confirmed | accepted 1, rejected 1 | yes | 5 earned of 5, 0 provisional | 0 |
| 8 | FRQ-AGT-07003-01 | photo | low-light photo rejected, read-back refused (409), abandoned | accepted 0, rejected 1 | no | no points | 0 |
| 9 | FRQ-AGT-05007-01 | typed | typed entry, full answer | no photograph | yes | 4 earned of 4, 0 provisional | 0 |
| 10 | FRQ-AGT-07003-01 | typed | typed entry, sign error in the final answer | no photograph | yes | 4 earned of 5, 0 provisional | 0 |
| 11 | FRQ-AGT-05007-01 | photo | clean photo read, never confirmed | accepted 1, rejected 0 | no | no points | 0 |
| 12 | FRQ-AGT-07003-01 | photo | clean photo read, never confirmed | accepted 1, rejected 0 | no | no points | 0 |
| 13 | FRQ-AGT-05007-01 | photo | sign-change page read, confirmed as read | accepted 1, rejected 0 | yes | 2 earned of 4, 2 provisional | 0 |
| 14 | FRQ-AGT-07003-01 | photo | read-back answer overwritten with a wrong answer, confirmed | accepted 1, rejected 0 | yes | 4 earned of 5, 0 provisional | 0 |
| 15 | FRQ-AGT-05007-01 | photo | angled photo read, confirmed as read | accepted 1, rejected 0 | yes | 4 earned of 4, 0 provisional | 0 |
| 16 | FRQ-AGT-07003-01 | photo | separation page read, confirmed as read | accepted 1, rejected 0 | yes | 5 earned of 5, 0 provisional | 0 |
| 17 | FRQ-AGT-05007-01 | photo | clean photo read, confirmed as read | accepted 1, rejected 0 | yes | 4 earned of 4, 0 provisional | 0 |
| 18 | FRQ-AGT-05007-01 | photo | blurred photo rejected, abandoned | accepted 0, rejected 1 | no | no points | 0 |
| 19 | FRQ-AGT-07003-01 | photo | crossed-out line deleted from the read-back, confirmed | accepted 1, rejected 0 | yes | 5 earned of 5, 0 provisional | 0 |
| 20 | FRQ-AGT-05007-01 | photo | sign-change page read, confirmed as read | accepted 1, rejected 0 | yes | 2 earned of 4, 1 provisional | 0 |

Result: 20 runs, 14 confirmed and graded, 6 never confirmed (2 abandoned after a read-back,
4 stopped at the image gate), and 0 gradings rows written before a confirmation. The five
provisional points appeared on the review screen, each with "Ask for a re-read"; pressing it on one
re-judged that point with three fresh samples, which split again, resolved the dispute row as
"re-read: still provisional" and offered the re-read again.

What real use needs to measure, logged by the pipeline as it runs: every photograph's gate
verdict and measurements (`frq_images.quality`), whether each read-back was corrected
(`attempts.transcription_corrected`), the read-back as read and as confirmed (`attempts.transcription`),
and metric 9 (`GET /frq/metrics`). The gate thresholds and the transcriber's accuracy on real
pencil are unmeasured until the operator photographs real pages.
