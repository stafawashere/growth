"""The startup caps in app/main.py. A tutor cap read from the environment has to be a finite
number, because an infinite cap passes the guard's rule that a role needs a cap while capping
nothing, and NaN compares false against every spend."""
import math
import re
from pathlib import Path

import pytest

from app.main import build_tutor_caps

NON_FINITE_SPELLINGS = ("inf", "Infinity", "-inf", "nan", "NaN")
CAP_VARIABLES = ("GROWTH_TUTOR_CAP_USD", "GROWTH_TUTOR_CAP_TOKENS")


@pytest.mark.parametrize("variable", CAP_VARIABLES)
@pytest.mark.parametrize("spelling", NON_FINITE_SPELLINGS)
def test_a_non_finite_startup_cap_is_refused_and_names_its_variable(variable, spelling):
   assert not math.isfinite(float(spelling))

   with pytest.raises(ValueError) as refused:
      build_tutor_caps({variable: spelling})

   assert variable in str(refused.value)


def test_finite_startup_caps_are_read_as_given():
   caps = build_tutor_caps({"GROWTH_TUTOR_CAP_USD": "0.25", "GROWTH_TUTOR_CAP_TOKENS": "20000"})["tutor"]

   assert (caps.cap_usd, caps.cap_tokens) == (0.25, 20000.0)


def tutor_cap_row_in_open_questions():
   plan_path = Path(__file__).resolve().parents[2] / "docs" / "plan" / "12-open-questions.md"
   rows = [line for line in plan_path.read_text().splitlines() if line.startswith("| Tutor daily cap |")]

   assert len(rows) == 1

   return rows[0]


def test_default_startup_caps_are_the_tunables_row_in_12():
   row = tutor_cap_row_in_open_questions()
   dollars_per_day = float(re.search(r"\$([0-9.]+) per day", row).group(1))
   tokens_per_day = float(re.search(r"([0-9,]+) tokens per day", row).group(1).replace(",", ""))

   caps = build_tutor_caps({})["tutor"]

   assert (caps.cap_usd, caps.cap_tokens) == (dollars_per_day, tokens_per_day)

