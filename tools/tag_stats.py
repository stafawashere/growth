"""Count records per evidence_tag for every collection in data/."""

import csv
import json
import os
from collections import Counter

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(REPO_ROOT, "data")
TAG_ORDER = ["verified", "single-source", "inferred", "uncertain"]


def count_collection(records):
   counts = Counter()

   for record in records:
      is_mapping = isinstance(record, dict)

      if not is_mapping:
         continue

      counts[record.get("evidence_tag", "none")] += 1

   return counts


def json_collections():
   rows = []

   for filename in sorted(os.listdir(DATA_DIR)):
      is_json = filename.endswith(".json")

      if not is_json:
         continue

      with open(os.path.join(DATA_DIR, filename), encoding="utf-8") as handle:
         payload = json.load(handle)

      if not isinstance(payload, dict):
         continue

      for key in sorted(payload):
         value = payload[key]
         is_record_list = isinstance(value, list) and value and isinstance(value[0], dict)

         if not is_record_list:
            continue

         rows.append((filename, key, count_collection(value)))

   return rows


def csv_collections():
   path = os.path.join(DATA_DIR, "prereq_edges.csv")
   exists = os.path.exists(path)

   if not exists:
      return []

   with open(path, newline="", encoding="utf-8") as handle:
      edges = list(csv.DictReader(handle))

   return [("prereq_edges.csv", "edges", count_collection(edges))]


def format_row(filename, collection, counts):
   total = sum(counts.values())
   known = [str(counts.get(tag, 0)) for tag in TAG_ORDER]
   other = total - sum(counts.get(tag, 0) for tag in TAG_ORDER)

   return "| {} | {} | {} | {} | {} |".format(
      filename, collection, " | ".join(known), other, total
   )


def main():
   rows = json_collections() + csv_collections()

   print("| file | collection | " + " | ".join(TAG_ORDER) + " | other | total |")
   print("|---|---|---|---|---|---|---|---|")

   grand = Counter()

   for filename, collection, counts in rows:
      grand.update(counts)
      print(format_row(filename, collection, counts))

   print(format_row("ALL", "all collections", grand))


if __name__ == "__main__":
   main()
