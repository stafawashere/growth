"""The released forms the six-week checkpoint draws from, read off the library, never restated."""
import json
from pathlib import Path

from app.checkpoint import forms, published

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]


def test_every_form_is_cached_ok_and_every_question_is_out_of_nine():
   offered, excluded = forms.catalogue()
   documents = forms.ok_documents()

   assert len(offered) > 0

   for form in offered:
      short = f"{form.year % 100:02d}"
      assert f"frq-{short}" in documents and f"sg-{short}" in documents
      assert form.free_response_url == documents[f"frq-{short}"]["requested_url"]

      for question in form.questions():
         assert sum(part.points for part in form.question_parts(question)) == forms.POINTS_PER_QUESTION

   excluded_years = {entry.year for entry in excluded}
   assert excluded_years.isdisjoint({form.year for form in offered})


def test_a_year_whose_parts_do_not_sum_to_nine_is_excluded_with_its_reason(tmp_path):
   records = json.loads((REPOSITORY_ROOT / "data" / "frq_records.json").read_text())["records"]
   year = forms.forms()[0].year
   shortened = [dict(record) for record in records]

   for record in shortened:
      is_target = record["year"] == year and record["question"] == 1 and record["part"].upper() == "A"

      if is_target:
         record["points"] -= 1

   path = tmp_path / "frq_records.json"
   path.write_text(json.dumps({"records": shortened}))
   offered, excluded = forms.catalogue(records_path=path)

   assert year not in {form.year for form in offered}
   assert any(entry.year == year and "question 1 totals 8" in entry.reason for entry in excluded)


def test_forms_with_published_means_come_first_newest_first():
   years = [form.year for form in forms.forms()]
   with_means = set(published.published_years())
   leading = [year for year in years if year in with_means]

   assert years[: len(leading)] == sorted(leading, reverse=True)
   assert forms.next_form(set(years)) is None


def test_the_section_plan_takes_its_timing_from_exam_structure():
   plan = forms.section_plan(forms.forms()[0])
   library_parts = published.free_response_parts()

   assert [section["minutes"] for section in plan] == [part.minutes for part in library_parts]
   assert [len(section["questions"]) for section in plan] == [part.questions for part in library_parts]


def test_a_point_the_guidelines_award_in_any_one_part_counts_toward_the_question():
   offered, excluded = forms.catalogue()
   form_2021 = forms.form_for(2021)
   question_4 = form_2021.question_parts(4)
   global_parts = [part for part in question_4 if part.part == forms.GLOBAL_PART_LABEL]

   assert len(offered) == 7
   assert 2021 not in {entry.year for entry in excluded}
   assert sum(part.points for part in question_4) == forms.POINTS_PER_QUESTION
   assert [(part.record_id, part.points, part.point_types) for part in global_parts] == [
      ("BC-FRQ-2021-Q4-A:global", 1, ("BC-PT-99024",)),
   ]
   assert question_4[0] == global_parts[0]
