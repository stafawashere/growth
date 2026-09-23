"""Trial harness for the Option E item template, docs/plan/13-ai-engineering.md.

The question this answers, and the only one: can a model author a parameterised item
template whose instantiations are mathematically correct and cleanly rendered across
300 parameter draws? The human-written proof of concept scored 8.5 to 10.1 percent of
steps with a surface defect and 4.5 percent of draws vacuous. The bar is set below.

Two subcommands, deliberately split so the expensive half runs once and the free half
runs as often as it likes.

  generate   one Opus 5 call per archetype, writes a template artifact per call.
             Needs ANTHROPIC_API_KEY in the environment. This is the paid half.
  draw       instantiates a template over N seeded parameter draws and counts defects.
             No network, no key. This is the half the tests exercise.

Model output is data and is never executed. Every expression string a template carries
is checked against EXPRESSION_ALLOWED before it reaches SymPy's parser, because
sympify evaluates its input and a template is untrusted by construction
(docs/plan/09-security-and-privacy.md, "Never instructions").
"""
import argparse
import json
import os
import random
import re
import sys
import urllib.request
from pathlib import Path

import sympy

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from app.items.verify import equivalence

MESSAGES_URL = "https://api.anthropic.com/v1/messages"
ANTHROPIC_VERSION = "2023-06-01"
MODEL = "claude-opus-5"
EFFORT = "medium"
MAX_OUTPUT_TOKENS = 16000

DRAWS = 300
MAX_DRAW_ATTEMPTS = 60

GATE_DRAWS = 60
MAX_GENERATION_ATTEMPTS = 3

# [inferred] 50 times the 40 published items per archetype, so selection has room to avoid a
# recently served parameter tuple instead of being forced onto the only one left. The first
# trial produced spaces of 180, 144 and 12, and 12 cannot fill a bank of 40 at all. What would
# settle the number: the measured repeat rate at a known space over a real 230 day cycle.
MIN_DRAW_SPACE = 2000

SURFACE_DEFECT_BAR = 0.02
KEY_DISAGREEMENT_BAR = 0

# docs/plan/04-item-generation.md: four options on a current-framework multiple choice item, so a
# template carries exactly three distractors. The representations whose items cannot be posed
# without a figure, by the taxonomy's own names: graphical, numerical table, slope field and
# geometric diagram. A template declares the one representation it serves.
OPTIONS_PER_ITEM = 4
DISTRACTORS_PER_ITEM = OPTIONS_PER_ITEM - 1
FIGURE_REPRESENTATIONS = frozenset({"BC-REP-02", "BC-REP-03", "BC-REP-07", "BC-REP-08"})
# Bejar's radicals and incidentals, with the finding that isomorphs do not share a difficulty
# (docs/plan/13-ai-engineering.md, "Radicals and incidentals"). A template declares each
# parameter's role, and an incidental is checked: varying it alone may not change the
# structure of any step or of the key. Distractor composition is a radical by construction.
PARAMETER_ROLES = ("radical", "incidental")
INCIDENTAL_VARIANTS = 32
FIGURE_KINDS = ("function_graph", "slope_field", "table", "region", "parametric_curve",
                "polar_curve", "vector_diagram", "number_line", "geometric_diagram")

EXPRESSION_ALLOWED = re.compile(r"^[A-Za-z0-9_+\-*/^(),.\s=<>!]+$")

ALLOWED_FUNCTIONS = {
   "sin", "cos", "tan", "sec", "csc", "cot", "asin", "acos", "atan",
   "sinh", "cosh", "tanh", "exp", "log", "ln", "sqrt", "Abs", "pi", "E",
   "Rational", "Integer", "Eq", "Ne", "Lt", "Le", "Gt", "Ge", "And", "Or",
   "Limit", "oo", "Symbol", "Derivative", "Integral",
}

PLACEHOLDER = re.compile(r"<<([A-Za-z_][A-Za-z0-9_]*)>>")

DOUBLED_SIGN = re.compile(r"[+\-]\s*[+\-]")


class TemplateRefused(Exception):
   """Raised instead of parsing. Carries what was refused and why, never the payload."""


def _refuse_unsafe_expression(name, text, declared):
   looks_like_an_expression = EXPRESSION_ALLOWED.match(text) is not None

   if not looks_like_an_expression:
      raise TemplateRefused(f"expression {name!r} contains a character outside the allowed set")

   words = set(re.findall(r"[A-Za-z_][A-Za-z0-9_]*", text))
   unknown = words - ALLOWED_FUNCTIONS - set(declared)

   if unknown:
      raise TemplateRefused(
         f"expression {name!r} names {sorted(unknown)}, which is neither a declared parameter "
         f"or expression nor an allowed function")


def parse_expression(name, text, local_names):
   _refuse_unsafe_expression(name, text, local_names)
   symbols = {n: sympy.Symbol(n) for n in local_names}

   return sympy.sympify(text, locals=symbols)


def draw_parameters(template, rng):
   """One draw satisfying every constraint, or None when the domain is too tight."""
   spec = template["parameters"]
   constraints = template.get("constraints") or []

   for _attempt in range(MAX_DRAW_ATTEMPTS):
      draw = {}

      for parameter in spec:
         draw[parameter["name"]] = _draw_one(parameter, rng)

      satisfied = _constraints_hold(constraints, draw)

      if satisfied:
         return draw

   return None


