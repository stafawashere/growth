"""Gate 26's other half: the module that turns a filled token file into CSS custom properties.

The client must never carry a hex value, so app/design/css.py is the only bridge between the
operator-filled token file and the React client. These tests scan app/design/tokens.py's own
vocabulary rather than typing a token list out a second time, and they check the generated
stylesheet against the token file it was built from rather than against a hand copied palette.
"""

import json
import re
from pathlib import Path

import pytest

from app.design import css
from app.design.tokens import COLOUR_TOKENS, SPACING_TOKENS, THEMES, TYPE_TOKENS

REPO_ROOT = Path(__file__).resolve().parents[2]
TEMPLATE_PATH = REPO_ROOT / "docs" / "operator" / "design-tokens.template.json"

SAMPLE_COLOUR = "#123456"
SAMPLE_TYPE_VALUE = "1rem"


def _full_token_file():
   tokens = {}

   for theme_index, theme in enumerate(THEMES):
      theme_tokens = {}

      for index, name in enumerate(COLOUR_TOKENS):
         theme_tokens[name] = "#{0:06x}".format(index + 1 + theme_index * 1000)

      for name in TYPE_TOKENS:
         theme_tokens[name] = "1rem"

      tokens[theme] = theme_tokens

   return tokens


def _theme_block(stylesheet, theme):
   pattern = r'\[data-theme="{0}"\]\s*\{{(.*?)\}}'.format(theme)
   match = re.search(pattern, stylesheet, re.DOTALL)
   found_block = match is not None

   assert found_block, "no selector found for theme {0}".format(theme)

   return match.group(1)


def _root_block(stylesheet):
   match = re.search(r":root\s*\{(.*?)\}", stylesheet, re.DOTALL)
   found_block = match is not None

   assert found_block, "no :root selector found in stylesheet"

   return match.group(1)


def _no_theme_fallback_blocks(stylesheet):
   """The two `:root:not([data-theme])` blocks app/design/css.py emits: the light one outside
   any media query, and the dark one nested in `@media (prefers-color-scheme: dark)`, in that
   order, matching app/web/src/theme.ts's own light-unless-dark-matches rule."""
   pattern = r":root:not\(\[data-theme\]\)\s*\{(.*?)\}"
   matches = list(re.finditer(pattern, stylesheet, re.DOTALL))

   assert len(matches) == 2, (
      "expected exactly two :root:not([data-theme]) blocks, found {0}".format(len(matches))
   )

   light_block, dark_block = matches[0].group(1), matches[1].group(1)

   return light_block, dark_block


def _declared_custom_properties(block):
   return dict(re.findall(r"(--growth-[a-z0-9-]+):\s*(.*?);", block))


def test_custom_properties_cover_every_token():
   tokens = _full_token_file()
   stylesheet = css.stylesheet_from_tokens(tokens)

   expected_names = [css.custom_property_name(name) for name in COLOUR_TOKENS]
   expected_names += [css.custom_property_name(name) for name in TYPE_TOKENS]

   for name in expected_names:
      assert name in css.CUSTOM_PROPERTIES

   for theme in THEMES:
      theme_block = _theme_block(stylesheet, theme)

      for property_name in expected_names:
         assert property_name in theme_block


def test_the_no_theme_fallback_follows_theme_ts_system_preference_rule():
   """app/web/src/theme.ts resolves the page's theme before any [data-theme] attribute exists
   by matching `(prefers-color-scheme: dark)`, dark on a match and light otherwise. Before that
   resolution runs, the document carries no data-theme attribute at all, so app/design/css.py
   has to give that unstyled moment the same two outcomes: light values under
   `:root:not([data-theme])`, overridden for a dark system preference by the same selector
   nested in a `(prefers-color-scheme: dark)` media block. Every custom property the themed
   selector declares must appear in the matching fallback block with the same value.
   """
   tokens = _full_token_file()
   stylesheet = css.stylesheet_from_tokens(tokens)

   light_fallback_index = stylesheet.index(":root:not([data-theme])")
   media_query_index = stylesheet.index("@media (prefers-color-scheme: dark)")

   assert light_fallback_index < media_query_index, (
      "the light fallback must sit outside the dark media query, not inside it"
   )

   light_fallback_block, dark_fallback_block = _no_theme_fallback_blocks(stylesheet)
   fallback_blocks = {"light": light_fallback_block, "dark": dark_fallback_block}

   for theme in THEMES:
      themed_declared = _declared_custom_properties(_theme_block(stylesheet, theme))
      fallback_declared = _declared_custom_properties(fallback_blocks[theme])

      assert fallback_declared == themed_declared, (
         "the {0} fallback declares {1}, the {0} theme declares {2}".format(
            theme, fallback_declared, themed_declared
         )
      )


