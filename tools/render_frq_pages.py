"""Render fixture photographs of written booklet pages, for tests and for golden set 3.

Usage: python3 tools/render_frq_pages.py <spec.json> <out_dir>
       python3 tools/render_frq_pages.py --golden   (golden sets 2 and 3, for the transcription eval)

No photograph of real handwriting exists yet, so the fixtures are drawn: the app's own booklet page
(app/capture/booklet.py) with the written lines of a spec set in a handwriting font, then
photographed in software under a named condition. They are a stand-in, labelled as rendered
wherever they are used, and the first real captures should replace them (BUILD-LEDGER.md).

A spec is {"pages": [{"name", "item_id", "parts": {"a": [line, ...]}, "conditions": [...]}]}. A
line is a string in a small markup: ^{...} is a superscript, _{...} a subscript, \\frac{a}{b} a
stacked fraction, and \\int \\pi \\sqrt \\infty \\to \\cdot \\theta \\approx \\le \\ge draw their symbols.
A line starting with "~~ " is drawn and struck through, as crossed-out work.

Conditions: clean (a phone photo on a desk, slightly rotated, uneven light), angled (a stronger
rotation), blur, low_light, cropped (the bottom of the page cut off) and far (the page small
in the frame). The fonts are macOS system fonts, read only when the tool runs; the rendered JPEGs
are what gets committed.
"""
import json
import random
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

from app.capture import booklet
from app.frq.items import load_frq_records

HAND_FONT_PATH = "/System/Library/Fonts/Supplemental/Bradley Hand Bold.ttf"
SYMBOL_FONT_PATH = "/System/Library/Fonts/Supplemental/STIXTwoMath.otf"
INK_COLOURS = ((20, 22, 30), (18, 30, 70))
LINE_HEIGHT_PX = 92
TEXT_SIZE_PX = 38
SCRIPT_SIZE_PX = 24
SYMBOLS = {
   "\\int": "\u222b",
   "\\pi": "\u03c0",
   "\\sqrt": "\u221a",
   "\\infty": "\u221e",
   "\\to": "\u2192",
   "\\cdot": "\u00b7",
   "\\theta": "\u03b8",
   "\\approx": "\u2248",
   "\\le": "\u2264",
   "\\ge": "\u2265",
   "\\Delta": "\u0394",
   "\\sum": "\u03a3",
   "\\neq": "\u2260",
   "\\pm": "\u00b1",
   "\\times": "\u00d7",
   "\\Rightarrow": "\u21d2",
   "\\prime": "'",
}
SYMBOL_CHARACTERS = set(SYMBOLS.values())


def fonts(size):
   return ImageFont.truetype(HAND_FONT_PATH, size), ImageFont.truetype(SYMBOL_FONT_PATH, size)


def draw_run(draw, x, y, text, size, ink):
   hand, symbol = fonts(size)

   for character in text:
      face = symbol if character in SYMBOL_CHARACTERS else hand
      draw.text((x, y), character, fill=ink, font=face)
      x += draw.textlength(character, font=face)

   return x


def symbolised(text):
   for command, glyph in SYMBOLS.items():
      text = text.replace(command, glyph)

   return text


NAMED = ("lim", "sin", "cos", "tan", "sec", "csc", "cot", "ln", "log", "exp", "arctan", "arcsin")
DROPPED = ("\\left", "\\right", "\\displaystyle", "\\(", "\\)", "\\[", "\\]")


def cleaned(markup):
   text = markup

   for dropped in DROPPED:
      text = text.replace(dropped, "")

   return text.replace("\\,", " ").replace("\\quad", "   ").replace("\\;", " ")


def braced(text, start):
   """The contents of the brace group opening at start, and the index just past it."""
   depth = 0

   for position in range(start, len(text)):
      if text[position] == "{":
         depth += 1
      elif text[position] == "}":
         depth -= 1

         if depth == 0:
            return text[start + 1:position], position + 1

   return text[start + 1:], len(text)


def argument(text, start):
   """A braced group, or the single character at start."""
   has_group = start < len(text) and text[start] == "{"

   if has_group:
      return braced(text, start)

   return text[start:start + 1], start + 1


def width_of(draw, text, size):
   scratch = Image.new("L", (1, 1))

   return render_markup(ImageDraw.Draw(scratch), 0, 0, text, size, 0, measure=True)


