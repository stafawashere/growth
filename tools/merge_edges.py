"""Merge data/staging/*.edges.csv into data/prereq_edges.csv, de-duplicated on (from, to, type)."""
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STAGING = ROOT / "data" / "staging"
OUT = ROOT / "data" / "prereq_edges.csv"
FIELDS = ["from", "to", "type", "evidence_tag", "note"]


def main():
   rows = {}

   for path in sorted(STAGING.glob("*.edges.csv")):
      with path.open() as handle:
         for row in csv.DictReader(handle):
            key = (row["from"], row["to"], row["type"])
            rows[key] = {field: row.get(field, "") for field in FIELDS}

   with OUT.open("w", newline="") as handle:
      writer = csv.DictWriter(handle, fieldnames=FIELDS)
      writer.writeheader()

      for key in sorted(rows):
         writer.writerow(rows[key])

   print(len(rows), "edges")


if __name__ == "__main__":
   main()
