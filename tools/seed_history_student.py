"""Give a test student weeks of practice history through the HTTP API of a local scratch server.

Usage: .venv/bin/python tools/seed_history_student.py --api http://127.0.0.1:8005 --username walk_history
   --password <password> --days 28 --accuracy 0.7 --seed 7 [--content-root content]
   [--skip-diagnostic-units 4,5,6,7,8,9,10]

For local development only: it signs up the installation's one user (or logs in when signup is
closed), runs the onboarding diagnostic, then walks one learning session a day for --days calendar
days ending yesterday by this machine's clock, which is the server's when both run here. Answers are
right with probability --accuracy, read from the item keys under content/items_*/, so the history
has a known shape. Any 4xx or 5xx stops the run with the response text and exit status 1.
"""
import argparse
import json
import random
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import date, timedelta
from http.cookiejar import CookieJar
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.items.ingest import load_records

SIGNUP_CLOSED_STATUS = 403
READING_KINDS = ("lesson", "refresher")
ANSWER_ELAPSED_MS = 45000
LESSON_ELAPSED_MS = 120000
CONFIDENT_SHARE = 0.6
ERROR_NOTE = "I rushed the last step and did not check the answer against the question."


class SeedFailure(Exception):
   pass


class UrllibTransport:
   """Keeps whatever cookies the server sets, which is how the session cookie comes back."""

   def __init__(self, api):
      self.api = api.rstrip("/")
      self.opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(CookieJar()))

   def request(self, method, path, body=None, params=None):
      url = self.api + path

      if params:
         url = f"{url}?{urllib.parse.urlencode(params)}"

      data = None if body is None else json.dumps(body).encode()
      headers = {"Content-Type": "application/json"} if data is not None else {}
      outgoing = urllib.request.Request(url, data=data, method=method, headers=headers)

      try:
         with self.opener.open(outgoing) as response:
            return response.status, response.read().decode()
      except urllib.error.HTTPError as refused:
         return refused.code, refused.read().decode()


class Api:
   def __init__(self, transport):
      self.transport = transport

   def send(self, method, path, body=None, params=None, allowed=()):
      status, text = self.transport.request(method, path, body, params)
      is_failure = status >= 400 and status not in allowed

      if is_failure:
         raise SeedFailure(f"{method} {path} answered {status}: {text}")

      return status, json.loads(text) if text else None

   def get(self, path, params=None):
      return self.send("GET", path, params=params)[1]

   def post(self, path, body=None):
      return self.send("POST", path, body=body)[1]


def load_keys(content_root):
   records = {}

   for directory in sorted(Path(content_root).glob("items_*")):
      if not directory.is_dir():
         continue

      for record in load_records(directory):
         records[record["id"]] = record

   return records


def waiting_unit_number(api, session_id):
   """The unit the diagnostic run filed the waiting item under, which is the unit the skip route
   records, read from the run in the session queue: BC-UNIT-03 is unit 3."""
   run = api.get(f"/sessions/{session_id}")["queue"]["diagnostic"]
   waiting = [entry for entry in run["asked"] if entry.get("outcome") is None]

   if not waiting:
      raise SeedFailure(f"diagnostic {session_id} serves an item but has no asked entry waiting")

   return int(waiting[0]["unit"].rsplit("-", 1)[-1])


def key_option_id(record):
   for option in record.get("options") or []:
      if option.get("is_key") is True:
         return option["id"]

   raise SeedFailure(f"item {record['id']} has no option marked is_key")


def distractor_option_id(record):
   for option in record.get("options") or []:
      if option.get("is_key") is not True:
         return option["id"]

   raise SeedFailure(f"item {record['id']} has no distractor to answer wrong with")


def wrong_mathjson(key):
   is_plain_number = isinstance(key, (int, float)) and not isinstance(key, bool)

   if is_plain_number:
      return key + 1

   return ["Add", key, 1]


def answer_for(served, keys, intends_correct):
   record = keys.get(served["id"])

   if record is None:
      raise SeedFailure(f"no content record carries a key for item {served['id']}")

   key_mathjson = (record.get("answer_key") or {}).get("mathjson")
   is_served_as_choice = served.get("format") == "mcq"
   is_statement_keyed = served.get("requires_choice") is True or key_mathjson is None
   answers_with_option = is_served_as_choice or is_statement_keyed

   if answers_with_option:
      chosen = key_option_id(record) if intends_correct else distractor_option_id(record)

      return {"option_id": chosen}

   return {"mathjson": key_mathjson if intends_correct else wrong_mathjson(key_mathjson)}


def sign_in(api, username, password):
   credentials = {"username": username, "password": password}
   status, body = api.send("POST", "/auth/signup", body=credentials, allowed=(SIGNUP_CLOSED_STATUS,))
   signup_is_closed = status == SIGNUP_CLOSED_STATUS

   if signup_is_closed:
      api.post("/auth/login", credentials)

      return "logged in"

   return f"signed up as {body['user']['id']}"


def run_diagnostic(api, keys, day, rng, accuracy, skipped_units):
   today = day.isoformat()
   opened = api.post("/sessions", {"mode": "diagnostic", "today": today})
   session_id = opened["id"]
   answered = 0
   skipped = 0
   served = api.get(f"/sessions/{session_id}/next", {"today": today})

   while served["item"] is not None:
      item = served["item"]
      is_in_skipped_unit = waiting_unit_number(api, session_id) in skipped_units

      if is_in_skipped_unit:
         skipped += 1
         body = {"item_id": item["id"], "elapsed_ms": ANSWER_ELAPSED_MS, "today": today}
         served = api.post(f"/sessions/{session_id}/diagnostic/skip-unit", body)

         continue

      intends_correct = rng.random() < accuracy
      api.post(
         f"/sessions/{session_id}/attempts",
         {
            "item_id": item["id"],
            "answer": answer_for(item, keys, intends_correct),
            "elapsed_ms": ANSWER_ELAPSED_MS,
            "today": today,
         },
      )
      answered += 1
      served = api.get(f"/sessions/{session_id}/next", {"today": today})

   result = api.get(f"/sessions/{session_id}/diagnostic")
   states = ", ".join(f"{entry['unit']} {entry['state']}" for entry in result["units"])

   return f"diagnostic {today}: answered {answered}, skipped by unit {skipped}; {states}"


