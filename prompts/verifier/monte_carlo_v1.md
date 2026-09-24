---
title: Monte Carlo family triage
version: v1
role: verifier
model: offline Claude Code session, claude-opus-5-5
purpose: How a failed Monte Carlo family pass is read and fixed: as a parameter-spec or template defect, never by filtering out the failing draws.
---

# When a family fails

`tools/template_gate.py <archetype id>` runs the family pass in code: 300 seeded draws from the
archetype's parameter spec, every invariant and every rejection rule a draw can break, checked on
each. No model judges a draw. This prompt governs what a session does with a failure.

1. Read the first failing draw the report prints, reproduce it with the printed seed, and name the
   rule it broke in the gate's own words.
2. Decide whose defect it is. A draw outside what the archetype measures (a zero width, a vanishing
   denominator, an answer that rounds to a whole number) is a spec defect: tighten the domain or add
   a constraint, and state the new constraint as a checkable expression. A draw inside the construct
   that the template mishandles (a wrong branch, a sign, a distractor that coincides with the key) is
   a template defect: fix the template.
3. Never make a failure disappear by catching it, by skipping the draw inside `build`, or by
   widening an invariant. A family that fails on 2 percent of draws has a latent bad item in it.
4. Rerun the full 300-draw pass. A template counts only on a pass with zero failures.
