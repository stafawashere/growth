"""docs/agent/drawing-design.md, The compiler: the figure grammar is a twin of the web grammar, reads
only what the design allows, and never hands a string to anything that parses or runs code, nor a
tree to SymPy, which expands an integer power such as 9^9^9 in full.

The shared fixture tests/fixtures/drawing/expressions.json is read here and by
app/web/src/lessons/expression.parity.test.ts, so the two grammars agree on every listed case.
"""
import ast
import json
from pathlib import Path

import pytest

from app.agent.drawing import expression

REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
FIXTURE = json.loads((REPOSITORY_ROOT / "tests" / "fixtures" / "drawing" / "expressions.json").read_text())
PACKAGE_ROOT = REPOSITORY_ROOT / "app" / "agent" / "drawing"
FORBIDDEN_NAMES = {"eval", "exec", "compile", "sympify", "parse_expr", "lambdify", "__import__", "sympy"}


def _named(cases):
   return [pytest.param(case, id=case["expression"][:40]) for case in cases]


@pytest.mark.parametrize("case", _named(FIXTURE["cases"]))
def test_every_shared_case_has_the_listed_values(case):
   tree = expression.parse(case["expression"], (case["variable"],))

   for point, expected in case["points"]:
      value = expression.evaluate(tree, {case["variable"]: point})
      allowed = FIXTURE["tolerance"] * max(1.0, abs(expected))

      assert value is not None
      assert abs(value - expected) <= allowed


@pytest.mark.parametrize("case", _named(FIXTURE["undefined"]))
def test_every_shared_undefined_case_evaluates_to_none(case):
   tree = expression.parse(case["expression"], (case["variable"],))

   for point in case["points"]:
      assert expression.evaluate(tree, {case["variable"]: point}) is None


@pytest.mark.parametrize("case", _named(FIXTURE["refusals"] + FIXTURE["python_only_refusals"]))
def test_every_refusing_string_refuses(case):
   with pytest.raises(expression.ExpressionRefused):
      expression.parse(case["expression"], (case["variable"],))


@pytest.mark.parametrize(
   "accepted, refused",
   [
      ("x" + " " * 79, "x" + " " * 80),
      ("-" + "+".join(["x"] * 24), "--" + "+".join(["x"] * 24)),
      ("(" * 10 + "x" + ")" * 10, "(" * 11 + "x" + ")" * 11),
      ("sin(" * 10 + "x" + ")" * 10, "sin(" * 11 + "x" + ")" * 11),
   ],
   ids=["80 characters", "48 tokens", "depth 10", "call depth 10"],
)
def test_each_cap_holds_at_its_limit_and_refuses_one_past_it_as_oversized(accepted, refused):
   expression.parse(accepted)

   with pytest.raises(expression.ExpressionRefused) as refusal:
      expression.parse(refused)

   assert refusal.value.reason == "oversized"


def _forbidden_uses(source):
   found = []

   for node in ast.walk(ast.parse(source)):
      is_text = isinstance(node, ast.Constant) and isinstance(node.value, str)

      if isinstance(node, ast.Name):
         name = node.id
      elif isinstance(node, ast.Attribute):
         name = node.attr
      elif isinstance(node, ast.alias):
         name = node.asname or node.name.split(".")[-1]
      elif is_text:
         name = node.value
      else:
         continue

      if name in FORBIDDEN_NAMES:
         found.append(name)

   return found


def test_the_drawing_package_never_names_a_call_that_parses_or_runs_code_nor_sympy():
   sources = sorted(PACKAGE_ROOT.glob("*.py"))
   generation_kit = (REPOSITORY_ROOT / "app" / "generation" / "kit.py").read_text()

   assert {path.name for path in sources} >= {"__init__.py", "expression.py", "spec.py", "compile.py"}
   assert {"lambdify", "sympify"} <= set(_forbidden_uses(generation_kit))

   for path in sources:
      assert _forbidden_uses(path.read_text()) == [], path.name
