"""docs/plan/13-ai-engineering.md, "Where app/providers/guard.py is wrong", item 1: the price table
has to price every model the routing names, and Gemini 3.8 Flash's promotional end date has to be
data because the price doubles on 2027-01-01.

Every expected number is parsed out of the plan's own price table and routing table, never retyped,
so a price patched in the guard without the plan changing, or the plan changing without the guard,
goes red here.
"""
import re
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

import pytest
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session as SqlSession

from app.db import models
from app.providers.base import Message, ProviderRequest
from app.providers.guard import (
   CACHE_READ_MULTIPLIER,
   CACHE_WRITE_1H_MULTIPLIER,
   MODEL_PRICES,
   BudgetCaps,
   GuardedProvider,
   price_for,
)
from app.providers.replay import ReplayProvider
from tools import cost_model

REPO = Path(__file__).resolve().parents[2]
PLAN_13 = (REPO / "docs" / "plan" / "13-ai-engineering.md").read_text()

MODEL_ID = re.compile(r"\b(?:claude|gemini)-[a-z0-9.-]*[a-z0-9]")
ISO_DAY = re.compile(r"\b(to|from) (\d{4}-\d{2}-\d{2})$")


def _section(start_marker, end_marker):
   start = PLAN_13.index(start_marker)
   end = PLAN_13.index(end_marker, start)

   return PLAN_13[start:end]


def _table_rows(text):
   rows = []

   for line in text.splitlines():
      is_row = line.startswith("| ")
      is_rule = line.startswith("| ---")

      if is_row and not is_rule:
         rows.append([cell.strip() for cell in line.strip("|").split("|")])

   return rows


def _rate(cell):
   return None if cell == "n/a" else float(cell)


def plan_price_rows():
   """The interactive rows of 13's price table. Batch rows are item 2, which the guard does not model."""
   rows = _table_rows(_section("## The cost model", "**Token assumptions per call.**"))
   priced = []

   for label, base_input, _write_5m, write_1h, cache_read, output, _source in rows[1:]:
      is_batch = ", batch" in label

      if is_batch:
         continue

      model = label.split(",")[0]
      boundary = ISO_DAY.search(label)

      priced.append({
         "label": label,
         "model": model,
         "boundary": None if boundary is None else (boundary.group(1), date.fromisoformat(boundary.group(2))),
         "input": _rate(base_input),
         "write_1h": _rate(write_1h),
         "read": _rate(cache_read),
         "output": _rate(output),
      })

   return priced


def routed_models():
   """Every model the D8 re-routing names, plus the two item 1 says the table needs."""
   routing = _section("## D8 row by row", "**tutor, kept.**")
   routed = set()

   for row in _table_rows(routing)[1:]:
      routed.update(MODEL_ID.findall(row[-1]))

   item_one = _section("1. **The price table cannot serve the routing.**", "2. **Batch pricing")
   needs_start = item_one.index("The table needs")
   needs_end = item_one.index(", and it needs", needs_start)
   routed.update(MODEL_ID.findall(item_one[needs_start:needs_end]))

   return routed


def dated_rows(model):
   rows = [row for row in plan_price_rows() if row["model"] == model and row["boundary"] is not None]
   through = next(row for row in rows if row["boundary"][0] == "to")
   starting = next(row for row in rows if row["boundary"][0] == "from")

   return through, starting


def test_the_plan_tables_parse_to_the_models_item_one_names():
   routed = routed_models()

   assert {"claude-haiku-4-5", "gemini-3.8-flash", "gemini-3.5-flash-lite", "claude-sonnet-5"} <= routed
   assert len(plan_price_rows()) >= 6


def test_every_routed_model_is_priced_on_both_sides_of_the_promotional_boundary():
   through, starting = dated_rows("gemini-3.8-flash")

   for model in sorted(routed_models()):
      for day in (through["boundary"][1], starting["boundary"][1]):
         price_for(model, day=day)


def test_the_guard_prices_exactly_the_models_the_plan_prices():
   assert set(MODEL_PRICES) == {row["model"] for row in plan_price_rows()}


def test_undated_prices_match_the_plan_table():
   undated = [row for row in plan_price_rows() if row["boundary"] is None]
   assert undated

   for row in undated:
      price = price_for(row["model"], day=date(2026, 9, 20))

      assert price.input_usd_per_mtok == row["input"], row["label"]
      assert price.output_usd_per_mtok == row["output"], row["label"]


