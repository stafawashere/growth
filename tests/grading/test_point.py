"""The per-point grader's gates, 11 P3 "Tests that gate the phase", unit tier.

test_three_decimal_cap: at most one rounding point is lost per question, never per part.
test_deterministic_precheck_priority: a mechanical point is never decided by the model when a
deterministic check can decide it.
test_disagreement_escalates (unit half): a split is escalated and provisional, never averaged.
The question records here are written for the tests, in the shape content/frq_items uses.
"""
import pytest

from app.grading import point as grader

LABELS = {
   "BC-PT-99004": "deterministic",
   "BC-PT-99005": "deterministic",
   "BC-PT-99001": "deterministic",
   "BC-PT-99010": "model_required",
}


def numeric_point(point_id, expected):
   return {
      "point_id": point_id,
      "point_type_id": "BC-PT-99004",
      "skills": ["BC-SKL-TEST"],
      "criterion": "the value",
      "eligible_only_if": [],
      "check": {"kind": "numeric_three_decimals", "expected": expected},
   }


def part(part_id, points):
   return {
      "id": part_id,
      "prompt": "Find it.",
      "setup_required": False,
      "answer_latex": "",
      "worked_solution": [],
      "points": points,
   }


def question(parts):
   return {
      "id": "FRQ-TEST-01",
      "archetype_id": "BC-QA-TEST",
      "stem": {"text": "A test question."},
      "skills": ["BC-SKL-TEST"],
      "parts": parts,
   }


def answered(answers):
   return {
      "parts": [
         {"part_id": part_id, "lines": [], "answer": answer}
         for part_id, answer in answers.items()
      ]
   }


def never_asked(*arguments):
   raise AssertionError("the model was asked about a point a deterministic check decides")


def earned_by(grading):
   return {decision.point_id: decision.earned for decision in grading.decisions}


def test_three_decimal_cap():
   """Three parts of one question, each answer rounded to two places. The cap is per question, so
   only the first rounding loss stands and the two in later parts are awarded; a per-part cap
   would have taken all three."""
   record = question([
      part("a", [numeric_point("a1", "log(4)")]),
      part("b", [numeric_point("b1", "sqrt(2)")]),
      part("c", [numeric_point("c1", "pi/3")]),
   ])
   work = answered({"a": "1.39", "b": "1.41", "c": "1.05"})

   grading = grader.grade_question(record, work, LABELS, never_asked)

   assert earned_by(grading) == {"a1": 0, "b1": 1, "c1": 1}
   assert grading.rounding_penalty_applied is True


def test_the_cap_does_not_forgive_a_wrong_value():
   record = question([part("a", [numeric_point("a1", "log(4)")]), part("b", [numeric_point("b1", "sqrt(2)")])])
   work = {"parts": [{"part_id": "a", "lines": [], "answer": "1.39"}, {"part_id": "b", "lines": [], "answer": "2.718"}]}

   grading = grader.grade_question(record, work, LABELS, never_asked)

   assert earned_by(grading) == {"a1": 0, "b1": 0}


def test_three_places_by_rounding_or_truncation_and_an_exact_answer_all_earn():
   record = question([
      part("a", [numeric_point("a1", "log(4)")]),
      part("b", [numeric_point("b1", "log(4)")]),
      part("c", [numeric_point("c1", "log(4)")]),
   ])
   work = {
      "parts": [
         {"part_id": "a", "lines": [], "answer": "1.386"},
         {"part_id": "b", "lines": [], "answer": "1.3862"},
         {"part_id": "c", "lines": [], "answer": "2\\ln 2"},
      ]
   }

   grading = grader.grade_question(record, work, LABELS, never_asked)

   assert earned_by(grading) == {"a1": 1, "b1": 1, "c1": 1}


