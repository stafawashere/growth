"""Item verification tools: SymPy equivalence, numeric probing, distractor
checks and the provenance rule (docs/plan/04-item-generation.md, "Checks on
the option set" and "Independent key verification"; docs/plan/11 R26, R30).
"""
import math
import multiprocessing
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


class ChildDiedError(Exception):
   """Raised when a forkserver child exits before sending a result, distinct from a plain
   timeout. Nothing about the arguments the child was given is folded into the message.
   """


def _raise_timeout(signum, frame):
   raise _Timeout()


_CHILD_RESULT = "result"
_CHILD_ERROR = "error"

COMPARISON_TIMEOUT_S = 5


def equivalence(left, right, timeout_s=COMPARISON_TIMEOUT_S):
   """Equivalent, not_equivalent or unsettled, and unsettled whenever the comparison outlives
   timeout_s. The default of 5 seconds is carried from the original code. No plan document gives
   one, and numeric_check and compare_expressions reuse it rather than adding another.
   """
   return run_bounded(_equivalence_impl, (left, right), timeout_s, "unsettled")


def run_bounded(function, arguments, timeout_s, unsettled):
   """function(*arguments), or unsettled once it outlives timeout_s. On the main thread SIGALRM
   interrupts it in process. Anywhere else, which is where a sync FastAPI route runs, it runs in a
   forkserver child that is killed at the deadline, so function must be importable by name. An
   exception it raises reaches the caller either way, and a child that exits before the deadline
   without sending anything back, whether it crashed at startup or died some other way, reaches
   the caller as ChildDiedError rather than as unsettled, because it never ran long enough to say
   the comparison did not settle.
   """
   is_number = isinstance(timeout_s, (int, float)) and not isinstance(timeout_s, bool)
   is_positive_number = is_number and timeout_s > 0

   if not is_positive_number:
      raise ValueError(f"a bounded comparison needs a positive timeout_s, got {timeout_s!r}")

   supports_alarm = hasattr(signal, "SIGALRM")
   on_main_thread = threading.current_thread() is threading.main_thread()
   can_set_alarm = supports_alarm and on_main_thread

   if not can_set_alarm:
      return _run_in_child(function, arguments, timeout_s, unsettled)

   previous_handler = signal.signal(signal.SIGALRM, _raise_timeout)

   # A one-shot alarm that fires while a gc.callbacks hook (hypothesis registers one, seen only
   # once the rest of the suite has imported it) is running never reaches this frame: CPython's
   # gc module catches whatever a callback raises and reports it as unraisable instead of letting
   # it propagate, so the single SIGALRM is silently lost and the comparison runs to completion
   # past timeout_s. A repeat interval keeps the alarm firing until one delivery lands outside a
   # gc callback, so the bound holds even when the first shot is swallowed that way.
   retry_interval_s = min(0.05, timeout_s)
   signal.setitimer(signal.ITIMER_REAL, timeout_s, retry_interval_s)

   try:
      return function(*arguments)
   except _Timeout:
      return unsettled
   finally:
      signal.setitimer(signal.ITIMER_REAL, 0)
      signal.signal(signal.SIGALRM, previous_handler)


def _child_context():
   context = multiprocessing.get_context("forkserver")
   context.set_forkserver_preload([__name__, "sympy"])

   return context


def _run_in_child(function, arguments, timeout_s, unsettled):
   context = _child_context()
   receiver, sender = context.Pipe(duplex=False)
   child = context.Process(
      target=_run_for_parent,
      args=(function, arguments, sender),
      daemon=True,
   )
   died_without_a_result = False
   kind, payload = None, None

   try:
      child.start()
      sender.close()
      answered_in_time = receiver.poll(timeout_s)

      if not answered_in_time:
         return unsettled

      try:
         kind, payload = receiver.recv()
      except EOFError:
         died_without_a_result = True
   finally:
      receiver.close()
      sender.close()
      child_was_started = child.pid is not None
      child_still_running = child_was_started and child.is_alive()

      if child_still_running:
         child.kill()

      if child_was_started:
         child.join()

   if died_without_a_result:
      raise ChildDiedError(
         f"the bounded child exited with code {child.exitcode} before sending a result"
      )

   is_error = kind == _CHILD_ERROR

   if is_error:
      raise payload

   return payload


