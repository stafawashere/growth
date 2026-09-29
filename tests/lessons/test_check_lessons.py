"""tools/check_lessons.py: every lint has a red fixture that fails it, and the hand-authored
lesson passes them all. The fixtures are the hand-authored lesson (or the decision lesson beside
it) with one defect planted, so a lint that stops firing turns its own test red."""
import json
from pathlib import Path

import pytest

from app.lessons.confusable import confusable_sets
from tests.lessons.conftest import FIXTURE_DIR, HAND_AUTHORED, load_fixture
from tools import check_lessons
from tools.check_lessons import Context, check_lesson

RED_FIXTURES = sorted(path.name for path in FIXTURE_DIR.glob("red_*.json"))
PLANTED_DRAW = {"structure": "planted collision", "first_factor": "x", "second_factor": "x"}


def lint_named_by(file_name):
   stem = file_name[len("red_"):-len(".json")]

   return stem.split("__")[0]


def planted_content_dir(tmp_path):
   bank = tmp_path / "items_planted"
   bank.mkdir()
   record = {"id": "ITM-PLANTED-00", "archetype_id": "BC-QA-02008", "parameter_draw": PLANTED_DRAW}
   (bank / "ITM-PLANTED-00.json").write_text(json.dumps(record))

   return tmp_path


def test_every_lint_has_a_red_fixture():
   named = {lint_named_by(name) for name in RED_FIXTURES}

   assert named == set(check_lessons.LINTS)


@pytest.mark.parametrize("file_name", RED_FIXTURES)
def test_red_fixture_fails_its_named_lint(file_name, snapshot, context, tmp_path):
   lint = lint_named_by(file_name)
   needs_a_published_twin = lint == "draw_exclusion"
   lesson = load_fixture(file_name)

   if needs_a_published_twin:
      lesson_context = Context(snapshot, content_dir=planted_content_dir(tmp_path))
   else:
      lesson_context = context

   findings = check_lesson(lesson, lesson_context)

   assert lint in findings, f"{file_name} did not fail {lint}: {sorted(findings)}"


def test_the_planted_twin_is_what_fails_draw_exclusion(snapshot, context, tmp_path):
   lesson = load_fixture("red_draw_exclusion.json")
   without_twin = check_lesson(lesson, context)
   with_twin = check_lesson(lesson, Context(snapshot, content_dir=planted_content_dir(tmp_path)))

   assert "draw_exclusion" not in without_twin
   assert "draw_exclusion" in with_twin


def test_hand_authored_lesson_passes_every_lint(context, hand_authored):
   findings = check_lesson(hand_authored, context)

   assert findings == {}


def test_decision_lesson_control_passes_every_lint(context):
   findings = check_lesson(load_fixture("decision_clean.json"), context)

   assert findings == {}


def test_cli_exits_zero_for_a_clean_directory(tmp_path, capsys):
   (tmp_path / HAND_AUTHORED.name).write_text(HAND_AUTHORED.read_text())

   exit_code = check_lessons.main(["check_lessons.py", str(tmp_path)])
   output = capsys.readouterr().out

   assert exit_code == 0
   assert "lessons read: 1" in output
   assert "with findings: 0" in output


def test_cli_exits_nonzero_when_a_lesson_has_findings(tmp_path, capsys):
   (tmp_path / "red_style.json").write_text((FIXTURE_DIR / "red_style.json").read_text())

   exit_code = check_lessons.main(["check_lessons.py", str(tmp_path)])
   output = capsys.readouterr().out

   assert exit_code == 1
   assert "style:" in output


def test_cli_refuses_an_empty_directory(tmp_path, capsys):
   exit_code = check_lessons.main(["check_lessons.py", str(tmp_path)])

   assert exit_code == 1
   assert "no lesson files were read" in capsys.readouterr().err


def test_sets_mode_prints_the_count(snapshot, capsys):
   exit_code = check_lessons.main(["check_lessons.py", "--sets"])
   output = capsys.readouterr().out
   expected = len(confusable_sets(snapshot))

   assert exit_code == 0
   assert f"confusable sets: {expected}" in output
   assert expected > 0


