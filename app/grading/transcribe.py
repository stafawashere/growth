"""The transcriber role: a photographed page becomes a read-back the student confirms.

11 P3 scope item 3. The read-back is a stage of its own, stored on the attempt and shown to the
student rendered as mathematics, and nothing is graded from it until the student confirms it or
corrects it (app/grading/service.py confirm_transcription). The transcriber is given the question
label and the part labels so it can file each line under its box, and never the answer, the
criteria or the worked solution: it records what is written, and a transcriber that knew the
expected answer could drift toward it.

The shape a read-back has everywhere in the app, whether the transcriber wrote it, the student
corrected it, or the student typed it in the typed mode:

   {"parts": [{"part_id": "a", "answer": "<LaTeX or empty>",
               "lines": [{"kind": "math" | "text", "content": "...", "crossed_out": false,
                          "outside_box": false}]}],
    "unreadable": ["part b, line 2, the exponent"]}
"""
import json
from pathlib import Path

from app.providers.base import CacheSettings, ImageInput, Message, ProviderRequest, render_template, split_template
from app.providers.model_routing import model_for

TEMPLATE_PATH = Path(__file__).resolve().parents[2] / "prompts" / "transcriber" / "readback_v1.md"
MAX_OUTPUT_TOKENS = 3000
PROVIDER_OPTIONS = {"thinking": {"type": "disabled"}}
LINE_KINDS = ("math", "text")

LINE_SCHEMA = {
   "type": "object",
   "properties": {
      "kind": {"type": "string", "enum": list(LINE_KINDS)},
      "content": {"type": "string"},
      "crossed_out": {"type": "boolean"},
      "outside_box": {"type": "boolean"},
   },
   "required": ["kind", "content", "crossed_out", "outside_box"],
   "additionalProperties": False,
}

TRANSCRIPTION_SCHEMA = {
   "type": "object",
   "properties": {
      "parts": {
         "type": "array",
         "items": {
            "type": "object",
            "properties": {
               "part_id": {"type": "string"},
               "lines": {"type": "array", "items": LINE_SCHEMA},
               "answer": {"type": "string"},
            },
            "required": ["part_id", "lines", "answer"],
            "additionalProperties": False,
         },
      },
      "unreadable": {"type": "array", "items": {"type": "string"}},
   },
   "required": ["parts", "unreadable"],
   "additionalProperties": False,
}


class TranscriptionFailed(Exception):
   pass


def part_labels(record):
   return "\n".join(f"part ({part['id']}): {part['prompt']}" for part in record["parts"])


def question_label(record):
   return record["id"]


def request_for(record, images):
   text = TEMPLATE_PATH.read_text()
   system, _variables = split_template(text)
   rendered = render_template(
      text,
      {"question_label": question_label(record), "part_labels": part_labels(record)},
   )

   return ProviderRequest(
      role="transcriber",
      model=model_for("transcriber"),
      system=system,
      messages=(Message(role="user", content=rendered),),
      max_output_tokens=MAX_OUTPUT_TOKENS,
      output_schema=TRANSCRIPTION_SCHEMA,
      cache=CacheSettings(prefix_breakpoints=1, ttl="5m"),
      provider_options={key: dict(value) for key, value in PROVIDER_OPTIONS.items()},
      images=tuple(images),
   )


def clean_line(line):
   kind = line.get("kind")
   is_known_kind = kind in LINE_KINDS

   return {
      "kind": kind if is_known_kind else "text",
      "content": str(line.get("content") or ""),
      "crossed_out": bool(line.get("crossed_out")),
      "outside_box": bool(line.get("outside_box")),
   }


def normalised_transcription(record, payload):
   """Every part of the item, in the item's order, each with its lines. A part the reader filed
   under a label the item does not have is kept as an unreadable note rather than dropped."""
   by_part = {}
   notes = [str(note) for note in payload.get("unreadable") or []]

   for part in payload.get("parts") or []:
      part_id = str(part.get("part_id", "")).strip().strip("()").lower()
      by_part.setdefault(part_id, {"lines": [], "answer": ""})
      by_part[part_id]["lines"].extend(clean_line(line) for line in part.get("lines") or [])
      has_answer = str(part.get("answer") or "").strip() != ""

      if has_answer:
         by_part[part_id]["answer"] = str(part["answer"])

   item_part_ids = [part["id"] for part in record["parts"]]

   for stray_id in sorted(set(by_part) - set(item_part_ids)):
      notes.append(f"work filed under a part this question does not have: {stray_id}")

   return {
      "parts": [
         {
            "part_id": part_id,
            "lines": by_part.get(part_id, {}).get("lines", []),
            "answer": by_part.get(part_id, {}).get("answer", ""),
         }
         for part_id in item_part_ids
      ],
      "unreadable": notes,
   }


def transcribe(provider, record, images):
   request = request_for(record, images)

   try:
      result = provider.generate(request)
   except Exception as raised:
      raise TranscriptionFailed(f"the page could not be read: {type(raised).__name__}") from None

   try:
      payload = json.loads(result.text or "")
   except ValueError:
      raise TranscriptionFailed("the reader's answer was not JSON") from None

   is_object = isinstance(payload, dict)

   if not is_object:
      raise TranscriptionFailed("the reader's answer was not an object")

   return normalised_transcription(record, payload)


def image_input(row):
   return ImageInput(media_type=row.media_type, data=row.data, width=row.width, height=row.height)


def corrected_transcription(record, submitted):
   """The student's confirmed or corrected read-back, held to the same shape."""
   is_object = isinstance(submitted, dict)

   if not is_object:
      raise ValueError("a read-back is an object with parts")

   return normalised_transcription(record, submitted)


def transcription_differs(original, confirmed):
   return json.dumps(original.get("parts"), sort_keys=True) != json.dumps(confirmed.get("parts"), sort_keys=True)
