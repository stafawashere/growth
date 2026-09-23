"""Gate 26's vocabulary and validator for the design token file.

docs/plan/08-design-brief.md fixes token names and roles and deliberately fixes no hex values.
docs/plan/11-phased-delivery.md item 26 and entry criterion 5 hand the hex values to the operator,
so this module never authors a colour. It carries the names 08 uses, a validator that reads a
hex-valued token file and reports every way it is malformed or fails 08's contrast floors, and
the template the operator fills is docs/operator/design-tokens.template.json, generated blank
from COLOUR_TOKENS and THEMES.

TYPE_TOKENS is the nine-row type scale table. 08's own sentence, "type-display and type-title may
sit at 3:1 and everything else must hold 4.5:1", is the only source for which two are marked
large; the other seven are normal text.

COLOUR_TOKENS is every colour token name 08's Colour system section lists: the nine-step neutral
ramp, so far as 08 names its steps (surface-page, surface-raised, surface-sunken, border-hairline,
text-primary, text-secondary, text-muted, text-on-accent, focus-ring), the accent base and its
tint ramp (08 writes "accent-tint-1 through accent-tint-4", an explicit range, so all four steps
are encoded), accent-contrast-text, and the two semantic colours, state-correct and
state-incorrect. 08 names a tint ramp for each semantic colour without enumerating its steps
("state-correct and its tint ramp"), so no semantic ramp step name is invented here; only the two
base semantic tokens are in the vocabulary.

The pairs token_violations checks are the ones 08 and 11 name: every general text role
(text-primary, text-secondary, text-muted) against every surface, text-on-accent against
accent-base, and focus-ring against every surface. 08 fixes token roles, not which role sits on
which screen at which size, so the wider reading is taken: every text role against every surface,
rather than a guessed subset. For the same reason, every pair here is checked against the same
floor, TEXT_CONTRAST_FLOOR: 08 never states that any specific colour pair renders only at
type-title or type-display size, so applying the lower large-text floor to a colour pair would be
an invented allowance rather than something 08 says. The large/normal marking on TYPE_TOKENS is
the record of which type-scale steps a future screen-level gate may bind to that lower floor.
"""

import json

from app.design.contrast import (
   LARGE_TEXT_CONTRAST_FLOOR,
   TEXT_CONTRAST_FLOOR,
   contrast_ratio,
   relative_luminance,
)

TYPE_TOKENS = {
   "type-display": "large",
   "type-title": "large",
   "type-heading": "normal",
   "type-body": "normal",
   "type-math-inline": "normal",
   "type-math-display": "normal",
   "type-label": "normal",
   "type-caption": "normal",
   "type-mono": "normal",
}

TYPE_TOKEN_FLOORS = {
   name: (LARGE_TEXT_CONTRAST_FLOOR if category == "large" else TEXT_CONTRAST_FLOOR)
   for name, category in TYPE_TOKENS.items()
}

COLOUR_TOKENS = (
   "surface-page",
   "surface-raised",
   "surface-sunken",
   "border-hairline",
   "text-primary",
   "text-secondary",
   "text-muted",
   "text-on-accent",
   "focus-ring",
   "accent-base",
   "accent-tint-1",
   "accent-tint-2",
   "accent-tint-3",
   "accent-tint-4",
   "accent-contrast-text",
   "state-correct",
   "state-incorrect",
)

THEMES = ("light", "dark")

TEXT_ROLES = ("text-primary", "text-secondary", "text-muted")

SURFACES = ("surface-page", "surface-raised", "surface-sunken")

ACCENT_BACKGROUNDS = ("accent-base", "accent-tint-1", "accent-tint-2", "accent-tint-3",
                      "accent-tint-4")

SEMANTIC_COLOURS = ("state-correct", "state-incorrect")


def load_tokens(path):
   """Reads and parses a JSON token file, raising ValueError with a useful message on
   malformed JSON."""
   text = open(path, "r").read()

   try:
      return json.loads(text)
   except json.JSONDecodeError as error:
      raise ValueError("token file {0} is not valid JSON: {1}".format(path, error))


def token_violations(tokens):
   """Every way a token file is malformed or fails 08's contrast floors, as a list of
   human-readable strings, empty when the file is sound.

   A null token value is reported as a violation, the same as a malformed hex value; it is
   never treated as an unfilled slot to skip over. Both themes are checked independently,
   because a ratio that passes in one theme does not pass in the other by construction.
   """
   violations = []

   for theme in THEMES:
      if theme not in tokens:
         violations.append("missing theme: {0}".format(theme))
         continue

      theme_tokens = tokens[theme]
      valid_hex = {}

      for name in COLOUR_TOKENS:
         has_name = name in theme_tokens

         if not has_name:
            violations.append("{0}: missing token {1}".format(theme, name))
            continue

         value = theme_tokens[name]

         try:
            relative_luminance(value)
            valid_hex[name] = value
         except ValueError:
            violations.append(
               "{0}: {1} is not a valid hex colour, got {2!r}".format(theme, name, value)
            )

      for name in TYPE_TOKENS:
         has_name = name in theme_tokens

         if not has_name:
            violations.append("{0}: missing token {1}".format(theme, name))

      for name in theme_tokens:
         is_colour = name in COLOUR_TOKENS
         is_type_step = name in TYPE_TOKENS
         is_known = is_colour or is_type_step

         if not is_known:
            violations.append("{0}: unknown token {1}".format(theme, name))

      for role in TEXT_ROLES:
         for surface in SURFACES:
            violations.extend(_pair_violations(theme, role, surface, valid_hex))

      violations.extend(_pair_violations(theme, "text-on-accent", "accent-base", valid_hex))

      for background in ACCENT_BACKGROUNDS:
         violations.extend(
            _pair_violations(theme, "accent-contrast-text", background, valid_hex)
         )

      for name in SEMANTIC_COLOURS:
         for surface in SURFACES:
            violations.extend(_pair_violations(theme, name, surface, valid_hex))

      for surface in SURFACES:
         violations.extend(_pair_violations(theme, "focus-ring", surface, valid_hex))

   return violations


def _pair_violations(theme, foreground_name, background_name, valid_hex):
   has_both = foreground_name in valid_hex and background_name in valid_hex

   if not has_both:
      return []

   ratio = contrast_ratio(valid_hex[foreground_name], valid_hex[background_name])
   is_below_floor = ratio < TEXT_CONTRAST_FLOOR

   if not is_below_floor:
      return []

   message = "{0}: {1} on {2} is {3:.2f}:1, below the {4}:1 floor".format(
      theme, foreground_name, background_name, ratio, TEXT_CONTRAST_FLOOR
   )

   return [message]
