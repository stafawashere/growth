"""The printable answer page, 11 P3 scope item 1.

It follows the documented free-response booklet: boxed, unlined, addressed by question and part,
with a header naming the calculator status of the part, and instructions to write in pencil or in
black or dark blue ink inside the boxes and that crossed-out work is not scored
(https://apcentral.collegeboard.org/media/pdf/ap-hybrid-digital-exams-free-response-booklets-overview.pdf,
[verified] in 05). The page is the app's own drawing: no official page is copied.

A solid square in each corner is the page marker app/capture/quality.py looks for, so a photograph
with all four markers has the whole page in frame. The page is rendered as a PNG at 150 dots per
inch on US Letter, which prints at full size from the browser.
"""
import io

from PIL import Image, ImageDraw, ImageFont

DOTS_PER_INCH = 150
PAGE_WIDTH_PX = int(8.5 * DOTS_PER_INCH)
PAGE_HEIGHT_PX = int(11 * DOTS_PER_INCH)
MARKER_SIDE_PX = 60
MARKER_MARGIN_PX = 45
BOX_MARGIN_PX = 90
HEADER_TOP_PX = 125
BOX_TOP_PX = 330
BOX_BOTTOM_MARGIN_PX = 130
BOX_GAP_PX = 28
INK = (0, 0, 0)
PAPER = (255, 255, 255)

CALCULATOR_HEADERS = {
   "no_calculator": "NO CALCULATOR IS ALLOWED FOR THIS QUESTION.",
   "calculator": "A GRAPHING CALCULATOR IS REQUIRED FOR THIS QUESTION.",
   "either": "NO CALCULATOR IS ALLOWED FOR THIS QUESTION.",
}

INSTRUCTIONS = (
   "Write in pencil or in black or dark blue ink, inside the boxes only.",
   "Crossed-out work is not scored. Show your work in the box for each part.",
)


def font(size):
   """Pillow's bundled scalable font, so the page draws the same on every machine."""
   return ImageFont.load_default(size=size)


def part_boxes(part_ids):
   """The box for each part as (left, top, right, bottom), stacked down the page."""
   count = max(1, len(part_ids))
   usable = PAGE_HEIGHT_PX - BOX_TOP_PX - BOX_BOTTOM_MARGIN_PX - BOX_GAP_PX * (count - 1)
   height = usable // count
   boxes = {}

   for index, part_id in enumerate(part_ids):
      top = BOX_TOP_PX + index * (height + BOX_GAP_PX)
      boxes[part_id] = (BOX_MARGIN_PX, top, PAGE_WIDTH_PX - BOX_MARGIN_PX, top + height)

   return boxes


def marker_boxes():
   side = MARKER_SIDE_PX
   margin = MARKER_MARGIN_PX
   right = PAGE_WIDTH_PX - margin - side
   bottom = PAGE_HEIGHT_PX - margin - side

   return [
      (margin, margin, margin + side, margin + side),
      (right, margin, right + side, margin + side),
      (margin, bottom, margin + side, bottom + side),
      (right, bottom, right + side, bottom + side),
   ]


def page_label(record, question=None):
   part_ids = [part["id"] for part in record["parts"]]
   named = ", ".join(f"({part_id})" for part_id in part_ids)
   is_addressed = question is not None

   if is_addressed:
      return f"Answer Question {question} parts {named} on this page."

   return f"Answer {record['id']} parts {named} on this page."


def draw_page(record, page_code="", header=None, question=None):
   """header and question address the page as a mock's booklet does (the header from the part,
   the question by its exam number); without them the page is addressed by the record."""
   image = Image.new("RGB", (PAGE_WIDTH_PX, PAGE_HEIGHT_PX), PAPER)
   draw = ImageDraw.Draw(image)

   for box in marker_boxes():
      draw.rectangle(box, fill=INK)

   header = header or CALCULATOR_HEADERS.get(record["calculator_status"], CALCULATOR_HEADERS["no_calculator"])
   draw.text((PAGE_WIDTH_PX // 2, HEADER_TOP_PX), header, fill=INK, font=font(30), anchor="mm")
   draw.text((PAGE_WIDTH_PX // 2, HEADER_TOP_PX + 55), page_label(record, question), fill=INK, font=font(24), anchor="mm")

   for index, line in enumerate(INSTRUCTIONS):
      draw.text((PAGE_WIDTH_PX // 2, HEADER_TOP_PX + 105 + index * 32), line, fill=INK, font=font(20), anchor="mm")

   part_ids = [part["id"] for part in record["parts"]]

   for part_id, box in part_boxes(part_ids).items():
      draw.rectangle(box, outline=INK, width=4)
      label_position = (box[0] + 16, box[1] + 12)
      draw.text(label_position, f"({part_id})", fill=INK, font=font(30))

   has_code = page_code != ""

   if has_code:
      code_position = (PAGE_WIDTH_PX // 2, PAGE_HEIGHT_PX - MARKER_MARGIN_PX - MARKER_SIDE_PX // 2)
      draw.text(code_position, page_code, fill=INK, font=font(18), anchor="mm")

   return image


def page_png(record, page_code="", header=None, question=None):
   buffer = io.BytesIO()
   draw_page(record, page_code, header=header, question=question).save(buffer, format="PNG")

   return buffer.getvalue()
