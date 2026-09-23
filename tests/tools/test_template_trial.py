"""What each test here catches, since a test that cannot fail for a stated reason is furniture.

The harness in tools/template_trial.py is a measuring instrument. Its only output is a defect
count, so the way it fails is silently: a counter that never fires reports a clean template and
nobody learns it was not measuring. Every test below names the counter it proves fires.
"""
import json
from pathlib import Path

import pytest
import sympy

from tools import template_trial as trial

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "template_trial"


def load(name):
   return json.loads((FIXTURES / name).read_text())


def test_the_expression_gate_refuses_a_name_outside_the_allowed_set():
   """Catches: model output reaching sympify unchecked. sympify evaluates its input, and a
   template is untrusted by construction, so the gate is the only thing between the two."""
   with pytest.raises(trial.TemplateRefused):
      trial.parse_expression("attack", "__import__('os')", {"a"})

   with pytest.raises(trial.TemplateRefused):
      trial.parse_expression("attack", "open", {"a"})

   with pytest.raises(trial.TemplateRefused):
      trial.parse_expression("attack", "a['b']", {"a"})

   allowed = trial.parse_expression("fine", "2*a + sin(a)", {"a"})
   assert allowed.free_symbols == {sympy.Symbol("a")}


def test_a_parameter_that_shadows_a_free_symbol_is_refused():
   """Catches: a template declaring a parameter named x, which would substitute the variable
   out of every expression and produce a numeric identity in place of a function."""
   template = load("clean_02011.json")
   template["parameters"].append({"name": "x", "kind": "integer", "low": 1, "high": 2})

   with pytest.raises(trial.TemplateRefused):
      trial.evaluate(template, {"a": 1, "b": 1, "c": 1, "x": 2})


def test_every_draw_satisfies_every_constraint():
   """Catches: constraints declared in a template but never applied, so a draw the author
   excluded still renders. The clean fixture excludes a == 0 and a zero slope."""
   import random

   rng = random.Random(7)

   for _ in range(200):
      draw = trial.draw_parameters(load("clean_02011.json"), rng)
      assert draw is not None
      assert draw["a"] != 0
      assert 2 * draw["a"] * draw["c"] + draw["b"] != 0


def test_a_constraint_that_excludes_everything_returns_no_draw():
   """Catches: draw_parameters looping forever, or returning an illegal draw, when the author
   writes a contradiction. It has to give up and say so."""
   import random

   template = load("clean_02011.json")
   template["constraints"] = ["Eq(a, 0)", "Ne(a, 0)"]

   assert trial.draw_parameters(template, random.Random(1)) is None


def test_doubled_sign_is_counted_on_the_defective_fixture():
   """Catches: the doubled-sign counter not firing. This is the 8.5 to 10.1 percent defect the
   earlier proof of concept hit, so a counter that misses it hides the headline number."""
   report = trial.run_draws(load("defective_02011.json"), draws=20, seed=3)

   assert report["doubled_sign"] == 20
   assert trial.has_doubled_sign(r"$y - -6 = 3\left(x - -2\right)$")
   assert not trial.has_doubled_sign(r"$y - 6 = 3\left(x + 2\right)$")


def test_unbalanced_latex_is_counted():
   """Catches: the balance counter not firing. A template that drops a brace renders markup a
   student sees as raw text, and nothing else in the harness would notice."""
   assert not trial.latex_is_balanced(r"$f(x) = \frac{1}{2$")
   assert not trial.latex_is_balanced(r"$\left(x + 1$")
   assert trial.latex_is_balanced(r"$f(x) = \frac{1}{2}$")

   template = load("clean_02011.json")
   template["steps"][0]["text"] = r"Broken: $\frac{{fp}$."
   report = trial.run_draws(template, draws=10, seed=5)

   assert report["unbalanced_latex"] == 10


