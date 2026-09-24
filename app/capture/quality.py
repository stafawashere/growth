"""The image quality gate that runs before any provider call, 11 P3 scope item 2.

Four checks, each on the decoded photograph, none of which calls a model:

- blur: the variance of a Laplacian over the page at a fixed analysis size. Handwriting is thin
  strokes, and a blurred photograph loses exactly the high-frequency energy the Laplacian measures.
- contrast: the spread between the darkest half percent of the page (ink and markers) and the
  95th luminance percentile (paper), and the mean luminance, which catch a page photographed in
  low light or washed out. A written page is mostly paper, so a wider percentile would measure
  paper against paper.
- page markers: the printed booklet page carries a solid square in each corner. Finding all four,
  one in each corner region, means the whole page is in the frame.
- crop: markers found but squeezed into a small part of the frame mean the page is too far away
  to read, so the markers must span most of the photograph.

Poor image quality is a named failure mode in the 2026 AIED study (https://arxiv.org/abs/2605.19043,
[single-source]), so capture failure is budgeted as routine and the verdict says what to fix. The
thresholds are [inferred] and were set on the rendered fixture pages in tests/fixtures/frq_pages
(sharp, blurred, low-light, cropped), which is golden set 3's rendered stand-in: no photograph of
real handwriting exists yet, and the first real captures should re-tune them (BUILD-LEDGER.md).
"""
import hashlib
import io
from dataclasses import dataclass, field

from PIL import Image, ImageFilter, ImageOps, ImageStat, UnidentifiedImageError

ACCEPTED_MEDIA_TYPES = ("image/jpeg", "image/png", "image/webp")
PIL_FORMAT_MEDIA_TYPES = {"JPEG": "image/jpeg", "PNG": "image/png", "WEBP": "image/webp", "MPO": "image/jpeg"}

# https://platform.claude.com/docs/en/build-with-claude/vision: 10 MB per image on the API.
MAX_IMAGE_BYTES = 10 * 1024 * 1024
MIN_SHORT_EDGE_PX = 700

ANALYSIS_LONG_EDGE_PX = 1000
MARKER_LONG_EDGE_PX = 500

MIN_LAPLACIAN_VARIANCE = 60.0
INK_SHARE = 0.005
MIN_LUMINANCE_SPREAD = 90
MIN_MEAN_LUMINANCE = 70
MAX_MEAN_LUMINANCE = 250

CORNER_REGION_SHARE = 0.3
MARKER_MIN_SIDE_SHARE = 0.015
MARKER_MAX_SIDE_SHARE = 0.12
MARKER_MIN_FILL = 0.65
MARKER_MAX_ASPECT = 1.7
MIN_MARKER_SPAN_SHARE = 0.55

CORNERS = ("top_left", "top_right", "bottom_left", "bottom_right")

LAPLACIAN = ImageFilter.Kernel((3, 3), [0, 1, 0, 1, -4, 1, 0, 1, 0], scale=1, offset=128)


@dataclass
class QualityVerdict:
   accepted: bool
   reasons: list = field(default_factory=list)
   measurements: dict = field(default_factory=dict)
   media_type: str | None = None
   width: int = 0
   height: int = 0
   sha256: str = ""

   def as_record(self):
      return {
         "accepted": self.accepted,
         "reasons": list(self.reasons),
         "measurements": dict(self.measurements),
      }


def decoded(data):
   """The image turned upright by its EXIF orientation, and the format it was stored in."""
   try:
      image = Image.open(io.BytesIO(data))
      image.load()
   except (UnidentifiedImageError, OSError, ValueError):
      return None, None

   return ImageOps.exif_transpose(image), image.format


def resized(image, long_edge):
   scale = long_edge / max(image.size)
   is_larger = scale < 1

   if not is_larger:
      return image.copy()

   size = (max(1, round(image.width * scale)), max(1, round(image.height * scale)))

   return image.resize(size, Image.Resampling.LANCZOS)


def percentile(histogram, share):
   total = sum(histogram)
   target = total * share
   running = 0

   for level, count in enumerate(histogram):
      running += count

      if running >= target:
         return level

   return len(histogram) - 1


def laplacian_variance(gray):
   return ImageStat.Stat(gray.filter(LAPLACIAN)).var[0]


def luminance_measurements(gray):
   histogram = gray.histogram()

   return {
      "ink": percentile(histogram, INK_SHARE),
      "p95": percentile(histogram, 0.95),
      "mean": ImageStat.Stat(gray).mean[0],
   }


def dark_components(binary, region):
   """Connected dark regions inside region = (left, top, right, bottom) of a 0/1 pixel grid."""
   left, top, right, bottom = region
   width = binary.width
   pixels = binary.load()
   seen = set()
   components = []

   for row in range(top, bottom):
      for column in range(left, right):
         is_new_dark = pixels[column, row] == 0 and (column, row) not in seen

         if not is_new_dark:
            continue

         stack = [(column, row)]
         seen.add((column, row))
         xs, ys = [], []

         while stack:
            x, y = stack.pop()
            xs.append(x)
            ys.append(y)

            for next_x, next_y in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
               inside = left <= next_x < right and top <= next_y < bottom and next_x < width
               is_unseen_dark = inside and (next_x, next_y) not in seen and pixels[next_x, next_y] == 0

               if is_unseen_dark:
                  seen.add((next_x, next_y))
                  stack.append((next_x, next_y))

         components.append((min(xs), min(ys), max(xs), max(ys), len(xs)))

   return components


