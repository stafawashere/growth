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
"""

from app.design.tokens import COLOUR_TOKENS, THEMES, TYPE_TOKENS

CUSTOM_PROPERTY_PREFIX = "--growth-"

_DECLARATION_BREAKING_CHARACTERS = (";", "{", "}", "<", ">", "\\", "\"", "'")

_DECLARATION_BREAKING_SEQUENCES = ("/*", "*/")


def custom_property_name(token):
   return CUSTOM_PROPERTY_PREFIX + token


CUSTOM_PROPERTIES = tuple(
   custom_property_name(name) for name in COLOUR_TOKENS
) + tuple(
   custom_property_name(name) for name in TYPE_TOKENS
)


def stylesheet_from_tokens(tokens):
   selectors = []

   for theme in THEMES:
      has_theme = theme in tokens

      if not has_theme:
         raise ValueError("token file is missing theme {0}".format(theme))

      selectors.append(_selector_for_theme(theme, tokens[theme]))

   return "\n\n".join(selectors)


def _selector_for_theme(theme, theme_tokens):
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

   selector = '[data-theme="{0}"]'.format(theme)

   return "{0} {{\n{1}\n}}".format(selector, "\n".join(declarations))


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
