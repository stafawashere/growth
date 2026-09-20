# Synthetic P1 items, for gate 23 only

Thirty six synthetic item records in the hand-authored shape `app/items/ingest.py` reads, six
each over six of the thirteen archetypes that scope item 2 of `docs/plan/11-phased-delivery.md`
fixes as the P1 subset: BC-QA-01008, BC-QA-02002, BC-QA-02006, BC-QA-02007, BC-QA-02011 and
BC-QA-03008.

The seven of the thirteen these files do not cover are BC-QA-01004, BC-QA-01015, BC-QA-02008,
BC-QA-02010, BC-QA-03001, BC-QA-03004 and BC-QA-03005. Six of those seven are gated at cold
start: the primary skill of each carries a hard prerequisite that is an ordinary BC-SKL record
rather than one of the seeded assumed-mastered parents, so the fringe cannot reach them in a
first session, and BC-QA-01004's gating parent BC-SKL-01028 belongs to BC-QA-01004 itself. The
seventh, BC-QA-02010, is reachable but adds nothing the six already give the flow. Only
BC-QA-01008 of the thirteen is reachable in Unit 1, so the six are one Unit 1 archetype, four
Unit 2 archetypes and one Unit 3 archetype rather than two per unit.

Every record carries `calculator_status: "no_calculator"` and `representation: "BC-REP-01"`, and
its `skills` array is the `skills` array of its archetype in `data/archetypes.json`, in that
order, so the primary skill stays first. The mathematics of each item is the mathematics its
archetype describes: a piecewise rule with two boundaries and a constant solved for continuity,
a derivative taken from the limit definition, a power and reciprocal expression differentiated by
rule, a cosine and exponential expression differentiated by rule, a tangent line written at a
point, and a second derivative.

They exist so that `tests/e2e/test_session_login_to_feedback.py` can assemble and run a session,
which is gate 23 of `docs/plan/11-phased-delivery.md`. Gate 23's property is the flow, login to
feedback to a persisted `skills_state` change. Item quality is not what it measures.

**None of these items counts toward gates 17, 29 or 30.** Those gates read the 130 hand-authored
items the operator writes, and no synthetic item may be substituted for one of them or enter the
100-item audit sample. Each archetype here is asked one question with six different coefficients,
which is far narrower than the variation a real item set carries.

What is real in each record, because the application reads it:

- `is_key` on every option, exactly one key per item, which is what ingestion checks.
- A BC-ERR id on every distractor, taken from `data/errors.json`, naming at least one skill the
  archetype lists and describing the mistake that produces that option's value, which is what the
  grader resolves and what the elaborated feedback screen reads. Items carry four options where
  three such errors exist and three options where only two do; BC-QA-01008's two distractors both
  carry BC-ERR-01017, once for each of the two boundaries, because that is the only active Unit 1
  error on those skills that produces a wrong value here.
- `violated_step` on every distractor, a zero-based index into the archetype's
  `expected_solution_path`, which is what `app/feedback/render.py` reads.
- MathJSON on the last worked-solution step, equal to the answer key, which is what the SymPy
  equivalence and numeric checks compare.

The files are written for this gate, not by a generator in the application: P1 has no generator,
and none was used here.