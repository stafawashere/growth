---
title: Calculator-active item templates
version: v1
role: generator
model: offline Claude Code session, claude-opus-5-5
purpose: How a template builds a calculator-active item whose answer is reported to three decimal places, with the setup asked for in the stem.
---

# Calculator items

A calculator item is one whose answer needs numerical work a graphing calculator does: a definite
integral with no elementary antiderivative, a root of a transcendental equation, the value of a
derivative at a point of a complicated expression.

- Compute with `kit.numeric_integral` and `kit.numeric_roots`, which work at 25 digits, and keep
  full precision until the key. The key is `Key(form="numeric", value=..., decimals=3)`; the
  instantiator rounds each option to three places.
- The stem asks for the setup and the value correct to three decimal places, and sets
  `setup_required=True`. It says "Using a calculator".
- The key must not be a whole number or zero at three places; choose the parameter domain so it
  never is, and state the invariant `nondegenerate_three_decimals(key)`.
- Distractors come from calculator-typical errors the archetype's skills hold: premature rounding
  of an intermediate value, degree mode, a setup error such as the wrong limits or a missing
  factor, reading the wrong root. Each is recomputed at full precision and must differ from the
  key at three places on every draw.
- An `either` archetype emits a calculator item only when the numbers need one; otherwise it emits
  a no-calculator item with an exact key.
