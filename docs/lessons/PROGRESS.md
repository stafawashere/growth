---
title: Lesson design progress ledger
research_date: 2026-09-29
status: in_progress
purpose: Durable record of the adaptive specialized lessons design run, so a fresh session can resume from it after compaction: the manifest of every lesson with its status, the decisions taken with their evidence, the failed hypotheses and the next action.
---

# Lesson design progress ledger

Statuses per lesson: todo, designed (a design doc exists), checked (tools/check_lesson_designs.py clean on it), resolved (blind re-solve agrees on every worked example and check key, verification/<id>.json), signed_off (sign-off audit records zero unsourced claims and zero mathematical errors).

The manifest below is rendered from docs/lessons/progress.json by `PYTHONPATH=. .venv/bin/python tools/check_lesson_designs.py --progress`. The statuses live in progress.json and are changed only after the checker output or verdict file that shows them exists.

## Stage 0 inventory, 2026-09-29

Counts computed from the loaded snapshot (`app.content.loader.load_snapshot`) and `app/lessons/confusable.py confusable_sets`, not by hand:

| Fact | Value | Against FIXED FACTS |
|---|---|---|
| BC-CON concepts | 170 (Unit 1 19, 2 15, 3 10, 4 15, 5 15, 6 20, 7 12, 8 21, 9 17, 10 26) | matches |
| BC-PRQ | 77 | matches |
| Active archetypes | 148 | matches |
| BC-PT | 76 | matches |
| Active BC-ERR, BC-MIS | 393, 213 | plan 15 says 391 errors; the ledger's stage 15 entry minted 2 more |
| Confusable sets | 10 (Unit 2 three, Unit 4 one, Unit 5 one, Unit 6 two, Unit 7 one, Unit 8 one, Unit 10 one) | matches |
| Concepts loaded by no active archetype | 0 (plan 15 named BC-CON-06014; stage 15 minted BC-QA-06017 for it) | differs from plan 15 |
| Concepts whose skills hold no active BC-ERR | 2, BC-CON-01003 and BC-CON-01018 | check 3 cannot be built for them; they carry 2 checks |
| Concepts with no BC-PT on any loading archetype | 56 | no what_a_reader_scores section on those lessons (plan 15, R14) |
| BC-PRQ listed by no archetype's prerequisites | 5 | their LSN-PRQ worked example draws from an archetype that loads a dependent skill instead |
| `confusable_with` | filled on 505 of 541 skills by tools/derive_confusable.py | plan 15's text (empty on all 541) is stale; confusable.py reads the field |
| Local main, branch head | main b80501e, branch 6a54a22 two commits ahead | main fast-forwards cleanly |

Decision ids: LSN-DEC-<unit>-<nn>, nn numbering the unit's sets in the order confusable_sets returns them (sorted by member id).

## Decisions with evidence

- D1. A design doc is Markdown with front matter, the template's sections in order, and one fenced JSON machine record carrying every served sentence, every step as a SymPy string and every check. Evidence: the prose alone cannot be CAS-checked, and a JSON-only doc cannot carry the recognition, time and band commentary the author needs; the machine record is one rename away from plan 15's lesson.json shape, which is what "an author fills the JSON without a teaching decision" needs.
- D2. Step relations in the machine record are equivalent, differentiate, integrate, evaluate, solve, limit and new, each checked by SymPy in tools/check_lesson_designs.py. Evidence: tools/check_lessons.py only accepts equivalence between consecutive valued steps, so the hand-authored lesson leaves evaluation and root-finding steps unvalued; a design that teaches the whole path needs the other relations checked, not skipped.
- D3. Lessons on the 2 concepts without an active error (BC-CON-01003, BC-CON-01018) carry 2 checks, which plan 15 allows (LESSON_CHECKS_MIN 2). Evidence: the count above.

- D4. The Unit 6 antidifferentiation-technique skills form one confusable component of 21 skills (computed with app/lessons/confusable.py components over confusable_graph), above DECISION_SET_MAX 6, so no technique decision lesson is derived; plan 15 names that drill first for L6. Recorded as a proposed amendment (split the component by archetype family, or raise the cap for a named set). The other two Unit 6 components above the cap hold 9 skills each.
- D5. Unit READMEs written by designers claimed `confusable_with` empty; the loaded snapshot has it filled on 505 skills (67 in Unit 1, 45 in Unit 2, 62 in Unit 5). The three README lines were corrected by hand before commit and later README prompts say so.
- D6. The design checker accepts `crabbc-YY:<page>` citations (cache/text/crabbc-25 exists), because the 2025 Chief Reader pages are where several archetype scoring notes live.

