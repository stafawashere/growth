"""Operator command-line report over the persistent developer spend cap.

Usage: python3 tools/dev_spend.py

app/providers/guard.py's GuardedProvider enforces the cap before every live call and reconciles
it after. This is a read-only reporter over the same DevSpendLedger, so the orchestrator can show
live spend against the operator's own Anthropic credit without importing the app. Never opens a
socket and never touches the ledger.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.providers.guard import DevSpendLedger, dev_spend_cap_usd


def report():
   spent = DevSpendLedger().spent()
   cap = dev_spend_cap_usd()
   remaining = cap - spent

   return spent, cap, remaining


def main():
   spent, cap, remaining = report()

   print(f"spent = {spent:.4f}")
   print(f"cap = {cap:.4f}")
   print(f"remaining = {remaining:.4f}")

   return 0


if __name__ == "__main__":
   sys.exit(main())