def read_lesson(api, session_id, entry):
   path = f"/sessions/{session_id}/lessons/{entry['lesson_id']}/events"
   marks = {"band": entry.get("band"), "reason": entry.get("reason")}
   api.post(path, dict(marks, event="opened", elapsed_ms=0))
   api.post(path, dict(marks, event="completed", elapsed_ms=LESSON_ELAPSED_MS))


def rating_for(intends_correct, rng):
   is_confident = intends_correct and rng.random() < CONFIDENT_SHARE

   return "confident" if is_confident else "unsure"


def answer_item(api, keys, session_id, item, today, rng, accuracy):
   intends_correct = rng.random() < accuracy
   attempt = api.post(
      f"/sessions/{session_id}/attempts",
      {
         "item_id": item["id"],
         "answer": answer_for(item, keys, intends_correct),
         "elapsed_ms": ANSWER_ELAPSED_MS,
         "today": today,
      },
   )
   attempt_path = f"/sessions/{session_id}/attempts/{attempt['id']}"
   awaits_rating = attempt["confidence"] is None

   if awaits_rating:
      api.post(f"{attempt_path}/confidence", {"confidence": rating_for(intends_correct, rng), "today": today})

   api.get(f"{attempt_path}/feedback")
   is_opener = item.get("is_opener") is True
   was_corrected = attempt["correct"] is False and not is_opener

   if was_corrected:
      api.post(f"{attempt_path}/error-note", {"note": ERROR_NOTE})

   return attempt["correct"] is True


def practise_day(api, keys, day, rng, accuracy):
   today = day.isoformat()
   session_id = api.post("/sessions", {"mode": "learning", "today": today})["id"]
   served_count = 0
   correct_count = 0
   lessons_read = 0

   while True:
      entry = api.get(f"/sessions/{session_id}/next", {"today": today})["item"]

      if entry is None:
         break

      is_reading = entry.get("kind") in READING_KINDS

      if is_reading:
         read_lesson(api, session_id, entry)
         lessons_read += 1

         continue

      served_count += 1

      if answer_item(api, keys, session_id, entry, today, rng, accuracy):
         correct_count += 1

   api.post(f"/sessions/{session_id}/close", {"today": today})
   is_closed = api.get(f"/sessions/{session_id}")["ended_at"] is not None

   return {"served": served_count, "correct": correct_count, "lessons": lessons_read, "closed": int(is_closed)}


def practice_days(last_day, count):
   return [last_day - timedelta(days=offset) for offset in range(count - 1, -1, -1)]


def seed(transport, options, last_day=None, out=print):
   api = Api(transport)
   rng = random.Random(options.seed)
   keys = load_keys(options.content_root)
   days = practice_days(last_day or date.today() - timedelta(days=1), options.days)
   out(sign_in(api, options.username, options.password))
   progress = api.get("/progress", {"today": days[0].isoformat()})
   is_first_login = progress["home_state"] == "first_login"
   has_unfinished_diagnostic = progress["diagnostic_in_progress"] is not None
   needs_diagnostic = is_first_login or has_unfinished_diagnostic

   if needs_diagnostic:
      diagnostic_day = days[0] - timedelta(days=1)
      out(run_diagnostic(api, keys, diagnostic_day, rng, options.accuracy, options.skip_diagnostic_units))
   else:
      out("diagnostic already taken, not run again")

   totals = {"served": 0, "correct": 0, "lessons": 0, "closed": 0}

   for day in days:
      tally = practise_day(api, keys, day, rng, options.accuracy)
      out(f"{day.isoformat()}  served {tally['served']:3d}  correct {tally['correct']:3d}  lessons {tally['lessons']}  sessions closed {tally['closed']}")

      for name in totals:
         totals[name] += tally[name]

   share = totals["correct"] / totals["served"] if totals["served"] else 0.0
   out(
      f"total over {len(days)} days: served {totals['served']}, correct {totals['correct']} ({share:.2f}), "
      f"lessons read {totals['lessons']}, sessions closed {totals['closed']}"
   )

   return totals


def unit_list(text):
   if not text:
      return set()

   return {int(part) for part in text.split(",") if part.strip()}


def parse_options(argv):
   parser = argparse.ArgumentParser(description="Seed a local test student with practice history.")
   parser.add_argument("--api", required=True)
   parser.add_argument("--username", required=True)
   parser.add_argument("--password", required=True)
   parser.add_argument("--days", type=int, default=28)
   parser.add_argument("--accuracy", type=float, default=0.7)
   parser.add_argument("--seed", type=int, default=7)
   parser.add_argument("--content-root", default="content")
   parser.add_argument("--skip-diagnostic-units", type=unit_list, default=set())

   return parser.parse_args(argv)


def main(argv=None):
   options = parse_options(argv)

   try:
      seed(UrllibTransport(options.api), options)
   except (SeedFailure, urllib.error.URLError) as failure:
      print(failure, file=sys.stderr)

      return 1

   return 0


if __name__ == "__main__":
   sys.exit(main())
