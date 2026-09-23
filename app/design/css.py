"""Turns a filled design-token file into the CSS custom-property stylesheet the React client
consumes.

docs/plan/08-design-brief.md fixes no hex value and entry criterion 5 of 11-phased-delivery.md
hands every hex value to the operator, so this module is the one place a colour crosses from the
hand-authored token file in docs/operator/design-tokens.template.json's shape into client CSS.
It never invents a value: a token the vocabulary in app/design/tokens.py names but the token file
omits is a refusal, not a gap filled with a guess. That holds for the type scale as much as for
the colours, because a type token silently dropped resolves to an empty custom property in the
client and falls back to the browser default without anything failing.

08-design-brief.md fixes no type-scale value, so a type value is checked only for the things that
hold whatever unit the operator chooses: it is a non-empty string, and it carries nothing that can
end the declaration, end the rule block, close the surrounding element or open a comment.

The spacing scale is different from every other token in this module: 08's Spacing and layout
section fixes the nine pixel values itself, so they are not operator input, carry no slot in the
operator's token file, and are emitted once in a theme-independent `:root` block rather than
inside either `[data-theme]` selector. Spacing emission never depends on what the token file
carries.
"""

import json

from app.design.tokens import COLOUR_TOKENS, SPACING_TOKENS, THEMES, TYPE_TOKENS

CUSTOM_PROPERTY_PREFIX = "--growth-"

_DECLARATION_BREAKING_CHARACTERS = (";", "{", "}", "<", ">", "\\", "\"", "'")

_DECLARATION_BREAKING_SEQUENCES = ("/*", "*/")


def custom_property_name(token):
   return CUSTOM_PROPERTY_PREFIX + token


CUSTOM_PROPERTIES = tuple(
   custom_property_name(name) for name in COLOUR_TOKENS
) + tuple(
   custom_property_name(name) for name in TYPE_TOKENS
) + tuple(
   custom_property_name(name) for name in SPACING_TOKENS
)


def stylesheet_from_tokens(tokens):
   selectors = [_root_selector()]

   for theme in THEMES:
      has_theme = theme in tokens

      if not has_theme:
         raise ValueError("token file is missing theme {0}".format(theme))

      selectors.append(_selector_for_theme(theme, tokens[theme]))

   selectors.append(_no_theme_attribute_fallback(tokens))

   return "\n\n".join(selectors)


def stylesheet_from_token_file(path):
   text = open(path, "r").read()

   try:
      tokens = json.loads(text)
   except json.JSONDecodeError as error:
      raise ValueError("token file {0} is not valid JSON: {1}".format(path, error))

   return stylesheet_from_tokens(tokens)


def _root_selector():
   declarations = [
      "   {0}: {1}px;".format(custom_property_name(name), value)
      for name, value in SPACING_TOKENS.items()
   ]

   return ":root {{\n{0}\n}}".format("\n".join(declarations))


def _selector_for_theme(theme, theme_tokens):
   declarations = _declarations_for_theme(theme, theme_tokens)
   selector = '[data-theme="{0}"]'.format(theme)

   return "{0} {{\n{1}\n}}".format(selector, "\n".join(declarations))


def _declarations_for_theme(theme, theme_tokens):
   declarations = []

   for name in COLOUR_TOKENS:
      has_token = name in theme_tokens

      if not has_token:
         raise ValueError("token file, theme {0}, is missing token {1}".format(theme, name))

      value = theme_tokens[name]
      is_hex_colour = isinstance(value, str) and value.startswith("#")

      if not is_hex_colour:
         raise ValueError(
            "token file, theme {0}, token {1} is not a hex colour, got {2!r}".format(
               theme, name, value
            )
         )

      declarations.append("   {0}: {1};".format(custom_property_name(name), value))

   for name in TYPE_TOKENS:
      has_token = name in theme_tokens

      if not has_token:
         raise ValueError("token file, theme {0}, is missing token {1}".format(theme, name))

      value = _emittable_type_value(theme, name, theme_tokens[name])

      declarations.append("   {0}: {1};".format(custom_property_name(name), value))

   return declarations


def _no_theme_attribute_fallback(tokens):
   """Before app/web/src/main.tsx runs and sets data-theme, the page carries neither
   [data-theme="light"] nor [data-theme="dark"], so it would otherwise render with no colour
   tokens at all. app/web/src/theme.ts resolves that same moment to the system preference,
   dark when `(prefers-color-scheme: dark)` matches and light otherwise, so the fallback here
   follows the same rule: light values live under `:root:not([data-theme])`, and a
   `(prefers-color-scheme: dark)` media block overrides them with the dark values for the same
   selector.
   """
   light_declarations = _declarations_for_theme("light", tokens["light"])
   dark_declarations = _declarations_for_theme("dark", tokens["dark"])

   light_rule = ":root:not([data-theme]) {{\n{0}\n}}".format("\n".join(light_declarations))

   indented_dark_declarations = "\n".join(
      "   " + declaration for declaration in dark_declarations
   )
   dark_rule = (
      "@media (prefers-color-scheme: dark) {{\n"
      "   :root:not([data-theme]) {{\n{0}\n   }}\n"
      "}}"
   ).format(indented_dark_declarations)

   return "{0}\n\n{1}".format(light_rule, dark_rule)


def _emittable_type_value(theme, name, value):
   is_text = isinstance(value, str)

   if not is_text:
      raise ValueError(
         "token file, theme {0}, token {1} is not a type-scale string, got {2!r}".format(
            theme, name, value
         )
      )

   trimmed = value.strip()
   is_empty = trimmed == ""

   if is_empty:
      raise ValueError(
         "token file, theme {0}, token {1} is empty".format(theme, name)
      )

   has_breaking_character = any(
      character in trimmed for character in _DECLARATION_BREAKING_CHARACTERS
   )
   has_breaking_sequence = any(
      sequence in trimmed for sequence in _DECLARATION_BREAKING_SEQUENCES
   )
   has_control_character = any(ord(character) < 32 for character in trimmed)
   escapes_the_declaration = has_breaking_character or has_breaking_sequence or has_control_character

   if escapes_the_declaration:
      raise ValueError(
         "token file, theme {0}, token {1} would escape its declaration, got {2!r}".format(
            theme, name, value
         )
      )

   return trimmed
