"""Gate 26 arithmetic, checked against hand derivations of the WCAG 2.2 formula.

docs/plan/11-phased-delivery.md item 26 says the contrast test reads hex values out of the token
file and computes the ratios itself. The token file is hand authored and does not exist yet, so
these tests exercise the computation alone, against colours whose luminance can be derived from
the formula without consulting any checker tool.
"""

import pytest

from app.design.contrast import (
   LARGE_TEXT_CONTRAST_FLOOR,
   TEXT_CONTRAST_FLOOR,
   contrast_ratio,
   relative_luminance,
)


def test_black_on_white_is_twenty_one_to_one():
   assert contrast_ratio("#000000", "#ffffff") == pytest.approx(21.0, abs=1e-12)


def test_a_colour_against_itself_is_one_to_one():
   assert contrast_ratio("#3f7ab2", "#3f7ab2") == pytest.approx(1.0, abs=1e-12)


def test_the_ratio_is_symmetric_in_its_arguments():
   forward = contrast_ratio("#1a1a1a", "#c9d4e2")
   backward = contrast_ratio("#c9d4e2", "#1a1a1a")

   assert forward == pytest.approx(backward, abs=1e-12)


def test_the_three_digit_shorthand_expands_to_six():
   assert relative_luminance("#09F") == pytest.approx(relative_luminance("#0099ff"), abs=1e-12)
   assert relative_luminance("#fff") == pytest.approx(relative_luminance("#FFFFFF"), abs=1e-12)


@pytest.mark.parametrize(
   "malformed",
   ["ffffff", "#ff", "#fffff", "#gggggg", "#ff ffff", "", None, 0xFFFFFF],
)
def test_a_malformed_hex_value_raises(malformed):
   with pytest.raises(ValueError):
      relative_luminance(malformed)


def test_a_known_mid_grey_reproduces_its_published_ratio():
   """#808080 against white and against pure blue, both derived from the formula.

   Every channel of #808080 is 128, so its linearised channel value is
   ((128 / 255 + 0.055) / 1.055) ** 2.4 = 0.2158605001138..., and because the three luminance
   coefficients sum to 1 the colour's relative luminance is that same number. White linearises
   to 1.0 in every channel, so its luminance is 1.0 and the ratio is
   1.05 / (0.2158605001138 + 0.05) = 3.9494396480491...

   Pure blue has only the blue channel lit, so its luminance is the blue coefficient itself,
   0.0722, and the grey against it is (0.2158605001138 + 0.05) / (0.0722 + 0.05)
   = 2.1756178405392.... That second ground is what pins the individual coefficients rather
   than only their sum, since a grey alone cannot tell the three of them apart.
   """
   grey_linear_channel = ((128 / 255 + 0.055) / 1.055) ** 2.4

   assert relative_luminance("#808080") == pytest.approx(grey_linear_channel, abs=1e-12)

   against_white = 1.05 / (grey_linear_channel + 0.05)
   against_blue = (grey_linear_channel + 0.05) / (0.0722 + 0.05)

   assert contrast_ratio("#808080", "#ffffff") == pytest.approx(against_white, abs=1e-12)
   assert contrast_ratio("#808080", "#0000ff") == pytest.approx(against_blue, abs=1e-12)


def test_the_floors_are_the_wcag_values_the_plan_states():
   assert TEXT_CONTRAST_FLOOR == 4.5
   assert LARGE_TEXT_CONTRAST_FLOOR == 3.0
