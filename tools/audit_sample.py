"""Deterministic sampler for the skeptic review audit. Seed 2027."""

import json
import os
import random
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SEED = 2027


def load(name):
   with open(os.path.join(ROOT, "data", name), encoding="utf-8") as handle:
      return json.load(handle)


def page_text(doc_id, page, limit=6000):
   base = os.path.join(ROOT, "cache", "text", str(doc_id))
   for suffix in ("raw.txt", "txt"):
      path = os.path.join(base, "page-%03d.%s" % (int(page), suffix))

      if os.path.exists(path):
         with open(path, encoding="utf-8", errors="replace") as handle:
            return path, handle.read()[:limit]

   return None, "MISSING PAGE %s/%s" % (doc_id, page)


def spread_by_year(records, wanted):
   """Pick records spread across years, deterministically."""
   buckets = {}

   for record in records:
      buckets.setdefault(record.get("year"), []).append(record)

   years = sorted(buckets, key=lambda value: str(value))

   for year in years:
      buckets[year].sort(key=lambda record: record["id"])

   rng = random.Random(SEED)
   picked = []
   index = 0

   while len(picked) < wanted:
      year = years[index % len(years)]
      pool = [record for record in buckets[year] if record not in picked]
      index += 1

      if not pool:
         continue

      picked.append(rng.choice(pool))

   return sorted(picked, key=lambda record: record["id"])


def sample(items, wanted, key="id"):
   ordered = sorted(items, key=lambda item: item[key])
   rng = random.Random(SEED)

   return sorted(rng.sample(ordered, min(wanted, len(ordered))), key=lambda item: item[key])


def main():
   groups = {}

   frq = load("frq_records.json")["records"]
   groups["frq"] = spread_by_year(frq, 25)

   skills = load("skills.json")["skills"]
   groups["skills"] = sample(skills, 15)

   points = load("scoring_points.json")["point_types"]
   groups["scoring_points"] = sample(points, 10)

   errors = load("errors.json")["errors"]
   cr_errors = [error for error in errors if error["id"].startswith("BC-ERR-99")]
   groups["cr_errors"] = sample(cr_errors, 10)

   mcq = load("mcq_records.json")["records"]
   groups["mcq"] = sample(mcq, 10)

   diagnostic_errors = sample(errors, 8)
   groups["diagnostic_errors"] = diagnostic_errors

   misconceptions = load("misconceptions.json")["misconceptions"]
   groups["diagnostic_misconceptions"] = sample(misconceptions, 8)

   groups["adaptive_skills"] = sample(skills, 10)

   if "--ids" in sys.argv:
      for name, rows in groups.items():
         print(name, [row["id"] for row in rows])

      return

   print(json.dumps({name: [row["id"] for row in rows] for name, rows in groups.items()}, indent=1))


if __name__ == "__main__":
   main()