def test_a_restated_step_is_counted_vacuous():
   """Catches: the vacuous-step counter not firing. A step that restates the previous value is
   the 4.5 percent degenerate-draw case, and it teaches nothing while looking like work."""
   report = trial.run_draws(load("defective_02011.json"), draws=20, seed=3)

   assert report["vacuous_step"] == 20


def test_a_key_that_differs_from_the_last_step_is_counted():
   """Catches: the key comparison never running. This is the only check standing between the
   bank and a silently wrong answer, which 04 calls the most damaging defect the product ships."""
   report = trial.run_draws(load("defective_02011.json"), draws=20, seed=3)

   assert report["key_disagreements"] == 20
   assert report["first_failure"]["key"] != report["first_failure"]["final_step"]


def test_the_clean_fixture_reports_no_defects():
   """The absence claim. It means something only because the four tests above prove every
   counter fires on an input that deserves it."""
   report = trial.run_draws(load("clean_02011.json"), draws=50, seed=11)

   assert report["steps_rendered"] == 250
   assert report["unbalanced_latex"] == 0
   assert report["doubled_sign"] == 0
   assert report["vacuous_step"] == 0
   assert report["key_disagreements"] == 0
   assert report["draws_that_raised"] == 0
   assert report["passes_bar"] is True


def test_the_bar_fails_on_a_key_disagreement_alone():
   """Catches: passes_bar reading only the surface rate. A template with clean rendering and a
   wrong key must not pass, because rendering is cosmetic and the key is not."""
   template = load("clean_02011.json")
   template["expressions"].append({"name": "off", "expr": "ln + 1"})
   template["key"]["name"] = "off"
   report = trial.run_draws(template, draws=10, seed=5)

   assert report["surface_defect_rate"] == 0.0
   assert report["key_disagreements"] == 10
   assert report["passes_bar"] is False


def test_draws_are_reproducible_from_a_seed():
   """Catches: an unseeded or globally seeded RNG, which would make a trial result impossible
   to reproduce and therefore impossible to argue with."""
   first = trial.run_draws(load("clean_02011.json"), draws=25, seed=99)
   second = trial.run_draws(load("clean_02011.json"), draws=25, seed=99)
   different = trial.run_draws(load("clean_02011.json"), draws=25, seed=100)

   assert first == second
   assert different["template_id"] == first["template_id"]


def test_generate_builds_the_prompt_from_the_real_archetype_record():
   """Catches: the generate path silently sending an empty or wrong archetype, which would make
   a failed trial look like a model failure when it was a harness failure."""
   prompt = trial.build_prompt("BC-QA-02011")
   carried = json.loads(prompt)

   assert carried["id"] == "BC-QA-02011"
   assert carried["expected_solution_path"][0] == "differentiate the function"
   assert "point_types" in carried


def test_generate_never_sends_a_tool_definition_and_pins_effort():
   """Catches: the trial drifting from the routing 13 decides. Effort left at the default high
   is the single largest avoidable cost in the document, and a tool definition on any call
   breaks 09's no-tools rule."""
   captured = {}

   def fake_transport(url, headers, body):
      captured["url"] = url
      captured["body"] = body

      return {"content": [{"type": "text", "text": "{}"}], "usage": {"output_tokens": 1}}

   trial.generate_template("BC-QA-02011", transport=fake_transport)

   assert "tools" not in captured["body"]
   assert captured["body"]["output_config"]["effort"] == "medium"
   assert captured["body"]["model"] == "claude-opus-5"
   assert captured["body"]["system"][0]["cache_control"]["ttl"] == "1h"