## Failed hypotheses

- None yet.

## Next action

- Stage 2: unit READMEs and concept designs, Unit 1 first (fringe order), batches of at most 8 per designer, up to 6 designers at once.

## Manifest

## Manifest

<!-- manifest:start (rendered by tools/check_lesson_designs.py --progress) -->

| Kind | todo | designed | checked | resolved | signed_off | total |
|---|---|---|---|---|---|---|
| concept | 169 | 0 | 1 | 0 | 0 | 170 |
| prerequisite | 77 | 0 | 0 | 0 | 0 | 77 |
| decision | 9 | 0 | 1 | 0 | 0 | 10 |

| Lesson | Target | Unit | Status | Note |
|---|---|---|---|---|
| LSN-CON-01001 | BC-CON-01001 | 01 | todo |  |
| LSN-CON-01002 | BC-CON-01002 | 01 | todo |  |
| LSN-CON-01003 | BC-CON-01003 | 01 | todo |  |
| LSN-CON-01004 | BC-CON-01004 | 01 | todo |  |
| LSN-CON-01005 | BC-CON-01005 | 01 | todo |  |
| LSN-CON-01006 | BC-CON-01006 | 01 | todo |  |
| LSN-CON-01007 | BC-CON-01007 | 01 | todo |  |
| LSN-CON-01008 | BC-CON-01008 | 01 | todo |  |
| LSN-CON-01009 | BC-CON-01009 | 01 | todo |  |
| LSN-CON-01010 | BC-CON-01010 | 01 | todo |  |
| LSN-CON-01011 | BC-CON-01011 | 01 | todo |  |
| LSN-CON-01012 | BC-CON-01012 | 01 | todo |  |
| LSN-CON-01013 | BC-CON-01013 | 01 | todo |  |
| LSN-CON-01014 | BC-CON-01014 | 01 | todo |  |
| LSN-CON-01015 | BC-CON-01015 | 01 | todo |  |
| LSN-CON-01016 | BC-CON-01016 | 01 | todo |  |
| LSN-CON-01017 | BC-CON-01017 | 01 | todo |  |
| LSN-CON-01018 | BC-CON-01018 | 01 | todo |  |
| LSN-CON-01019 | BC-CON-01019 | 01 | todo |  |
| LSN-CON-02001 | BC-CON-02001 | 02 | todo |  |
| LSN-CON-02002 | BC-CON-02002 | 02 | todo |  |
| LSN-CON-02003 | BC-CON-02003 | 02 | todo |  |
| LSN-CON-02004 | BC-CON-02004 | 02 | todo |  |
| LSN-CON-02005 | BC-CON-02005 | 02 | todo |  |
| LSN-CON-02006 | BC-CON-02006 | 02 | todo |  |
| LSN-CON-02007 | BC-CON-02007 | 02 | todo |  |
| LSN-CON-02008 | BC-CON-02008 | 02 | todo |  |
| LSN-CON-02009 | BC-CON-02009 | 02 | todo |  |
| LSN-CON-02010 | BC-CON-02010 | 02 | todo |  |
| LSN-CON-02011 | BC-CON-02011 | 02 | todo |  |
| LSN-CON-02012 | BC-CON-02012 | 02 | todo |  |
| LSN-CON-02013 | BC-CON-02013 | 02 | checked | reference design; checker clean 2026-09-29 |
| LSN-CON-02014 | BC-CON-02014 | 02 | todo |  |
| LSN-CON-02015 | BC-CON-02015 | 02 | todo |  |
| LSN-CON-03001 | BC-CON-03001 | 03 | todo |  |
| LSN-CON-03002 | BC-CON-03002 | 03 | todo |  |
| LSN-CON-03003 | BC-CON-03003 | 03 | todo |  |
| LSN-CON-03004 | BC-CON-03004 | 03 | todo |  |
| LSN-CON-03005 | BC-CON-03005 | 03 | todo |  |
| LSN-CON-03006 | BC-CON-03006 | 03 | todo |  |
| LSN-CON-03007 | BC-CON-03007 | 03 | todo |  |
| LSN-CON-03008 | BC-CON-03008 | 03 | todo |  |
| LSN-CON-03009 | BC-CON-03009 | 03 | todo |  |
| LSN-CON-03010 | BC-CON-03010 | 03 | todo |  |
| LSN-CON-04001 | BC-CON-04001 | 04 | todo |  |
| LSN-CON-04002 | BC-CON-04002 | 04 | todo |  |
| LSN-CON-04003 | BC-CON-04003 | 04 | todo |  |
| LSN-CON-04004 | BC-CON-04004 | 04 | todo |  |
| LSN-CON-04005 | BC-CON-04005 | 04 | todo |  |
| LSN-CON-04006 | BC-CON-04006 | 04 | todo |  |
| LSN-CON-04007 | BC-CON-04007 | 04 | todo |  |
| LSN-CON-04008 | BC-CON-04008 | 04 | todo |  |
| LSN-CON-04009 | BC-CON-04009 | 04 | todo |  |
| LSN-CON-04010 | BC-CON-04010 | 04 | todo |  |
| LSN-CON-04011 | BC-CON-04011 | 04 | todo |  |
| LSN-CON-04012 | BC-CON-04012 | 04 | todo |  |
| LSN-CON-04013 | BC-CON-04013 | 04 | todo |  |
| LSN-CON-04014 | BC-CON-04014 | 04 | todo |  |
| LSN-CON-04015 | BC-CON-04015 | 04 | todo |  |
| LSN-CON-05001 | BC-CON-05001 | 05 | todo |  |
| LSN-CON-05002 | BC-CON-05002 | 05 | todo |  |
| LSN-CON-05003 | BC-CON-05003 | 05 | todo |  |
| LSN-CON-05004 | BC-CON-05004 | 05 | todo |  |
| LSN-CON-05005 | BC-CON-05005 | 05 | todo |  |
| LSN-CON-05006 | BC-CON-05006 | 05 | todo |  |
| LSN-CON-05007 | BC-CON-05007 | 05 | todo |  |
| LSN-CON-05008 | BC-CON-05008 | 05 | todo |  |
| LSN-CON-05009 | BC-CON-05009 | 05 | todo |  |
| LSN-CON-05010 | BC-CON-05010 | 05 | todo |  |
| LSN-CON-05011 | BC-CON-05011 | 05 | todo |  |
| LSN-CON-05012 | BC-CON-05012 | 05 | todo |  |
| LSN-CON-05013 | BC-CON-05013 | 05 | todo |  |
| LSN-CON-05014 | BC-CON-05014 | 05 | todo |  |
| LSN-CON-05015 | BC-CON-05015 | 05 | todo |  |
| LSN-CON-06001 | BC-CON-06001 | 06 | todo |  |
| LSN-CON-06002 | BC-CON-06002 | 06 | todo |  |
| LSN-CON-06003 | BC-CON-06003 | 06 | todo |  |
| LSN-CON-06004 | BC-CON-06004 | 06 | todo |  |
| LSN-CON-06005 | BC-CON-06005 | 06 | todo |  |
| LSN-CON-06006 | BC-CON-06006 | 06 | todo |  |
| LSN-CON-06007 | BC-CON-06007 | 06 | todo |  |
| LSN-CON-06008 | BC-CON-06008 | 06 | todo |  |
| LSN-CON-06009 | BC-CON-06009 | 06 | todo |  |
| LSN-CON-06010 | BC-CON-06010 | 06 | todo |  |
| LSN-CON-06011 | BC-CON-06011 | 06 | todo |  |
| LSN-CON-06012 | BC-CON-06012 | 06 | todo |  |
| LSN-CON-06013 | BC-CON-06013 | 06 | todo |  |
| LSN-CON-06014 | BC-CON-06014 | 06 | todo |  |
| LSN-CON-06015 | BC-CON-06015 | 06 | todo |  |
| LSN-CON-06016 | BC-CON-06016 | 06 | todo |  |
| LSN-CON-06017 | BC-CON-06017 | 06 | todo |  |
| LSN-CON-06018 | BC-CON-06018 | 06 | todo |  |
| LSN-CON-06019 | BC-CON-06019 | 06 | todo |  |
| LSN-CON-06020 | BC-CON-06020 | 06 | todo |  |
| LSN-CON-07001 | BC-CON-07001 | 07 | todo |  |
| LSN-CON-07002 | BC-CON-07002 | 07 | todo |  |
| LSN-CON-07003 | BC-CON-07003 | 07 | todo |  |
| LSN-CON-07004 | BC-CON-07004 | 07 | todo |  |
| LSN-CON-07005 | BC-CON-07005 | 07 | todo |  |
| LSN-CON-07006 | BC-CON-07006 | 07 | todo |  |
| LSN-CON-07007 | BC-CON-07007 | 07 | todo |  |
| LSN-CON-07008 | BC-CON-07008 | 07 | todo |  |
| LSN-CON-07009 | BC-CON-07009 | 07 | todo |  |
| LSN-CON-07010 | BC-CON-07010 | 07 | todo |  |
| LSN-CON-07011 | BC-CON-07011 | 07 | todo |  |
| LSN-CON-07012 | BC-CON-07012 | 07 | todo |  |
| LSN-CON-08001 | BC-CON-08001 | 08 | todo |  |
| LSN-CON-08002 | BC-CON-08002 | 08 | todo |  |
| LSN-CON-08003 | BC-CON-08003 | 08 | todo |  |
| LSN-CON-08004 | BC-CON-08004 | 08 | todo |  |
| LSN-CON-08005 | BC-CON-08005 | 08 | todo |  |
| LSN-CON-08006 | BC-CON-08006 | 08 | todo |  |
| LSN-CON-08007 | BC-CON-08007 | 08 | todo |  |
| LSN-CON-08008 | BC-CON-08008 | 08 | todo |  |
| LSN-CON-08009 | BC-CON-08009 | 08 | todo |  |
| LSN-CON-08010 | BC-CON-08010 | 08 | todo |  |
| LSN-CON-08011 | BC-CON-08011 | 08 | todo |  |
| LSN-CON-08012 | BC-CON-08012 | 08 | todo |  |
| LSN-CON-08013 | BC-CON-08013 | 08 | todo |  |
| LSN-CON-08014 | BC-CON-08014 | 08 | todo |  |
| LSN-CON-08015 | BC-CON-08015 | 08 | todo |  |
| LSN-CON-08016 | BC-CON-08016 | 08 | todo |  |
| LSN-CON-08017 | BC-CON-08017 | 08 | todo |  |
| LSN-CON-08018 | BC-CON-08018 | 08 | todo |  |
| LSN-CON-08019 | BC-CON-08019 | 08 | todo |  |
| LSN-CON-08020 | BC-CON-08020 | 08 | todo |  |
| LSN-CON-08021 | BC-CON-08021 | 08 | todo |  |
| LSN-CON-09001 | BC-CON-09001 | 09 | todo |  |
| LSN-CON-09002 | BC-CON-09002 | 09 | todo |  |
| LSN-CON-09003 | BC-CON-09003 | 09 | todo |  |
| LSN-CON-09004 | BC-CON-09004 | 09 | todo |  |
| LSN-CON-09005 | BC-CON-09005 | 09 | todo |  |
| LSN-CON-09006 | BC-CON-09006 | 09 | todo |  |
| LSN-CON-09007 | BC-CON-09007 | 09 | todo |  |
| LSN-CON-09008 | BC-CON-09008 | 09 | todo |  |
| LSN-CON-09009 | BC-CON-09009 | 09 | todo |  |
| LSN-CON-09010 | BC-CON-09010 | 09 | todo |  |
| LSN-CON-09011 | BC-CON-09011 | 09 | todo |  |
| LSN-CON-09012 | BC-CON-09012 | 09 | todo |  |
| LSN-CON-09013 | BC-CON-09013 | 09 | todo |  |
| LSN-CON-09014 | BC-CON-09014 | 09 | todo |  |
| LSN-CON-09015 | BC-CON-09015 | 09 | todo |  |
| LSN-CON-09016 | BC-CON-09016 | 09 | todo |  |
| LSN-CON-09017 | BC-CON-09017 | 09 | todo |  |
| LSN-CON-10001 | BC-CON-10001 | 10 | todo |  |
| LSN-CON-10002 | BC-CON-10002 | 10 | todo |  |
| LSN-CON-10003 | BC-CON-10003 | 10 | todo |  |
| LSN-CON-10004 | BC-CON-10004 | 10 | todo |  |
| LSN-CON-10005 | BC-CON-10005 | 10 | todo |  |
| LSN-CON-10006 | BC-CON-10006 | 10 | todo |  |
| LSN-CON-10007 | BC-CON-10007 | 10 | todo |  |
| LSN-CON-10008 | BC-CON-10008 | 10 | todo |  |
| LSN-CON-10009 | BC-CON-10009 | 10 | todo |  |
| LSN-CON-10010 | BC-CON-10010 | 10 | todo |  |
| LSN-CON-10011 | BC-CON-10011 | 10 | todo |  |
| LSN-CON-10012 | BC-CON-10012 | 10 | todo |  |
| LSN-CON-10013 | BC-CON-10013 | 10 | todo |  |
| LSN-CON-10014 | BC-CON-10014 | 10 | todo |  |
| LSN-CON-10015 | BC-CON-10015 | 10 | todo |  |
| LSN-CON-10016 | BC-CON-10016 | 10 | todo |  |
| LSN-CON-10017 | BC-CON-10017 | 10 | todo |  |
| LSN-CON-10018 | BC-CON-10018 | 10 | todo |  |
| LSN-CON-10019 | BC-CON-10019 | 10 | todo |  |
| LSN-CON-10020 | BC-CON-10020 | 10 | todo |  |
| LSN-CON-10021 | BC-CON-10021 | 10 | todo |  |
| LSN-CON-10022 | BC-CON-10022 | 10 | todo |  |
| LSN-CON-10023 | BC-CON-10023 | 10 | todo |  |
| LSN-CON-10024 | BC-CON-10024 | 10 | todo |  |
| LSN-CON-10025 | BC-CON-10025 | 10 | todo |  |
| LSN-CON-10026 | BC-CON-10026 | 10 | todo |  |
| LSN-DEC-02-01 | BC-UNIT-02 | 02 | todo |  |
| LSN-DEC-02-02 | BC-UNIT-02 | 02 | todo |  |
| LSN-DEC-02-03 | BC-UNIT-02 | 02 | todo |  |
| LSN-DEC-04-01 | BC-UNIT-04 | 04 | todo |  |
| LSN-DEC-05-01 | BC-UNIT-05 | 05 | todo |  |
| LSN-DEC-06-01 | BC-UNIT-06 | 06 | checked | reference design; checker clean 2026-09-29 |
| LSN-DEC-06-02 | BC-UNIT-06 | 06 | todo |  |
| LSN-DEC-07-01 | BC-UNIT-07 | 07 | todo |  |
| LSN-DEC-08-01 | BC-UNIT-08 | 08 | todo |  |
| LSN-DEC-10-01 | BC-UNIT-10 | 10 | todo |  |
| LSN-PRQ-01001 | BC-PRQ-01001 | 01 | todo |  |
| LSN-PRQ-01002 | BC-PRQ-01002 | 01 | todo |  |
| LSN-PRQ-01003 | BC-PRQ-01003 | 01 | todo |  |
| LSN-PRQ-01004 | BC-PRQ-01004 | 01 | todo |  |
| LSN-PRQ-01005 | BC-PRQ-01005 | 01 | todo |  |
| LSN-PRQ-01006 | BC-PRQ-01006 | 01 | todo |  |
| LSN-PRQ-01007 | BC-PRQ-01007 | 01 | todo |  |
| LSN-PRQ-01008 | BC-PRQ-01008 | 01 | todo |  |
| LSN-PRQ-01009 | BC-PRQ-01009 | 01 | todo |  |
| LSN-PRQ-01010 | BC-PRQ-01010 | 01 | todo |  |
| LSN-PRQ-02001 | BC-PRQ-02001 | 02 | todo |  |
| LSN-PRQ-02002 | BC-PRQ-02002 | 02 | todo |  |
| LSN-PRQ-02003 | BC-PRQ-02003 | 02 | todo |  |
| LSN-PRQ-02004 | BC-PRQ-02004 | 02 | todo |  |
| LSN-PRQ-02005 | BC-PRQ-02005 | 02 | todo |  |
| LSN-PRQ-03001 | BC-PRQ-03001 | 03 | todo |  |
| LSN-PRQ-03002 | BC-PRQ-03002 | 03 | todo |  |
| LSN-PRQ-03003 | BC-PRQ-03003 | 03 | todo |  |
| LSN-PRQ-03004 | BC-PRQ-03004 | 03 | todo |  |
| LSN-PRQ-03005 | BC-PRQ-03005 | 03 | todo |  |
| LSN-PRQ-03006 | BC-PRQ-03006 | 03 | todo |  |
| LSN-PRQ-03007 | BC-PRQ-03007 | 03 | todo |  |
| LSN-PRQ-04001 | BC-PRQ-04001 | 04 | todo |  |
| LSN-PRQ-04002 | BC-PRQ-04002 | 04 | todo |  |
| LSN-PRQ-04003 | BC-PRQ-04003 | 04 | todo |  |
| LSN-PRQ-04004 | BC-PRQ-04004 | 04 | todo |  |
| LSN-PRQ-04005 | BC-PRQ-04005 | 04 | todo |  |
| LSN-PRQ-04006 | BC-PRQ-04006 | 04 | todo |  |
| LSN-PRQ-04007 | BC-PRQ-04007 | 04 | todo |  |
| LSN-PRQ-04008 | BC-PRQ-04008 | 04 | todo |  |
| LSN-PRQ-04009 | BC-PRQ-04009 | 04 | todo |  |
| LSN-PRQ-05001 | BC-PRQ-05001 | 05 | todo |  |
| LSN-PRQ-05002 | BC-PRQ-05002 | 05 | todo |  |
| LSN-PRQ-05003 | BC-PRQ-05003 | 05 | todo |  |
| LSN-PRQ-05004 | BC-PRQ-05004 | 05 | todo |  |
| LSN-PRQ-05005 | BC-PRQ-05005 | 05 | todo |  |
| LSN-PRQ-05006 | BC-PRQ-05006 | 05 | todo |  |
| LSN-PRQ-05007 | BC-PRQ-05007 | 05 | todo |  |
| LSN-PRQ-05008 | BC-PRQ-05008 | 05 | todo |  |
| LSN-PRQ-06001 | BC-PRQ-06001 | 06 | todo |  |
| LSN-PRQ-06002 | BC-PRQ-06002 | 06 | todo |  |
| LSN-PRQ-06003 | BC-PRQ-06003 | 06 | todo |  |
| LSN-PRQ-06004 | BC-PRQ-06004 | 06 | todo |  |
| LSN-PRQ-06005 | BC-PRQ-06005 | 06 | todo |  |
| LSN-PRQ-06006 | BC-PRQ-06006 | 06 | todo |  |
| LSN-PRQ-06007 | BC-PRQ-06007 | 06 | todo |  |
| LSN-PRQ-06008 | BC-PRQ-06008 | 06 | todo |  |
| LSN-PRQ-06009 | BC-PRQ-06009 | 06 | todo |  |
| LSN-PRQ-06010 | BC-PRQ-06010 | 06 | todo |  |
| LSN-PRQ-06011 | BC-PRQ-06011 | 06 | todo |  |
| LSN-PRQ-06012 | BC-PRQ-06012 | 06 | todo |  |
| LSN-PRQ-06013 | BC-PRQ-06013 | 06 | todo |  |
| LSN-PRQ-07001 | BC-PRQ-07001 | 07 | todo |  |
| LSN-PRQ-07002 | BC-PRQ-07002 | 07 | todo |  |
| LSN-PRQ-07003 | BC-PRQ-07003 | 07 | todo |  |
| LSN-PRQ-07004 | BC-PRQ-07004 | 07 | todo |  |
| LSN-PRQ-07005 | BC-PRQ-07005 | 07 | todo |  |
| LSN-PRQ-07006 | BC-PRQ-07006 | 07 | todo |  |
| LSN-PRQ-08001 | BC-PRQ-08001 | 08 | todo |  |
| LSN-PRQ-08002 | BC-PRQ-08002 | 08 | todo |  |
| LSN-PRQ-08003 | BC-PRQ-08003 | 08 | todo |  |
| LSN-PRQ-08004 | BC-PRQ-08004 | 08 | todo |  |
| LSN-PRQ-08005 | BC-PRQ-08005 | 08 | todo |  |
| LSN-PRQ-08006 | BC-PRQ-08006 | 08 | todo |  |
| LSN-PRQ-08007 | BC-PRQ-08007 | 08 | todo |  |
| LSN-PRQ-09001 | BC-PRQ-09001 | 09 | todo |  |
| LSN-PRQ-09002 | BC-PRQ-09002 | 09 | todo |  |
| LSN-PRQ-09003 | BC-PRQ-09003 | 09 | todo |  |
| LSN-PRQ-09004 | BC-PRQ-09004 | 09 | todo |  |
| LSN-PRQ-10001 | BC-PRQ-10001 | 10 | todo |  |
| LSN-PRQ-10002 | BC-PRQ-10002 | 10 | todo |  |
| LSN-PRQ-10003 | BC-PRQ-10003 | 10 | todo |  |
| LSN-PRQ-10004 | BC-PRQ-10004 | 10 | todo |  |
| LSN-PRQ-10005 | BC-PRQ-10005 | 10 | todo |  |
| LSN-PRQ-10006 | BC-PRQ-10006 | 10 | todo |  |
| LSN-PRQ-10007 | BC-PRQ-10007 | 10 | todo |  |
| LSN-PRQ-10008 | BC-PRQ-10008 | 10 | todo |  |

<!-- manifest:end -->
