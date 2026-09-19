"""Diagnostic breadth: every active error has at least two possible causes overall and specific
non-conceptual causes; every active skill has at least one diagnostic signal."""
from collections import Counter
from qa_common import load_json, finish

failures, warnings = [], []
errors = load_json("errors.json")["errors"]
skills = load_json("skills.json")["skills"]
signals = load_json("diagnostic_signals.json")["signals"]
active_errors = [e for e in errors if e.get("status") != "retired"]
cause_lists = Counter(tuple(sorted(e.get("non_conceptual_causes", []))) for e in active_errors)
boilerplate = {key for key, count in cause_lists.items() if count >= 8}

for error in active_errors:
   causes = len(error.get("possible_misconceptions", [])) + len(error.get("non_conceptual_causes", []))
   has_breadth = causes >= 2
   is_boilerplate = tuple(sorted(error.get("non_conceptual_causes", []))) in boilerplate

   if not has_breadth:
       failures.append(f"{error['id']} lists fewer than two possible causes")

   if is_boilerplate:
       failures.append(f"{error['id']} non_conceptual_causes is a list shared by 8 or more errors")

covered = {s.get("skill") for s in signals if s.get("status") != "retired"}

for skill in skills:
   is_active = skill.get("status") != "retired"
   has_signal = skill["id"] in covered or bool(skill.get("diagnostic_signals"))

   if is_active and not has_signal:
      failures.append(f"{skill['id']} has no diagnostic signal")

warnings.append(f"{len(active_errors)} active errors, {len(boilerplate)} boilerplate cause lists, {len(covered)} skills with signals")
finish("14_diagnosis", failures, warnings)