def render_markup(draw, x, y, text, size, ink, measure=False):
   """Draws the markup from x on baseline row y and returns the x it ends at. Handles nested
   \\frac, \\sqrt, ^ and _ groups, \\text and the symbol commands."""
   position = 0

   while position < len(text):
      character = text[position]

      if character in "^_":
         group, position = argument(text, position + 1)
         offset = -int(size * 0.38) if character == "^" else int(size * 0.5)
         x = render_markup(draw, x + 2, y + offset, group, max(18, int(size * 0.62)), ink, measure) + 2
         continue

      if character in "{}":
         position += 1
         continue

      if character != "\\":
         if not measure:
            draw_run(draw, x, y, character, size, ink)

         x += draw.textlength(character, font=fonts(size)[0])
         position += 1
         continue

      end = position + 1

      while end < len(text) and text[end].isalpha():
         end += 1

      command = text[position:end]
      name = command[1:]
      position = end

      if name == "frac":
         numerator, position = argument(text, position)
         denominator, position = argument(text, position)
         small = max(22, int(size * 0.75))
         top_width = width_of(draw, numerator, small)
         bottom_width = width_of(draw, denominator, small)
         width = max(top_width, bottom_width) + 8
         render_markup(draw, x + (width - top_width) / 2, y - int(size * 0.62), numerator, small, ink, measure)
         render_markup(draw, x + (width - bottom_width) / 2, y + int(size * 0.62), denominator, small, ink, measure)

         if not measure:
            draw.line((x, y + int(size * 0.56), x + width, y + int(size * 0.54)), fill=ink, width=3)

         x += width + 6
         continue

      if name in ("text", "mathrm", "sout"):
         group, position = argument(text, position)
         x = render_markup(draw, x, y, group, size, ink, measure)
         continue

      if name == "sqrt":
         group, position = argument(text, position)

         if not measure:
            draw_run(draw, x, y, SYMBOLS["\\sqrt"], size, ink)

         inner_start = x + draw.textlength(SYMBOLS["\\sqrt"], font=fonts(size)[1])
         end_x = render_markup(draw, inner_start, y, group, size, ink, measure)

         if not measure:
            draw.line((inner_start, y + 2, end_x, y + 2), fill=ink, width=2)

         x = end_x + 4
         continue

      glyph = SYMBOLS.get(command)
      shown = glyph if glyph is not None else (name if name in NAMED else name)

      if not measure:
         draw_run(draw, x, y, shown, size, ink)

      face = fonts(size)[1] if glyph is not None else fonts(size)[0]
      x += draw.textlength(shown, font=face) + (4 if name in NAMED else 0)

   return x


def draw_line(draw, x, y, markup, ink):
   return x, render_markup(draw, x, y, cleaned(markup), TEXT_SIZE_PX, ink)


def written_page(record, parts, seed):
   rng = random.Random(seed)
   page = booklet.draw_page(record)
   draw = ImageDraw.Draw(page)
   ink = INK_COLOURS[seed % len(INK_COLOURS)]
   boxes = booklet.part_boxes([part["id"] for part in record["parts"]])

   for part_id, lines in parts.items():
      left, top, _right, bottom = boxes[part_id]
      y = top + 70

      for line in lines:
         in_margin = line.startswith("@@ ")

         if in_margin:
            draw_line(draw, left + 420, bottom + 22, line[3:], ink)
            continue

         crossed = line.startswith("~~ ")
         markup = line[3:] if crossed else line
         x = left + 60 + rng.randint(-6, 6)
         start_x, end_x = draw_line(draw, x, y + rng.randint(-3, 3), markup, ink)

         if crossed:
            draw.line((start_x - 5, y + 22, end_x + 5, y + 18), fill=ink, width=4)

         y += LINE_HEIGHT_PX + rng.randint(-4, 6)

   return page


def on_desk(page, scale, rotation, rng):
   desk = Image.new("RGB", (int(page.width * scale * 1.25), int(page.height * scale * 1.18)), (118, 96, 72))
   noise = Image.effect_noise(desk.size, 18).convert("RGB")
   desk = Image.blend(desk, noise, 0.12)
   small = page.resize((int(page.width * scale), int(page.height * scale)), Image.Resampling.LANCZOS)
   rotated = small.rotate(rotation, expand=True, resample=Image.Resampling.BICUBIC, fillcolor=(118, 96, 72))
   left = (desk.width - rotated.width) // 2 + rng.randint(-20, 20)
   top = (desk.height - rotated.height) // 2 + rng.randint(-20, 20)
   desk.paste(rotated, (left, top))

   return desk


def uneven_light(photo, strength):
   gradient = Image.linear_gradient("L").resize(photo.size).rotate(35, expand=False, fillcolor=128)

   return Image.blend(photo, Image.composite(photo, ImageEnhance.Brightness(photo).enhance(0.8), gradient), strength)


