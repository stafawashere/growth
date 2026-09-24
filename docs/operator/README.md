---
title: Operator work order
research_date: 2026-09-20
status: in_progress
purpose: Name the five artefacts the operator must still produce for P1 and point to their specs.
---

# Operator work order

Everything else in P1 is built. These five artefacts are the whole remaining critical path
to merge. Each one unblocks specific gates named in docs/plan/11-phased-delivery.md.

1. **130 hand-authored items.** Unblocks gate 17 (`test_item_verification_tools`), gate 30
   (`eval_p1_distractor_paths`) and exit criterion 7. Spec: docs/operator/items.md.
2. **100-item key audit.** Unblocks gate 29 (`eval_p1_key_error_rate`) and exit criterion 4.
   Spec: docs/operator/key-audit.md.
3. **Design token file.** Unblocks entry criterion 5, gate 26 (`test_contrast_floors`) and
   remaining implementer decision 6. Spec: docs/operator/design-tokens.md.
4. **A key-backed measurement of the tutor prompt's cacheable prefix.** Unblocks gate 22
   (`test_prompt_cache_prefix_length`). Spec: docs/operator/provider-key.md.
5. **The provider key itself**, needed only to make artefact 4 possible. Same spec:
   docs/operator/provider-key.md.

None of these documents restates the plan's reasoning. Read docs/plan/11-phased-delivery.md
for that.

## Beyond P1 [verified]

Items for the Units 1 to 3 archetypes P1 left out and for Units 4 to 10 (P2 scope item 8) are
specified in docs/operator/items-units-4-to-10.md: which 38 archetypes get items and why the
other 24 do not, the per-unit banks under content/items_unitNN_agent/, and how they are verified,
signed off and audited.
