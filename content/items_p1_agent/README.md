---
title: Agent-drafted P1 items
research_date: 2026-09-23
status: pending_operator_review
purpose: Says what the 130 item records in this directory are, how they were audited, and why they never count as the operator's hand-authored items.
---

# Agent-drafted P1 items [verified]

This directory holds 130 original item records, 10 for each of the 13 P1 archetypes named in scope item 2 of docs/plan/11-phased-delivery.md. Each record is in the output schema of docs/plan/04-item-generation.md and carries `"authored_by": "claude-opus-5-5 agent draft, pending operator review"`. No record copies an AP question stem, figure or rubric text. 79 are MCQ with a BC-ERR `error_path` on every distractor. 48 of those have four options and 31 have three, although 11 describes a four-option MCQ. The other 51 are short answer only and have no options. When R29 gives one of them an MCQ turn at stage unsupported, it is served with no options and cannot be graded. BUILD-LEDGER.md lists this under Known defects, waiting on an operator ruling.

## Provenance and what they count toward [verified]

The operator ruled on 2026-09-23, under delegated authority, that these drafts may be served by the app so it can teach now. They are not the operator's hand-authored items. `app/items/ingest.py` writes their provenance `model` as the `authored_by` value, never `operator`, and only the operator may change that. Exit criterion 7, gates 17 and 30, and the gate 29 key-audit sample count only items whose provenance model is `operator`, so none of these 130 count toward any of them. `tools/check_items.py` prints them under "items per archetype" and leaves them out of "operator-authored items per archetype".

## How they reach the app [verified]

`app/main.py` reads `GROWTH_ITEMS_DIR`. Unset, it points at this directory, and the item bank (`app/runtime/bank.py`) ingests any record whose id is not already in the items table on its first query. `GROWTH_ITEMS_DIR=none` turns that off.

## Audit [verified]

Each archetype's 10 items were re-solved blind by an independent agent on 2026-09-23. Every key matched, and `tools/check_items.py` exited 0 for each archetype. The audit changed only distractor metadata. It reindexed `violated_step` to point at the archetype's `expected_solution_path`, which is what `app/feedback/render.py` reads, in 01004, 01008, 02007, 03001, 03005 and 03008. It relabelled two 02002 distractors from BC-ERR-02008 to BC-ERR-02007, and it replaced three 03004 distractors whose values did not follow from the error they named. It changed no key.

## Open for the operator [inferred]

Operator review is pending for all 130. The auditors left some things for that review. 31 MCQs have three options, and 11 describes four. The audit named three of them, the 01004 MCQs 00, 03 and 05. In 01004 the value 1 appears in four of the five MCQs. The step index given to the cosine sign error in 02007 is a judgement call. The scratchpad generators for 02002 and 02007 are not in the repository, and rerunning the 02007 one would bring back the old `violated_step` values.