def _domain(parameter):
   excluded = set(parameter.get("exclude") or [])

   if parameter.get("kind") == "choice":
      return [v for v in parameter["choices"] if v not in excluded]

   return [v for v in range(parameter["low"], parameter["high"] + 1) if v not in excluded]


def _draw_one(parameter, rng):
   kind = parameter.get("kind", "integer")
   excluded = set(parameter.get("exclude") or [])

   if kind == "choice":
      options = [v for v in parameter["choices"] if v not in excluded]

      return rng.choice(options)

   low, high = parameter["low"], parameter["high"]
   candidates = [v for v in range(low, high + 1) if v not in excluded]

   return rng.choice(candidates)


def _constraints_hold(constraints, draw):
   for index, text in enumerate(constraints):
      predicate = parse_expression(f"constraint[{index}]", text, draw.keys())
      value = predicate.subs(draw)
      holds = bool(value) is True

      if not holds:
         return False

   return True


FREE_SYMBOLS = ("x", "t", "y")


def evaluate(template, draw):
   """Resolve the named expressions in declaration order against one parameter draw.

   Declaration order is the contract: an expression may reference any parameter and any
   expression declared before it, and nothing else. Substituting the whole accumulated
   values map at each step is what makes that true.
   """
   clashes = set(draw) & set(FREE_SYMBOLS)

   if clashes:
      raise TemplateRefused(f"parameter {sorted(clashes)} shadows a free symbol")

   values = {name: sympy.Integer(value) if isinstance(value, int) else sympy.sympify(value)
             for name, value in draw.items()}

   for declared in template["expressions"]:
      name, text = declared["name"], declared["expr"]
      expression = parse_expression(name, text, set(FREE_SYMBOLS) | set(values))
      values[name] = sympy.simplify(expression.subs(values))

   return values


def render(text, values):
   """Substitute {name} with the LaTeX of that value. Never executes anything."""
   def _one(match):
      name = match.group(1)
      known = name in values

      if not known:
         raise TemplateRefused(f"template names {name!r}, which the expressions do not define")

      return sympy.latex(values[name])

   return PLACEHOLDER.sub(_one, text)


def uses_math_mode(text):
   """A template that writes formulas as plain text renders x^3 literally to a student, and the
   balance check passes trivially on zero dollar signs. Found on the first real template."""
   return text.count("$") >= 2


def key_check_is_tautological(template):
   """Comparing the key against the last step is worth something only when the two are written
   by different routes.

   Symbolic equality is the wrong test: inside one template the key and the final step have to
   be mathematically equal, so a symbolic check would flag every correct template. What makes
   the comparison vacuous is a COPY, not an agreement. Three shapes of copy are caught: the key
   names the same expression as the final step, the key's declared body is that expression's
   name, and the key's declared body is character-identical to the final step's. A key written
   as a different arrangement of the parameters that happens to agree is exactly what the check
   wants and is left alone.

   Measured across 18 real templates: 14 declared a key equal to the final step's and 12 of
   those were character-identical, while the earlier name-only check called none of them
   tautological.
   """
   with_expressions = [s for s in template["steps"] if s.get("expr")]
   nothing_to_compare = len(with_expressions) == 0

   if nothing_to_compare:
      return True

   key_name = template["key"]["name"]
   final_name = with_expressions[-1]["expr"]

   if key_name == final_name:
      return True

   bodies = {e["name"]: e["expr"] for e in template["expressions"]}
   key_body = bodies.get(key_name)
   final_body = bodies.get(final_name)
   undeclared = key_body is None or final_body is None

   if undeclared:
      return False

   normalise = lambda text: "".join(text.split())
   aliases_the_final_step = normalise(key_body) == final_name
   copies_the_final_body = normalise(key_body) == normalise(final_body)

   return aliases_the_final_step or copies_the_final_body


_REGISTRY = {}


def registry():
   """The library ids a template may reference: active BC-ERR ids, BC-PT ids, and each
   archetype's record. Read once from data/, never written."""
   if _REGISTRY:
      return _REGISTRY

   errors = json.loads((REPO / "data" / "errors.json").read_text())["errors"]
   point_types = json.loads((REPO / "data" / "scoring_points.json").read_text())["point_types"]
   archetypes = json.loads((REPO / "data" / "archetypes.json").read_text())["archetypes"]

   _REGISTRY["error_ids"] = frozenset(r["id"] for r in errors if r.get("status") != "retired")
   _REGISTRY["error_skills"] = {r["id"]: frozenset(r.get("skills") or []) for r in errors
                                if r.get("status") != "retired"}
   _REGISTRY["point_type_ids"] = frozenset(r["id"] for r in point_types if r.get("status") != "retired")
   _REGISTRY["archetypes"] = {r["id"]: r for r in archetypes}

   return _REGISTRY


