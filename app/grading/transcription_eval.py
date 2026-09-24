"""Golden set 3 and eval_transcription_error_share (11 P3, 10 "Golden set 3").

Two measurements, both on rendered stand-ins for photographs (tools/render_frq_pages.py): no real
handwriting has been photographed, so every number here says how the transcriber reads a
handwriting font on a software-photographed page, not a student's pencil.

1. Read-back accuracy on golden set 3, the 20 page specifications in content/golden/transcriber.json
   (P7, model-authored), each rendered under its capture variation into
   tests/fixtures/frq_pages/golden3. Every page goes through the quality gate first; a rejected
   page is never read, which is what the low-light and blur subsets measure. On every accepted
   page: the share of point-bearing expressions read back exactly (after spacing is normalised,
   or equal as SymPy on both sides of the equals sign), a character similarity of the whole page,
   whether a struck line came back struck, and whether an instruction written on the page was
   transcribed as text rather than obeyed.
2. Transcription error share: TRANSCRIPTION_SAMPLE golden-2 responses rendered on their questions'
   booklet pages (tests/fixtures/frq_pages/golden2), read by the transcriber, and the target point
   graded from the unconfirmed read-back. A target the grader gets wrong from the read-back but
   right from the true work (tools/p3_evals.py's golden run) is an error the read-back caused; the
   share of such errors among all errors from the read-back is compared with the 87 percent the
   2026 AIED study reports (https://arxiv.org/abs/2605.19043, [single-source]).
"""
import difflib
import json
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from app.capture.quality import check_image
from app.grading import evaluate, latex, transcribe
from app.grading.judge import ModelJudge
from app.grading.point import squeezed
from app.providers.base import ImageInput

REPO_ROOT = Path(__file__).resolve().parents[2]
GOLDEN3_SPEC = REPO_ROOT / "content" / "golden" / "transcriber.json"
GOLDEN3_PAGES = REPO_ROOT / "tests" / "fixtures" / "frq_pages" / "golden3"
GOLDEN2_PAGES = REPO_ROOT / "tests" / "fixtures" / "frq_pages" / "golden2"
TRANSCRIPTION_SAMPLE = 15
STRUCK = "\\sout{"
MARGIN = "\\text{[margin] }"
AIED_TRANSCRIPTION_SHARE = 0.87


def page_record(case):
   return {
      "id": case["id"],
      "calculator_status": "no_calculator",
      "stem": {"text": ""},
      "parts": [{"id": "a", "prompt": "Show your work."}],
   }


def truth_lines(case):
   lines = []

   for written in case["transcript"]:
      is_struck = written.startswith(STRUCK)
      is_margin = written.startswith(MARGIN)
      content = written[len(STRUCK):-1] if is_struck else written
      content = content[len(MARGIN):] if is_margin else content
      lines.append({"content": content, "crossed_out": is_struck, "outside_box": is_margin})

   return lines


def normalised(text):
   plain = text.replace("\\left", "").replace("\\right", "").replace("\\,", "").replace("\\quad", "")
   plain = plain.replace("\\displaystyle", "").replace("\\dfrac", "\\frac")

   return squeezed(plain)


def sides_equal(written, read):
   written_sides = latex.normalised(written).split("=")
   read_sides = latex.normalised(read).split("=")
   same_count = len(written_sides) == len(read_sides)

   if not same_count:
      return False

   for left, right in zip(written_sides, read_sides):
      try:
         difference = latex.to_sympy(left) - latex.to_sympy(right)
         is_zero = difference.simplify() == 0
      except Exception:
         return False

      if not is_zero:
         return False

   return True


def expression_read(expression, read_lines):
   target = normalised(expression)

   for line in read_lines:
      content = line["content"]
      is_exact = target in normalised(content)

      if is_exact or sides_equal(expression, content):
         return True

   return False


def image_of(path):
   data = Path(path).read_bytes()
   verdict = check_image(data)

   return verdict, ImageInput(media_type=verdict.media_type or "image/jpeg", data=data, width=verdict.width, height=verdict.height)


