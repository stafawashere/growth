"""Relative luminance and contrast ratio, the arithmetic behind gate 26.

The formula and every coefficient below come from WCAG 2.2, the relative luminance and contrast
ratio definitions in the specification and the worked wording in Understanding SC 1.4.3,
https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html. That is the source of 0.2126,
0.7152 and 0.0722, of the 0.04045 linearisation threshold, of 12.92, 1.055, 0.055 and 2.4, and of
the 0.05 flare term in the ratio.

The two floors are the only numbers here that are a plan decision rather than a formula constant.
4.5 and 3.0 come from WCAG 2.2 SC 1.4.3 as quoted in docs/plan/08-design-brief.md, the Colour
system section, and in docs/plan/11-phased-delivery.md item 26: 4.5:1 for anything at type-body
and below, 3:1 for type-title and type-display, which are the two steps of the type scale that
cross the large-text boundary.

No colour values live in this module. The token file is hand authored by the operator and the gate
reads the hex values out of it and calls these functions.
"""

TEXT_CONTRAST_FLOOR = 4.5
LARGE_TEXT_CONTRAST_FLOOR = 3.0

# WCAG 2.2 SC 1.4.11 Non-text Contrast, Level AA: graphical objects and user interface components
# hold "at least 3:1 against adjacent color(s)". Read off
# https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html on 2026-09-24, the fetch 08's
# Colour system section asks for before the mastery map and the calibration curve are finalised.
NON_TEXT_CONTRAST_FLOOR = 3.0

_LINEARISATION_THRESHOLD = 0.04045
_LOW_CHANNEL_DIVISOR = 12.92
_GAMMA_OFFSET = 0.055
_GAMMA_DIVISOR = 1.055
_GAMMA_EXPONENT = 2.4

_RED_COEFFICIENT = 0.2126
_GREEN_COEFFICIENT = 0.7152
_BLUE_COEFFICIENT = 0.0722

_FLARE = 0.05

_HEX_DIGITS = "0123456789abcdefABCDEF"


def relative_luminance(hex_color):
   """WCAG 2.2 relative luminance of an sRGB colour given as "#rgb" or "#rrggbb", case
   insensitive. Raises ValueError on anything else."""
   red, green, blue = _channels(hex_color)

   weighted_red = _RED_COEFFICIENT * _linearise(red)
   weighted_green = _GREEN_COEFFICIENT * _linearise(green)
   weighted_blue = _BLUE_COEFFICIENT * _linearise(blue)

   return weighted_red + weighted_green + weighted_blue


def contrast_ratio(hex_a, hex_b):
   """WCAG 2.2 contrast ratio, (L_lighter + 0.05) / (L_darker + 0.05), so the result is
   symmetric in its arguments and lies in [1, 21]."""
   luminance_a = relative_luminance(hex_a)
   luminance_b = relative_luminance(hex_b)

   lighter = max(luminance_a, luminance_b)
   darker = min(luminance_a, luminance_b)

   return (lighter + _FLARE) / (darker + _FLARE)


def _channels(hex_color):
   is_text = isinstance(hex_color, str)

   if not is_text:
      raise ValueError("colour must be a string of the form #rgb or #rrggbb, got {0!r}".format(hex_color))

   starts_with_hash = hex_color.startswith("#")
   body = hex_color[1:]
   has_known_length = len(body) in (3, 6)
   is_all_hex_digits = all(character in _HEX_DIGITS for character in body)
   is_well_formed = starts_with_hash and has_known_length and is_all_hex_digits

   if not is_well_formed:
      raise ValueError("colour must be a string of the form #rgb or #rrggbb, got {0!r}".format(hex_color))

   is_shorthand = len(body) == 3

   if is_shorthand:
      body = "".join(character * 2 for character in body)

   return (
      int(body[0:2], 16) / 255,
      int(body[2:4], 16) / 255,
      int(body[4:6], 16) / 255,
   )


def _linearise(channel):
   is_low = channel <= _LINEARISATION_THRESHOLD

   if is_low:
      return channel / _LOW_CHANNEL_DIVISOR

   return ((channel + _GAMMA_OFFSET) / _GAMMA_DIVISOR) ** _GAMMA_EXPONENT
