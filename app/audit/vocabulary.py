"""The controlled vocabulary of audit_log actions.

docs/plan/09-security-and-privacy.md, "Audit log": each entry carries the action from a controlled
vocabulary. The plan states the vocabulary in prose, which controls it in the plan and not in the
code, where any string reaches the column and a typo becomes a row no query will ever find. This
module is the enumeration, and the three audit writers, app/auth/service.py's write_audit,
app/content/reconcile.py's entry writer and app/session/purge.py's, refuse anything outside it.

The list below is 09's Recorded sentence turned into names, so the phases that have not been
built yet do not hit a ValueError the day they are. Most of these have no call site in P1, which
is expected: tests/audit/test_vocabulary.py checks the direction that matters, that every action
the code writes is in the list, not that every listed action is written.

Six names are in the code and not in 09's prose. session_closed, because 09 names the session
established and a session that ends is the same class of event. reauth_established, because 09
does name a session established from a new authenticator. coverage_gap_fail_closed, because R18's
fail-closed gap needs a record an operator can query for what is missing from the bank.
budget_hard_stop and budget_call_refused, because 09 records a budget cap changed and a cap that
stops a role is the same class of event. provider_result_unreadable, because a call whose
accounting could not be settled against the provider's own usage block is the same class of event
as a cap that stops a role, and unlike an ordinary call it is rare by construction, so it cannot
flood the record. An ordinary provider call is not here at all: its
accounting lives in budgets, and a row per call would flood a record 09 describes as durable and
queryable.
"""
AUDIT_ACTIONS = (
   "budget_call_refused",
   "budget_cap_changed",
   "budget_hard_stop",
   "claudebox_disabled",
   "claudebox_enabled",
   "content_snapshot_reloaded",
   "coverage_gap_fail_closed",
   "export_produced",
   "frq_image_deleted",
   "grading_rerun",
   "passkey_recovery_used",
   "passkey_registered",
   "passkey_removed",
   "provider_key_removed",
   "provider_key_rotated",
   "provider_key_set",
   "provider_result_unreadable",
   "purge",
   "reauth_established",
   "review_queue_item_resolved",
   "session_closed",
   "session_established",
   "skill_merged",
   "skill_orphaned",
   "skill_rewritten",
   "zero_data_retention_changed",
)


def is_known_action(action):
   return action in AUDIT_ACTIONS