def photographed(page, condition, seed):
   rng = random.Random(seed)
   rotation = rng.uniform(-2.0, 2.0)
   photo = on_desk(page, 1.5, rotation, rng)
   photo = uneven_light(photo, 0.5)

   if condition == "angled":
      photo = on_desk(page, 1.5, rng.uniform(-6.0, 6.0), rng)

   if condition == "blur":
      photo = photo.filter(ImageFilter.GaussianBlur(radius=7))

   if condition == "slight_blur":
      photo = photo.filter(ImageFilter.GaussianBlur(radius=1.6))

   if condition == "low_light":
      photo = ImageEnhance.Brightness(photo).enhance(0.22)
      noise = Image.effect_noise(photo.size, 30).convert("RGB")
      photo = Image.blend(photo, noise, 0.08)

   if condition == "cropped":
      photo = photo.crop((0, 0, photo.width, int(photo.height * 0.72)))

   if condition == "far":
      far_desk = Image.new("RGB", (photo.width * 2, photo.height * 2), (118, 96, 72))
      far_desk.paste(photo, (photo.width // 2, photo.height // 2))
      photo = far_desk.resize(photo.size, Image.Resampling.LANCZOS)

   return photo


def render(spec_path, out_dir):
   spec = json.loads(Path(spec_path).read_text())
   records = {record["id"]: record for record in load_frq_records(REPO_ROOT / "content" / "frq_items")}
   records.update({record["id"]: record for record in spec.get("records", [])})
   out = Path(out_dir)
   out.mkdir(parents=True, exist_ok=True)
   written = []

   for index, page_spec in enumerate(spec["pages"]):
      record = records[page_spec["item_id"]]
      page = written_page(record, page_spec["parts"], seed=index)

      for condition in page_spec.get("conditions", ["clean"]):
         photo = photographed(page, condition, seed=index * 31 + len(condition))
         path = out / f"{page_spec['name']}__{condition}.jpg"
         photo.save(path, format="JPEG", quality=85)
         written.append(path)

   return written


GOLDEN3_CONDITIONS = {
   "good_light": "clean",
   "low_light": "low_light",
   "slight_blur": "slight_blur",
   "angled": "angled",
   "crossed_out": "clean",
   "margin_work": "clean",
   "injected_instruction": "clean",
}
GOLDEN3_OUT = REPO_ROOT / "tests" / "fixtures" / "frq_pages" / "golden3"
GOLDEN2_OUT = REPO_ROOT / "tests" / "fixtures" / "frq_pages" / "golden2"


def golden3_markup(written):
   struck = "\\sout{"
   margin = "\\text{[margin] }"

   if written.startswith(struck):
      return "~~ " + written[len(struck):-1]

   if written.startswith(margin):
      return "@@ " + written[len(margin):]

   return written


GOLDEN_LONG_EDGE_PX = 2000


def smaller(photo):
   """A phone photo scaled to a 2000 px long edge, which the transcriber's high-resolution tier
   still reads whole and which keeps the committed fixtures small."""
   scale = GOLDEN_LONG_EDGE_PX / max(photo.size)

   return photo.resize((round(photo.width * scale), round(photo.height * scale)), Image.Resampling.LANCZOS)


def render_golden_pages():
   """Golden set 3's pages from P7's page specifications, and golden-2 responses on their own
   question's booklet page, for app/grading/transcription_eval.py."""
   from app.grading import transcription_eval

   written = []
   cases = json.loads(transcription_eval.GOLDEN3_SPEC.read_text())["cases"]
   GOLDEN3_OUT.mkdir(parents=True, exist_ok=True)

   for index, case in enumerate(cases):
      record = transcription_eval.page_record(case)
      page = written_page(record, {"a": [golden3_markup(line) for line in case["transcript"]]}, seed=index)
      photo = photographed(page, GOLDEN3_CONDITIONS[case["variation"]], seed=100 + index)
      path = GOLDEN3_OUT / f"{case['id']}.jpg"
      smaller(photo).save(path, format="JPEG", quality=80)
      written.append(path)

   records, sample = transcription_eval.golden2_sample()
   GOLDEN2_OUT.mkdir(parents=True, exist_ok=True)

   for index, response in enumerate(sample):
      parts = {
         part["part_id"]: [("~~ " if line["crossed_out"] else "") + line["content"] for line in part["lines"]]
         for part in response["work"]["parts"]
      }
      page = written_page(records[response["item_id"]], parts, seed=200 + index)
      photo = photographed(page, "clean", seed=300 + index)
      path = GOLDEN2_OUT / f"{response['id']}.jpg"
      smaller(photo).save(path, format="JPEG", quality=80)
      written.append(path)

   return written


if __name__ == "__main__":
   is_golden = sys.argv[1] == "--golden"
   written_paths = render_golden_pages() if is_golden else render(sys.argv[1], sys.argv[2])

   for written_path in written_paths:
      print(written_path.relative_to(REPO_ROOT) if written_path.is_relative_to(REPO_ROOT) else written_path)