def contract_check(template, library=None):
   """The four checks the item contract in 04 imposes that no draw can reveal.

   representation_undeclared: the template does not say which of the archetype's
      representations it serves, so nothing can decide whether it needs a figure.
   figure_missing: the declared representation is one whose items cannot be posed without a
      graph, table, slope field or diagram, and the template carries no figure spec.
   unresolved_error_paths: distractors whose error_path is not an active BC-ERR id, which
      rejection rule 7 rejects one by one.
   unresolved_point_types: steps whose point_type_id is not a BC-PT id, which rule 9 rejects.
   option_count_wrong: the key plus the distractors is not four options.
   """
   library = registry() if library is None else library
   archetype = library["archetypes"].get(template.get("archetype_id"), {})
   allowed = archetype.get("representations") or []
   declared = template.get("representation")
   representation_undeclared = declared is None or declared not in allowed
   needs_figure = declared in FIGURE_REPRESENTATIONS
   figure_missing = needs_figure and not template.get("figure")

   distractors = template.get("distractors") or []
   error_paths = [d.get("error_path") for d in distractors]
   unresolved_error_paths = sum(1 for path in error_paths if path not in library["error_ids"])

   tagged = [s.get("point_type_id") for s in template["steps"] if s.get("point_type_id")]
   unresolved_point_types = sum(1 for tag in tagged if tag not in library["point_type_ids"])

   option_count = 1 + len(distractors)
   option_count_wrong = option_count != OPTIONS_PER_ITEM

   clean = (not representation_undeclared and not figure_missing and unresolved_error_paths == 0
            and unresolved_point_types == 0 and not option_count_wrong)

   return {
      "representation": declared,
      "representation_undeclared": representation_undeclared,
      "figure_required": needs_figure,
      "figure_missing": figure_missing,
      "distractors": len(distractors),
      "unresolved_error_paths": unresolved_error_paths,
      "point_types_tagged": len(tagged),
      "unresolved_point_types": unresolved_point_types,
      "option_count": option_count,
      "option_count_wrong": option_count_wrong,
      "clean": clean,
   }


def structure(value):
   """What an incidental may not move: whether a value is zero, its head, the functions it
   contains, its degree in the free symbol when polynomial, and its arity. The sign of a number
   is not structure, because a negative slope is solved the same way as a positive one; a zero
   is, because it deletes a term. Two values with the same structure are solved by the same
   path."""
   if value is None:
      return None

   x = sympy.Symbol("x")

   if value.is_number:
      return ("number", "zero" if value == 0 else "nonzero")

   heads = tuple(sorted({f.func.__name__ for f in value.atoms(sympy.Function)}))
   degree = sympy.degree(value, x) if value.is_polynomial(x) else None

   return (value.func.__name__, heads, degree, len(value.args))


def path_signature(template, draw):
   values = evaluate(template, draw)
   steps = tuple(structure(values.get(step.get("expr"))) for step in template["steps"])
   key = structure(values.get(template["key"]["name"]))

   return steps + (key,)


def incidental_check(template, rng):
   """Every parameter needs a declared role. For each incidental, the base draw is varied on
   that parameter alone over its whole domain, or over a sample of INCIDENTAL_VARIANTS values
   when the domain is larger than that, and the path signature of every variant must equal
   the base's."""
   undeclared = [p["name"] for p in template["parameters"] if p.get("role") not in PARAMETER_ROLES]
   incidentals = [p for p in template["parameters"] if p.get("role") == "incidental"]
   radicals = [p["name"] for p in template["parameters"] if p.get("role") == "radical"]
   changes_path = []
   base = draw_parameters(template, rng)
   nothing_to_vary = base is None or undeclared

   if nothing_to_vary:
      return {"parameter_role_undeclared": undeclared, "incidental_changes_path": changes_path,
              "radicals": radicals + ["distractor composition"], "incidentals_checked": 0}

   constraints = template.get("constraints") or []
   base_signature = path_signature(template, base)

   for parameter in incidentals:
      name = parameter["name"]
      candidates = [value for value in _domain(parameter) if value != base[name]]
      too_many = len(candidates) > INCIDENTAL_VARIANTS

      if too_many:
         candidates = rng.sample(candidates, INCIDENTAL_VARIANTS)

      for value in candidates:
         variant = dict(base)
         variant[name] = value

         if not _constraints_hold(constraints, variant):
            continue

         moved = path_signature(template, variant) != base_signature

         if moved:
            changes_path.append(name)
            break

   return {"parameter_role_undeclared": undeclared, "incidental_changes_path": changes_path,
           "radicals": radicals + ["distractor composition"], "incidentals_checked": len(incidentals)}


def draw_space(template):
   """How many distinct parameter tuples exist before constraints. A template whose space is
   smaller than the bank it has to fill cannot fill it."""
   size = 1

   for parameter in template["parameters"]:
      if parameter.get("kind") == "choice":
         size *= len(parameter["choices"])
      else:
         span = parameter["high"] - parameter["low"] + 1
         size *= max(span - len(parameter.get("exclude") or []), 1)

   return size


def latex_is_balanced(text):
   dollars_balanced = text.count("$") % 2 == 0
   braces_balanced = text.count("{") == text.count("}")
   delimiters_balanced = text.count(r"\left") == text.count(r"\right")

   return dollars_balanced and braces_balanced and delimiters_balanced


def has_doubled_sign(text):
   return DOUBLED_SIGN.search(text) is not None


