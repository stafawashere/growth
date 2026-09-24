"""No served item text shares more than the anchor-quote cap of consecutive words with official text.

Every record in every content/items_* directory is scanned, field by field, against every cached
official page. The positive control is built from a cached page at run time.
"""
from app.generation import dedupe

CONTROL_SPAN_LENGTH = 30


def test_no_official_text_served():
   official_pages = dedupe.load_official_pages()
   official_index = dedupe.OfficialShingleIndex(official_pages)
   control_page = next(page for page in official_index.pages if len(page.tokens) >= 2 * CONTROL_SPAN_LENGTH)
   control_span = control_page.tokens[CONTROL_SPAN_LENGTH:2 * CONTROL_SPAN_LENGTH]
   control_record = {"id": "ITM-CONTROL-00", "stem": {"text": " ".join(control_span)}, "options": []}
   control_length, control_where = official_index.longest_run(dedupe.normalise(dedupe.served_texts(control_record)[0][1]))

   assert control_length >= CONTROL_SPAN_LENGTH, f"control span of {CONTROL_SPAN_LENGTH} words found only {control_length} at {control_where}"

   records = dedupe.load_bank_records()
   longest = (0, None, None, None)
   fields_scanned = 0

   for record in records:
      for field_name, text in dedupe.served_texts(record):
         run_length, run_where = official_index.longest_run(dedupe.normalise(text))
         fields_scanned += 1

         if run_length > longest[0]:
            longest = (run_length, record["id"], field_name, run_where)

   assert records, "no item records found under content/items_*"

   longest_length, longest_item, longest_field, longest_where = longest
   report = (
      f"{len(records)} records, {fields_scanned} fields, {len(official_index.pages)} official page variants; "
      f"longest shared run {longest_length} words, {longest_item} {longest_field} against {longest_where}; "
      f"control run {control_length} words"
   )

   assert longest_length <= dedupe.ANCHOR_QUOTE_CAP, report
