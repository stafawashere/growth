"""Shared definitions for registries, ID formats, and evidence tags."""

import re

EVIDENCE_TAGS = ["verified", "single-source", "inferred", "uncertain"]
SCOPES = ["AB_only", "shared", "BC_only", "n/a"]

ID_PATTERNS = {
   "BC-UNIT": r"^BC-UNIT-\d{2}$",
   "BC-TOP": r"^BC-TOP-\d{4}$",
   "BC-LO": r"^BC-LO-[A-Z]{3}-\d+[A-Z]$",
   "BC-EK": r"^BC-EK-[A-Z]{3}-\d+[A-Z]\d+$",
   "BC-MP": r"^BC-MP-\d$",
   "BC-MPS": r"^BC-MPS-\d[A-Z]$",
   "BC-CON": r"^BC-CON-\d{5}$",
   "BC-SKL": r"^BC-SKL-\d{5}$",
   "BC-PRQ": r"^BC-PRQ-\d{5}$",
   "BC-QA": r"^BC-QA-\d{5}$",
   "BC-QV": r"^BC-QV-\d{5}-\d{2}$",
   "BC-PT": r"^BC-PT-\d{5}$",
   "BC-ERR": r"^BC-ERR-\d{5}$",
   "BC-MIS": r"^BC-MIS-\d{5}$",
   "BC-SIG": r"^BC-SIG-\d{5}$",
   "BC-REP": r"^BC-REP-\d{2}$",
   "BC-DF": r"^BC-DF-\d{2}$",
   "BC-CV": r"^BC-CV-\d{2}$",
   "BC-FRQ": r"^BC-FRQ-\d{4}-Q\d(-[A-F])?$",
   "BC-MCQ": r"^BC-MCQ-[A-Z0-9]+-\d{3}$",
   "BC-SRC": r"^BC-SRC-[a-z0-9-]+$",
}

ANY_ID = re.compile(r"\bBC-(?:UNIT|TOP|LO|EK|MP|MPS|CON|SKL|PRQ|QA|QV|PT|ERR|MIS|SIG|REP|DF|CV|FRQ|MCQ|SRC)-[A-Za-z0-9-]+\b")

REGISTRY_FILES = {
   "BC-UNIT": "curriculum.json:units",
   "BC-TOP": "curriculum.json:topics",
   "BC-LO": "curriculum.json:learning_objectives",
   "BC-EK": "curriculum.json:essential_knowledge",
   "BC-MP": "curriculum.json:practices",
   "BC-MPS": "curriculum.json:practice_skills",
   "BC-CON": "skills.json:concepts",
   "BC-SKL": "skills.json:skills",
   "BC-PRQ": "skills.json:prerequisites",
   "BC-QA": "archetypes.json:archetypes",
   "BC-QV": "archetypes.json:variants",
   "BC-PT": "scoring_points.json:point_types",
   "BC-ERR": "errors.json:errors",
   "BC-MIS": "misconceptions.json:misconceptions",
   "BC-SIG": "diagnostic_signals.json:signals",
   "BC-REP": "taxonomies.json:representations",
   "BC-DF": "taxonomies.json:difficulty_factors",
   "BC-CV": "taxonomies.json:command_verbs",
   "BC-FRQ": "frq_records.json:records",
   "BC-MCQ": "mcq_records.json:records",
   "BC-SRC": "sources.json:sources",
}

FORBIDDEN_PREDICTION = [
   r"will (definitely |certainly |almost certainly )?(appear|be tested|be on the exam|show up)",
   r"\bexpect(ed)? (to see|on the (2027|exam))",
   r"\bguaranteed\b",
   r"\bhigh probability of appearing\b",
   r"\blikely to appear\b",
   r"\bpredict(s|ed)? that\b",
]