DELIVERY_FINDINGS = {
   "red_delivery.json": "must be step_reveal",
   "red_delivery__fallback.json": "needs a fallback",
   "red_delivery__reduced_motion.json": "needs a reduced_motion line",
   "red_delivery__placement.json": "places a label",
   "red_delivery__count.json": "at most 2",
   "red_delivery__kind.json": "is not a known spec kind",
}


@pytest.mark.parametrize("file_name", sorted(DELIVERY_FINDINGS))
def test_delivery_fixture_fails_for_its_planted_rule(file_name, context):
   messages = check_lessons.lint_delivery(load_fixture(file_name), context)
   expected = DELIVERY_FINDINGS[file_name]

   assert any(expected in message for message in messages), messages


def test_a_missing_delivery_fails_the_schema(context):
   lesson = load_fixture("red_schema__delivery.json")
   findings = check_lesson(lesson, context)
   lesson["sections"][0]["delivery"] = {"mode": "text", "reason": "restored"}
   restored = check_lessons.lint_schema(lesson, context)

   assert "schema" in findings
   assert any(message.startswith("sections/0") for message in findings["schema"])
   assert restored == []


def test_a_strategy_block_carrying_delivery_fails_the_schema(context, hand_authored):
   strategy = next(section for section in hand_authored["sections"] if section["type"] == "strategy")
   strategy["delivery"] = {"mode": "text", "reason": "planted"}
   findings = check_lesson(hand_authored, context)

   assert "schema" in findings


def test_hand_authored_delivery_matches_its_design(hand_authored):
   modes = [section["delivery"]["mode"] for section in hand_authored["sections"] if "delivery" in section]

   assert modes == ["text", "text", "step_reveal", "step_reveal", "step_reveal", "step_reveal", "step_reveal"]


def test_cli_takes_a_file_path(tmp_path, capsys):
   record = tmp_path / HAND_AUTHORED.name
   record.write_text(HAND_AUTHORED.read_text())

   exit_code = check_lessons.main(["check_lessons.py", str(record)])

   assert exit_code == 0
   assert "lessons read: 1" in capsys.readouterr().out


def test_three_drawn_blocks_are_not_capped_per_lesson(context, hand_authored):
   spec = {"kind": "graph", "curves": [{"expr": "x**2"}], "labels": [{"text": "y", "placement": "inside"}]}

   for section in hand_authored["sections"][1:4]:
      if "delivery" in section:
         section["delivery"] = {"mode": "figure", "reason": "planted", "spec": spec, "fallback": "f", "keyboard": "k"}

   assert check_lessons.lint_delivery(hand_authored, context) == []


def example_with_steps(hand_authored, steps):
   example = next(section for section in hand_authored["sections"] if section["type"] == "worked_example")
   example["steps"] = [{"cue": "c", "why": "w", **step} for step in steps]
   example["answer"] = {"form": "symbolic", "mathjson": steps[-1]["expression"]}

   return example


def test_a_differentiate_relation_is_checked_as_a_derivative(context, hand_authored):
   example = example_with_steps(hand_authored, [
      {"expression": ["Power", "x", 3], "relation": "new"},
      {"expression": ["Multiply", 3, ["Power", "x", 2]], "relation": "differentiate", "variable": "x"},
   ])
   good = check_lessons.lint_step_equivalence(hand_authored, context)
   example["steps"][1]["expression"] = ["Multiply", 2, ["Power", "x", 2]]
   bad = check_lessons.lint_step_equivalence(hand_authored, context)

   assert good == []
   assert any("is not the derivative" in message for message in bad)


def test_equation_steps_chain_without_crashing(context, hand_authored):
   example_with_steps(hand_authored, [
      {"expression": ["Equal", ["Add", "k", "m"], 2], "relation": "new"},
      {"expression": ["Equal", "k", ["Add", 2, ["Negate", "m"]]], "relation": "equivalent"},
   ])

   assert check_lessons.lint_step_equivalence(hand_authored, context) == []


