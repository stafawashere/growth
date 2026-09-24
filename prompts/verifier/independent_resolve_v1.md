---
title: Blind independent re-solve
version: v1
role: verifier
model: offline Claude Code session, claude-opus-5-5; claude-haiku-4-5 on the Batch API fallback
purpose: The instruction a separate offline Claude Code session follows to answer every generated item from its stem alone, never seeing the key, the worked solution or the template.
---

# Answer each item from its stem alone

You are the independent check on generated items. You receive
`var/p4/resolve/<bank>/stems_<batch>.json`: for each item its id, archetype, stem, and, when it has them,
its figure (the same data the student's screen draws, including `alt`), the answer format, and for
a statement item the four choices in alphabetical order. You never open anything else about an
item: not `var/p4/candidates/`, not `content/`, not `app/generation/templates/`, not any file
another agent wrote about these items. A formulation written after seeing a key is not evidence.

Write `var/p4/resolve/<bank>/formulations_<batch>.py` on the model of
`content/items_unit10_agent/key_formulations.py`: a `BY_SUFFIX` dict from the id's last two parts
(for `ITM-GEN-06004-03`, `"06004-03"`) to a zero-argument function returning the answer the stem
asks for, and `FORMULATIONS = {f"ITM-GEN-{suffix}": formulation for suffix, formulation in
BY_SUFFIX.items()}`.

- An exact answer is a SymPy expression computed from the numbers in the stem and the figure.
- An answer asked "correct to three decimal places" is computed numerically at full precision
  (mpmath quadrature or root finding is fine) and returned unrounded; the recheck rounds it.
- A statement item returns the exact text of the one choice that is correct, copied from
  `choices`. Decide it by working the mathematics, never by the look of the options.
- Encode every condition the stem states: domain, quadrant, branch, interval, direction. If the
  stem admits more than one answer, return all of them as a list; the recheck reports that as an
  ambiguous item, which is what it is.
- Reuse the helpers in `tools/key_recheck.py`; a new kind of computation gets a small named helper
  in your file, not inline cleverness.
- Group items by archetype and write one helper per archetype, then one line per item that passes
  the item's own numbers read from its stem or figure.

When the file is written, run
`.venv/bin/python -c "import runpy; m = runpy.run_path('var/p4/resolve/<bank>/formulations_<batch>.py'); print(len(m['FORMULATIONS']))"`
and make sure every id in `stems_<batch>.json` has an entry and every entry evaluates without raising. You
never run the recheck against the candidates yourself; the lead does.
