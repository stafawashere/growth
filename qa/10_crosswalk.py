"""Re-extract CED codes from the cached CED text and diff against curriculum.json."""
import re
from qa_common import CACHE, load_json, finish

failures, warnings = [], []
curriculum = load_json("curriculum.json")

if curriculum is None:
   finish("10_crosswalk", ["curriculum.json missing"])

text = "\n".join(path.read_text() for path in sorted((CACHE / "text" / "ced").glob("page-*.txt")) if not path.name.endswith(".raw.txt"))
ek_codes = set(re.findall(r"\b(LIM|CHA|FUN)-(\d+)\s*\.\s*([A-Z])\s*\.\s*(\d+)\b", text))
ek_codes = {f"{a}-{b}.{c}.{d}" for a, b, c, d in ek_codes}
lo_codes = {code.rsplit(".", 1)[0] for code in ek_codes}
ours_ek = {ek["ced_code"] for ek in curriculum["essential_knowledge"]}
ours_lo = {lo["ced_code"] for lo in curriculum["learning_objectives"]}

for code in sorted(ek_codes - ours_ek):
   failures.append(f"EK {code} in CED text but not in curriculum.json")

for code in sorted(ours_ek - ek_codes):
   failures.append(f"EK {code} in curriculum.json but not found in CED text")

for code in sorted(lo_codes - ours_lo):
   failures.append(f"LO {code} in CED text but not in curriculum.json")

warnings.append(f"CED text: {len(ek_codes)} EK codes, {len(lo_codes)} LO codes; registry: {len(ours_ek)} EK, {len(ours_lo)} LO")
finish("10_crosswalk", failures, warnings)