def test_error_block_with_equations_compares(context, hand_authored):
   block = next(section for section in hand_authored["sections"] if section["type"] == "common_error")
   block["wrong_step"]["expression"] = ["Equal", ["Add", "k", "m"], 3]
   block["right_step"]["expression"] = ["Equal", ["Add", "k", "m"], 2]
   block["relation"] = "distinct"

   assert check_lessons.relation_messages(block) == []


def test_a_research_citation_is_held_when_its_heading_exists(context, hand_authored):
   good = "research/units/unit-02-differentiation-definition-properties.md#2.8 The Product Rule"
   bad = "research/units/unit-02-differentiation-definition-properties.md#No Such Heading"
   hand_authored["sections"][0]["sources"] = [good]
   held = check_lessons.unknown_source_messages(hand_authored, context)
   hand_authored["sections"][0]["sources"] = [bad]
   missing = check_lessons.unknown_source_messages(hand_authored, context)

   assert held == []
   assert any("heading is not" in message for message in missing)


def test_a_numeric_key_on_a_no_calculator_check_is_allowed(context, hand_authored):
   check = hand_authored["checks"][2]
   check["answer_key"]["form"] = "numeric"
   check["calculator_status"] = "no_calculator"

   assert check_lessons.lint_calculator_boundary(hand_authored, context) == []


NEW_LINT_FINDINGS = {
   "red_prediction_section.json": "0 prediction sections",
   "red_prediction_section__key.json": "key is neither the answer",
   "red_prediction_section__options.json": "2 key options",
   "red_prediction_section__decision.json": "which a decision lesson does not carry",
   "red_contrast.json": "carries no contrast",
   "red_contrast__second.json": "which only the first strategy block holds",
   "red_contrast__same.json": "are the same stem",
   "red_contrast__archetype.json": "contrast this names BC-QA-02009",
   "red_fade.json": "is worked example 2 and carries no fade_from",
   "red_fade__range.json": "is outside 2 to 3",
   "red_fade__bands.json": "only a low-band example fades",
   "red_fade__value.json": "shows no valued step before fade_from",
   "red_fix_prompt.json": "carries no fix_prompt",
   "red_fix_prompt__relation.json": "an error marked equivalent needs false",
   "red_figure_presence.json": "must carry no_figure_reason",
   "red_figure_presence__drawn.json": "and carries no_figure_reason",
   "red_served_text.json": "carries 'BC-EK-FUN-3B1'",
   "red_served_text__label.json": "starts with the reader's label",
   "red_served_text__rival.json": "LSN-CON-02013#s4 rival starts with the reader's label 'Rival:'",
   "red_served_text__tag.json": "carries '[inferred]'",
}


@pytest.mark.parametrize("file_name", sorted(NEW_LINT_FINDINGS))
def test_new_lint_fixture_fails_for_its_planted_rule(file_name, context):
   lint = lint_named_by(file_name)
   messages = check_lessons.LINTS[lint](load_fixture(file_name), context)
   expected = NEW_LINT_FINDINGS[file_name]

   assert any(expected in message for message in messages), messages


def prediction_of(lesson):
   return next(section for section in lesson["sections"] if section["type"] == "prediction")


def test_a_short_answer_prediction_keyed_on_example_one_passes(context, hand_authored):
   prediction = prediction_of(hand_authored)
   example = next(section for section in hand_authored["sections"] if section["type"] == "worked_example")
   prediction["format"] = "short_answer"
   prediction.pop("options")
   prediction["answer_key"] = {"form": "symbolic", "mathjson": example["answer"]["mathjson"]}

   assert check_lessons.lint_prediction_section(hand_authored, context) == []