def step_is_vacuous(previous, current):
   """A step that restates the previous one under this draw teaches nothing."""
   nothing_before = previous is None

   if nothing_before:
      return False

   verdict = equivalence(previous, current)

   return verdict == "equivalent"


def instantiate(template, draw):
   """One item from one draw. Returns the rendered parts and the defects found in them."""
   values = evaluate(template, draw)
   stem = render(template["stem"]["template"], values)

   rendered_steps = []
   defects = {"unbalanced_latex": 0, "doubled_sign": 0, "vacuous_step": 0, "plain_text": 0}
   examples = {}
   previous = None

   for step in template["steps"]:
      text = render(step["text"], values)
      rendered_steps.append(text)

      if not latex_is_balanced(text):
         defects["unbalanced_latex"] += 1
         examples.setdefault("unbalanced_latex", text)

      if has_doubled_sign(text):
         defects["doubled_sign"] += 1
         examples.setdefault("doubled_sign", text)

      if not uses_math_mode(text):
         defects["plain_text"] += 1
         examples.setdefault("plain_text", text)

      current = values.get(step.get("expr"))
      carries_an_expression = current is not None

      if carries_an_expression and step_is_vacuous(previous, current):
         defects["vacuous_step"] += 1

      if carries_an_expression:
         previous = current

   if not latex_is_balanced(stem):
      defects["unbalanced_latex"] += 1

   if has_doubled_sign(stem):
      defects["doubled_sign"] += 1

   if not uses_math_mode(stem):
      defects["plain_text"] += 1

   key = _key_value(template, values)
   final = previous

   return {
      "stem": stem,
      "steps": rendered_steps,
      "key": key,
      "final_step_value": final,
      "defects": defects,
      "examples": examples,
      "step_count": len(rendered_steps) + 1,
   }


def _key_value(template, values):
   name = template["key"]["name"]
   resolved = name in values

   if not resolved:
      raise TemplateRefused(f"key names {name!r}, which the expressions do not define")

   return values[name]


def key_agrees(key, final):
   nothing_to_compare = key is None or final is None

   if nothing_to_compare:
      return "unsettled"

   return equivalence(key, final)


def run_draws(template, draws=DRAWS, seed=20260920):
   rng = random.Random(seed)
   totals = {"unbalanced_latex": 0, "doubled_sign": 0, "vacuous_step": 0, "plain_text": 0}
   steps_seen = 0
   examples = {}
   key_disagreements = 0
   key_unsettled = 0
   refused_draws = 0
   raised = 0
   first_failure = None

   for _index in range(draws):
      try:
         draw = draw_parameters(template, rng)
      except (TemplateRefused, TypeError, ValueError, ZeroDivisionError, AttributeError) as failure:
         raised += 1

         if first_failure is None:
            first_failure = {"stage": "draw_parameters", "exception": type(failure).__name__,
                             "detail": str(failure)[:200]}
         continue

      if draw is None:
         refused_draws += 1
         continue

      try:
         item = instantiate(template, draw)
      except (TemplateRefused, TypeError, ValueError, ZeroDivisionError, AttributeError) as failure:
         raised += 1

         if first_failure is None:
            first_failure = {"stage": "instantiate",
                             "draw": {k: str(v) for k, v in draw.items()},
                             "exception": type(failure).__name__,
                             "detail": str(failure)[:200]}
         continue

      steps_seen += item["step_count"]

      for name, count in item["defects"].items():
         totals[name] += count

      for name, text in item["examples"].items():
         examples.setdefault(name, {"text": text, "draw": {k: str(v) for k, v in draw.items()}})

      verdict = key_agrees(item["key"], item["final_step_value"])

      if verdict == "not_equivalent":
         key_disagreements += 1

         if first_failure is None:
            first_failure = {"draw": {k: str(v) for k, v in draw.items()},
                             "key": str(item["key"]),
                             "final_step": str(item["final_step_value"])}

      if verdict == "unsettled":
         key_unsettled += 1

   contract = contract_check(template)

   try:
      roles = incidental_check(template, rng)
   except (TemplateRefused, TypeError, ValueError, ZeroDivisionError, AttributeError) as failure:
      roles = {"parameter_role_undeclared": [], "incidental_changes_path": [],
               "radicals": [], "incidentals_checked": 0,
               "exception": type(failure).__name__}

   roles_clean = not roles["parameter_role_undeclared"] and not roles["incidental_changes_path"] \
      and "exception" not in roles
   plain_text_blocks = totals["plain_text"]
   surface_defects = totals["unbalanced_latex"] + totals["doubled_sign"] + plain_text_blocks
   rendered_nothing = steps_seen == 0
   surface_rate = None if rendered_nothing else surface_defects / steps_seen
   vacuous_rate = None if rendered_nothing else totals["vacuous_step"] / steps_seen

   return {
      "template_id": template.get("template_id"),
      "archetype_id": template.get("archetype_id"),
      "draws_requested": draws,
      "draws_refused_by_constraints": refused_draws,
      "draws_that_raised": raised,
      "steps_rendered": steps_seen,
      "unbalanced_latex": totals["unbalanced_latex"],
      "plain_text_blocks": totals["plain_text"],
      "key_check_is_tautological": key_check_is_tautological(template),
      "draw_space": draw_space(template),
      "doubled_sign": totals["doubled_sign"],
      "vacuous_step": totals["vacuous_step"],
      "surface_defect_rate": None if surface_rate is None else round(surface_rate, 4),
      "vacuous_step_rate": None if vacuous_rate is None else round(vacuous_rate, 4),
      "rendered_nothing": rendered_nothing,
      "key_disagreements": key_disagreements,
      "key_unsettled": key_unsettled,
      "first_failure": first_failure,
      "examples": examples,
      "draw_space_floor": MIN_DRAW_SPACE,
      "contract": contract,
      "roles": roles,
      "passes_bar": (not rendered_nothing
                     and surface_rate < SURFACE_DEFECT_BAR
                     and key_disagreements == KEY_DISAGREEMENT_BAR
                     and not key_check_is_tautological(template)
                     and raised == 0
                     and draw_space(template) >= MIN_DRAW_SPACE
                     and contract["clean"]
                     and roles_clean),
   }


