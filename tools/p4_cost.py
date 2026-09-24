"""Cost per published generated item, with the batch discount visible (11 P4 exit criterion).

The bank was authored and re-solved offline in Claude Code sessions on the operator's subscription
(docs/operator/offline-authoring.md), so the API spend is $0.00. The same work bought on the API is
priced from tools/cost_model.py's per-call figures for the Claude-only routing: one template
authoring call per template attempt on the generator model and one blind re-solve per candidate on
the verifier model, at list price and at the Batch API's 50 percent discount.

Usage: python3 tools/p4_cost.py
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tools import cost_model

CONTENT = ROOT / "content"
REVIEW = CONTENT / "generation_review"
TEMPLATES = ROOT / "app" / "generation" / "templates"


def counts():
   published = len(list(CONTENT.glob("items_gen_*/ITM-GEN-*.json")))
   held = len(list(REVIEW.glob("*/ITM-GEN-*.json")))
   templates = len(list(TEMPLATES.glob("qa_*.py")))

   return {"templates": templates, "candidates": published + held, "published": published}


def api_equivalent(templates, candidates, batch):
   generator = cost_model.CLAUDE_ONLY_ROLE_MODELS["generator"]
   verifier = cost_model.CLAUDE_ONLY_ROLE_MODELS["verifier"]
   authoring_calls = templates * cost_model.TEMPLATE_ATTEMPTS
   authoring = authoring_calls * cost_model.role_cost("template", 1, writes=1, model=generator, batch=batch)
   resolving = candidates * cost_model.role_cost("verifier", 1, model=verifier, batch=batch, cached=False)

   return {"authoring_usd": round(authoring, 4), "resolving_usd": round(resolving, 4), "total_usd": round(authoring + resolving, 4)}


def report():
   measured = counts()
   published = measured["published"]
   list_price = api_equivalent(measured["templates"], measured["candidates"], batch=False)
   batch_price = api_equivalent(measured["templates"], measured["candidates"], batch=True)

   return {
      **measured,
      "api_spend_usd": 0.0,
      "api_spend_per_published_item_usd": 0.0,
      "api_equivalent_list": list_price,
      "api_equivalent_batch": batch_price,
      "per_published_item_list_usd": round(list_price["total_usd"] / published, 5) if published else None,
      "per_published_item_batch_usd": round(batch_price["total_usd"] / published, 5) if published else None,
      "template_attempts_assumed": cost_model.TEMPLATE_ATTEMPTS,
      "models": {
         "generator": cost_model.CLAUDE_ONLY_ROLE_MODELS["generator"],
         "verifier": cost_model.CLAUDE_ONLY_ROLE_MODELS["verifier"],
      },
   }


def main():
   print(json.dumps(report(), indent=1))

   return 0


if __name__ == "__main__":
   sys.exit(main())
