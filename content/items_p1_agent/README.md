---
title: Agent-drafted P1 items
research_date: 2026-09-23
status: pending_operator_review
purpose: Says what the 130 item records in this directory are, how they were audited, and why they never count as the operator's hand-authored items.
---

# Agent-drafted P1 items [verified]

This directory holds 130 original item records, 10 for each of the 13 P1 archetypes named in scope item 2 of docs/plan/11-phased-delivery.md. Each record is in the output schema of docs/plan/04-item-generation.md and carries `"authored_by": "claude-opus-5-5 agent draft, pending operator review"`. No record copies an AP question stem, figure or rubric text. Every record carries four options, one key with a null `error_path` and three distractors each tagged with a BC-ERR id held by the archetype's own skills, in a per-item shuffled order.

## Provenance and what they count toward [verified]

The operator ruled on 2026-09-23, under delegated authority, that these drafts may be served by the app so it can teach now. They are not the operator's hand-authored items. `app/items/ingest.py` writes their provenance `model` as the `authored_by` value, never `operator`, and only the operator may change that. Exit criterion 7, gates 17 and 30, and the gate 29 key-audit sample count only items whose provenance model is `operator`, so none of these 130 count toward any of them. `tools/check_items.py` prints them under "items per archetype" and leaves them out of "operator-authored items per archetype".

## How they reach the app [verified]

`app/main.py` reads `GROWTH_ITEMS_DIR`. Unset, it points at this directory, and the item bank (`app/runtime/bank.py`) ingests any record whose id is not already in the items table on its first query. `GROWTH_ITEMS_DIR=none` turns that off.

## Audit [verified]

Each archetype's 10 items were re-solved blind by an independent agent on 2026-09-23. Every key matched, and `tools/check_items.py` exited 0 for each archetype. That audit changed only distractor metadata, and no key.

A second audit on 2026-09-23 re-derived every distractor from the archetype's own named errors: 30 options in each of the 12 archetypes other than BC-QA-02010, whose distractors were re-derived the session before. Of those 360 options, 167 had their value, `violated_step` or tag corrected, 42 were left unchanged because no error the archetype's skills hold produces a third distinct value for that stem, and the rest were already correct. No key changed. `tools/check_items.py content/items_p1_agent` exits 0 with all 130 clean, but that gate checks only that each tag resolves to an active id and that options are distinct, so it does not show that a distractor follows from its error.

## Open for the operator [inferred]

Operator review is pending for all 130. BUILD-LEDGER.md, Known defects, twenty-sixth session, lists by item the 42 distractors whose tag does not produce their value, which need a new BC-ERR record, a tag from outside the archetype's skills, or a stem redesign (01008-01 and 01008-06 support no legitimate distractor at all). It also lists the fixes flagged as weak: three values that need two slips in 03005, two 03004 options whose tag and value both changed, several looser readings of a named error, and three 03004 options that contain a free dy/dx symbol. In 01004 the value 1 appears as an option in five of the ten items (00, 01, 03, 05, 08). The scratchpad generators and the option shuffle are not in the repository.
