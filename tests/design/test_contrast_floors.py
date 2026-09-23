"""Gate 26, docs/plan/11-phased-delivery.md: every text token holds 4.5:1, and type-title and
type-display hold 3:1, in both themes.

The hex values are read out of app/design/growth-tokens.json, the file entry criterion 5 and
implementer decision 6 have the implementer produce, and every ratio is computed here with
app/design/contrast.py. The pairs are app/design/tokens.py's CONTRAST_PAIRS and the floors are its
TYPE_TOKEN_FLOORS, so nothing below types a colour name, a ratio or a size of its own.
"""

import re
from pathlib import Path

from app.design import tokens
from app.design.contrast import contrast_ratio

REPO_ROOT = Path(__file__).resolve().parents[2]
TOKEN_FILE_PATH = REPO_ROOT / "app" / "design" / "growth-tokens.json"
BRIEF_PATH = REPO_ROOT / "docs" / "plan" / "08-design-brief.md"


def _token_file():
   return tokens.load_tokens(TOKEN_FILE_PATH)


def _names_with_prefix(prefix):
   return [name for name in tokens.COLOUR_TOKENS if name.startswith(prefix)]


def test_contrast_floors():
   token_file = _token_file()
   below_floor = []

   for theme in tokens.THEMES:
      theme_tokens = token_file[theme]

      for foreground_name, background_name in tokens.CONTRAST_PAIRS:
         ratio = contrast_ratio(theme_tokens[foreground_name], theme_tokens[background_name])

         for type_name, floor in tokens.TYPE_TOKEN_FLOORS.items():
            is_below_floor = ratio < floor

            if is_below_floor:
               below_floor.append(
                  "{0}: {1} on {2} at {3} is {4:.2f}:1, floor {5}:1".format(
                     theme, foreground_name, background_name, type_name, ratio, floor
                  )
               )

   assert below_floor == []


def test_the_token_file_passes_the_validator_it_is_checked_by():
   assert tokens.token_violations(_token_file()) == []


def test_the_gate_pairs_put_every_text_role_on_every_surface():
   """Read off the vocabulary by name, so a pair dropped from CONTRAST_PAIRS cannot shrink what
   the gate checks without this failing."""
   pairs = set(tokens.CONTRAST_PAIRS)
   surfaces = _names_with_prefix("surface-")
   text_roles = [name for name in _names_with_prefix("text-") if name != "text-on-accent"]
   missing = [
      (role, surface)
      for role in text_roles
      for surface in surfaces
      if (role, surface) not in pairs
   ]

   assert surfaces
   assert text_roles
   assert missing == []


def test_every_text_and_state_token_is_a_foreground_in_the_gate():
   foregrounds = {foreground for foreground, _ in tokens.CONTRAST_PAIRS}
   carries_a_floor = [
      name
      for name in tokens.COLOUR_TOKENS
      if "text" in name or name.startswith("state-") or name == "focus-ring"
   ]
   unchecked = [name for name in carries_a_floor if name not in foregrounds]

   assert unchecked == []


def test_the_gate_pairs_put_focus_ring_and_every_semantic_colour_on_every_surface():
   """08's Accessibility section says focus-ring is visible against every surface, and 08's
   Colour system gives state-correct and state-incorrect a role on every surface too. The
   required pairs are derived here from SURFACES and from COLOUR_TOKENS' own state- names, never
   typed as a literal list, so a CONTRAST_PAIRS edit that quietly drops a surface for either
   vocabulary member fails this rather than only shrinking silently."""
   pairs = set(tokens.CONTRAST_PAIRS)
   surfaces = _names_with_prefix("surface-")
   semantic_colours = _names_with_prefix("state-")

   required = [("focus-ring", surface) for surface in surfaces] + [
      (colour, surface) for colour in semantic_colours for surface in surfaces
   ]

   missing = [pair for pair in required if pair not in pairs]

   assert surfaces
   assert semantic_colours
   assert missing == []


def _brief_type_sizes():
   text = BRIEF_PATH.read_text()
   start = text.index("## Type system")
   end = text.index("## Colour system", start)
   rows = re.findall(r"\|\s*`(type-[a-z-]+)`\s*\|\s*(\d+) px\s*\|", text[start:end])

   return {name: "{0}px".format(size) for name, size in rows}


def test_the_token_file_type_values_are_08s_sizes():
   brief_sizes = _brief_type_sizes()
   token_file = _token_file()

   assert set(brief_sizes) == set(tokens.TYPE_TOKENS)

   for theme in tokens.THEMES:
      file_sizes = {name: token_file[theme][name] for name in tokens.TYPE_TOKENS}

      assert file_sizes == brief_sizes