def test_stylesheet_carries_no_colour_the_token_file_did_not_give():
   incomplete_tokens = _full_token_file()
   del incomplete_tokens["light"][COLOUR_TOKENS[0]]

   with pytest.raises(Exception):
      css.stylesheet_from_tokens(incomplete_tokens)

   complete_tokens = _full_token_file()
   stylesheet = css.stylesheet_from_tokens(complete_tokens)

   given_hex_values = set()

   for theme in THEMES:
      for value in complete_tokens[theme].values():
         is_hex_value = isinstance(value, str) and value.startswith("#")

         if is_hex_value:
            given_hex_values.add(value)

   hex_literals_in_stylesheet = set(re.findall(r"#[0-9a-fA-F]{3,6}", stylesheet))

   assert len(hex_literals_in_stylesheet) > 0

   for hex_literal in hex_literals_in_stylesheet:
      assert hex_literal in given_hex_values


def _filled_real_template():
   template = json.loads(TEMPLATE_PATH.read_text())
   filled = {}

   for theme, theme_tokens in template.items():
      values = {}

      for name in theme_tokens:
         is_colour = name in COLOUR_TOKENS
         values[name] = SAMPLE_COLOUR if is_colour else SAMPLE_TYPE_VALUE

      filled[theme] = values

   return filled


def test_the_operator_template_offers_every_token_the_vocabulary_names():
   template = json.loads(TEMPLATE_PATH.read_text())
   expected_names = set(COLOUR_TOKENS) | set(TYPE_TOKENS)

   assert set(template.keys()) == set(THEMES)

   for theme in THEMES:
      offered_names = set(template[theme].keys())

      assert offered_names == expected_names, (
         "the operator cannot fill a token the template does not offer, and these are "
         "missing from theme {0}: {1}".format(theme, sorted(expected_names - offered_names))
      )

      for name, value in template[theme].items():
         assert value is None, "the template carries no value, {0} holds {1!r}".format(name, value)


def test_the_filled_operator_template_emits_every_advertised_custom_property():
   stylesheet = css.stylesheet_from_tokens(_filled_real_template())
   operator_property_names = {
      css.custom_property_name(name) for name in list(COLOUR_TOKENS) + list(TYPE_TOKENS)
   }
   spacing_property_names = {css.custom_property_name(name) for name in SPACING_TOKENS}

   assert operator_property_names | spacing_property_names == set(css.CUSTOM_PROPERTIES)

   for theme in THEMES:
      theme_block = _theme_block(stylesheet, theme)
      declared = set(re.findall(r"(--growth-[a-z0-9-]+)\s*:", theme_block))

      assert declared == operator_property_names, (
         "theme {0} declares {1} of the {2} operator-filled custom properties, missing {3}".format(
            theme, len(declared), len(operator_property_names),
            sorted(operator_property_names - declared)
         )
      )

   root_declared = set(re.findall(r"(--growth-[a-z0-9-]+)\s*:", _root_block(stylesheet)))

   assert root_declared == spacing_property_names, (
      "the :root block declares {0} of the {1} spacing custom properties, missing {2}".format(
         len(root_declared), len(spacing_property_names),
         sorted(spacing_property_names - root_declared)
      )
   )


def test_a_type_token_the_token_file_omits_is_refused():
   for name in TYPE_TOKENS:
      tokens = _filled_real_template()
      del tokens["light"][name]

      with pytest.raises(ValueError) as refusal:
         css.stylesheet_from_tokens(tokens)

      assert name in str(refusal.value)