TEMPLATE_SCHEMA = {
   "type": "object",
   "additionalProperties": False,
   "required": ["archetype_id", "template_id", "representation", "parameters", "expressions",
                "key", "stem", "steps", "distractors"],
   "properties": {
      "archetype_id": {"type": "string"},
      "template_id": {"type": "string"},
      "representation": {"type": "string"},
      "figure": {
         "type": "object",
         "additionalProperties": False,
         "required": ["kind", "labels"],
         "properties": {
            "kind": {"enum": list(FIGURE_KINDS)},
            "domain": {"type": "array", "items": {"type": "string"}},
            "range": {"type": "array", "items": {"type": "string"}},
            "curves": {"type": "array", "items": {"type": "string"}},
            "marks": {"type": "array", "items": {"type": "string"}},
            "labels": {
               "type": "array",
               "items": {
                  "type": "object",
                  "additionalProperties": False,
                  "required": ["text", "anchor"],
                  "properties": {"text": {"type": "string"},
                                 "anchor": {"type": "array", "items": {"type": "string"}}},
               },
            },
         },
      },
      "parameters": {
         "type": "array",
         "items": {
            "type": "object",
            "additionalProperties": False,
            "required": ["name", "kind", "role"],
            "properties": {
               "name": {"type": "string"},
               "kind": {"enum": ["integer", "choice"]},
               "role": {"enum": list(PARAMETER_ROLES)},
               "low": {"type": "integer"},
               "high": {"type": "integer"},
               "exclude": {"type": "array", "items": {"type": "integer"}},
               "choices": {"type": "array", "items": {"type": "integer"}},
            },
         },
      },
      "constraints": {"type": "array", "items": {"type": "string"}},
      "expressions": {
         "type": "array",
         "items": {
            "type": "object",
            "additionalProperties": False,
            "required": ["name", "expr"],
            "properties": {"name": {"type": "string"}, "expr": {"type": "string"}},
         },
      },
      "key": {
         "type": "object",
         "additionalProperties": False,
         "required": ["name"],
         "properties": {"name": {"type": "string"}, "form": {"type": "string"}},
      },
      "stem": {
         "type": "object",
         "additionalProperties": False,
         "required": ["template"],
         "properties": {"template": {"type": "string"}},
      },
      "steps": {
         "type": "array",
         "items": {
            "type": "object",
            "additionalProperties": False,
            "required": ["text"],
            "properties": {
               "text": {"type": "string"},
               "expr": {"type": "string"},
               "point_type_id": {"type": "string"},
               "rule_named": {"type": "string"},
            },
         },
      },
      "distractors": {
         "type": "array",
         "items": {
            "type": "object",
            "additionalProperties": False,
            "required": ["expr", "mechanism"],
            "properties": {
               "expr": {"type": "string"},
               "mechanism": {"type": "string"},
               "error_path": {"type": "string"},
            },
         },
      },
   },
}