def test_deterministic_precheck_priority():
   """A deterministic point with a check that settles is decided by the check, and the model is
   never called for it, whether the check passes or fails. A model_required point with the same
   work goes to the model."""
   asked = []

   def judge(record, part_record, point, work, strictness, label):
      asked.append(point["point_id"])

      return {"decision": "earned", "evidence_quote": "", "rule_field": "earns", "rule_cited": "x", "eligibility_note": ""}

   exact = {
      "point_id": "a1",
      "point_type_id": "BC-PT-99004",
      "skills": ["BC-SKL-TEST"],
      "criterion": "the derivative",
      "eligible_only_if": [],
      "check": {"kind": "sympy_equivalence", "target": "answer", "expected": "2*x*exp(x**2)", "variable": "x"},
   }
   wrong = dict(exact, point_id="a2", check=dict(exact["check"], expected="exp(x**2)"))
   judged = dict(exact, point_id="a3", point_type_id="BC-PT-99010")
   record = question([part("a", [exact, wrong, judged])])
   work = {"parts": [{"part_id": "a", "lines": [], "answer": "f'(x) = 2xe^{x^2}"}]}

   grading = grader.grade_question(record, work, LABELS, judge)
   decisions = grading.by_point()

   assert decisions["a1"].decided_by == grader.DETERMINISTIC
   assert decisions["a1"].earned == 1
   assert decisions["a2"].decided_by == grader.DETERMINISTIC
   assert decisions["a2"].earned == 0
   assert decisions["a3"].decided_by == grader.MODEL
   assert asked == ["a3", "a3", "a3"]


def test_an_unsettled_check_falls_through_to_the_model():
   asked = []

   def judge(record, part_record, point, work, strictness, label):
      asked.append(point["point_id"])

      return {"decision": "not_earned", "evidence_quote": "", "rule_field": "earns", "rule_cited": "x", "eligibility_note": ""}

   unreadable = {
      "point_id": "a1",
      "point_type_id": "BC-PT-99004",
      "skills": ["BC-SKL-TEST"],
      "criterion": "the value",
      "eligible_only_if": [],
      "check": {"kind": "sympy_equivalence", "target": "answer", "expected": "3", "variable": "x"},
   }
   record = question([part("a", [unreadable])])
   work = {"parts": [{"part_id": "a", "lines": [], "answer": "\\begin{matrix} 3 \\end{matrix}"}]}

   grading = grader.grade_question(record, work, LABELS, judge)

   assert grading.decisions[0].decided_by == grader.MODEL
   assert grading.decisions[0].deterministic_check["outcome"] == "unsettled"
   assert asked == ["a1", "a1", "a1"]


def scripted(decisions_by_label, quote=""):
   def judge(record, part_record, point, work, strictness, label):
      return {
         "decision": decisions_by_label[label],
         "evidence_quote": quote,
         "rule_field": "earns",
         "rule_cited": "the clause",
         "eligibility_note": "",
      }

   return judge


JUDGED_POINT = {
   "point_id": "a1",
   "point_type_id": "BC-PT-99010",
   "skills": ["BC-SKL-TEST"],
   "criterion": "the justification",
   "eligible_only_if": [],
   "check": None,
}
JUDGED_WORK = {"parts": [{"part_id": "a", "lines": [{"kind": "text", "content": "f' > 0 on (0, 2)"}], "answer": ""}]}


@pytest.mark.parametrize(
   "split",
   [
      {"temp0_a": "earned", "temp0_b": "earned", "strict": "not_earned"},
      {"temp0_a": "earned", "temp0_b": "not_earned", "strict": "earned"},
      {"temp0_a": "not_earned", "temp0_b": "earned", "strict": "not_earned"},
   ],
)
def test_a_split_escalates_and_is_never_averaged(split):
   record = question([part("a", [dict(JUDGED_POINT)])])

   grading = grader.grade_question(record, JUDGED_WORK, LABELS, scripted(split))
   decision = grading.decisions[0]

   assert decision.decided_by == grader.ESCALATED
   assert decision.earned is None
   assert decision.provisional is True
   assert decision.agreement == grader.SPLIT
   assert len(decision.samples) == 3


def test_unanimous_samples_publish_the_decision():
   record = question([part("a", [dict(JUDGED_POINT)])])
   unanimous = {"temp0_a": "not_earned", "temp0_b": "not_earned", "strict": "not_earned"}

   grading = grader.grade_question(record, JUDGED_WORK, LABELS, scripted(unanimous))
   decision = grading.decisions[0]

   assert decision.decided_by == grader.MODEL
   assert decision.earned == 0
   assert decision.provisional is False


