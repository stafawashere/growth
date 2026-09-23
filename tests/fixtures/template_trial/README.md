---
title: Template trial fixtures
research_date: 2026-09-20
status: in_progress
purpose: Reference templates that prove the trial harness measures what it claims, and nothing about model-authored template quality.
---

# Template trial fixtures

Both files here are hand written. Neither is evidence about whether a model can author a
template, which is the only question `tools/template_trial.py` exists to answer. They are the
positive controls the harness needs so that a clean report from a real model-authored template
means something.

`clean_02011.json` is a correct template for BC-QA-02011, written to the same contract the
model is given. Its `constraints` exclude the zero-slope draw that makes step 4 vacuous, which
is the 4.5 percent case the earlier proof of concept hit.

`defective_02011.json` trips three detectors deliberately and every draw:

- a doubled sign, because step 4 substitutes a negative `y0` straight after a minus sign,
- a vacuous step, because step 3 restates step 2's value,
- a key disagreement, because `key` names `wrong`, which is the line plus one.

Its parameter domains are pinned negative so those defects fire on every draw rather than
sometimes, which is what makes the control deterministic.

`clean_02011.json` also carries what the item contract in `docs/plan/04-item-generation.md`
demands and no draw can reveal: a declared `representation`, exactly three distractors each
with an `error_path` that resolves to an active BC-ERR id, and `point_type_id` tags that
resolve to BC-PT ids. The contract tests in `tests/tools/test_template_trial.py` mutate this
file one field at a time to prove each of those checks fires.

Every parameter in `clean_02011.json` also declares a role. `a` is the one incidental: varying
it alone leaves every step and the key in the same form. `b` and `c` are radical because a zero
value deletes a term from a step, and the roles test flips `c` to incidental to prove the
path-invariance check fires on a false declaration.