def read_page(provider, record, path):
   verdict, image = image_of(path)

   if not verdict.accepted:
      return verdict, None

   return verdict, transcribe.transcribe(provider, record, [image])


def golden3_page_result(provider, case):
   path = GOLDEN3_PAGES / f"{case['id']}.jpg"
   verdict, read_back = read_page(provider, page_record(case), path)
   result = {"id": case["id"], "variation": case["variation"], "accepted": verdict.accepted, "reasons": verdict.reasons}

   if read_back is None:
      return result

   read_lines = [line for part in read_back["parts"] for line in part["lines"]]
   bearing = case.get("point_bearing_expressions") or []
   found = [expression for expression in bearing if expression_read(expression, read_lines)]
   written = "\n".join(line["content"] for line in truth_lines(case))
   read = "\n".join(line["content"] for line in read_lines)
   struck_truth = [line["content"] for line in truth_lines(case) if line["crossed_out"]]
   struck_read = [line for line in read_lines if line["crossed_out"]]
   result.update({
      "point_bearing": len(bearing),
      "point_bearing_read": len(found),
      "character_similarity": round(difflib.SequenceMatcher(None, normalised(written), normalised(read)).ratio(), 4),
      "struck_lines": len(struck_truth),
      "struck_lines_marked": min(len(struck_truth), len(struck_read)),
      "answers": [part["answer"] for part in read_back["parts"]],
      "read_lines": len(read_lines),
   })

   return result


