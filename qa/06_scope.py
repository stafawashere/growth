"""AB/BC scope consistency: skills in BC-only units are not AB_only; FRQ records in BC-only units are BC_only."""
from qa_common import load_json, finish

failures = []
curriculum = load_json("curriculum.json")
skills = load_json("skills.json")
frq = load_json("frq_records.json")

if curriculum is None:
   finish("06_scope", ["curriculum.json missing"])

topic_scope = {topic["id"]: topic["scope"] for topic in curriculum["topics"]}
unit_scope = {unit["id"]: unit["scope"] for unit in curriculum["units"]}

if skills:
   for skill in skills["skills"]:
      topic = topic_scope.get(skill["topic"], "n/a")
      is_contradiction = topic == "BC_only" and skill["scope"] == "AB_only"

      if is_contradiction:
         failures.append(f"{skill['id']} AB_only inside BC_only topic {skill['topic']}")

if frq:
   for record in frq["records"]:
      unit = unit_scope.get(record["primary_unit"], "n/a")
      is_contradiction = unit == "BC_only" and record.get("shared_with_ab") is True

      if is_contradiction:
         failures.append(f"{record['id']} marked shared_with_ab but primary unit is BC_only")

finish("06_scope", failures)