def test_a_latex_brace_group_is_not_read_as_a_placeholder():
   """Catches the defect the first real trial run exposed. The old {name} syntax collided with
   LaTeX, which uses braces for every group, so a correct \\int_{a}^{b} was read as two
   placeholders and every draw of that template was refused. The substitution marker has to be
   something LaTeX never emits."""
   values = {"a": sympy.Integer(2)}

   assert trial.render(r"$\int_{a}^{b} f(x)\,dx$", values) == r"$\int_{a}^{b} f(x)\,dx$"
   assert trial.render(r"$\frac{1}{2}x^{-3}$", values) == r"$\frac{1}{2}x^{-3}$"
   assert trial.render(r"$\int_0^{<<a>>} f$", values) == r"$\int_0^{2} f$"


def test_a_template_written_without_math_mode_is_counted():
   """Catches: a template writing formulas as plain text. It renders x^3 literally to a student,
   and the balance check passes trivially on zero dollar signs, so nothing else would notice."""
   assert not trial.uses_math_mode("Let f(x) = 3x^3 + 2x.")
   assert trial.uses_math_mode(r"Let $f(x) = 3x^3$.")

   template = load("clean_02011.json")
   template["steps"][0]["text"] = "Differentiate. f'(x) is the derivative."
   report = trial.run_draws(template, draws=10, seed=5)

   assert report["plain_text_blocks"] == 10
   assert report["passes_bar"] is False


def test_a_key_named_after_the_last_step_is_refused_as_tautological():
   """Catches: a template naming the key after the last step's expression, which compares a
   value with itself and reports a pass that means nothing. The first real template did this."""
   template = load("clean_02011.json")
   last = [s for s in template["steps"] if s.get("expr")][-1]
   template["key"]["name"] = last["expr"]
   report = trial.run_draws(template, draws=10, seed=5)

   assert report["key_check_is_tautological"] is True
   assert report["key_disagreements"] == 0
   assert report["passes_bar"] is False


def test_the_draw_space_is_reported_so_a_bank_can_be_sized_against_it():
   """Catches: a template whose parameter domain holds fewer tuples than the bank it must fill,
   which would serve the same item under a different label. Exclusions have to count."""
   template = load("clean_02011.json")

   assert trial.draw_space(template) == 12 * 17 * 11

   template["parameters"][0]["exclude"] = [0, 1, 2]

   assert trial.draw_space(template) == 10 * 17 * 11


def test_a_template_that_raises_on_every_draw_cannot_pass():
   """Catches: passes_bar reading only rates. A template refused on every draw renders nothing,
   so every rate is vacuously clean while the template is unusable."""
   template = load("clean_02011.json")
   template["steps"][0]["text"] = "$<<undefined_name>>$"
   report = trial.run_draws(template, draws=10, seed=5)

   assert report["draws_that_raised"] == 10
   assert report["steps_rendered"] == 0
   assert report["passes_bar"] is False


def _transport_returning(templates):
   """A fake Messages API that hands back the next template in the list on each call."""
   sent = []
   remaining = list(templates)

   def transport(url, headers, body):
      sent.append(body)
      payload = remaining.pop(0)

      return {"content": [{"type": "text", "text": json.dumps(payload)}],
              "usage": {"input_tokens": 500, "output_tokens": 3000,
                        "cache_creation_input_tokens": 0, "cache_read_input_tokens": 1900}}

   return transport, sent


def test_a_template_below_the_draw_space_floor_fails_the_gate():
   """Catches the trap the first real run walked into. A template scores zero defects by keeping
   its domains tiny, and BC-QA-06016 came back with twelve distinct tuples against a bank of
   forty. Clean rendering on a domain that cannot fill the bank is not a pass."""
   template = load("clean_02011.json")
   template["parameters"] = [{"name": "a", "kind": "integer", "low": 1, "high": 3},
                             {"name": "b", "kind": "integer", "low": 1, "high": 3},
                             {"name": "c", "kind": "integer", "low": 1, "high": 3}]
   report = trial.run_draws(template, draws=20, seed=4)

   assert report["draw_space"] == 27
   assert report["surface_defect_rate"] == 0.0
   assert report["passes_bar"] is False


