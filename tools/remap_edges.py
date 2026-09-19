"""Rewrite cross-unit edges that point at a BC-TOP id to the BC-SKL the edge note names.

Cross-unit edges were written before the other unit's skills existed, so the endpoint is the
topic id and the note names the intended skill in prose. This compares the note with the names
of the skills registered under that topic and rewrites the endpoint when one skill wins
outright. Ties and empty overlaps keep the topic id and get "unmapped" appended to the note.
"""
import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STAGING = ROOT / "data" / "staging"
SKILLS = ROOT / "data" / "skills.json"
FIELDS = ["from", "to", "type", "evidence_tag", "note"]

STOPWORDS = {
   "a", "an", "and", "as", "at", "be", "by", "for", "from", "in", "is", "it", "its", "of",
   "on", "or", "that", "the", "this", "to", "with", "which", "are", "was", "unit", "topic",
   "skill", "id", "ids", "exists", "exist", "no", "not", "time", "writing", "data",
   "skills", "json", "prerequisite", "prerequisites", "supports", "support", "underlie",
   "underlies", "used", "use", "uses", "step", "when", "student", "students",
}


def tokenise(text):
   words = re.findall(r"[a-z']+", text.lower())
   return {word for word in words if word not in STOPWORDS and len(word) > 2}


def load_topic_index():
   registry = json.loads(SKILLS.read_text())
   index = {}

   for skill in registry["skills"]:
      name_tokens = tokenise(skill["name"])
      body_tokens = tokenise(skill.get("description_plain", "")) | tokenise(skill.get("description_formal", ""))
      index.setdefault(skill["topic"], []).append((skill["id"], name_tokens, body_tokens))

   return index


def best_match(note, candidates):
   note_tokens = tokenise(note)
   scored = []

   for skill_id, name_tokens, body_tokens in candidates:
      name_overlap = len(note_tokens & name_tokens)
      body_overlap = len(note_tokens & (body_tokens - name_tokens))
      score = 3 * name_overlap + body_overlap

      if score:
         scored.append((score, skill_id))

   if not scored:
      return None

   scored.sort(reverse=True)
   top_score, winner = scored[0]
   runner_up = scored[1][0] if len(scored) > 1 else 0

   is_unambiguous = top_score >= 3 and top_score > runner_up

   if not is_unambiguous:
      return None

   return winner


def remap_row(row, topic_index):
   remapped = 0
   unmapped = 0

   for endpoint in ("from", "to"):
      value = row[endpoint]
      is_topic = value.startswith("BC-TOP-")

      if not is_topic:
         continue

      match = best_match(row["note"], topic_index.get(value, []))

      if match:
         row[endpoint] = match
         remapped += 1
      else:
         already_flagged = row["note"].rstrip().endswith("unmapped")

         if not already_flagged:
            row["note"] = f"{row['note'].rstrip().rstrip('.')}; unmapped"

         unmapped += 1

   return remapped, unmapped


def main():
   topic_index = load_topic_index()
   total_remapped = 0
   total_unmapped = 0

   for path in sorted(STAGING.glob("*.edges.csv")):
      with path.open() as handle:
         rows = [dict(row) for row in csv.DictReader(handle)]

      for row in rows:
         row["note"] = re.sub(r"[;.]?\s*unmapped\s*$", "", row["note"]).rstrip()

      file_remapped = 0

      for row in rows:
         remapped, unmapped = remap_row(row, topic_index)
         file_remapped += remapped
         total_remapped += remapped
         total_unmapped += unmapped

      with path.open("w", newline="") as handle:
         writer = csv.DictWriter(handle, fieldnames=FIELDS)
         writer.writeheader()

         for row in rows:
            writer.writerow({field: row.get(field, "") for field in FIELDS})

      print(path.name, "remapped", file_remapped)

   print("remapped", total_remapped, "endpoints; still topic-level", total_unmapped)


if __name__ == "__main__":
   main()
