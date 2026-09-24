"""The blind formulations for this bank, one part per solver run.

Each formulations_<batch>.py was written by a separate Claude Code session from the stems alone
(prompts/verifier/independent_resolve_v1.md), never from the keys. tools/key_recheck.py reads
FORMULATIONS from this file.
"""
import runpy
from pathlib import Path

FORMULATIONS = {}

for part in sorted(Path(__file__).parent.glob("formulations_*.py")):
   FORMULATIONS.update(runpy.run_path(str(part))["FORMULATIONS"])