def test_a_quote_that_is_not_on_the_page_escalates_a_unanimous_point():
   record = question([part("a", [dict(JUDGED_POINT)])])
   unanimous = {"temp0_a": "earned", "temp0_b": "earned", "strict": "earned"}

   grading = grader.grade_question(record, JUDGED_WORK, LABELS, scripted(unanimous, quote="f'' < 0 on (0, 2)"))

   assert grading.decisions[0].decided_by == grader.ESCALATED


def test_a_quote_written_without_the_math_delimiters_is_on_the_page():
   record = question([part("a", [dict(JUDGED_POINT)])])
   work = {"parts": [{"part_id": "a", "lines": [{"kind": "text", "content": "\\(f'\\) is positive on \\((0, 2)\\)"}], "answer": ""}]}
   unanimous = {"temp0_a": "earned", "temp0_b": "earned", "strict": "earned"}

   grading = grader.grade_question(record, work, LABELS, scripted(unanimous, quote="f' is positive on (0, 2)"))

   assert grading.decisions[0].decided_by == grader.MODEL
   assert grading.decisions[0].earned == 1


def test_a_lost_point_makes_its_dependant_ineligible_and_a_provisional_one_provisional():
   setup = {
      "point_id": "a1",
      "point_type_id": "BC-PT-99001",
      "skills": ["BC-SKL-TEST"],
      "criterion": "the integral",
      "eligible_only_if": [],
      "check": {"kind": "bounds_match", "lower": "0", "upper": "2", "integrand": None, "variable": "x"},
   }
   answer = numeric_point("a2", "8/3")
   answer["eligible_only_if"] = ["a1"]
   record = question([part("a", [setup, answer])])
   wrong_bounds = {"parts": [{"part_id": "a", "lines": [{"kind": "math", "content": "\\int_{0}^{3} x^{2}\\,dx"}], "answer": "\\frac{8}{3}"}]}

   grading = grader.grade_question(record, wrong_bounds, LABELS, never_asked)
   decisions = grading.by_point()

   assert decisions["a1"].earned == 0
   assert decisions["a2"].earned == 0
   assert "a1" in decisions["a2"].eligibility_note


def test_no_judge_leaves_judged_points_pending_and_decides_the_rest():
   record = question([part("a", [numeric_point("a1", "1/2"), dict(JUDGED_POINT, point_id="a2")])])
   work = {"parts": [{"part_id": "a", "lines": [], "answer": "0.5"}]}

   grading = grader.grade_question(record, work, LABELS, None)
   decisions = grading.by_point()

   assert decisions["a1"].earned == 1
   assert decisions["a2"].decided_by == grader.PENDING
   assert decisions["a2"].provisional is True


def test_a_failed_check_after_a_lost_earlier_result_is_judged_as_follow_through():
   """Part (a) is wrong, and part (b) carries the wrong value forward correctly. The fixed key
   fails (b), so the model judges it as follow-through; without follows_from it stays failed and
   the model is never asked."""
   asked = []

   def judge(record, part_record, point, work, strictness, label):
      asked.append((point["point_id"], point["criterion"]))

      return {"decision": "earned", "evidence_quote": "", "rule_field": "eligibility_after_error", "rule_cited": "x", "eligibility_note": ""}

   carried = numeric_point("b1", "2*log(4)")
   carried["follows_from"] = ["a1"]
   record = question([part("a", [numeric_point("a1", "log(4)")]), part("b", [carried])])
   work = answered({"a": "1.5", "b": "3.0"})

   grading = grader.grade_question(record, work, LABELS, judge)
   decisions = grading.by_point()

   assert decisions["a1"].earned == 0
   assert decisions["b1"].decided_by == grader.MODEL
   assert decisions["b1"].earned == 1
   assert "follow-through" in decisions["b1"].eligibility_note
   assert len(asked) == 3
   assert all("consistency with the student's own earlier result" in criterion for _point, criterion in asked)

   carried.pop("follows_from")
   asked.clear()

   plain = grader.grade_question(record, work, LABELS, judge)

   assert plain.by_point()["b1"].earned == 0
   assert asked == []