def test_the_feedback_names_every_failed_check():
   """Catches: a retry message that says only "it failed". A model asked to fix an unnamed
   defect guesses, and the loop burns a call per guess."""
   template = load("defective_02011.json")
   report = trial.run_draws(template, draws=20, seed=3)
   message = trial.defect_feedback(template, report)

   assert "doubled sign" in message
   assert "restate the previous step" in message
   assert "disagree between the declared key and the last step" in message
   assert str(trial.MIN_DRAW_SPACE) in message


def test_the_feedback_carries_a_rendered_example_from_a_real_draw():
   """Catches: feedback that reports a rate with no instance. The template author cannot see
   which prose produced the defect from a percentage alone."""
   template = load("defective_02011.json")
   report = trial.run_draws(template, draws=20, seed=3)
   message = trial.defect_feedback(template, report)

   assert "drawn " in message
   assert trial.DOUBLED_SIGN.search(report["examples"]["doubled_sign"]["text"]) is not None


def test_the_retry_loop_stops_on_the_first_passing_attempt():
   """Catches: a loop that keeps spending after the gate is satisfied."""
   clean = load("clean_02011.json")
   transport, sent = _transport_returning([clean, clean, clean])
   _template, report, history = trial.generate_with_retry(
      "BC-QA-02011", attempts=3, transport=transport, draws=10)

   assert report["passes_bar"] is True
   assert len(history) == 1
   assert len(sent) == 1


def test_the_retry_loop_gives_up_after_the_attempt_cap():
   """Catches: an unbounded loop on an archetype the model cannot get right, which would spend
   without a ceiling."""
   broken = load("defective_02011.json")
   transport, sent = _transport_returning([broken, broken, broken])
   _template, report, history = trial.generate_with_retry(
      "BC-QA-02011", attempts=3, transport=transport, draws=10)

   assert report["passes_bar"] is False
   assert len(history) == 3
   assert len(sent) == 3


def test_the_retry_turn_carries_the_previous_template_and_its_defects():
   """Catches: a retry that re-asks the original question. Without the previous attempt and its
   named defects the second call is an independent draw, not a correction."""
   broken = load("defective_02011.json")
   clean = load("clean_02011.json")
   transport, sent = _transport_returning([broken, clean])
   _template, report, history = trial.generate_with_retry(
      "BC-QA-02011", attempts=3, transport=transport, draws=10)

   assert report["passes_bar"] is True
   assert len(history) == 2

   first_turn = sent[0]["messages"][0]["content"]
   second_turn = sent[1]["messages"][0]["content"]

   assert "Previous template:" not in first_turn
   assert "Previous template:" in second_turn
   assert broken["template_id"] in second_turn
   assert "doubled sign" in second_turn
   assert sent[1]["system"][0]["text"] == sent[0]["system"][0]["text"]


def test_an_undeclared_short_name_is_refused_rather_than_crashing_the_batch():
   """Catches the defect that killed the 15 archetype sample run on its fourth archetype. Any
   word of two characters or fewer counted as declared, so a constraint naming an undeclared A
   reached SymPy and raised TypeError: invalid input: A outside every guard."""
   with pytest.raises(trial.TemplateRefused):
      trial.parse_expression("constraint", "Gt(A, 0)", {"a", "b"})

   allowed = trial.parse_expression("constraint", "Gt(a, 0)", {"a", "b"})
   assert allowed.free_symbols == {sympy.Symbol("a")}


def test_a_malformed_constraint_is_counted_not_raised():
   """Catches: one bad template ending a whole batch. draw_parameters sat outside the guard, so
   a constraint that cannot be parsed took down every archetype queued behind it."""
   template = load("clean_02011.json")
   template["constraints"] = ["Gt(UNDECLARED, 0)"]
   report = trial.run_draws(template, draws=10, seed=5)

   assert report["draws_that_raised"] == 10
   assert report["first_failure"]["stage"] == "draw_parameters"
   assert report["passes_bar"] is False