def test_a_null_type_value_is_refused():
   tokens = _filled_real_template()
   tokens["dark"]["type-body"] = None

   with pytest.raises(ValueError) as refusal:
      css.stylesheet_from_tokens(tokens)

   assert "type-body" in str(refusal.value)


def test_a_type_value_that_escapes_its_declaration_is_refused():
   escaping_values = (
      "1rem; color: red",
      "1rem} body {display: none",
      "1rem</style><script>alert(1)</script>",
      "1rem/* comment",
      "1rem\\3c /style",
      "",
      "   ",
   )

   for escaping_value in escaping_values:
      tokens = _filled_real_template()
      tokens["light"]["type-display"] = escaping_value

      with pytest.raises(ValueError) as refusal:
         css.stylesheet_from_tokens(tokens)

      assert "type-display" in str(refusal.value)


def test_custom_properties_advertise_every_spacing_token():
   expected_names = [css.custom_property_name(name) for name in SPACING_TOKENS]

   for name in expected_names:
      assert name in css.CUSTOM_PROPERTIES


def test_root_block_carries_every_spacing_value_regardless_of_the_token_file():
   tokens = _full_token_file()
   stylesheet = css.stylesheet_from_tokens(tokens)
   root_block = _root_block(stylesheet)

   for name, value in SPACING_TOKENS.items():
      expected_declaration = "{0}: {1}px;".format(css.custom_property_name(name), value)

      assert expected_declaration in root_block


def test_spacing_never_appears_inside_a_theme_block():
   tokens = _full_token_file()
   stylesheet = css.stylesheet_from_tokens(tokens)

   for theme in THEMES:
      theme_block = _theme_block(stylesheet, theme)

      for name in SPACING_TOKENS:
         assert css.custom_property_name(name) not in theme_block


def _write_token_file(path, tokens):
   path.write_text(json.dumps(tokens))

   return path


def test_stylesheet_from_token_file_reads_the_file_and_validates_it(tmp_path):
   tokens = _filled_real_template()
   path = _write_token_file(tmp_path / "tokens.json", tokens)

   from_file = css.stylesheet_from_token_file(path)
   from_dict = css.stylesheet_from_tokens(tokens)

   assert from_file == from_dict


def test_stylesheet_from_token_file_refuses_a_missing_token(tmp_path):
   tokens = _filled_real_template()
   del tokens["light"]["type-body"]
   path = _write_token_file(tmp_path / "tokens.json", tokens)

   with pytest.raises(ValueError) as refusal:
      css.stylesheet_from_token_file(path)

   assert "type-body" in str(refusal.value)


def test_stylesheet_from_token_file_refuses_a_null_token(tmp_path):
   tokens = _filled_real_template()
   tokens["dark"]["text-primary"] = None
   path = _write_token_file(tmp_path / "tokens.json", tokens)

   with pytest.raises(ValueError):
      css.stylesheet_from_token_file(path)


def test_stylesheet_from_token_file_raises_on_invalid_json(tmp_path):
   path = tmp_path / "tokens.json"
   path.write_text("{ not valid json")

   with pytest.raises(Exception):
      css.stylesheet_from_token_file(path)


def test_stylesheet_from_token_file_raises_on_an_unreadable_file(tmp_path):
   path = tmp_path / "does-not-exist.json"

   with pytest.raises(Exception):
      css.stylesheet_from_token_file(path)


def test_the_stylesheet_carries_no_value_the_token_file_did_not_give():
   tokens = _filled_real_template()
   stylesheet = css.stylesheet_from_tokens(tokens)

   given_values = set()

   for theme_tokens in tokens.values():
      given_values.update(theme_tokens.values())

   operator_property_count = len(COLOUR_TOKENS) + len(TYPE_TOKENS)

   for theme in THEMES:
      theme_block = _theme_block(stylesheet, theme)
      emitted = re.findall(r"--growth-[a-z0-9-]+:\s*(.*?);", theme_block)

      assert len(emitted) == operator_property_count

      for value in emitted:
         assert value in given_values