INSTRUCTIONS = r"""You author one parameterised item template for an AP Calculus BC practice
bank. The template is executed by a program, not read by a person, so every field has to be
machine correct rather than merely plausible.

The program does this with what you return, in this order. It draws one value for each entry
in parameters. It discards the draw unless every string in constraints evaluates true under
it. It then resolves expressions in the order they appear in the array, substituting the drawn
parameters and any expression already resolved. It renders stem.template and every steps[].text by replacing
each <<name>> with the LaTeX of that value. It compares the value named by key against the value
named by the last step's expr and rejects the template if they disagree.

Rules that the program enforces and that a violation of makes the template unusable.

Every string in expressions and constraints is parsed by SymPy. Use only arithmetic, **, and
these names: sin cos tan sec csc cot asin acos atan sinh cosh tanh exp log sqrt Abs pi E
Rational Integer Eq Ne Lt Le Gt Ge And Or oo. Parameter names and expression names must be one
or two characters. Nothing else is accepted.

Substitution uses <<name>>, never braces. Braces belong to LaTeX and the program does not
touch them, so write \int_{a}^{b} and \frac{1}{2} exactly as LaTeX wants them. Every <<name>>
in stem.template or a step's text must be an expressions[].name or a parameter name.

Write every formula inside math mode, $ ... $. A step with no math delimiters renders as plain
text and is rejected.

Never name the key after the last step's expression. The key is compared against the last step
to catch a template whose stem and solution disagree, and naming them the same makes that
comparison compare a value with itself.

Write the prose so no substitution can produce a doubled sign. Never write "x - <<c>>" or "A - <<B>>" when the substituted value can be negative, because
that renders as "- -". Write the whole signed term as its own expression and substitute that.

Never write a step that restates the previous step's value. Under some draws an operation is
the identity, and the program counts that as a defect. Use constraints to exclude the draws
that make a step vacuous.

The parameter domains together must admit at least 2000 distinct tuples before constraints,
because one template has to fill a bank of forty items with room for selection to avoid a
recently served draw. Reaching that by allowing negative values is fine and is expected; what
is not fine is prose that renders a doubled sign when it does. Write the signed term as its own
expression.

Choose parameter domains so that every draw is a well posed calculus problem: no division by
zero, no logarithm of a non-positive quantity, no square root of a negative, no degenerate
interval.

The steps must follow the archetype's expected_solution_path in order, one step per entry.
Tag a step with its point_type_id when the archetype lists point types.

Declare in representation the one BC-REP id from the archetype's representations that this
template serves. If it is BC-REP-02 (graphical), BC-REP-03 (numerical table), BC-REP-07 (slope
field) or BC-REP-08 (geometric diagram), the item cannot be posed without a figure, so include a
figure object: a kind from the schema, curves or marks as expression strings in the same
allowed grammar, and every label inside the figure with an anchor. Write nothing that only a
drawn image could carry into the stem.

Give every parameter a role. An incidental is a parameter whose value changes the numbers
and nothing else: every step keeps its form, no step becomes trivial, the key keeps its form.
A radical changes what the solver has to do, such as which rule applies, how many terms
appear, or whether a case splits. The program varies each incidental on its own and rejects
the template if the structure of any step or of the key moves. When in doubt, declare radical.

Include exactly three distractors, because an item has four options. Each distractor carries
error_path, which must be one of the allowed_error_paths ids given with the archetype; those
are the BC-ERR records reachable from the archetype's skills. A distractor whose error_path
is anything else is rejected. Each point_type_id on a step must be one of the archetype's
point_types, which are BC-PT ids; never a BC-SKL id.

Return only the template object."""


def defect_feedback(template, report):
   """The retry message. Names every check that failed, with the measured rate and one rendered
   example from a real draw, because a model asked to fix an unnamed defect guesses."""
   lines = []
   space = draw_space(template)

   if report["rendered_nothing"]:
      lines.append("No draw rendered at all, so nothing below was measured.")

   if report["draws_that_raised"] > 0:
      failure = report["first_failure"] or {}
      lines.append(
         f"{report['draws_that_raised']} of {report['draws_requested']} draws could not be "
         f"rendered at all. First one: {json.dumps(failure)}. A name used in the prose is not "
         f"declared in parameters or expressions, or an expression divides by zero on that draw."
      )

   if space < MIN_DRAW_SPACE:
      lines.append(
         f"The parameter domains admit only {space} distinct tuples, and the bank needs at "
         f"least {MIN_DRAW_SPACE}. Widen the domains or add a parameter. Do not widen them by "
         f"admitting values that make the prose render a doubled sign; fix the prose instead."
      )

   named = (("doubled_sign", "steps render a doubled sign such as \"- -\" or \"+ -\""),
            ("plain_text_blocks", "blocks carry no math delimiters, so the formula renders as plain text"),
            ("unbalanced_latex", "blocks have unbalanced dollar signs, braces or left and right"),
            ("vacuous_step", "steps restate the previous step's value under this draw"))

   for key, description in named:
      count = report[key]

      if count == 0:
         continue

      share = count / report["steps_rendered"]
      example = report["examples"].get(key.replace("_blocks", ""))
      lines.append(f"{count} of {report['steps_rendered']} {description} ({share:.1%}).")

      if example is not None:
         lines.append(f"  drawn {json.dumps(example['draw'])} rendered: {example['text']}")

   if report["key_disagreements"] > 0:
      failure = report["first_failure"] or {}
      lines.append(
         f"{report['key_disagreements']} draws disagree between the declared key and the last "
         f"step. First one: {json.dumps(failure)}."
      )

   if report["key_check_is_tautological"]:
      lines.append(
         "The key names the last step's expression, or an alias of it, so comparing them "
         "proves nothing. Derive the key by its own route from the parameters."
      )

   contract = report["contract"]
   roles = report["roles"]

   if roles["parameter_role_undeclared"]:
      lines.append(
         f"Parameters {roles['parameter_role_undeclared']} declare no role. Set role to "
         f"radical or incidental on every parameter."
      )

   if roles["incidental_changes_path"]:
      lines.append(
         f"Parameters {roles['incidental_changes_path']} are declared incidental but varying "
         f"one of them alone changes the form of a step or of the key. Declare it radical, or "
         f"add a constraint that keeps the form fixed."
      )

   if contract["representation_undeclared"]:
      lines.append(
         "The template does not declare which of the archetype's representations it serves, "
         "or declares one the archetype does not list. Set representation to one BC-REP id."
      )

   if contract["figure_missing"]:
      lines.append(
         f"The declared representation {contract['representation']} needs a figure and the "
         f"template carries none. Add a figure object with its labels inside."
      )

   if contract["unresolved_error_paths"] > 0:
      lines.append(
         f"{contract['unresolved_error_paths']} of {contract['distractors']} distractors carry "
         f"an error_path that is not an allowed BC-ERR id. Use only the allowed_error_paths ids."
      )

   if contract["unresolved_point_types"] > 0:
      lines.append(
         f"{contract['unresolved_point_types']} of {contract['point_types_tagged']} step tags are "
         f"not BC-PT ids. Use only the archetype's point_types."
      )

   if contract["option_count_wrong"]:
      lines.append(
         f"The key plus {contract['distractors']} distractors is {contract['option_count']} "
         f"options; an item has exactly {OPTIONS_PER_ITEM}."
      )

   return "\n".join(lines)