def test_a_template_that_renders_nothing_reports_no_rate_rather_than_one():
   """Catches: a sentinel read as a measurement. A template rendering zero steps reported a
   surface defect rate of 1.0, which reads in a run log as 100 percent defective rather than
   as nothing measured."""
   template = load("clean_02011.json")
   template["constraints"] = ["Gt(UNDECLARED, 0)"]
   report = trial.run_draws(template, draws=10, seed=5)

   assert report["rendered_nothing"] is True
   assert report["surface_defect_rate"] is None
   assert "No draw rendered at all" in trial.defect_feedback(template, report)


def test_a_truncated_response_is_named_rather_than_arriving_as_a_parse_error():
   """Catches the defect that killed the sample run twice. The model hit max_tokens mid-JSON and
   the failure surfaced as JSONDecodeError: Unterminated string, which names neither the cause
   nor the archetype."""
   def transport(url, headers, body):
      return {"content": [{"type": "text", "text": '{"archetype_id": "BC-QA'}],
              "stop_reason": "max_tokens", "usage": {"output_tokens": 16000}}

   with pytest.raises(trial.TemplateRefused, match="max_tokens"):
      trial.generate_template("BC-QA-02011", transport=transport)


def test_a_generation_failure_is_fed_back_and_the_loop_continues():
   """Catches: a failed generation ending the loop. A truncated response is a defect of that
   attempt like any other, and the next attempt has to be told what went wrong."""
   clean = load("clean_02011.json")
   calls = []

   def transport(url, headers, body):
      calls.append(body)
      first = len(calls) == 1

      if first:
         return {"content": [{"type": "text", "text": "{"}], "stop_reason": "max_tokens",
                 "usage": {"output_tokens": 16000}}

      return {"content": [{"type": "text", "text": json.dumps(clean)}],
              "stop_reason": "end_turn", "usage": {"output_tokens": 3000}}

   template, report, history = trial.generate_with_retry(
      "BC-QA-02011", attempts=3, transport=transport, draws=10)

   assert template is not None
   assert report["passes_bar"] is True
   assert len(history) == 2
   assert "generation_error" in history[0]
   assert "could not be used" in calls[1]["messages"][0]["content"]


def test_every_attempt_failing_to_generate_returns_no_template():
   """Catches: the loop returning a template variable that was never assigned, which would raise
   an unbound local error and take the batch down instead of recording the archetype as failed."""
   def transport(url, headers, body):
      return {"content": [{"type": "text", "text": "{"}], "stop_reason": "max_tokens",
              "usage": {"output_tokens": 16000}}

   template, report, history = trial.generate_with_retry(
      "BC-QA-02011", attempts=2, transport=transport, draws=10)

   assert template is None
   assert report is None
   assert len(history) == 2
   assert all("generation_error" in entry for entry in history)


def test_a_key_aliased_to_the_last_step_is_caught_as_tautological():
   """Catches the defect that made the first full trial meaningless. The check compared names, so
   a template declaring K as an alias of B satisfied it while both bodies were the same string.
   Measured across 18 real templates, 14 declared a key equal to the final step and 12 of those
   were character-identical, so 'zero key disagreements over 22,800 steps' established nothing
   for them. Both copy shapes are exercised here: a duplicated body and a bare alias."""
   template = load("clean_02011.json")
   final = [s for s in template["steps"] if s.get("expr")][-1]["expr"]
   body = {e["name"]: e["expr"] for e in template["expressions"]}[final]

   template["expressions"].append({"name": "al", "expr": body})
   template["key"]["name"] = "al"

   assert trial.key_check_is_tautological(template) is True

   report = trial.run_draws(template, draws=10, seed=5)
   assert report["key_disagreements"] == 0
   assert report["passes_bar"] is False

   bare_alias = load("clean_02011.json")
   last = [s for s in bare_alias["steps"] if s.get("expr")][-1]["expr"]
   bare_alias["expressions"].append({"name": "al", "expr": last})
   bare_alias["key"]["name"] = "al"

   assert trial.key_check_is_tautological(bare_alias) is True