def is_marker_shaped(component, short_edge):
   x0, y0, x1, y1, area = component
   side_x = x1 - x0 + 1
   side_y = y1 - y0 + 1
   longer = max(side_x, side_y)
   shorter = min(side_x, side_y)
   aspect = longer / shorter
   fill = area / (side_x * side_y)
   big_enough = shorter >= MARKER_MIN_SIDE_SHARE * short_edge
   small_enough = longer <= MARKER_MAX_SIDE_SHARE * short_edge
   square_enough = aspect <= MARKER_MAX_ASPECT
   solid_enough = fill >= MARKER_MIN_FILL

   return big_enough and small_enough and square_enough and solid_enough


def corner_regions(width, height):
   region_width = int(width * CORNER_REGION_SHARE)
   region_height = int(height * CORNER_REGION_SHARE)

   return {
      "top_left": (0, 0, region_width, region_height),
      "top_right": (width - region_width, 0, width, region_height),
      "bottom_left": (0, height - region_height, region_width, height),
      "bottom_right": (width - region_width, height - region_height, width, height),
   }


def find_markers(gray):
   small = resized(gray, MARKER_LONG_EDGE_PX)
   histogram = small.histogram()
   threshold = (percentile(histogram, 0.02) + percentile(histogram, 0.6)) / 2
   binary = small.point(lambda level: 0 if level < threshold else 255, mode="L")
   short_edge = min(small.size)
   found = {}

   for corner, region in corner_regions(*small.size).items():
      shaped = [component for component in dark_components(binary, region) if is_marker_shaped(component, short_edge)]
      has_marker = len(shaped) > 0

      if has_marker:
         largest = max(shaped, key=lambda component: component[4])
         x0, y0, x1, y1, _area = largest
         found[corner] = ((x0 + x1) / 2 / small.width, (y0 + y1) / 2 / small.height)

   return found


def marker_span(markers):
   xs = [position[0] for position in markers.values()]
   ys = [position[1] for position in markers.values()]

   return min(max(xs) - min(xs), max(ys) - min(ys))


def check_image(data, declared_media_type=None):
   digest = hashlib.sha256(data).hexdigest()
   is_too_large = len(data) > MAX_IMAGE_BYTES

   if is_too_large:
      return QualityVerdict(False, ["the photo is larger than 10 MB; a smaller photo of the same page is fine"], sha256=digest)

   image, stored_format = decoded(data)

   if image is None:
      return QualityVerdict(False, ["this file is not a photo the app can open; a JPEG or PNG works"], sha256=digest)

   media_type = PIL_FORMAT_MEDIA_TYPES.get(stored_format or "", declared_media_type)
   is_accepted_type = media_type in ACCEPTED_MEDIA_TYPES

   if not is_accepted_type:
      return QualityVerdict(False, ["this file is not a JPEG, PNG or WebP photo"], sha256=digest)

   width, height = image.size
   reasons = []
   is_too_small = min(width, height) < MIN_SHORT_EDGE_PX

   if is_too_small:
      reasons.append("the photo is too small to read; take it at the camera's normal size")

   gray = resized(image.convert("L"), ANALYSIS_LONG_EDGE_PX)
   sharpness = laplacian_variance(gray)
   luminance = luminance_measurements(gray)
   spread = luminance["p95"] - luminance["ink"]
   markers = find_markers(gray)
   has_all_markers = len(markers) == len(CORNERS)
   span = marker_span(markers) if has_all_markers else 0.0

   is_blurred = sharpness < MIN_LAPLACIAN_VARIANCE
   is_dark = luminance["mean"] < MIN_MEAN_LUMINANCE
   is_washed_out = luminance["mean"] > MAX_MEAN_LUMINANCE
   is_flat = spread < MIN_LUMINANCE_SPREAD
   is_too_far = has_all_markers and span < MIN_MARKER_SPAN_SHARE

   if is_blurred:
      reasons.append("the photo is blurred; hold the phone still and let it focus")

   if is_dark:
      reasons.append("the photo is too dark; more light on the page will help")

   if is_washed_out or is_flat:
      reasons.append("the writing is too faint against the page; more even light or darker ink will help")

   if not has_all_markers:
      missing = [corner.replace("_", " ") for corner in CORNERS if corner not in markers]
      reasons.append(f"the corner squares were not all found ({', '.join(missing)}); the whole page must be in the photo")

   if is_too_far:
      reasons.append("the page fills too little of the photo; move closer so the page fills the frame")

   measurements = {
      "laplacian_variance": round(sharpness, 2),
      "luminance_mean": round(luminance["mean"], 2),
      "luminance_spread": spread,
      "markers_found": sorted(markers),
      "marker_span": round(span, 3),
   }

   return QualityVerdict(
      accepted=len(reasons) == 0,
      reasons=reasons,
      measurements=measurements,
      media_type=media_type,
      width=width,
      height=height,
      sha256=digest,
   )