def generate_with_retry(archetype_id, attempts=MAX_GENERATION_ATTEMPTS, transport=None,
                        draws=GATE_DRAWS):
   """Generate, gate, and send the defects back by name until the gate passes or attempts run out.

   Every attempt is a fresh single turn carrying the previous template and its defect list, not
   a growing conversation, so the cached instruction prefix is reused and the input stays small.
   """
   history = []
   previous = None
   feedback = None

   for attempt in range(1, attempts + 1):
      try:
         template, usage = generate_template(archetype_id, transport=transport,
                                             previous=previous, feedback=feedback)
      except TemplateRefused as refusal:
         history.append({"attempt": attempt, "usage": {}, "passes_bar": False,
                         "draw_space": 0, "surface_defect_rate": None,
                         "generation_error": str(refusal)})
         feedback = (f"Your previous response could not be used: {refusal}. Return a complete, "
                     f"valid template object and keep the prose short enough to finish it.")
         continue

      report = run_draws(template, draws=draws)
      history.append({"attempt": attempt, "usage": usage,
                      "passes_bar": report["passes_bar"],
                      "draw_space": report["draw_space"],
                      "surface_defect_rate": report["surface_defect_rate"],
                      "rendered_nothing": report["rendered_nothing"],
                      "first_failure": report["first_failure"]})

      if report["passes_bar"]:
         return template, report, history

      previous = template
      feedback = defect_feedback(template, report)

   never_generated = all("generation_error" in entry for entry in history)

   if never_generated:
      return None, None, history

   return template, report, history


def _archetype(archetype_id):
   records = json.loads((REPO / "data" / "archetypes.json").read_text())["archetypes"]

   for record in records:
      if record["id"] == archetype_id:
         return record

   raise SystemExit(f"no archetype {archetype_id} in data/archetypes.json")


def _user_turn(archetype_id, previous, feedback):
   """Feedback travels on its own. A generation that failed outright leaves no previous template
   to quote, and dropping the feedback with it made the retry an independent draw rather than a
   correction."""
   base = build_prompt(archetype_id)
   nothing_to_say = feedback is None

   if nothing_to_say:
      return base

   parts = [base, "Your previous attempt at this archetype failed the checks below. Return a "
                  "corrected template for the same archetype."]

   if previous is not None:
      parts.append(f"Previous template:\n{json.dumps(previous, ensure_ascii=False)}")

   parts.append(f"What failed:\n{feedback}")

   return "\n\n".join(parts)


def build_prompt(archetype_id):
   record = _archetype(archetype_id)
   fields = ["id", "name", "invariant_structure", "safe_variables", "difficulty_variables",
             "expected_solution_path", "common_distractors", "representations",
             "calculator_status", "point_types", "skills"]
   carried = {k: record.get(k) for k in fields if record.get(k) not in (None, [], "")}
   library = registry()
   skills = frozenset(record.get("skills") or [])
   carried["allowed_error_paths"] = sorted(
      error_id for error_id, held in library["error_skills"].items() if not skills.isdisjoint(held))

   return json.dumps(carried, ensure_ascii=False, indent=2)


def generate_template(archetype_id, transport=None, dry_run=False,
                      previous=None, feedback=None):
   api_key = os.environ.get("ANTHROPIC_API_KEY")
   has_key = api_key is not None and api_key != ""
   needs_key = transport is None and not dry_run

   if needs_key and not has_key:
      raise SystemExit("ANTHROPIC_API_KEY is not set")

   body = {
      "model": MODEL,
      "max_tokens": MAX_OUTPUT_TOKENS,
      "system": [{"type": "text", "text": INSTRUCTIONS,
                  "cache_control": {"type": "ephemeral", "ttl": "1h"}}],
      "messages": [{"role": "user", "content": _user_turn(archetype_id, previous, feedback)}],
      "output_config": {
         "effort": EFFORT,
         "format": {"type": "json_schema", "schema": TEMPLATE_SCHEMA},
      },
   }
   headers = {
      "x-api-key": api_key,
      "anthropic-version": ANTHROPIC_VERSION,
      "content-type": "application/json",
   }
   if dry_run:
      return body, {}

   send = transport if transport is not None else _post
   response = send(MESSAGES_URL, headers, body)

   usage = response.get("usage", {})
   stopped_short = response.get("stop_reason") == "max_tokens"

   if stopped_short:
      raise TemplateRefused(
         f"the response hit max_tokens at {MAX_OUTPUT_TOKENS} and the template is truncated")

   blocks = [b.get("text", "") for b in response.get("content", []) if b.get("type") == "text"]

   try:
      template = json.loads("".join(blocks))
   except json.JSONDecodeError as failure:
      raise TemplateRefused(f"the response is not parseable JSON: {failure}")

   return template, usage


