"""Render fixture photographs of written booklet pages, for tests and for golden set 3.

Usage: python3 tools/render_frq_pages.py <spec.json> <out_dir>

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
import re
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
LINE_HEIGHT_PX = 58
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
}
SYMBOL_CHARACTERS = set(SYMBOLS.values())
TOKEN = re.compile(r"\\frac\{([^{}]*)\}\{([^{}]*)\}|\^\{([^{}]*)\}|_\{([^{}]*)\}|(\\[a-zA-Z]+)|(.)", re.S)


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


def draw_line(draw, x, y, markup, ink):
   start_x = x

   for match in TOKEN.finditer(markup):
      numerator, denominator, superscript, subscript, command, plain = match.groups()

      if numerator is not None:
         top_width = draw_run(draw, x, y - 20, symbolised(numerator), SCRIPT_SIZE_PX + 4, ink) - x
         bottom_width = draw_run(draw, x, y + 18, symbolised(denominator), SCRIPT_SIZE_PX + 4, ink) - x
         width = max(top_width, bottom_width) + 6
         draw.line((x - 2, y + 17, x + width, y + 16), fill=ink, width=3)
         x += width + 6
      elif superscript is not None:
         x = draw_run(draw, x + 2, y - 14, symbolised(superscript), SCRIPT_SIZE_PX, ink) + 3
      elif subscript is not None:
         x = draw_run(draw, x + 2, y + 20, symbolised(subscript), SCRIPT_SIZE_PX, ink) + 3
      elif command is not None:
         x = draw_run(draw, x, y, SYMBOLS.get(command, command.lstrip("\\")), TEXT_SIZE_PX, ink)
      else:
         x = draw_run(draw, x, y, plain, TEXT_SIZE_PX, ink)

   return start_x, x


def written_page(record, parts, seed):
   rng = random.Random(seed)
   page = booklet.draw_page(record)
   draw = ImageDraw.Draw(page)
   ink = INK_COLOURS[seed % len(INK_COLOURS)]
   boxes = booklet.part_boxes([part["id"] for part in record["parts"]])

   for part_id, lines in parts.items():
      left, top, _right, _bottom = boxes[part_id]
      y = top + 70

      for line in lines:
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


if __name__ == "__main__":
   for written_path in render(sys.argv[1], sys.argv[2]):
      print(written_path.relative_to(REPO_ROOT) if written_path.is_relative_to(REPO_ROOT) else written_path)
