import math
import sys

from PIL import Image, ImageDraw, ImageFilter

SIZE = 1024
SCALE = 4
canvas_size = SIZE * SCALE


def scaled(value):
   return value * SCALE


def leaf_polygon(base, tip, half_width, steps=120):
   base_x, base_y = base
   tip_x, tip_y = tip
   length = math.hypot(tip_x - base_x, tip_y - base_y)
   along_x = (tip_x - base_x) / length
   along_y = (tip_y - base_y) / length
   normal_x = -along_y
   normal_y = along_x
   outline = []

   for side in (1, -1):
      for step in range(steps + 1):
         fraction = step / steps if side == 1 else 1 - step / steps
         bulge = half_width * math.sin(math.pi * fraction) ** 0.9 * (1 - 0.25 * fraction)
         point_x = base_x + along_x * length * fraction + normal_x * bulge * side
         point_y = base_y + along_y * length * fraction + normal_y * bulge * side
         outline.append((scaled(point_x), scaled(point_y)))

   return outline


background = Image.new("RGBA", (canvas_size, canvas_size), (0, 0, 0, 0))
gradient = Image.new("RGBA", (canvas_size, canvas_size))
gradient_draw = ImageDraw.Draw(gradient)

top_color = (60, 205, 125)
bottom_color = (16, 108, 72)

for row in range(canvas_size):
   blend = row / canvas_size
   row_color = tuple(int(top_color[channel] * (1 - blend) + bottom_color[channel] * blend) for channel in range(3))
   gradient_draw.line([(0, row), (canvas_size, row)], fill=row_color + (255,))

mask = Image.new("L", (canvas_size, canvas_size), 0)
inset = scaled(100)
ImageDraw.Draw(mask).rounded_rectangle([inset, inset, canvas_size - inset, canvas_size - inset], radius=scaled(185), fill=255)
background.paste(gradient, (0, 0), mask)

sprout = Image.new("RGBA", (canvas_size, canvas_size), (0, 0, 0, 0))
sprout_draw = ImageDraw.Draw(sprout)
white = (255, 255, 255, 255)

stem_radius = scaled(20)
for step in range(601):
   fraction = step / 600
   center_x = scaled(512 + 18 * math.sin(math.pi * fraction))
   center_y = scaled(780 - 330 * fraction)
   sprout_draw.ellipse([center_x - stem_radius, center_y - stem_radius, center_x + stem_radius, center_y + stem_radius], fill=white)
sprout_draw.ellipse([scaled(492), scaled(430), scaled(532), scaled(470)], fill=white)

sprout_draw.polygon(leaf_polygon((515, 470), (270, 290), 95), fill=white)
sprout_draw.polygon(leaf_polygon((520, 440), (780, 230), 110), fill=white)

sprout_draw.rounded_rectangle([scaled(352), scaled(762), scaled(672), scaled(806)], radius=scaled(22), fill=white)

shadow = sprout.split()[3].filter(ImageFilter.GaussianBlur(scaled(10)))
shadow_layer = Image.new("RGBA", (canvas_size, canvas_size), (0, 60, 30, 0))
shadow_layer.putalpha(shadow.point(lambda alpha: int(alpha * 0.35)))
background.alpha_composite(shadow_layer, (0, scaled(8)))
background.alpha_composite(sprout)

final = background.resize((SIZE, SIZE), Image.LANCZOS)
output_path = sys.argv[1]
final.save(output_path)
