"""The Message Batches path for the independent re-solve, the documented fallback to offline work.

docs/plan/11-phased-delivery.md P4 scope item 8: generation and verification run off the
interactive path, so on the API they run as a batch at 50 percent off input and output, up to
100,000 requests or 256 MB per batch, with max_tokens 0 refused inside a batch
(https://platform.claude.com/docs/en/build-with-claude/batch-processing). The operator's standing
route is offline Claude Code work at $0.00 API (docs/operator/offline-authoring.md); this module
builds and prices the batch a paid run would send, and reads its results back into the same
formulation shape the blind solver writes, so either route feeds tools/key_recheck.py.

Nothing here sends a request. submit() takes the transport as an argument, and no test passes a
real one.
"""
import json
from pathlib import Path

from tools.cost_model import USD_PER_MTOK, price

ROOT = Path(__file__).resolve().parents[2]
RESOLVE_PROMPT = ROOT / "prompts" / "verifier" / "independent_resolve_v1.md"
BATCHES_URL = "https://api.anthropic.com/v1/messages/batches"

MAX_REQUESTS_PER_BATCH = 100_000
MAX_BATCH_BYTES = 256 * 1024 * 1024
RESOLVE_MAX_TOKENS = 2000
CHARACTERS_PER_TOKEN = 3.1
ANSWER_OPEN = "<answer>"
ANSWER_CLOSE = "</answer>"

SYSTEM_INSTRUCTIONS = (
   "You answer one AP Calculus BC practice item from its stem alone. You are not shown any key or "
   "solution. Work the mathematics, then give only the final answer between <answer> and </answer>: "
   "an exact value in plain SymPy syntax, a decimal correct to three places when the item asks for "
   "one, or, when choices are listed, the exact text of the one correct choice."
)


class BatchTooLarge(ValueError):
   pass


def user_turn(entry):
   parts = [f"Item {entry['id']}.", entry["stem"]]
   figure = entry.get("figure")

   if figure is not None:
      parts.append("Figure data: " + json.dumps(figure, sort_keys=True))

   if entry.get("answer_format"):
      parts.append(f"Give the answer as {entry['answer_format']}.")

   if entry.get("choices"):
      parts.append("Choices:\n" + "\n".join(f"- {choice}" for choice in entry["choices"]))

   return "\n\n".join(parts)


def resolve_requests(stems, model):
   """One Message Batches request per item, keyed by its id. max_tokens is always positive,
   because the batch endpoint refuses max_tokens 0."""
   requests = [
      {
         "custom_id": entry["id"],
         "params": {
            "model": model,
            "max_tokens": RESOLVE_MAX_TOKENS,
            "system": SYSTEM_INSTRUCTIONS,
            "messages": [{"role": "user", "content": user_turn(entry)}],
         },
      }
      for entry in stems
   ]
   body = json.dumps({"requests": requests})
   too_many = len(requests) > MAX_REQUESTS_PER_BATCH
   too_big = len(body.encode()) > MAX_BATCH_BYTES

   if too_many or too_big:
      raise BatchTooLarge(f"{len(requests)} requests, {len(body.encode())} bytes")

   return requests


def estimated_cost(requests, model, expected_output_tokens=RESOLVE_MAX_TOKENS // 2):
   """The batch's cost at list price and at the batch discount, from a character count of the
   input and an expected output, so the discount is visible beside the undiscounted figure."""
   input_tokens = sum(
      (len(request["params"]["system"]) + len(json.dumps(request["params"]["messages"]))) / CHARACTERS_PER_TOKEN
      for request in requests
   )
   output_tokens = expected_output_tokens * len(requests)
   list_rates = price(model, False)
   batch_rates = price(model, True)

   def cost(rates):
      return (input_tokens * rates["input"] + output_tokens * rates["output"]) * USD_PER_MTOK

   return {"requests": len(requests), "list_usd": cost(list_rates), "batch_usd": cost(batch_rates)}


def answers_from_results(result_lines):
   """The answer text per item from a results JSONL, and the ids that errored or gave none."""
   answers = {}
   failed = []

   for line in result_lines:
      if not line.strip():
         continue

      result = json.loads(line)
      custom_id = result["custom_id"]
      outcome = result["result"]

      if outcome.get("type") != "succeeded":
         failed.append(custom_id)
         continue

      text = "".join(block.get("text", "") for block in outcome["message"]["content"] if block.get("type") == "text")
      has_answer = ANSWER_OPEN in text and ANSWER_CLOSE in text

      if not has_answer:
         failed.append(custom_id)
         continue

      answers[custom_id] = text.split(ANSWER_OPEN, 1)[1].split(ANSWER_CLOSE, 1)[0].strip()

   return answers, failed


def submit(requests, api_key, transport):
   """Send one batch. The caller supplies the transport; the operator's rule is that no paid call
   is made without first logging why the subscription could not do the work."""
   headers = {
      "x-api-key": api_key,
      "anthropic-version": "2023-06-01",
      "content-type": "application/json",
   }

   return transport(BATCHES_URL, headers, {"requests": requests})