def test_a_key_derived_by_its_own_route_is_not_tautological():
   """The other side of the same gate. A key written as a different expression of the parameters
   must still pass, or the check would reject every template including a correct one."""
   template = load("clean_02011.json")

   assert trial.key_check_is_tautological(template) is False
   assert trial.run_draws(template, draws=10, seed=5)["passes_bar"] is True


def test_the_clean_fixture_meets_the_item_contract():
   """The absence claim for the four contract checks. It means something only because the
   five tests below prove each one fires on a template that deserves it."""
   contract = trial.contract_check(load("clean_02011.json"))

   assert contract["representation"] == "BC-REP-01"
   assert contract["representation_undeclared"] is False
   assert contract["figure_missing"] is False
   assert contract["unresolved_error_paths"] == 0
   assert contract["unresolved_point_types"] == 0
   assert contract["option_count"] == trial.OPTIONS_PER_ITEM
   assert contract["clean"] is True


def test_an_undeclared_or_foreign_representation_fails_the_gate():
   """Catches: a template that never says which representation it serves, which is every one
   of the 26 measured templates, and one that names a representation the archetype does not
   list. Without the declaration the figure check cannot fire, so this is the check it rests on."""
   template = load("clean_02011.json")
   del template["representation"]
   report = trial.run_draws(template, draws=5, seed=1)

   assert report["contract"]["representation_undeclared"] is True
   assert report["passes_bar"] is False

   template["representation"] = "BC-REP-13"

   assert trial.contract_check(template)["representation_undeclared"] is True


def test_a_graphical_representation_without_a_figure_fails_the_gate():
   """Catches: a template for a graph, table, slope field or diagram archetype that poses the
   item in prose alone, which 11 of the 18 first templates did because the schema had no
   figure field. BC-QA-02011 lists BC-REP-02 among its representations."""
   template = load("clean_02011.json")
   template["representation"] = "BC-REP-02"
   report = trial.run_draws(template, draws=5, seed=1)

   assert report["contract"]["figure_required"] is True
   assert report["contract"]["figure_missing"] is True
   assert report["passes_bar"] is False

   template["figure"] = {"kind": "function_graph", "labels": [{"text": "f", "anchor": ["1", "1"]}]}

   assert trial.contract_check(template)["figure_missing"] is False


def test_a_distractor_whose_error_path_is_not_a_bc_err_id_fails_the_gate():
   """Catches: distractors carrying a prose error_path such as "sign slip", which 63 of 63
   measured distractors did, and which rejection rule 7 rejects one by one at ingest."""
   template = load("clean_02011.json")
   template["distractors"][1]["error_path"] = "sign slip when dividing"
   report = trial.run_draws(template, draws=5, seed=1)

   assert report["contract"]["unresolved_error_paths"] == 1
   assert report["passes_bar"] is False

   template["distractors"][1]["error_path"] = "BC-ERR-00000"

   assert trial.contract_check(template)["unresolved_error_paths"] == 1


def test_a_step_tagged_with_a_skill_id_instead_of_a_point_type_fails_the_gate():
   """Catches: point_type_id set to a BC-SKL id, which two measured templates did, and to a
   BC-PT id that does not exist. Rule 9 checks the tag against the archetype's point types."""
   template = load("clean_02011.json")
   template["steps"][0]["point_type_id"] = "BC-SKL-02012"
   template["steps"][1]["point_type_id"] = "BC-PT-00000"
   report = trial.run_draws(template, draws=5, seed=1)

   assert report["contract"]["unresolved_point_types"] == 2
   assert report["passes_bar"] is False


