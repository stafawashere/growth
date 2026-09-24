"""Collect the error-to-skill links proposed while authoring templates into one staging file.

Each var/p4/error_links/<archetype>.json names existing BC-ERR records whose skills should gain the
archetype's skills, with the reason the error occurs there. The links become
data/staging/error-links-p4.json, an "append" staging file, so tools/merge_staging.py adds the
skills without replacing any other field of the error record.

Usage: python3 tools/merge_error_links.py
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROPOSALS = ROOT / "var" / "p4" / "error_links"
STAGING = ROOT / "data" / "staging" / "error-links-p4.json"


def collect(proposal_paths, known_errors, known_skills):
   additions = {}
   reasons = {}
   problems = []

   for path in proposal_paths:
      proposal = json.loads(path.read_text())

      for link in proposal["links"]:
         error_id = link["error_id"]
         unknown_skills = [skill for skill in link["add_skills"] if skill not in known_skills]

         if error_id not in known_errors:
            problems.append(f"{path.name}: {error_id} is not an active error")
            continue

         if unknown_skills:
            problems.append(f"{path.name}: unknown skills {unknown_skills}")
            continue

         additions.setdefault(error_id, [])

         for skill in link["add_skills"]:
            if skill not in additions[error_id]:
               additions[error_id].append(skill)

         reasons.setdefault(error_id, []).append(f"{proposal['archetype_id']}: {link['reason']}")

   return additions, reasons, problems


def main():
   errors = json.loads((ROOT / "data" / "errors.json").read_text())["errors"]
   skills = json.loads((ROOT / "data" / "skills.json").read_text())["skills"]
   known_errors = {error["id"] for error in errors if error.get("status", "active") == "active"}
   known_skills = {skill["id"] for skill in skills}
   existing = json.loads(STAGING.read_text()) if STAGING.exists() else {"errors": [], "reasons": {}}
   additions = {record["id"]: list(record["skills"]) for record in existing["errors"]}
   reasons = dict(existing.get("reasons", {}))
   new_additions, new_reasons, problems = collect(sorted(PROPOSALS.glob("*.json")), known_errors, known_skills)

   if problems:
      print("\n".join(problems), file=sys.stderr)
      return 1

   for error_id, skill_ids in new_additions.items():
      merged = additions.setdefault(error_id, [])
      merged.extend(skill for skill in skill_ids if skill not in merged)

   for error_id, texts in new_reasons.items():
      kept = reasons.setdefault(error_id, [])
      kept.extend(text for text in texts if text not in kept)

   staged = {
      "registry": "errors",
      "merge": "append",
      "errors": [{"id": error_id, "skills": additions[error_id]} for error_id in sorted(additions)],
      "reasons": {error_id: reasons[error_id] for error_id in sorted(reasons)},
   }
   STAGING.write_text(json.dumps(staged, indent=1) + "\n")
   print(f"{len(additions)} errors carry proposed skill links in {STAGING.relative_to(ROOT)}")

   return 0


if __name__ == "__main__":
   sys.exit(main())