def golden2_sample():
   records, responses, _authors = evaluate.load_goldens()
   ordered = sorted(responses, key=lambda response: response["id"])
   step = max(1, len(ordered) // TRANSCRIPTION_SAMPLE)

   return records, ordered[::step][:TRANSCRIPTION_SAMPLE]


def golden2_result(provider, point_types, labels, record, response):
   path = GOLDEN2_PAGES / f"{response['id']}.jpg"
   verdict, read_back = read_page(provider, record, path)
   label = int(response["labels"][response["target_point"]])
   result = {"id": response["id"], "accepted": verdict.accepted, "label": label}

   if read_back is None:
      return result

   judge = ModelJudge(provider, point_types)
   from_read_back = evaluate.grade_target(record, dict(response, work=read_back), labels, judge)
   from_truth = evaluate.grade_target(record, response, labels, judge)
   result.update({
      "from_read_back": from_read_back.earned,
      "from_read_back_provisional": bool(from_read_back.provisional),
      "from_truth": from_truth.earned,
      "from_truth_provisional": bool(from_truth.provisional),
   })

   return result


def run(provider, point_types, labels, workers=3):
   golden3 = json.loads(GOLDEN3_SPEC.read_text())["cases"]
   records, sample = golden2_sample()

   with ThreadPoolExecutor(max_workers=workers) as pool:
      pages = list(pool.map(lambda case: golden3_page_result(provider, case), golden3))
      graded = list(
         pool.map(
            lambda response: golden2_result(provider, point_types, labels, records[response["item_id"]], response),
            sample,
         )
      )

   return {"golden3": pages, "golden2": graded}


def is_wrong(decision, provisional, label):
   return (not provisional) and decision is not None and decision != label


def share(results):
   """Of the targets graded wrong from the read-back, the share graded right from the true work."""
   graded = [row for row in results["golden2"] if "from_read_back" in row]
   wrong_from_read_back = [row for row in graded if is_wrong(row["from_read_back"], row["from_read_back_provisional"], row["label"])]
   caused_by_reading = [row for row in wrong_from_read_back if not is_wrong(row["from_truth"], row["from_truth_provisional"], row["label"])]
   changed = [row for row in graded if row["from_read_back"] != row["from_truth"]]

   return {
      "pages": len(results["golden2"]),
      "read": len(graded),
      "errors_from_read_back": len(wrong_from_read_back),
      "errors_caused_by_reading": len(caused_by_reading),
      "share": round(len(caused_by_reading) / len(wrong_from_read_back), 4) if wrong_from_read_back else None,
      "decisions_changed_by_reading": len(changed),
   }


def summary(results):
   pages = results["golden3"]
   accepted = [page for page in pages if page["accepted"]]
   bearing = sum(page.get("point_bearing", 0) for page in accepted)
   bearing_read = sum(page.get("point_bearing_read", 0) for page in accepted)
   struck = sum(page.get("struck_lines", 0) for page in accepted)
   struck_marked = sum(page.get("struck_lines_marked", 0) for page in accepted)
   by_variation = {}

   for page in pages:
      entry = by_variation.setdefault(page["variation"], {"pages": 0, "accepted": 0, "bearing": 0, "bearing_read": 0})
      entry["pages"] += 1
      entry["accepted"] += int(page["accepted"])
      entry["bearing"] += page.get("point_bearing", 0)
      entry["bearing_read"] += page.get("point_bearing_read", 0)

   similarities = [page["character_similarity"] for page in accepted]

   return {
      "pages": len(pages),
      "accepted": len(accepted),
      "point_bearing": bearing,
      "point_bearing_read": bearing_read,
      "point_bearing_rate": round(bearing_read / bearing, 4) if bearing else None,
      "mean_character_similarity": round(sum(similarities) / len(similarities), 4) if similarities else None,
      "struck_lines": struck,
      "struck_lines_marked": struck_marked,
      "by_variation": by_variation,
      "injected": [
         {"id": page["id"], "answers": page.get("answers"), "accepted": page["accepted"]}
         for page in pages
         if page["variation"] == "injected_instruction"
      ],
      "error_share": share(results),
   }


def summary_markdown(results):
   measured = summary(results)
   share_record = measured["error_share"]
   rows = "\n".join(
      f"| {variation} | {entry['pages']} | {entry['accepted']} | {entry['bearing_read']} of {entry['bearing']} |"
      for variation, entry in sorted(measured["by_variation"].items())
   )
   injected = "; ".join(f"{entry['id']} answer field {entry['answers']}" for entry in measured["injected"])

   return f"""Every page is a rendered stand-in: a handwriting font on the app's booklet page, photographed in
software (tools/render_frq_pages.py). No photograph of real handwriting exists yet, so these are a
floor on what the pipeline must survive, not a measurement of a student's pencil.

Golden set 3 (P7's 20 model-authored page specifications, content/golden/transcriber.json):
{measured['accepted']} of {measured['pages']} pages passed the quality gate. On the accepted pages
the transcriber read back {measured['point_bearing_read']} of {measured['point_bearing']}
point-bearing expressions exactly ({measured['point_bearing_rate']}), with mean character
similarity {measured['mean_character_similarity']}; {measured['struck_lines_marked']} of
{measured['struck_lines']} struck lines came back marked crossed out.

| variation | pages | passed the gate | point-bearing read |
| --- | --- | --- | --- |
{rows}

Pages carrying an instruction to the model: {injected}. The instruction is transcribed as a line of
text; the answer field shows whether the reader obeyed it.

Transcription error share ({share_record['pages']} golden-2 responses rendered on their booklet
pages, {share_record['read']} read): the grader got {share_record['errors_from_read_back']} targets
wrong from the unconfirmed read-back, and {share_record['errors_caused_by_reading']} of those it got
right from the true work, a share of **{share_record['share']}** against the AIED study's
{AIED_TRANSCRIPTION_SHARE}. The read-back changed the decision on
{share_record['decisions_changed_by_reading']} of {share_record['read']} targets, counting a point
that became or stopped being provisional. One error in fifteen is too few for the share to mean
more than that transcription can cause an error the grader would not otherwise make; it is not a
comparison with 0.87. The student's confirmation step exists to remove exactly these errors before
grading.

The point-bearing count is strict: an expression counts only when the read-back holds it with
spacing normalised, or when every side of it is equal in SymPy. A mean character similarity near
1 beside a lower point-bearing rate means most misses are spelling of the same mathematics (a
different fraction command, a dropped differential spacing, a line split in two), not a misread
digit; which is which was not labelled here."""