def test_the_cache_read_multiplier_reproduces_every_printed_cache_read_price():
   """The guard charges a cache read at input times one multiplier. Every row the plan prints a read
   price for, Gemini included, must come out at that printed price."""
   for row in plan_price_rows():
      day = date(2026, 9, 20) if row["boundary"] is None else row["boundary"][1]
      price = price_for(row["model"], day=day)

      assert price.input_usd_per_mtok * CACHE_READ_MULTIPLIER == pytest.approx(row["read"]), row["label"]


def test_the_cache_write_multiplier_reproduces_every_printed_1h_write_price():
   written = [row for row in plan_price_rows() if row["write_1h"] is not None]
   assert written

   for row in written:
      price = price_for(row["model"], day=date(2026, 9, 20))

      assert price.input_usd_per_mtok * CACHE_WRITE_1H_MULTIPLIER == pytest.approx(row["write_1h"]), row["label"]


def test_gemini_flash_is_promotional_through_the_end_date_and_standard_from_the_next_day():
   through, starting = dated_rows("gemini-3.8-flash")
   last_promotional_day = through["boundary"][1]
   first_standard_day = starting["boundary"][1]

   assert first_standard_day == last_promotional_day + timedelta(days=1)

   promotional = price_for("gemini-3.8-flash", day=last_promotional_day)
   standard = price_for("gemini-3.8-flash", day=first_standard_day)

   assert (promotional.input_usd_per_mtok, promotional.output_usd_per_mtok) == (through["input"], through["output"])
   assert (standard.input_usd_per_mtok, standard.output_usd_per_mtok) == (starting["input"], starting["output"])


def test_the_guard_agrees_with_the_cost_model_it_is_cited_beside():
   _through, starting = dated_rows("gemini-3.8-flash")
   standard = price_for("gemini-3.8-flash", day=starting["boundary"][1])
   recorded_2027 = cost_model.PRICES["gemini-3.8-flash-2027"]

   assert (standard.input_usd_per_mtok, standard.output_usd_per_mtok) == (recorded_2027["input"], recorded_2027["output"])

   for model in MODEL_PRICES:
      price = price_for(model, day=date(2026, 9, 20))
      recorded = cost_model.PRICES[model]

      assert (price.input_usd_per_mtok, price.output_usd_per_mtok) == (recorded["input"], recorded["output"]), model


def test_a_dated_price_asked_for_without_a_day_is_refused():
   with pytest.raises(ValueError):
      price_for("gemini-3.8-flash")


def test_a_model_the_plan_does_not_price_is_refused():
   with pytest.raises(ValueError):
      price_for("gemini-3.8-pro", day=date(2026, 9, 20))


class FixedClock:
   def __init__(self, moment):
      self.moment = moment

   def __call__(self):
      return self.moment


def _charged_cost(day, usage):
   engine = create_engine("sqlite:///:memory:")
   models.Base.metadata.create_all(engine)
   db = SqlSession(engine)

   cassette = {"text": "Check the sign of the derivative.", "finish_reason": "end_turn", "usage": usage}
   guard = GuardedProvider(
      ReplayProvider(cassette=cassette),
      db,
      user_id="USR-1",
      clock=FixedClock(datetime(day.year, day.month, day.day, 12, 0, tzinfo=timezone.utc)),
      caps={"verifier": BudgetCaps(cap_usd=1000.0)},
      provider_name="gemini",
   )
   request = ProviderRequest(
      role="verifier",
      model="gemini-3.8-flash",
      system="s" * 400,
      messages=(Message(role="user", content="u" * 400),),
      max_output_tokens=1000,
   )

   guard.generate(request)

   return db.execute(select(models.Budget.cost_usd)).scalar_one()


def test_the_guard_charges_the_price_in_force_on_its_clock_day():
   through, starting = dated_rows("gemini-3.8-flash")
   usage = dict(input_tokens=50_000, output_tokens=20_000, cached_read_tokens=0, cached_write_tokens=0)

   for row in (through, starting):
      expected = (50_000 / 1_000_000) * row["input"] + (20_000 / 1_000_000) * row["output"]

      assert _charged_cost(row["boundary"][1], usage) == pytest.approx(expected), row["label"]