def _run_for_parent(function, arguments, sender):
   try:
      message = (_CHILD_RESULT, function(*arguments))
   except Exception as failure:
      message = (_CHILD_ERROR, failure)

   try:
      sender.send(message)
   except Exception as unpicklable:
      sender.send((_CHILD_ERROR, RuntimeError(repr(unpicklable))))
   finally:
      sender.close()


def _equivalence_impl(left, right):
   difference = left - right
   settles_to_zero = _settles_to_zero(difference)

   if settles_to_zero:
      return "equivalent"

   numeric_result = _numeric_check_impl(left, right)

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


def numeric_check(
   left,
   right,
   points=7,
   rel_tol=_NUMERIC_REL_TOL,
   abs_floor=_NUMERIC_ABS_FLOOR,
   timeout_s=COMPARISON_TIMEOUT_S,
):
   """True, False, or None when the sampled points did not settle it or it outlived timeout_s."""
   arguments = (left, right, points, rel_tol, abs_floor)

   return run_bounded(_numeric_check_impl, arguments, timeout_s, None)


def _numeric_check_impl(
   left, right, points=7, rel_tol=_NUMERIC_REL_TOL, abs_floor=_NUMERIC_ABS_FLOOR
):
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


UNSETTLED_VIOLATION = "unsettled"

EQUAL = "equal"
DISTINCT = "distinct"

KEY_COMPARISON = "key"
PAIR_COMPARISON = "pair"

MISSING_ERROR_PATH = "missing"
UNRESOLVABLE_ERROR_PATH = "unresolvable"

RULE_5 = "rule_5"
RULE_6 = "rule_6"
RULE_7 = "rule_7"


def compare_expressions(key, candidate, timeout_s=COMPARISON_TIMEOUT_S):
   """Equal, distinct, or neither. A comparison that did not settle is its own answer, because
   rejection rule 5 in 04 asks whether a distractor equals the key and an unsettled comparison
   has not established that it does not. One bound of timeout_s covers the symbolic and the
   numeric step together, and a comparison that outlives it has not settled.
   """
   return run_bounded(_compare_impl, (key, candidate), timeout_s, UNSETTLED_VIOLATION)


def _compare_impl(key, candidate):
   settles_to_zero = _settles_to_zero(key - candidate)

   if settles_to_zero:
      return EQUAL

   numeric_result = _numeric_check_impl(key, candidate)

   if numeric_result is True:
      return EQUAL

   if numeric_result is False:
      return DISTINCT

   return UNSETTLED_VIOLATION


def comparison_findings(key, distractors):
   """Rejection rules 5 and 6 of docs/plan/04-item-generation.md over one option set: every
   distractor against the key, then every distractor against every later one. A key of None
   asks rule 6 alone, which is what a record with no single readable key gets.

   A finding carries its kind, the positions in distractors it is about, and the comparison.
   This is the only implementation of those two loops. distractor_checks below and
   distractor_path_violations in app/items/distractor_paths.py are its two callers and differ
   only in the vocabulary they render and in their policy on a comparison that did not settle.
   """
   findings = []
   has_a_key = key is not None

   if has_a_key:
      for index, distractor in enumerate(distractors):
         findings.append({
            "kind": KEY_COMPARISON,
            "left": None,
            "right": index,
            "comparison": compare_expressions(key, distractor),
         })

   for left_index in range(len(distractors)):
      for right_index in range(left_index + 1, len(distractors)):
         findings.append({
            "kind": PAIR_COMPARISON,
            "left": left_index,
            "right": right_index,
            "comparison": compare_expressions(
               distractors[left_index], distractors[right_index]
            ),
         })

   return findings