def test_a_template_with_four_distractors_fails_the_gate():
   """Catches: five options against 04's four, which 9 of 18 measured templates produced, and
   fewer than four, which cannot be served as an MCQ at all."""
   template = load("clean_02011.json")
   template["distractors"].append(dict(template["distractors"][0]))
   report = trial.run_draws(template, draws=5, seed=1)

   assert report["contract"]["option_count"] == 5
   assert report["contract"]["option_count_wrong"] is True
   assert report["passes_bar"] is False

   template["distractors"] = template["distractors"][:2]

   assert trial.contract_check(template)["option_count_wrong"] is True


def test_the_feedback_names_every_failed_contract_check():
   """Catches: a contract failure the model is never told about, so the retry repeats it."""
   template = load("clean_02011.json")
   del template["representation"]
   template["distractors"][0]["error_path"] = "prose"
   template["steps"][0]["point_type_id"] = "BC-SKL-02012"
   template["distractors"].append(dict(template["distractors"][1]))
   report = trial.run_draws(template, draws=5, seed=1)
   message = trial.defect_feedback(template, report)

   assert "does not declare which of the archetype's representations" in message
   assert "not an allowed BC-ERR id" in message
   assert "not BC-PT ids" in message
   assert f"exactly {trial.OPTIONS_PER_ITEM}" in message

   template["representation"] = "BC-REP-02"
   report = trial.run_draws(template, draws=5, seed=1)

   assert "needs a figure" in trial.defect_feedback(template, report)


def test_the_prompt_carries_the_allowed_error_paths():
   """Catches: the model being asked for BC-ERR ids it was never shown, which guarantees the
   prose error paths the first 26 templates produced."""
   carried = json.loads(trial.build_prompt("BC-QA-02011"))

   assert "BC-ERR-02027" in carried["allowed_error_paths"]
   assert all(path.startswith("BC-ERR-") for path in carried["allowed_error_paths"])
   assert "allowed_error_paths" in trial.INSTRUCTIONS


def test_the_clean_fixture_declares_a_role_on_every_parameter_and_its_incidental_holds():
   """The absence claim for the roles check. In the fixture `a` is the only incidental:
   `b = 0` and `c = 0` each delete a term from a step, so both are declared radical."""
   report = trial.run_draws(load("clean_02011.json"), draws=5, seed=1)

   assert report["roles"]["parameter_role_undeclared"] == []
   assert report["roles"]["incidentals_checked"] == 1
   assert report["roles"]["incidental_changes_path"] == []
   assert "distractor composition" in report["roles"]["radicals"]
   assert report["passes_bar"] is True


def test_a_parameter_with_no_declared_role_fails_the_gate():
   """Catches: a template that leaves the radical or incidental question unanswered, which
   is every one of the 26 measured templates, so the isomorph-difficulty finding could not be
   acted on at all."""
   template = load("clean_02011.json")
   del template["parameters"][1]["role"]
   report = trial.run_draws(template, draws=5, seed=1)

   assert report["roles"]["parameter_role_undeclared"] == ["b"]
   assert report["passes_bar"] is False


def test_an_incidental_that_changes_the_form_of_a_step_fails_the_gate():
   """Catches: a parameter declared incidental whose value deletes a term or changes a head.
   `c = 0` turns the point of tangency into the origin and the line into a single term, so
   declaring `c` incidental is a false declaration and the check must say so."""
   template = load("clean_02011.json")
   template["parameters"][2]["role"] = "incidental"
   report = trial.run_draws(template, draws=5, seed=1)

   assert report["roles"]["incidental_changes_path"] == ["c"]
   assert report["passes_bar"] is False

   message = trial.defect_feedback(template, report)

   assert "declared incidental but varying" in message

   template["parameters"][2]["role"] = "radical"
   template["parameters"][2]["exclude"] = [0]
   report = trial.run_draws(template, draws=5, seed=1)

   assert report["roles"]["incidental_changes_path"] == []
