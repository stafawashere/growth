"""Command-line wrapper around app.design.tokens for the operator.

Usage: python3 tools/check_tokens.py <path to a token file>

Prints every violation the token file has, one per line, then the computed contrast ratio for
every pair token_violations checks, so the operator sees the margin and not only the verdict.
Exits 0 when there are no violations and 1 otherwise.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.design.contrast import contrast_ratio
from app.design.tokens import CONTRAST_PAIRS, THEMES, load_tokens, token_violations


def _print_ratios(tokens):
   for theme in THEMES:
      has_theme = theme in tokens

      if not has_theme:
         continue

      theme_tokens = tokens[theme]

      for foreground_name, background_name in CONTRAST_PAIRS:
         has_both = foreground_name in theme_tokens and background_name in theme_tokens

         if not has_both:
            continue

         foreground_value = theme_tokens[foreground_name]
         background_value = theme_tokens[background_name]

         try:
            ratio = contrast_ratio(foreground_value, background_value)
         except ValueError:
            continue

         print("{0}: {1} on {2} is {3:.2f}:1".format(theme, foreground_name, background_name, ratio))


def main():
   has_path_argument = len(sys.argv) == 2

   if not has_path_argument:
      print("usage: python3 tools/check_tokens.py <path>", file=sys.stderr)
      return 2

   path = sys.argv[1]

   try:
      tokens = load_tokens(path)
   except ValueError as error:
      print(str(error), file=sys.stderr)
      return 1

   violations = token_violations(tokens)

   for violation in violations:
      print(violation)

   _print_ratios(tokens)

   has_violations = len(violations) > 0

   return 1 if has_violations else 0


if __name__ == "__main__":
   sys.exit(main())
