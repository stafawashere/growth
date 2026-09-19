"""Deterministic IDs for CED objects. Import and call; never hand-type these."""


def unit_id(number):
   return f"BC-UNIT-{number:02d}"


def topic_id(unit, topic):
   return f"BC-TOP-{unit:02d}{topic:02d}"


def lo_id(ced_code):
   """LIM-1.A -> BC-LO-LIM-1A"""
   big_idea, rest = ced_code.split("-")
   return "BC-LO-" + big_idea + "-" + rest.replace(".", "")


def ek_id(ced_code):
   """LIM-1.A.1 -> BC-EK-LIM-1A1"""
   big_idea, rest = ced_code.split("-")
   return "BC-EK-" + big_idea + "-" + rest.replace(".", "")


def mp_id(number):
   return f"BC-MP-{number}"


def mps_id(code):
   """3.D -> BC-MPS-3D"""
   return "BC-MPS-" + code.replace(".", "")


def frq_id(year, question, part=None):
   suffix = f"-{part.upper()}" if part else ""
   return f"BC-FRQ-{year}-Q{question}{suffix}"
