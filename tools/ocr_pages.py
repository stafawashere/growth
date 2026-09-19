"""OCR fallback for pages whose text layer is incomplete. Renders each page with PyMuPDF at 200 dpi,
runs RapidOCR, and writes page-NNN.ocr.txt beside the primary text. Usage: python3 tools/ocr_pages.py <doc_id> [pages]"""
import json
import sys
from pathlib import Path

import pymupdf
from rapidocr_onnxruntime import RapidOCR

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = json.loads((ROOT / "cache" / "manifest.json").read_text())


def main():
   doc_id = sys.argv[1]
   wanted = [int(p) for p in sys.argv[2:]] if len(sys.argv) > 2 else None
   record = MANIFEST[doc_id]
   document = pymupdf.open(ROOT / "cache" / "pdf" / f"{record['sha256']}.pdf")
   engine = RapidOCR()
   out_dir = ROOT / "cache" / "text" / doc_id

   for index, page in enumerate(document):
      number = index + 1
      is_wanted = wanted is None or number in wanted

      if not is_wanted:
         continue

      pixmap = page.get_pixmap(dpi=200)
      image_path = ROOT / "cache" / f"ocr-tmp-{doc_id}-{number}.png"
      pixmap.save(image_path)
      result, _ = engine(str(image_path))
      image_path.unlink()
      lines = [item[1] for item in (result or [])]
      (out_dir / f"page-{number:03d}.ocr.txt").write_text("\n".join(lines))
      print(number, len(lines), "lines", flush=True)


if __name__ == "__main__":
   main()
