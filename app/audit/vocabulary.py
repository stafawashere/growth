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
queryable. dev_spend_cap_refused is the same class of event as budget_call_refused, one level up:
the persistent developer spend cap in app/providers/guard.py stops every role at once rather than
one role's daily cap, and is bounded the same way, one row per day rather than one per refused call.
dev_spend_ledger_reconcile_failed is a different failure than provider_result_unreadable: the
provider result read fine and the per-role budget row already settled against it, and it is only
the second store, the dev-spend ledger file, that failed on its own true-up read. Folding it into
provider_result_unreadable would misreport a working call as an unreadable one, so it gets its own
name, bounded the same way, one row per day.

Ruled 2026-09-27, when passwords replaced passkeys: the three passkey actions went, and five names
came in. account_created is the sign-up, the old passkey_registered with the credential gone.
login_failed_lockout is written once each time wrong passwords lock the account, with the count and
the lock deadline and nothing of the password. password_changed and password_reset_via_recovery are
09's recovery-code-used entry split by how the password was set. recovery_code_issued is the
operator's command line in app/auth/issue_recovery_code.py handing out a fresh code.

Added 2026-09-28 with the productive-failure opener: opener_gap_fail_open, because an opener due
for a concept with no published generation item is skipped rather than refused, the fail-open
twin of coverage_gap_fail_closed, and an operator needs the same queryable record of which concept
had nothing to open with. It is bounded the same way, one row per user, concept and day.

Added 2026-09-29 with the lessons layer (docs/plan/15-lessons.md, API, migrations, telemetry):
lesson_gap_fail_open, the lessons twin of opener_gap_fail_open, bounded one row per user, concept
and day; lesson_stale, written when ingest finds a record whose sources moved or whose ids went
inactive; lesson_signed_off, written when ingest first stores a signed_off version.

Added 2026-09-29 with the Today redesign (docs/pedagogy/today/design.md D4): due_skill_unserved,
a due skill block 1 leaves unserved with its reason, so the rulings on the block 1 cap and the
retrieval floor rest on counts. It is bounded one row per user, skill and day.

Added 2026-09-29 with the live tutor agent (docs/agent/architecture.md, "Guard, pacing, audit,
purge and export"): agent_reply_withheld, written when the output screen withholds a reply, bounded
one row per user and day, with the check that fired and the turn id; agent_memory_deleted,
agent_memory_edited, agent_memory_cleared and agent_conversation_deleted, written when the student
forgets, rewrites or clears what the tutor remembers or deletes a conversation; agent_memory_paused
and agent_memory_resumed for the student's pause switch; agent_consolidation_applied, one row per
consolidation job with the counts of applied and rejected proposals. None of them carries the text
of an entry, a turn or a proposal, only ids and counts.
"""
AUDIT_ACTIONS = (
   "account_created",
   "agent_consolidation_applied",
   "agent_conversation_deleted",
   "agent_memory_cleared",
   "agent_memory_deleted",
   "agent_memory_edited",
   "agent_memory_paused",
   "agent_memory_resumed",
   "agent_reply_withheld",
   "budget_call_refused",
   "budget_cap_changed",
   "budget_hard_stop",
   "claudebox_disabled",
   "claudebox_enabled",
   "content_snapshot_reloaded",
   "coverage_gap_fail_closed",
   "dev_spend_cap_refused",
   "dev_spend_ledger_reconcile_failed",
   "due_skill_unserved",
   "export_produced",
   "frq_image_deleted",
   "grading_rerun",
   "lesson_gap_fail_open",
   "lesson_signed_off",
   "lesson_stale",
   "login_failed_lockout",
   "opener_gap_fail_open",
   "password_changed",
   "password_reset_via_recovery",
   "provider_key_removed",
   "provider_key_rotated",
   "provider_key_set",
   "provider_result_unreadable",
   "purge",
   "reauth_established",
   "recovery_code_issued",
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
