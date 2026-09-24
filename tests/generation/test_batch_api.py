"""The blind re-solve hand-off: what the second solver is given, the batch it would be sent as on
the paid fallback, and how its answers come back. Replay only; nothing here reaches the wire."""
import json

import pytest

from app.generation import batch_api
from app.generation.instantiate import instantiate
from app.generation.template import template_module
from tools.generate_bank import stems_entry


def record_for(archetype_id, index=0):
   return instantiate(template_module(archetype_id), index, f"{archetype_id}:batch-test:{index}", generated_at="test")


@pytest.mark.parametrize("archetype_id", ["BC-QA-06004", "BC-QA-08001", "BC-QA-10007"])
def test_the_blind_solver_is_never_given_the_key_or_the_solution(archetype_id):
   record = record_for(archetype_id)
   entry = stems_entry(record)
   sent = json.dumps(batch_api.resolve_requests([entry], "claude-haiku-4-5"))
   step_texts = [step["text"] for step in record["worked_solution"]]
   derivations = [option["derivation"] for option in record["options"] if not option["is_key"]]

   assert "is_key" not in sent
   assert "error_path" not in sent
   assert "answer_key" not in sent
   assert all(text not in sent for text in step_texts)
   assert all(json.dumps(text)[1:-1] not in sent for text in derivations)

   if record["answer_key"]["form"] != "statement":
      assert "options" not in entry and "choices" not in entry


def test_a_statement_item_lists_its_choices_in_an_order_that_does_not_mark_the_key():
   record = record_for("BC-QA-10007")
   entry = stems_entry(record)

   assert entry["choices"] == sorted(option["label"] for option in record["options"])


def test_every_request_asks_for_a_positive_output_budget_and_carries_the_item_id():
   entries = [stems_entry(record_for("BC-QA-06004", index)) for index in range(3)]
   requests = batch_api.resolve_requests(entries, "claude-haiku-4-5")

   assert [request["custom_id"] for request in requests] == [entry["id"] for entry in entries]
   assert all(request["params"]["max_tokens"] > 0 for request in requests)


def test_the_batch_discount_halves_the_estimate():
   requests = batch_api.resolve_requests([stems_entry(record_for("BC-QA-06004"))], "claude-haiku-4-5")
   cost = batch_api.estimated_cost(requests, "claude-haiku-4-5")

   assert cost["batch_usd"] == pytest.approx(cost["list_usd"] / 2)
   assert cost["list_usd"] > 0


def test_results_are_read_back_as_answers_and_failures():
   lines = [
      json.dumps({"custom_id": "ITM-GEN-06004-00", "result": {"type": "succeeded", "message": {"content": [{"type": "text", "text": "Work.\n<answer>9/2 - 2*pi</answer>"}]}}}),
      json.dumps({"custom_id": "ITM-GEN-06004-01", "result": {"type": "errored", "error": {"type": "overloaded_error"}}}),
      json.dumps({"custom_id": "ITM-GEN-06004-02", "result": {"type": "succeeded", "message": {"content": [{"type": "text", "text": "I am not sure."}]}}}),
   ]
   answers, failed = batch_api.answers_from_results(lines)

   assert answers == {"ITM-GEN-06004-00": "9/2 - 2*pi"}
   assert failed == ["ITM-GEN-06004-01", "ITM-GEN-06004-02"]


def test_an_oversized_batch_is_refused_before_it_is_built(monkeypatch):
   monkeypatch.setattr(batch_api, "MAX_REQUESTS_PER_BATCH", 2)
   entries = [stems_entry(record_for("BC-QA-06004", index)) for index in range(3)]

   with pytest.raises(batch_api.BatchTooLarge):
      batch_api.resolve_requests(entries, "claude-haiku-4-5")