def test_a_statement_prediction_key_is_not_compared(context, hand_authored):
   prediction = prediction_of(hand_authored)
   prediction["format"] = "short_answer"
   prediction.pop("options")
   prediction["answer_key"] = {"form": "statement", "mathjson": "two terms"}

   assert check_lessons.lint_prediction_section(hand_authored, context) == []


def test_a_prediction_after_the_orientation_is_refused(context, hand_authored):
   sections = hand_authored["sections"]
   sections[0], sections[1] = sections[1], sections[0]
   messages = check_lessons.lint_prediction_section(hand_authored, context)
   order = check_lessons.lint_section_order(hand_authored, context)

   assert "the prediction is not the first section" in messages
   assert order != []


def test_a_misspelt_new_field_fails_the_schema(context, hand_authored):
   prediction_of(hand_authored)["resolutoin"] = {"text": "planted"}
   strategy = next(section for section in hand_authored["sections"] if section["type"] == "strategy")
   strategy["contrast"]["feture"] = "planted"
   hand_authored["no_figure_reasons"] = "planted"
   messages = check_lessons.lint_schema(hand_authored, context)
   locations = " ".join(messages)

   assert "sections/0" in locations
   assert "sections/3" in locations
   assert "<root>" in locations


def test_the_new_caps_fire(context, hand_authored):
   prediction_of(hand_authored)["stem"]["text"] = " ".join(["word"] * 41)
   strategy = next(section for section in hand_authored["sections"] if section["type"] == "strategy")
   strategy["contrast"]["not_this"]["why_not"] = " ".join(["word"] * 21)
   hand_authored["no_figure_reason"] = " ".join(["word"] * 41)
   messages = " | ".join(check_lessons.lint_caps(hand_authored, context))

   assert "s1 stem is 41 words, and the cap is 40" in messages
   assert "contrast why_not is 21 words, and the cap is 20" in messages
   assert "no_figure_reason is 41 words, and the cap is 40" in messages


READER_LABEL_PLANTS = [
   ("strategy", "cue", "Cue:"),
   ("strategy", "method", "First line:"),
   ("strategy", "method", "First written line:"),
   ("strategy", "method", "Method:"),
   ("strategy", "method", "First step:"),
   ("strategy", "rival", "Rival:"),
   ("strategy", "rival", "Rivals:"),
   ("strategy", "separating_feature", "Separating feature:"),
   ("strategy", "separating_feature", "Feature:"),
   ("strategy", "contrast.feature", "Feature:"),
   ("strategy", "contrast.not_this.why_not", "Why not:"),
   ("prediction", "stem.text", "Predict."),
   ("prediction", "stem.text", "Predict:"),
   ("prediction", "stem.text", "Prediction."),
   ("prediction", "stem.text", "Prediction:"),
   ("prediction", "stem.text", "Predict"),
]


@pytest.mark.parametrize("section_type, field, label", READER_LABEL_PLANTS)
def test_a_served_field_opening_with_the_reader_label_is_refused(section_type, field, label, context, hand_authored):
   section = next(section for section in hand_authored["sections"] if section["type"] == section_type)
   *parents, leaf = field.split(".")
   holder = section

   for key in parents:
      holder = holder[key]

   holder[leaf] = "  " + label.upper() + " " + holder[leaf]
   messages = check_lessons.lint_served_text(hand_authored, context)
   expected = f"{section['id']} {field} starts with the reader's label {label!r}"

   assert expected in messages, messages


def test_a_prediction_stem_that_uses_predict_as_its_verb_is_served(context, hand_authored):
   prediction_of(hand_authored)["stem"]["text"] = "Predict the sign of \\(h'(1)\\) before differentiating."

   assert check_lessons.lint_served_text(hand_authored, context) == []


def test_error_record_words_are_exempt_from_served_text(context, hand_authored):
   block = next(section for section in hand_authored["sections"] if section["type"] == "common_error")
   block["observed_behavior"] += " (BC-ERR-02020)"
   block["scoring_consequence"] += " sg-25:20"

   assert check_lessons.lint_served_text(hand_authored, context) == []