def error_path_findings(error_paths, active_error_ids):
   """Rejection rule 7 of 04 over one option set: a non-key option that carries no error path,
   or one whose id does not resolve to an active BC-ERR record. The only implementation of that
   resolution, shared by distractor_checks and by gate 30's checker.
   """
   findings = []

   for index, error_path in enumerate(error_paths):
      is_missing = error_path is None
      is_unresolvable = error_path is not None and error_path not in active_error_ids

      if is_missing:
         findings.append({"index": index, "reason": MISSING_ERROR_PATH, "error_path": None})

      if is_unresolvable:
         findings.append({
            "index": index,
            "reason": UNRESOLVABLE_ERROR_PATH,
            "error_path": error_path,
         })

   return findings


def distractor_checks(key, distractors, error_paths, active_error_ids):
   """Rejection rules 5, 6 and 7 rendered as rule codes over the findings above.

   Policy on a comparison that did not settle: it comes back under its own code,
   UNSETTLED_VIOLATION, and never as a broken rule, because app/items/ingest.py reads that code
   as indeterminate and routes the item to review instead of rejecting it. Gate 30's checker,
   distractor_path_violations in app/items/distractor_paths.py, reads the same findings under
   the opposite policy and calls an unsettled comparison a violation outright. Both policies are
   deliberate; the loops and the error-path resolution beneath them are not duplicated.
   """
   violations = []

   for finding in comparison_findings(key, distractors):
      is_key_comparison = finding["kind"] == KEY_COMPARISON
      is_equal = finding["comparison"] == EQUAL
      did_not_settle = finding["comparison"] == UNSETTLED_VIOLATION

      if is_equal:
         violations.append(RULE_5 if is_key_comparison else RULE_6)

      if did_not_settle:
         violations.append(UNSETTLED_VIOLATION)

   broken_error_paths = error_path_findings(error_paths, active_error_ids)

   violations.extend(RULE_7 for _ in broken_error_paths)

   return list(dict.fromkeys(violations))


KEY_WITH_ERROR_PATH = "key_with_error_path"
EXACTLY_ONE_KEY = "exactly_one_key"
OPTION_WITHOUT_IS_KEY = "option_without_is_key"


def option_set_violations(options):
   """04's Output schema requires a boolean is_key on every option, and 06 and R26 put a null
   error_path on the key and a BC-ERR id on every distractor. The split is read from is_key, so a
   record whose error paths disagree with it is refused rather than reclassified. A distractor
   with a null path is left to rule 7.
   """
   violations = []
   has_options = len(options) > 0

   if not has_options:
      return violations

   for option in options:
      has_boolean_is_key = isinstance(option.get("is_key"), bool)
      is_key = option.get("is_key") is True
      key_carries_a_path = is_key and option.get("error_path") is not None

      if not has_boolean_is_key:
         violations.append(OPTION_WITHOUT_IS_KEY)

      if key_carries_a_path:
         violations.append(KEY_WITH_ERROR_PATH)

   key_count = len([option for option in options if option.get("is_key") is True])
   has_exactly_one_key = key_count == 1

   if not has_exactly_one_key:
      violations.append(EXACTLY_ONE_KEY)

   return violations


def verify_item(item, active_error_ids):
   options = item["options"]
   key_options = [option for option in options if option.get("is_key") is True]
   distractor_options = [option for option in options if option.get("is_key") is not True]
   has_exactly_one_key = len(key_options) == 1
   key_source = key_options[0]["value"] if has_exactly_one_key else item["answer_key"]

   from app.items.mathjson import to_sympy

   key_expr = to_sympy(key_source)
   distractor_exprs = [to_sympy(option["value"]) for option in distractor_options]
   error_paths = [option.get("error_path") for option in distractor_options]

   violations = option_set_violations(options)
   violations.extend(distractor_checks(key_expr, distractor_exprs, error_paths, active_error_ids))
   violations = list(dict.fromkeys(violations))
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
