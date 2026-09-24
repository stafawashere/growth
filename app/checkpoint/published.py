"""Read, never restate, the two library files the checkpoint compares against.

research/exam/exam-structure.md owns every exam count and time, and research/exam/scoring-system.md
owns the published per-question free-response means. Both are parsed at run time from their
Markdown tables, so a correction in the library reaches the app without a code change and no
number is copied into code.
"""
import re
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
EXAM_STRUCTURE_PATH = REPOSITORY_ROOT / "research" / "exam" / "exam-structure.md"
SCORING_SYSTEM_PATH = REPOSITORY_ROOT / "research" / "exam" / "scoring-system.md"

MEAN_CELL = re.compile(r"^\s*(\d+(?:\.\d+)?)\s*\((\d+(?:\.\d+)?)\)\s*$")
MINUTES_CELL = re.compile(r"^\s*(\d+)\s+minutes\s*$")


def table_rows(text, first_header_cell):
   """The data rows of the first Markdown table whose header starts with first_header_cell."""
   lines = text.splitlines()

   for index, line in enumerate(lines):
      cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
      is_header = line.startswith("|") and cells and cells[0] == first_header_cell

      if not is_header:
         continue

      header = cells
      rows = []

      for row_line in lines[index + 2:]:
         is_table_line = row_line.startswith("|")

         if not is_table_line:
            break

         rows.append([cell.strip() for cell in row_line.strip().strip("|").split("|")])

      return header, rows

   raise ValueError(f"no table headed {first_header_cell!r}")


@dataclass(frozen=True)
class ExamPart:
   section: str
   part: str
   question_type: str
   questions: int
   minutes: int
   calculator: str


@lru_cache(maxsize=1)
def exam_parts(path=EXAM_STRUCTURE_PATH):
   header, rows = table_rows(Path(path).read_text(), "Section")
   column = {name: position for position, name in enumerate(header)}
   parts = []

   for row in rows:
      minutes = MINUTES_CELL.match(row[column["Timing"]])

      if minutes is None:
         raise ValueError(f"unreadable timing {row[column['Timing']]!r} in {path}")

      parts.append(
         ExamPart(
            section=row[column["Section"]],
            part=row[column["Part"]],
            question_type=row[column["Question type"]],
            questions=int(row[column["Questions"]]),
            minutes=int(minutes.group(1)),
            calculator=row[column["Calculator"]],
         )
      )

   return tuple(parts)


def free_response_parts():
   return tuple(part for part in exam_parts() if part.question_type == "Free response")


@dataclass(frozen=True)
class QuestionMean:
   year: int
   question: int
   mean: float
   sd: float


@lru_cache(maxsize=1)
def question_means(path=SCORING_SYSTEM_PATH):
   """Maps (year, question) to its published mean and standard deviation out of 9."""
   header, rows = table_rows(Path(path).read_text(), "Question")
   years = []

   for cell in header[1:]:
      year = re.match(r"^(\d{4}) mean \(SD\)$", cell)

      if year is None:
         raise ValueError(f"unexpected column {cell!r} in {path}")

      years.append(int(year.group(1)))

   means = {}

   for row in rows:
      question = int(row[0])

      for year, cell in zip(years, row[1:]):
         parsed = MEAN_CELL.match(cell)

         if parsed is None:
            raise ValueError(f"unreadable mean {cell!r} in {path}")

         means[(year, question)] = QuestionMean(year, question, float(parsed.group(1)), float(parsed.group(2)))

   return means


def published_years():
   return tuple(sorted({year for year, _ in question_means()}))


def comparison_mean(year, question):
   """The same year's published mean when one exists, else the mean of the published years' means
   for that question position, with the years it came from."""
   means = question_means()
   exact = means.get((year, question))

   if exact is not None:
      return exact.mean, (year,)

   pooled = [means[(published, question)].mean for published in published_years() if (published, question) in means]
   has_pooled = len(pooled) > 0

   if not has_pooled:
      return None, ()

   return sum(pooled) / len(pooled), published_years()
