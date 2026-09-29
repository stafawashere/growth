"""Plant one defect per rule of tools/check_lesson_designs.py into the clean designs under clean/
and write red_<rule>/ beside them. The clean designs are fixtures in their own right, not copies
refreshed from docs/lessons, so the live designs can lag a new rule. Run from the repository root:
PYTHONPATH=. .venv/bin/python tests/fixtures/lesson_designs/make_red_fixtures.py
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

FIXTURE_DIR = Path(__file__).resolve().parent
CLEAN_CONCEPT = FIXTURE_DIR / "clean" / "LSN-CON-02013.md"
CLEAN_DECISION = FIXTURE_DIR / "clean" / "LSN-DEC-06-01.md"
FENCE = re.compile(r"```json\n(.*?)\n```", re.S)


def record_of(text):
   return json.loads(FENCE.search(text).group(1))


def with_record(text, record):
   return FENCE.sub(lambda match: "```json\n" + json.dumps(record, indent=1, ensure_ascii=False) + "\n```", text)


def edit(text, change):
   record = record_of(text)
   change(record)

   return with_record(text, record)


def no_front_matter(text):
   return text.split("---\n", 2)[2]


def drop_section(text):
   return text.replace("\n## Time\n", "\n## Timing\n")


def broken_json(text):
   return text.replace("```json\n{", "```json\n{,")


def wrong_target(record):
   record["target_id"] = "BC-CON-02014"


def retired_id(record):
   record["sources"].append("BC-SKL-06046")


def missing_page(record):
   record["sources"].append("sg-25:999")


def missing_heading(record):
   record["sources"].append("research/scoring/common-point-losses.md#No such heading")


def long_cue(record):
   record["worked_examples"][0]["steps"][0]["cue"] = " ".join(["word"] * 21)


def wrong_words(record):
   record["word_count"]["full"] += 1


def dash(record):
   record["orientation"]["text"] += " — with a dash"


def prediction(record):
   record["orientation"]["text"] += " This is guaranteed."


def wrong_quote(record):
   record["key_ideas"][0]["quote"]["text"] = "This sentence is not on the cited page at all."


def broken_step(record):
   record["worked_examples"][0]["steps"][2]["expr"] = "2*x*cos(x) + (x**2+3)*sin(x)"


def wrong_key(record):
   record["checks"][1]["key"]["expr"] = "2*x*sin(x) - (x**2-2)*cos(x)"


def wrong_relation(record):
   record["common_errors"][0]["relation"] = "equivalent"


def foreign_path(record):
   record["checks"][2]["options"][0]["error_path"] = "BC-ERR-06027"


def wrong_scores(record):
   record["what_a_reader_scores"][0]["lines"][0]["text"] = "Product rule. Earned by: anything."


def published_draw(record):
   record["worked_examples"][0]["parameter_draw"] = {"numerator": "linear", "leading": "1", "constant": "-11", "trig": "sin", "angle": "1/3"}


def untagged_inferred(record):
   record["inferred"][0].pop("settles")


def missing_delivery(record):
   record["delivery"] = [entry for entry in record["delivery"] if entry["block"] != "ex-1"]


def no_prediction(record):
   record.pop("prediction")


def no_contrast(record):
   record["strategy"][0].pop("contrast")


def unfaded_second_example(record):
   record["worked_examples"][1].pop("fade_from")


def fix_prompt_on_equivalent(record):
   record["common_errors"][1]["fix_prompt"] = True


def no_figure_reason(record):
   record.pop("no_figure_reason")


def id_in_rival(record):
   record["strategy"][0]["rival"] += " (BC-ERR-02020)"


def two_features(record):
   record["decision"]["stems"][1]["parameter_draw"]["integrand"] = "sin(t)"


CONCEPT_DEFECTS = {
   "front_matter": no_front_matter,
   "sections": drop_section,
   "machine_record": broken_json,
   "manifest_id": lambda text: edit(text, wrong_target),
   "referential": lambda text: edit(text, retired_id),
   "citations": lambda text: edit(text, missing_page),
   "research_lines": lambda text: edit(text, missing_heading),
   "caps": lambda text: edit(text, long_cue),
   "band_caps": lambda text: edit(text, wrong_words),
   "style": lambda text: edit(text, dash),
   "prediction": lambda text: edit(text, prediction),
   "quotes": lambda text: edit(text, wrong_quote),
   "steps": lambda text: edit(text, broken_step),
   "keys": lambda text: edit(text, wrong_key),
   "errors": lambda text: edit(text, wrong_relation),
   "distractor_paths": lambda text: edit(text, foreign_path),
   "reader_scores": lambda text: edit(text, wrong_scores),
   "draw_exclusion": lambda text: edit(text, published_draw),
   "inferred": lambda text: edit(text, untagged_inferred),
   "delivery": lambda text: edit(text, missing_delivery),
   "prediction_section": lambda text: edit(text, no_prediction),
   "contrast": lambda text: edit(text, no_contrast),
   "fade": lambda text: edit(text, unfaded_second_example),
   "fix_prompt": lambda text: edit(text, fix_prompt_on_equivalent),
   "figure_presence": lambda text: edit(text, no_figure_reason),
   "served_text": lambda text: edit(text, id_in_rival),
}
DECISION_DEFECTS = {
   "decision_stems": lambda text: edit(text, two_features),
}


def write(path, text):
   path.parent.mkdir(parents=True, exist_ok=True)
   path.write_text(text)


def main():
   concept = CLEAN_CONCEPT.read_text()
   decision = CLEAN_DECISION.read_text()

   for rule, defect in CONCEPT_DEFECTS.items():
      write(FIXTURE_DIR / f"red_{rule}" / "LSN-CON-02013.md", defect(concept))

   for rule, defect in DECISION_DEFECTS.items():
      write(FIXTURE_DIR / f"red_{rule}" / "LSN-DEC-06-01.md", defect(decision))

   print(f"wrote {len(CONCEPT_DEFECTS) + len(DECISION_DEFECTS)} red fixtures")


if __name__ == "__main__":
   main()