def _post(url, headers, body):
   """urllib raises HTTPError with the body unread, so a 400 arrives with no reason attached.
   The API puts the reason in the body and it is the only thing worth having on a failure."""
   request = urllib.request.Request(url, data=json.dumps(body).encode("utf-8"),
                                    headers=headers, method="POST")

   try:
      with urllib.request.urlopen(request) as response:
         return json.loads(response.read().decode("utf-8"))
   except urllib.error.HTTPError as failure:
      detail = failure.read().decode("utf-8", errors="replace")

      raise SystemExit(f"HTTP {failure.code} from the Messages API: {detail}")


def _cost(usage):
   """Opus 5 list price, https://platform.claude.com/docs/en/about-claude/pricing, 2026-09-20."""
   base_in, write_1h, read, out = 5.0, 10.0, 0.50, 25.0
   cost = (usage.get("input_tokens", 0) / 1e6) * base_in
   cost += (usage.get("cache_creation_input_tokens", 0) / 1e6) * write_1h
   cost += (usage.get("cache_read_input_tokens", 0) / 1e6) * read
   cost += (usage.get("output_tokens", 0) / 1e6) * out

   return cost


def main(argv=None):
   parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
   sub = parser.add_subparsers(dest="command", required=True)

   gen = sub.add_parser("generate", help="one paid model call per archetype")
   gen.add_argument("archetypes", nargs="+")
   gen.add_argument("--out", default="var/template_trial")
   gen.add_argument("--dry-run", action="store_true", help="print the wire body and spend nothing")
   gen.add_argument("--attempts", type=int, default=MAX_GENERATION_ATTEMPTS,
                    help="how many times a failing template is sent back with its defect list")

   run = sub.add_parser("draw", help="instantiate a template over N draws, no network")
   run.add_argument("templates", nargs="+")
   run.add_argument("--draws", type=int, default=DRAWS)
   run.add_argument("--seed", type=int, default=20260920)

   args = parser.parse_args(argv)

   if args.command == "generate":
      out = Path(args.out)
      out.mkdir(parents=True, exist_ok=True)
      spent = 0.0
      attempts_used = 0
      archetypes_done = 0
      abandoned = []

      for archetype_id in args.archetypes:
         if args.dry_run:
            body, _ = generate_template(archetype_id, dry_run=True)
            print(json.dumps(body, indent=2))
            continue

         try:
            template, report, history = generate_with_retry(archetype_id, attempts=args.attempts)
         except Exception as failure:
            print(f"{archetype_id}: ABANDONED, {type(failure).__name__}: {failure}", flush=True)
            abandoned.append(archetype_id)
            continue

         attempts_used += len(history)
         archetypes_done += 1

         if template is None:
            print(f"{archetype_id}: no usable template after {len(history)} attempts", flush=True)
            abandoned.append(archetype_id)

            for entry in history:
               print(f"{archetype_id} attempt {entry['attempt']}: "
                     f"generation_error={entry.get('generation_error')}", flush=True)
            continue

         path = out / f"{archetype_id}.json"
         path.write_text(json.dumps(template, ensure_ascii=False, indent=2) + "\n")

         for entry in history:
            spent += _cost(entry["usage"])
            failure = entry.get("first_failure")
            why = "" if failure is None else f" why={json.dumps(failure)}"
            print(f"{archetype_id} attempt {entry['attempt']}: "
                  f"passes={entry['passes_bar']} space={entry['draw_space']} "
                  f"surface={entry['surface_defect_rate']}{why} "
                  f"usage={json.dumps(entry['usage'])}", flush=True)

         verdict = "PASS" if report["passes_bar"] else "FAIL after every attempt"
         print(f"{archetype_id}: {verdict}, wrote {path}", flush=True)

      if not args.dry_run:
         per_archetype = attempts_used / archetypes_done if archetypes_done else 0
         print(f"total spent at list price: ${spent:.4f} over {attempts_used} attempts "
               f"for {archetypes_done} archetypes, {per_archetype:.2f} calls per archetype")

         if abandoned:
            print(f"abandoned: {', '.join(abandoned)}")

      return 0

   reports = []

   for path in args.templates:
      template = json.loads(Path(path).read_text())
      report = run_draws(template, draws=args.draws, seed=args.seed)
      reports.append(report)
      print(json.dumps(report, indent=2, default=str))

   passed = [r for r in reports if r["passes_bar"]]
   print(f"\n{len(passed)} of {len(reports)} templates pass the bar "
         f"(surface defect rate under {SURFACE_DEFECT_BAR}, key disagreements == {KEY_DISAGREEMENT_BAR})")

   return 0 if len(passed) == len(reports) else 1


if __name__ == "__main__":
   raise SystemExit(main())
