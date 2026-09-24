"""The released free-response forms the six-week checkpoint draws from (docs/plan/01 "External
checkpoint", 10 "The external checkpoint", 11 P7 scope item 5).

A form is one year's released Section II, both parts, worked under the published part timings that
app/checkpoint/published.py reads from research/exam/exam-structure.md. The material is used by
reference and never redistributed (01, 09): the app names the year, question and page and links
College Board's own published document, and it serves no stem, figure or scoring text. The
student works on paper and records the points earned per part against College Board's scoring
guidelines, also by reference.

A year is a form only when all of these hold, so every number the checkpoint reports can be traced:

- the free-response document and the scoring guidelines for that year are both in
  cache/manifest.json with status ok;
- every question of the year has part records in data/frq_records.json with a point total, and
  each question's parts sum to 9, the per-question maximum the published means are out of.

Forms are offered in a fixed order: years whose per-question means are published come first,
newest first, so the first checkpoints compare against the same year's population; the rest follow,
newest first. A year already used is never offered again.
"""
import json
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

from app.checkpoint import published

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
FRQ_RECORDS_PATH = REPOSITORY_ROOT / "data" / "frq_records.json"
MANIFEST_PATH = REPOSITORY_ROOT / "cache" / "manifest.json"

POINTS_PER_QUESTION = 9


@dataclass(frozen=True)
class FormPart:
   record_id: str
   question: int
   part: str
   points: int
   point_types: tuple
   calculator: str


@dataclass(frozen=True)
class Form:
   year: int
   parts: tuple
   free_response_url: str
   scoring_guidelines_url: str

   def questions(self):
      return sorted({part.question for part in self.parts})

   def question_parts(self, question):
      return [part for part in self.parts if part.question == question]


@dataclass(frozen=True)
class ExcludedYear:
   year: int
   reason: str


def two_digit(year):
   return f"{year % 100:02d}"


def ok_documents(manifest_path=MANIFEST_PATH):
   manifest = json.loads(Path(manifest_path).read_text())

   return {
      doc_id: entry
      for doc_id, entry in manifest.items()
      if entry.get("status") == "ok"
   }


def active_records(records_path=FRQ_RECORDS_PATH):
   records = json.loads(Path(records_path).read_text())["records"]

   return [record for record in records if record.get("status", "active") == "active"]


@lru_cache(maxsize=1)
def catalogue(records_path=FRQ_RECORDS_PATH, manifest_path=MANIFEST_PATH):
   """Returns (forms in offering order, excluded years with the reason)."""
   documents = ok_documents(manifest_path)
   by_year = {}

   for record in active_records(records_path):
      by_year.setdefault(record["year"], []).append(record)

   forms = []
   excluded = []

   for year in sorted(by_year):
      free_response_id = f"frq-{two_digit(year)}"
      guidelines_id = f"sg-{two_digit(year)}"
      has_documents = free_response_id in documents and guidelines_id in documents

      if not has_documents:
         excluded.append(ExcludedYear(year, "the free-response document or the scoring guidelines is not cached with status ok"))
         continue

      parts = tuple(
         FormPart(
            record_id=record["id"],
            question=record["question"],
            part=record["part"].upper(),
            points=record["points"],
            point_types=tuple(record.get("point_types") or ()),
            calculator=record["calculator"],
         )
         for record in sorted(by_year[year], key=lambda record: (record["question"], record["part"]))
      )
      totals = {}

      for part in parts:
         totals[part.question] = totals.get(part.question, 0) + part.points

      expected_questions = sum(section.questions for section in published.free_response_parts())
      has_every_question = sorted(totals) == list(range(1, expected_questions + 1))
      short_questions = [question for question, total in sorted(totals.items()) if total != POINTS_PER_QUESTION]

      if not has_every_question:
         excluded.append(ExcludedYear(year, f"the library holds questions {sorted(totals)} only"))
         continue

      if short_questions:
         listed = ", ".join(f"question {question} totals {totals[question]}" for question in short_questions)
         excluded.append(ExcludedYear(year, f"the library's part points do not sum to {POINTS_PER_QUESTION}: {listed}"))
         continue

      forms.append(
         Form(
            year=year,
            parts=parts,
            free_response_url=documents[free_response_id]["requested_url"],
            scoring_guidelines_url=documents[guidelines_id]["requested_url"],
         )
      )

   published_years = set(published.published_years())
   forms.sort(key=lambda form: (form.year not in published_years, -form.year))

   return tuple(forms), tuple(excluded)


def forms():
   return catalogue()[0]


def form_for(year):
   for form in forms():
      if form.year == year:
         return form

   raise KeyError(f"no checkpoint form for {year}")


def next_form(used_years):
   for form in forms():
      if form.year not in used_years:
         return form

   return None


def section_plan(form):
   """The form's questions grouped by Section II part, with each part's timing and calculator
   rule, in exam order. Question numbering runs across the parts, as on the exam."""
   plan = []
   first_question = 1

   for section in published.free_response_parts():
      questions = list(range(first_question, first_question + section.questions))
      plan.append({
         "part": f"{section.section}-{section.part}",
         "minutes": section.minutes,
         "calculator": section.calculator,
         "questions": [
            {
               "question": question,
               "parts": [
                  {
                     "record_id": part.record_id,
                     "part": part.part,
                     "points": part.points,
                  }
                  for part in form.question_parts(question)
               ],
            }
            for question in questions
         ],
      })
      first_question += section.questions

   return plan
