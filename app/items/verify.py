"""Item verification tools: SymPy equivalence, numeric probing, distractor
checks and the provenance rule (docs/plan/04-item-generation.md, "Checks on
the option set" and "Independent key verification"; docs/plan/11 R26, R30).
"""
import math
import random
import signal
import threading

import sympy

_NUMERIC_SAMPLE_SEED = 20260919
_NUMERIC_SAMPLE_RANGE = 3.0
_MAX_ATTEMPT_MULTIPLIER = 20
_NUMERIC_REL_TOL = 1e-6
_NUMERIC_ABS_FLOOR = 1e-9


class _Timeout(Exception):
   pass


def _raise_timeout(signum, frame):
   raise _Timeout()


def equivalence(left, right, timeout_s=5):
   supports_alarm = hasattr(signal, "SIGALRM")
   on_main_thread = threading.current_thread() is threading.main_thread()
   can_set_alarm = supports_alarm and on_main_thread

   if not can_set_alarm:
      return _equivalence_impl(left, right)

   previous_handler = signal.signal(signal.SIGALRM, _raise_timeout)
   signal.setitimer(signal.ITIMER_REAL, timeout_s)

   try:
      return _equivalence_impl(left, right)
   except _Timeout:
      return "unsettled"
   finally:
      signal.setitimer(signal.ITIMER_REAL, 0)
      signal.signal(signal.SIGALRM, previous_handler)


def _equivalence_impl(left, right):
   difference = left - right
   settles_to_zero = _settles_to_zero(difference)

   if settles_to_zero:
      return "equivalent"

   numeric_result = numeric_check(left, right)

   if numeric_result is True:
      return "equivalent"

   if numeric_result is False:
      return "not_equivalent"

   return "unsettled"


def _settles_to_zero(difference):
   candidates = (
      sympy.simplify(difference),
      sympy.simplify(sympy.expand_trig(difference)),
      sympy.simplify(sympy.logcombine(difference, force=True)),
      sympy.radsimp(sympy.simplify(difference)),
   )

   for candidate in candidates:
      is_zero = candidate == 0

      if is_zero:
         return True

   return False


def numeric_check(left, right, points=7, rel_tol=_NUMERIC_REL_TOL, abs_floor=_NUMERIC_ABS_FLOOR):
   free_symbols = sorted(left.free_symbols | right.free_symbols, key=lambda symbol: symbol.name)
   has_no_symbols = len(free_symbols) == 0

   if has_no_symbols:
      values = _evaluate(left, right, {})

      if values is None:
         return None

      return _close(*values, rel_tol, abs_floor)

   rng = random.Random(_NUMERIC_SAMPLE_SEED)
   max_attempts = points * _MAX_ATTEMPT_MULTIPLIER
   matches = 0

   for _ in range(max_attempts):
      substitution = {symbol: _sample_value(rng) for symbol in free_symbols}
      values = _evaluate(left, right, substitution)

      if values is None:
         continue

      if not _close(*values, rel_tol, abs_floor):
         return False

      matches += 1

      if matches >= points:
         return True

   return None


def _sample_value(rng):
   value = rng.uniform(-_NUMERIC_SAMPLE_RANGE, _NUMERIC_SAMPLE_RANGE)
   is_near_zero = abs(value) < 0.05

   if is_near_zero:
      value += 0.5

   return value


def _evaluate(left, right, substitution):
   try:
      left_value = complex(left.subs(substitution).evalf())
      right_value = complex(right.subs(substitution).evalf())
   except (TypeError, ValueError, sympy.SympifyError):
      return None

   is_finite = (
      math.isfinite(left_value.real)
      and math.isfinite(left_value.imag)
      and math.isfinite(right_value.real)
      and math.isfinite(right_value.imag)
   )

   if not is_finite:
      return None

   return left_value, right_value


def _close(left_value, right_value, rel_tol, abs_floor):
   magnitude = max(abs(left_value), abs(right_value))
   tolerance = max(rel_tol * magnitude, abs_floor)

   return abs(left_value - right_value) < tolerance


def _equals_key(key, candidate):
   symbolic_result = equivalence(key, candidate)
   equals_symbolically = symbolic_result == "equivalent"

   if equals_symbolically:
      return True

   return numeric_check(key, candidate) is True


def distractor_checks(key, distractors, error_paths, active_error_ids):
   violations = []

   for distractor in distractors:
      violates_rule_5 = _equals_key(key, distractor)

      if violates_rule_5:
         violations.append("rule_5")

   for left_index in range(len(distractors)):
      for right_index in range(left_index + 1, len(distractors)):
         violates_rule_6 = _equals_key(distractors[left_index], distractors[right_index])

         if violates_rule_6:
            violations.append("rule_6")

   for error_path in error_paths:
      is_missing = error_path is None
      is_unresolvable = error_path is not None and error_path not in active_error_ids

      if is_missing or is_unresolvable:
         violations.append("rule_7")

   return list(dict.fromkeys(violations))


def verify_item(item, active_error_ids):
   options = item["options"]
   key_options = [option for option in options if option.get("error_path") is None]
   distractor_options = [option for option in options if option.get("error_path") is not None]
   has_key_option = len(key_options) > 0
   key_source = key_options[0]["value"] if has_key_option else item["answer_key"]

   from app.items.mathjson import to_sympy

   key_expr = to_sympy(key_source)
   distractor_exprs = [to_sympy(option["value"]) for option in distractor_options]
   error_paths = [option.get("error_path") for option in distractor_options]

   violations = distractor_checks(key_expr, distractor_exprs, error_paths, active_error_ids)
   violations.extend(_provenance_violations(item.get("provenance", {})))

   return {"verified": len(violations) == 0, "violations": violations}


def _provenance_violations(provenance):
   model = provenance.get("model")
   is_operator = model == "operator"

   if is_operator:
      prompt_template_version = provenance.get("prompt_template_version")
      generation_job_id = provenance.get("generation_job_id")
      fields_are_null = prompt_template_version is None and generation_job_id is None

      if not fields_are_null:
         return ["provenance_operator_fields"]

      return []

   has_model_id = bool(model)

   if not has_model_id:
      return ["provenance_missing_model"]

   return []
