---
title: Build ledger
research_date: 2026-09-23
status: in_progress
purpose: Where the application build stands, session by session, so the next session can pick the next slice without rereading the plan.
---

# Build ledger

Application code lives at the repository root under `app/` and `tests/`, at the paths docs/plan names. The project CLAUDE.md still says "docs-only, no product"; that sentence is the operator's to amend and this ledger only records the conflict. Tooling: uv-managed Python 3.12.13 in `.venv/`, dependencies in `pyproject.toml`, tests via `.venv/bin/python -m pytest`. Every H2 below carries a tag because `qa/04_tags.py` scans root-level Markdown: [verified] means the test output or the registry was checked in the session named, [inferred] means a judgement.

## Overnight orchestration status, 2026-09-23 [verified]

The operator's overnight run stopped on its 10-slice limit. P1 to P3 cannot all be met without the
operator: gates 17, 29 and 30 and exit criterion 7 count only items with provenance `operator`, and
the key audit is a human verdict. Every commit below was pushed to `origin/main` only after the
orchestrator reran `.venv/bin/python -m pytest`, `npx vitest run`, `npx tsc --noEmit` and
`qa/12_report.py` in the same session, and each exited 0.

| Slice | Commit | What landed |
| --- | --- | --- |
| 0 | 8a046d0 | Session fourteen's 139 uncommitted files: export, progress and settings routes, security headers, the account client |
| 1 | db348bc | Persistent cumulative developer spend cap, $15.00, in `app/providers/guard.py`; `tools/dev_spend.py`; Opus 5.5 priced |
| 2 | 3a16d02 | Claude-only tier priced; one role-to-model table (`app/providers/model_routing.py`) pinned to `tools/cost_model.py` |
| 3 | 4b85ba3 | Stage example collects a graded answer and a rating; credited observation count; mastery path flake pinned |
| 4 | 4e4a527 | The 76 BC-PT records labelled for deterministic grading (48 deterministic, 28 model required); grader priced from it |
| 5 | cab28e1 | Rulings: retryable stream errors, passkey re-auth, audit sample enforcement, purge phrase, token CSS default, eval cadence |
| 6 | 8ca265d | 130 agent-drafted P1 items in `content/items_p1_agent/`, served by default, provenance names the model |
| 7 | 7acb7ee | Four shuffled options on every draft; SymPy bound alarm rearmed; missing audit sample refused with a 400 |
| 8 | 5162a79 | 360 distractor options re-derived against their named errors, 167 retagged or revalued |
| 9 | baecad3 | The 42 items whose distractors no held error produced were redesigned |
| 10 | 5691f56 | First live calls: Haiku 4.5 tutor cassettes, measured prompt tokens per model, cost per served item |

Tests at close: pytest collects 870 and exits 0; vitest 307 passed; tsc exits 0; qa 14 PASS, 0 FAIL;
`tools/check_items.py content/items_p1_agent` 130 clean.

Live spend: $0.0353 over seventeen claude-haiku-4-5 calls (see "Live API spend log"). The developer
cap reads spent 0.0353, cap 15.0000, remaining 14.9647. The key held $19.25 before the run, so about
$19.21 should remain on it.

Per-student projection, `tier.hundred_claude_only.cycle` in `tools/cost_model.py`: $92.95 to exam
day, inside the $50 to $100 target with $7.05 of headroom. Split, on the operator's 2026-09-23
instruction to use the Claude Code subscription wherever the terms allow: $52.14 stays on the API
key (`tier.hundred_claude_only.api_cycle`, runtime: tutor, grader, transcriber, diagnostician,
screen, evals) and $40.81, 43.90 percent of the tier, moves to offline Claude Code sessions at
$0.00 API spend (`tier.hundred_claude_only.offline_cycle`, template authoring and the verifier's
blind re-solve). See `docs/plan/14-token-economy.md` "Offline work on the operator's Claude Code
subscription" and `docs/operator/offline-authoring.md`. It rests on three things the operator
should know. The grader line uses the agent's determinism labels, which are [inferred]; if every
judged point needed a model the tier would be $128.95. The golden set 2 canary cadence was cut from
9 runs to 2 on the operator's delegated authority. Most role token figures are still characters
divided by 3.1, because only the tutor has a real template to measure. The measured tutor cost is a
median of $0.00206 per served item on Haiku, uncached because the 1,092-token prefix is under
Haiku's 4,096 cache minimum; the same tokens on the assigned Sonnet 5 with the 1-hour cache price at
a $0.00157 median, so the tutor stays on Sonnet 5.

Open for the operator, in order of what unblocks most:

1. Review the 130 drafts in `content/items_p1_agent/`, including the judgment calls listed in Known
   defects (twenty-sixth session entry), and author or approve the operator-provenance items gates
   17 and 30 need. Only the operator may relabel a draft `operator`.
2. Draw the 100-item key audit sample (`tools/draw_key_audit_sample.py`) over operator items and
   record verdicts, for gate 29 and exit criterion 4.
3. Approve or change the eval cadence ruling and the `CHARACTERS_PER_TOKEN` replacement in 14.
4. The fixture items in `tests/session/test_serve_format.py` have no options, so a server guard that
   never serves MCQ without options would turn them red; a ruling on those fixtures unblocks the guard.

Recommended next slice: P2 review mode and FSRS scheduling with `test_desired_retention_switch`,
replay only, since the P1 gates still open are the operator's and the engine needs a finite due
queue to teach from now to May 2027.

## Done [verified]
- 2026-09-23, Slice 2 of the subscription backend: live validation, latency, Slice 1's three
  defects closed, and the runtime cost lines moved to $0.00 API on the subscription backend.
  Defect a: `app/providers/guard.py` gains `SubscriptionPacingCaps`, `SubscriptionPacingLedger`
  (`var/subscription_pacing.json`, locked like the dev ledger) and `SubscriptionPaceExceeded` (a
  `BudgetStopped`); `GuardedProvider(subscription_pacing=...)` counts the call against a per-role
  daily call cap and a per-minute rate instead of the per-role dollar and token caps, never touches
  the budgets row, still sets `last_accounting`, releases the slot on a `RefusedBeforeWire`, and
  audits a pacing refusal once per role, day and cap. Defaults tutor 60 a day, other roles 20, 4 a
  minute per role, set by `GROWTH_SUBSCRIPTION_<ROLE>_CALLS_PER_DAY` and
  `GROWTH_SUBSCRIPTION_CALLS_PER_MINUTE` (`app/main.py` `build_subscription_pacing`, a bad value
  stops startup), wired through `Settings.subscription_pacing` into `app/api/routes/sessions.py`.
  The $15.00 dev cap is untouched. Defect b: `app/main.py` `refuse_the_legacy_paid_switch` stops
  startup when `GROWTH_TUTOR_PROVIDER=anthropic` or `GROWTH_TUTOR_PROVIDER=api` is set without
  `GROWTH_AI_BACKEND=api`, naming the variable to set; `none` and `replay` still work. Defect c: `app/feedback/drain.py` and
  `tools/drain_subscription_queue.py` retry due `provider_call_queued` jobs through the backend
  `build_tutor` builds (subscription or api only, never replay or none), under the same guard,
  store the sentence on `attempt.tutor_sentence` where `compose_sentence` reads it first, mark the
  job done, re-queue a still-limited job 30 minutes later and stop without counting an attempt,
  stop cleanly on a pacing, budget or developer spend cap stop, fail a job after 3 other
  failures, and fail a job without a call when its attempt or session is already at the tutor
  ceiling (3 per item, 20 per session, `tutor.ceiling_reached`). `app/feedback/tutor.py` gains `request_from_messages` for the rebuild. Live
  validation: `tools/subscription_smoke.py` (new) ran 27 calls against the real CLI 2.1.277 on the
  keychain login (Live API spend log). The Slice 1 argv was accepted as built. The CLI's default
  thinking made one Haiku tutor call take 60.3 s and 6,176 output tokens, so
  `app/providers/subscription.py` now maps `thinking: disabled` to a fixed `MAX_THINKING_TOKENS=0`
  in the subprocess environment and `output_config.effort` to `--effort`, both accepted by the CLI.
  Measured tutor latency (wall, n=10 each): Haiku 4.5 median 3.03 s, p90 3.16 s; Sonnet 5 median
  3.72 s, p90 4.32 s, under the 10 s line. API latency is unknown (no cassette or ledger entry
  recorded one). Cost: `tools/cost_model.py` emits
  `tier.hundred_claude_only.subscription_backend_api_cycle` = $0.00,
  `subscription_runtime_notional` = $52.14 (the `api_cycle`, kept as the fallback),
  `runtime_lines_without_evals` = $29.27, `target.per_student_low` and `dev_spend.cap`; projected
  API cost per student to exam day on the subscription backend is $0.00 against the $50 to $100
  target. `docs/plan/14-token-economy.md` "Runtime calls on the operator's subscription" rewritten
  with the backend cost table, the latency table and the pacing sizing; the tier table gains the
  $0.00 row. `docs/plan/07-ai-provider-layer.md` and `docs/operator/provider-key.md` (switching
  backends, where the token goes, draining) updated. Tests added:
  `tests/providers/test_subscription_pacing.py` (5), `tests/api/test_subscription_drain.py` (11),
  two in `tests/api/test_subscription_limit.py`, two in `tests/providers/test_subscription.py`,
  six in `tests/api/test_wiring.py` (one parametrized over three backends), two in
  `tests/tools/test_cost_model.py`. Each was shown red against a mutation of the code it guards
  (21 mutations from a scratchpad script: pacing ignored, no minute rate, no daily cap, release a
  no-op, the route unpaced, the legacy switch allowed, the pacing environment ignored, the drain
  not storing, retrying at once, continuing past a limit, unpaced, the tool draining replay, the
  tool unpaced, a limit wait counted as a failed attempt, the developer spend cap uncaught, the thinking variable dropped, effort dropped, the host thinking value copied, the
  evals left on the API, the screen dropped from the runtime lines, and the quoted dev cap
  changed), one or more tests red each, then green on restore. Suite at close: pytest 936 passed (exit 0), vitest 310 passed, tsc exit 0, qa/12_report.py exit 0.
- 2026-09-23, Slice 1 of the subscription backend: the AI engine runs by default on the
  operator's Claude subscription through the official Claude Code CLI, and the paid key is a
  fallback chosen only explicitly. `app/providers/subscription.py` (new) `SubscriptionProvider`
  runs one `claude -p` per call from an argument list, never a shell: `--model` from the request,
  `--system-prompt=<static prefix>`, `--output-format json`, `--json-schema` when the request
  carries a schema, `--max-budget-usd` per role (tutor 0.10, others 0.25),
  `--no-session-persistence`, `--setting-sources ""`, `--strict-mcp-config` with an empty
  `--mcp-config`, `--disable-slash-commands`, `--permission-prompts none`, `--tools ""` and a named
  `--disallowedTools` list, with the user prompt on stdin and the working directory an empty temp
  directory removed afterwards. Every flag was checked against `claude -p --help` on CLI 2.1.277;
  `--bare` and `--max-turns` are not used. The subprocess environment is `PATH`, `HOME`, `USER`,
  `LANG`, `TMPDIR` and the operator's OAuth token when set, and never an `ANTHROPIC_*` variable.
  The JSON result maps onto `ProviderResult` (`result` or `structured_output`, the four usage
  counts, `total_cost_usd`, `duration_ms`, `subtype`), and `total_cost_usd` goes to
  `app/providers/guard.py` `SubscriptionSpendLedger` (`var/subscription_spend_ledger.json`), never
  to the $15.00 `DevSpendLedger`. A usage-limit answer raises `SubscriptionLimitReached`; a
  timeout, a non-zero exit or non-JSON output raises `SubscriptionTransportError`, and a missing
  binary raises `SubscriptionBinaryMissing`, which is refused before the wire. Compliance:
  `AnthropicProvider` refuses an `sk-ant-oat` key before the wire (`SubscriptionTokenRefused`);
  only `subscription.py` in `app/` names the token variable and it imports no HTTP client, socket
  or SDK; the backend refuses to construct over a database with more than one user
  (`app/main.py` `installed_user_count`, read-only); registration already refuses a second account
  unconditionally. `app/main.py` adds `GROWTH_AI_BACKEND` (`subscription` default, `api`,
  `replay`, `none`) as the primary switch, with `GROWTH_TUTOR_PROVIDER` read only when it is
  unset, and logs the choice. Degradation: `app/feedback/tutor.py` queues a limited call through
  `app/providers/call_queue.py` (new) as a `provider_call_queued` row in the existing `jobs` table,
  one per attempt, and re-raises; `app/api/routes/sessions.py` serves the static feedback with
  `tutor_unavailable` true. Docs: new sections in `docs/plan/07-ai-provider-layer.md` ("The
  subscription backend") and `docs/plan/14-token-economy.md` ("Runtime calls on the operator's
  subscription"), and `docs/operator/provider-key.md` and `ai-operating-costs.md` now name
  `GROWTH_AI_BACKEND`. No cost figure changed. Tests: `tests/fixtures/fake_claude/claude` (a fake
  CLI that records argv, stdin, environment and working directory, with success, structured,
  weekly-limit, five-hour-limit, malformed and non-zero modes, configured through `HOME`);
  `tests/conftest.py` (new) fails any test that resolves a claude binary outside
  `tests/fixtures` and points the subscription ledger at a temp file;
  `tests/providers/test_subscription.py` (15), `tests/providers/test_subscription_compliance.py`
  (11), `tests/api/test_subscription_limit.py` (4) and six new backend-selection tests in
  `tests/api/test_wiring.py`. Each new test was shown red against a mutation of the code it
  guards (32 mutations, one or more tests red each, run from a scratchpad script), then green on
  restore. Suite at close: 909 passed. No live CLI or API call.
- 2026-09-23, a verified review finding against Slice 1 of the subscription backend:
  `tests/providers/test_subscription.py`
  `test_the_reported_cost_lands_on_the_subscription_counter_and_never_on_the_api_cap` built a
  `DevSpendLedger` at a fresh temp path that nothing ever wrote to, so its "never on the API cap"
  half could not go red. The test now points `app/providers/guard.py` `DEV_SPEND_LEDGER_PATH` at a
  temp file (with a positive control that `DevSpendLedger()` resolves there), runs two calls and
  asserts the default ledger is still empty and its file absent. The provider-level test cannot
  see the route wiring, so `tests/api/test_subscription_limit.py` gained
  `test_a_served_subscription_sentence_is_counted_off_the_api_dev_cap`, which serves a real
  sentence through `/sessions/.../feedback` over the same redirected ledger and asserts the
  subscription counter holds 0.0123 and the API cap ledger is untouched. Red against two
  mutations: `SubscriptionProvider._record_cost` also adding to `DevSpendLedger()` (both tests
  red) and `sessions.py` passing `dev_spend_track=True` (the route test red, `0.00418 == 0.0`);
  green on restore. No application code changed. Suite at close: 910 tests collected, pytest
  exit 0 with no failure. No live CLI or API call.
- 2026-09-23, a second review finding against Slice 1 of the subscription backend:
  `app/settings/providers.py` `PROVIDER_NAMES` had no entry for the new default backend, so
  `GET /settings/providers` reported the tutor as the class name `SubscriptionProvider` instead
  of `subscription`. `PROVIDER_NAMES` now maps `SubscriptionProvider` to `subscription`, and
  `tests/api/test_settings_routes.py` gained
  `test_providers_names_the_default_subscription_tutor_by_its_backend`. Red with the map entry
  removed, green on restore. Suite at close: pytest 911 passed, vitest 310 passed, tsc exit 0,
  qa/12_report.py exit 0. No live CLI or API call.
- 2026-09-23, a verified review finding against the MCQ math-rendering fix below: the `stem`
  fix in `app/items/ingest.py` `item_row` only reaches a record on its first ingest.
  `ingest_new_records` (`app/runtime/bank.py` `ItemBank._ingest_pending_source`) skips any id
  already in `items`, so a row ingested before the fix keeps serving its `{"text": ...}` wrapper
  forever; restarting the app over the operator's persistent database would not touch it. Fixed
  with a startup data repair rather than a one-off SQL script, since nothing else in this
  codebase re-ingests: `app/db/migrate.py` `repair_wrapped_stems` selects the rows whose `stem`
  looks JSON-wrapped (`LIKE '{%'`), unwraps the ones that parse to `{"text": <string>}`, and
  leaves everything else (a legitimate stem that happens to start with `{`, or one that starts
  with `{` but is not valid JSON) untouched; `app/db/models.py` `make_engine` calls it right after
  `apply_additive_migrations`, so it runs once per process start and is a no-op once every row has
  been unwrapped. Tests: `tests/db/test_migrate.py` gained
  `test_repair_wrapped_stems_unwraps_a_row_ingested_under_the_old_code` (a wrapped row, a plain
  row and a row that merely starts with `{` but is not JSON, asserting only the wrapped one
  changes) and `test_repair_wrapped_stems_is_idempotent`; both proved red (`ImportError: cannot
  import name 'repair_wrapped_stems'`) against the pre-fix `app/db/migrate.py` and
  `app/db/models.py`, restored, then green. `.venv/bin/python -m pytest -q -p no:cacheprovider`
  exits 0. No live Anthropic API call.
- 2026-09-23, MCQ options no longer render raw MathJSON. `McqControl.tsx` typesets each option's
  `mathjson`/`value` (a bare number, symbol or an expression tree such as
  `["Add", ["Multiply", -5, ["Sin", "x"]], 3]`) through `mathlive`'s `convertMathJsonToLatex` and
  KaTeX's `renderToString` (`app/web/src/math/mathjson.ts`, `MathValue.tsx`, new); the typeset
  markup is `aria-hidden`, and a `convertLatexToAsciiMath` rendering carries the accessible name in
  a `.visually-hidden` span instead, so radio semantics, keyboard use and focus styling are
  untouched. `Item.tsx`'s stem and worked-solution steps, which some curated items carry with
  inline `\( \)`-delimited LaTeX, now route through the same pattern via `MathText.tsx` (new); an
  agent-drafted item's plain-text stem with no delimiters renders exactly as before. `mathlive`
  needs the compute engine loaded before `convertMathJsonToLatex` works, so
  `@cortex-js/compute-engine` (already a transitive dependency) joined `package.json` directly.
  `ServedOption.value` is now typed `unknown` in `api/types.ts`, matching what the server actually
  sends, not `string`. Fixed in the same pass: `app/items/ingest.py`'s `item_row` was storing
  `json.dumps(record["stem"])`, the whole `{"text": ...}` wrapper, into the `stem` column, so every
  served item's stem was the literal JSON string, not the plain text; it now stores
  `record["stem"]["text"]`. `docs/operator/items.md` corrected: `violated_step` indexes the
  archetype's own `expected_solution_path` (`app/feedback/render.py` `violated_step_index`), not
  the item's `worked_solution`, and `options` may sit on a `short_answer` item for the turns
  `format_for_attempt` serves it as `mcq`. Tests: `McqControl.test.tsx` gained a MathJSON-array
  option case (red on `option.label ?? option.value ?? option.id` rendered as a plain string,
  green after; the assertion was tightened once, from checking the raw LaTeX source never appears
  anywhere in the DOM to checking it never appears in the visible `.katex-html` node, since KaTeX's
  own MathML annotation legitimately carries the LaTeX source hidden from sighted users). `math/
  MathText.test.tsx` (new) covers both the agent-drafted plain-text case and the `\( \)`-delimited
  case, each proven red on a stub `MathText` and green after. `tests/items/test_ingest.py` gained
  a stem-shape test, red on the old `json.dumps` line and green after. `.venv/bin/python -m pytest
  -q -p no:cacheprovider` exits 0; `npx vitest run` exits 0, 310 tests; `npx tsc --noEmit` exits 0;
  `qa/12_report.py` exits 0, 14 PASS. Verified live: a session driven through
  `tests/fixtures/items_p1/` to an `mcq`-stage item (`ITM-SYN-02002-02`, option A
  `["Multiply", 8, "x"]`) served the fixed stem and options over HTTP; a browser build of the real
  `McqControl`/`MathText`/`mathjson.ts` source against that served JSON showed `8x`, `0`, `4`, `8`
  as typeset options with no `Multiply` or bracket text anywhere. `GET /progress` would not answer
  within 45s against that same seeded state even in isolation, unrelated to this fix and not
  investigated further; see Known defects. No live Anthropic API call.
- 2026-09-23, independent item review of `content/items_p1_agent/` applied and re-checked. The
  review judged all 130 items: 65 approve, 57 fix, 8 reject, 0 wrong keys. Applying it changed 65
  item files, by archetype 01004 8, 01008 3, 01015 10, 02002 5, 02006 1, 02007 6, 02008 3,
  02010 8, 02011 3, 03001 2, 03004 4, 03005 8, 03008 4. A separate agent per archetype then
  re-solved the changed items blind, confirmed every key with SymPy and re-derived every
  distractor from its tagged error, and corrected 8 items: `01004-06` (new stem, key -1 no longer
  the only negative), `01008-08` (options reordered, key to D, breaking a run of three B keys),
  `02010-05` (new stem, key no longer the smallest and no option alone in form), `02011-01` and
  `02011-09` (redesigned so the `BC-ERR-02028` sign drop is literal), and `03005-00`, `03005-06`,
  `03005-09` (constants changed so the key is interior; key extreme in 4 of 10 03005 items, down
  from 7). 01015, 02002, 02006, 02007, 02008, 03001, 03004 and 03008 needed no correction. Every
  re-check agent's `tools/check_items.py` run exited 0. After the pass, `.venv/bin/python
  tools/check_items.py content/items_p1_agent` exits 0 with "records read: 130", "clean: 130",
  "with violations: 0" and 10 items in each of the 13 archetypes, and `.venv/bin/python -m pytest
  -q -p no:cacheprovider tests/tools tests/items tests/e2e` exits 0 with 162 dots and no F or E
  (the doubled `-q` suppresses the summary line). Operator sign-off is still pending for all
  130. What remains is under Known defects, twenty-sixth session.
- Twenty-eighth session, 2026-09-23, a verified review finding against the twenty-seventh
  session's runbook: `docs/operator/offline-authoring.md` step 2 had the blind re-solve agent
  compare its own key against the drafted key, which required handing the drafted key to that
  agent and broke `docs/plan/13-ai-engineering.md` line 14, "the verifier never sees the key."
  Step 2 now has the re-solving agent write its own key and worked solution to a file of its own,
  never given the drafted key, and a script, not the agent, reads both files and compares the two
  keys; the step no longer contradicts its own claim that the deterministic checks around the
  verifier are unchanged. Docs-only change, no code touched.
- Twenty-seventh session, 2026-09-23, offline work on the operator's Claude Code subscription:
  `tools/cost_model.py` gained a Claude-only offline split, `tier.hundred_claude_only.api_cycle`
  ($52.14, the tutor, grader, transcriber, diagnostician, screen and evals, all of which stay on
  the API key) against `tier.hundred_claude_only.offline_cycle` ($40.81, 43.90 percent of the
  $92.95 tier, template authoring and the verifier's blind re-solve, both moved to Claude Code
  sessions at $0.00 API spend). Evals do not split: golden set 1 already costs $0.00 on the
  template gate, and golden sets 2 and 3 grade the production grader and transcriber prompts on
  their production model, so both stay on the API key in full. `docs/plan/14-token-economy.md`
  gained "Offline work on the operator's Claude Code subscription" with the Agent SDK quickstart
  and Claude Code authentication quotes and URLs, and the $100 tier table's Total row gained two
  "of which" lines. `docs/operator/offline-authoring.md` is the new runbook, describing the
  one-agent-per-archetype author, independent blind re-solve, and `tools/check_items.py` gate
  shape the twenty-sixth session actually ran, and naming the rolling five hour and weekly
  subscription limits as the pacing risk. `tests/tools/test_cost_model.py` gained
  `test_claude_only_tier_splits_into_runtime_api_and_offline_claude_code_lines`, run red against
  the pre-edit `tools/cost_model.py` (`KeyError:
  'tier.hundred_claude_only.offline_template_line'`) and green after, restored via `git stash`
  around the code edit alone so the test file's addition was never itself reverted. All four
  checks quoted: `.venv/bin/python -m pytest -q -p no:cacheprovider` exit 0 (870-plus collected,
  no FAILED lines, the doubled `-q` from `addopts` suppresses the summary line);
  `npx vitest run` 307 passed, exit 0; `npx tsc --noEmit` exit 0; `qa/12_report.py` exit 0.
  `python3 tools/cost_model.py --check docs/plan/13-ai-engineering.md
  docs/operator/ai-operating-costs.md docs/plan/14-token-economy.md` prints "0 unknown dollar
  figures" for all three and exits 0. No live Anthropic API call was made.
  `content/items_p1_agent/` and `app/web/` were not touched by this session; both showed unrelated
  concurrent changes in `git diff` during the session, from other work in progress on this
  repository, not from anything this session wrote.
- Twenty-sixth session, 2026-09-23, distractor repair: nine archetypes' open audit findings were
  repaired one agent per archetype, 42 items in all. 39 stems were redesigned so that every
  distractor is a single application of an error the archetype's skills hold (01004 5, 01008 7,
  01015 1, 02007 2, 02008 8, 03001 5, 03004 2, 03005 7, 03008 2), with keys, worked solutions and
  `parameter_draw` rewritten to match and every key letter left in place. Three more `BC-QA-03004`
  options that held a free `dydx` (`03004-00` B, `03004-08` B, `03004-09` A) were re-derived as
  numeric or closed-form `BC-ERR-03007` and `BC-ERR-03008` values, and `03004-03` A was rechecked
  and left unchanged. Each agent checked its keys against a blind SymPy solve and every option
  pair with `compare_expressions`. A spot check solved 8 randomly chosen repaired items by hand and
  with SymPy (`03001-02`, `03008-07`, `01004-05`, `02008-07`, `02007-04`, `02008-08`, `01008-02`,
  `01008-04`): all 8 keys matched and all 24 distractors equal their tagged error's computation,
  so nothing was changed. `.venv/bin/python tools/check_items.py content/items_p1_agent` exits 0
  with "records read: 130" and "clean: 130", 10 items in each of the 13 archetypes, and
  `.venv/bin/python -m pytest -q -p no:cacheprovider tests/tools tests/items tests/e2e` exits 0
  with 171 dots and no failures (the doubled `-q` from `addopts` suppresses the summary line).
  What the repair left open is under Known defects.
- Twenty-sixth session, 2026-09-23, distractor audit: the twelve archetypes in
  `content/items_p1_agent/` other than `BC-QA-02010` (re-derived last session) were audited one
  agent per archetype, 30 distractor options each, 360 in all. Each agent re-derived every
  distractor from the archetype's own named errors (the BC-ERR ids its skills hold) and either
  corrected the value, the `violated_step`, or the tag, or left the option unchanged and said why.
  No key changed, and the 03005 auditor rechecked all ten of its keys with SymPy. Options fixed and
  left unresolved, per archetype: 01004 11 and 2, 01008 6 and 10, 01015 11 and 1, 02002 9 and 0,
  02006 12 and 0, 02007 21 and 3, 02008 12 and 11, 02011 18 and 0 (plus `violated_step`
  normalized to 1 on the already-correct options of items 00 to 05), 03001 9 and 6, 03004 25
  and 2, 03005 15 and 4, 03008 18 and 3. That is 167 fixed and 42 unresolved of 360; the rest were
  already correct. Each auditor's `tools/check_items.py` run exited 0. After all twelve,
  `.venv/bin/python tools/check_items.py content/items_p1_agent` exits 0 with "records read: 130,
  clean: 130, with violations: 0", and `.venv/bin/python -m pytest -q -p no:cacheprovider
  tests/tools tests/items tests/e2e` exits 0. `var/growth.db` holds no `ITM-AGT-` rows (its items
  table is empty), so the bank's skip-existing-ids rule leaves no stale copy of an edited item and
  nothing was deleted. What the audit could not fix is under Known defects.
- Twenty-fifth session, 2026-09-23, slice 7 review follow-up: two verified findings against the
  twenty-fourth session's distractor generator, fixed. First, the generator always placed the key
  at option A for the 51 previously options-less items and only ever moved a fourth distractor to
  D for the 31 three-option items, so the key sat at A 67 times against 29, 23 and 11 for B, C and
  D across the 130 items; a student could score short-answer-turned-MCQ items by picking A with no
  regard for the item. Every item's option order is now a deterministic per-item shuffle
  (`hashlib.sha256(item id)` seeding `random.Random`, one script run, not committed, since it is a
  one-shot content fix like the generator it corrects), re-lettered A to D by the shuffled
  position; the key now sits at A 32, B 36, C 28, D 34. `tools/check_items.py content/items_p1_agent`
  still exits 0, 130 clean, and
  `tests/tools/test_agent_drafts_have_four_options.py`'s two tests still pass, since neither reads
  option order. Second, `ITM-AGT-02010-08`'s option B held `sin theta/cos^2 theta`, the item's own
  undifferentiated step-1 rewrite, tagged `BC-ERR-02025` ("cofunction derivative given without its
  negative sign"), and option C held the key's exact negation tagged `BC-ERR-02026` ("trigonometric
  quotient differentiated term by term"); neither value is a computation either error actually
  produces. Re-derived both with SymPy from the item's own quotient-rule work (`u = sin theta`,
  `v = cos^2 theta`): B is now the quotient rule with the denominator derivative's sign dropped,
  `sec theta - 2 sec theta tan^2 theta`; C is now the literal term-by-term quotient `u'/v'`,
  `-1/(2 sin theta)`. `ITM-AGT-02010-07` carried the identical pattern (option B equal to its own
  step-1 rewrite tagged `BC-ERR-02025`, option C equal to the negated key tagged `BC-ERR-02026`)
  and was fixed the same way (`6 - 6 tan^2 x + sec x tan x` and `-6/tan x`). Both items' distractor
  `violated_step` now indexes `BC-QA-02010`'s `expected_solution_path[1]` ("apply the quotient
  rule"), where the sign-drop and term-by-term errors actually happen, rather than the previous 0
  or 3. `ITM-AGT-02010-00` and `-01` held two further `BC-ERR-02025` distractors apiece
  (`violated_step: 1`) whose values were correct as sign flips on one term of the final split-form
  key, the CED-literal reading of "given without its negative sign", but that sign only appears at
  `expected_solution_path[3]` ("write the result in the requested trigonometric form") in those two
  items' own worked solutions, not at the quotient-rule step; `violated_step` corrected from 1 to 3
  on those four options, values unchanged. All four values checked distinct from the key and from
  each other with `sympy.simplify`, and the full `BC-QA-02010` archetype's ten items re-verified
  against a general quotient-rule/sign-drop/term-by-term SymPy model built from each item's own
  `worked_solution` Divide step; no further mismatches found in that archetype.
  `tools/check_items.py content/items_p1_agent` exits 0, 130 clean, after these edits.
- Twenty-fourth session, 2026-09-23, slice 7: every one of the 130 agent drafts in
  `content/items_p1_agent/` now carries exactly four options (one key, `error_path: null`, plus
  three distractors, each a BC-ERR id held by the archetype's own skills with a `violated_step`
  index into that archetype's `expected_solution_path`), closing the options-less and
  three-option gaps the twenty-third session left in Known defects. `tools/check_items.py
  content/items_p1_agent` exits 0, 130 clean. The 48 items the previous session already gave four
  options were left untouched; the 31 three-option and 51 zero-option items were filled by a
  generator (its source is not part of this repo, since it is a one-shot authoring tool and not a
  gate). Every added distractor's value is either a genuine intermediate quantity from the item's
  own `worked_solution` (a value a student really reaches partway through the correct derivation,
  used prematurely as the final answer) or an algebraic sign flip, dropped multiplicative factor,
  or off-by-one integer count taken from the item's own key expression, and every one is checked
  distinct from the key and from every other option by `app/items/verify.py`'s own
  `compare_expressions` (SymPy symbolic difference, then a 7-point numeric probe) before being
  written, the same machinery `distractor_path_violations` runs at gate time. Where an archetype
  holds more error ids than an item needed new distractors for, an error id already used by that
  item's pre-existing distractors was reused for the generic sign-flip or count-perturbation
  candidates rather than invented; one id, `BC-ERR-01008` ("indeterminate form read as the answer
  zero"), is restricted in the generator to the one candidate that is literally that reading (the
  worked solution's own step-zero value), because nothing else can honestly carry that name. The
  reused-id distractors are mechanically verified (distinct, valid error id, valid step index) but
  were not each individually hand-checked for being the most natural instance of that named error
  the way the original 48 items' distractors were; this is flagged below for operator review.
  `tests/items/test_ingest.py::test_a_short_answer_item_carrying_mcq_options_still_ingests` (new,
  red under a temporary guard that refused options on a `short_answer`-format record, green with
  the guard removed) confirms `app/items/ingest.py` already accepted options on a short_answer
  item without any change, since nothing in that module reads the `format` field at all; the
  operator's contingency instruction to change ingest did not apply.
  `tests/tools/test_agent_drafts_have_four_options.py` (new) reads the real directory and asserts
  every record carries exactly four options, one key with a null `error_path` and three
  distractors each with one, since `tools/check_items.py`'s own checks pass an item with fewer
  options or none (they check whatever option set is actually there, which is why that gate alone
  did not catch the twenty-third session's options-less items); red with one record's options cut
  to two, green restored.
- Twenty-fourth session, 2026-09-23: `app/items/verify.py` `run_bounded`'s SIGALRM path could
  silently miss its own bound. A one-shot `signal.setitimer` that fires while a `gc.callbacks`
  hook is executing (the suite registers one only once something imports `hypothesis`, which is
  why this never reproduced from `tests/items/test_verify_bound.py` run alone) never reaches
  `run_bounded`'s `except _Timeout`: CPython's gc module catches whatever a callback raises and
  reports it through `sys.unraisablehook` instead of letting it propagate, so the alarm is lost
  and the comparison runs to completion past `timeout_s`. Seen directly in a full-suite run as
  `test_a_pathological_comparison_on_the_main_thread_is_unsettled_within_the_bound` failing with
  `not_equivalent` instead of `unsettled`, plus a `PytestUnraisableExceptionWarning` naming
  `app.items.verify._raise_timeout` raised from inside `hypothesis`'s `gc_callback`. Reproduced
  deterministically outside the full suite by wrapping `_raise_timeout` to swallow exactly its
  first delivery (mimicking that gc behaviour) and calling `run_bounded` over a busy-loop:
  the pre-fix single-shot `setitimer` let the loop run to completion (one alarm delivered, zero
  effect); the fix, a repeating `setitimer(..., timeout_s, min(0.05, timeout_s))`, still returned
  the timeout sentinel because a second delivery landed outside the callback 0.05 s later. The
  test's margin assertion was briefly switched to `time.process_time()`; the orchestrator
  reverted that because CPU time weakens a wall-clock bound, so the test still measures
  `time.monotonic()`. Proof run: 20/20 green on `tests/items/test_verify_bound.py` alone (both before and
  after the real fix, since the file-alone run never touched hypothesis's callback), and three
  full-suite runs, all exit 0, zero failures. The exact race reproduced again live in the second
  of those three runs, the same `gc_callback`/`_raise_timeout`/`PytestUnraisableExceptionWarning`
  as the original symptom, and the fix carried the test through it.
- Twenty-fourth session, 2026-09-23: `app/api/app.py` `Settings.resolve_key_audit_sample_ids`
  raised `FileNotFoundError` (HTTP 500 through `POST /review-queue/{id}/resolve`) when
  `GROWTH_KEY_AUDIT_SAMPLE_PATH` named a file that did not exist, and used
  `item_id in set(sample_ids)` for membership, which reads a dict's keys or a string's characters
  when the sample file's JSON was not a list, rather than refusing it. Both now fail closed with
  a `ValueError`, which the route already turns into the documented 400
  (`tests/api/test_review_routes.py::test_resolving_an_item_audit_with_a_missing_sample_file_is_refused_not_500`
  and `..._with_a_non_list_sample_file_is_refused_not_500`, both new, red against the pre-fix code
  (`FileNotFoundError` propagating unhandled, and a 200 from the dict-keys membership check),
  then green).
- Twenty-third session, 2026-09-23, serving the agent-drafted P1 items under the operator's
  ruling and keeping them out of every operator count. `content/items_p1_agent/` holds 130 drafts,
  10 per P1 archetype, each with `"authored_by": "claude-opus-5-5 agent draft, pending operator
  review"`, audited by an independent agent's blind re-solve on 2026-09-23 (its README says what
  was corrected). `app/items/ingest.py` `provenance_model` now reads `authored_by`: absent gives
  `operator` as before, present gives that string, and `is_operator_authored` is the one test for
  operator provenance (test_an_agent_draft_keeps_its_author_as_the_provenance_model, red
  `assert 'operator' == 'claude-opus-5-5 agent draft, pending operator review'`, then green).
  `tools/check_items.py` prints a second table, operator-authored items per archetype, which is
  the one exit criterion 7 and gates 17 and 30 read. `tools/draw_key_audit_sample.py` draws only
  operator items, and fixing that exposed two older defects that meant it could never draw
  anything. It filtered on status `published`, which ingest never writes, because the bank's
  published status is `verified`. It also read `archetype["unit"]`, which archetype records do
  not carry, so it raised `KeyError: 'unit'`. It now uses `PUBLISHED_STATUS` and `primary_unit`.
  `tests/tools/test_agent_drafts_uncounted.py` puts one operator item and one agent draft side by
  side. It went red with both filters removed (`assert 2 == 1` and a sample holding both ids),
  then green. Gates 17, 29 and 30 still have no test function (gate_status: missing), so nothing
  there counted the drafts. `tools/gate_status.py` counts gate tests, not items, and needed no
  change. The app now loads a bank directory. `GROWTH_ITEMS_DIR` (`app/main.py`) defaults to
  `content/items_p1_agent` when that directory exists, `none` turns it off, and a set path that is
  not a directory stops startup. `app/runtime/bank.py` `ItemSource` goes through
  `ingest.ingest_new_records` on the bank's first query, which skips ids already in items. It
  runs then and not at build time because the checks take about 12 s over 130 records and most
  application builds (the API wiring tests among them) never open a session.
  `tests/e2e/conftest.py`'s gate 23 world sets `GROWTH_ITEMS_DIR=none`, so gate 23 still serves
  only its own `ITM-SYN` fixtures. `tests/e2e/test_agent_drafts_served.py` builds the app with the
  variable unset, registers, and drains sessions with the replay tutor until a `BC-UNIT-02` item
  is served. It answers that item, rates it, reads its feedback, and checks that the stored
  provenance model is the agent author. It went red with the default made `None`, then green.
  `tools/check_items.py content/items_p1_agent` exits 0 with 130 clean and 10 per archetype.
- Slice 4, twentieth session, 2026-09-23, the BC-PT deterministic labelling pass and bringing the
  Claude-only tier's overrun down. `data/bc_pt_determinism_labels.json` carries one `[inferred]`
  label per active BC-PT record, `deterministic` or `model_required`, with a short reason read
  against the record's own `earns`, `does_not_earn`, `notation_requirements` and `precision_rules`
  text and against the four checks and partition rule in `docs/plan/03-diagnosis-and-feedback.md`.
  48 of 76 are `deterministic`, 28 `model_required`, 17 of them on `justification_required`,
  `interpretation_required` or `hypotheses_required` alone and 11 more on the earns text itself (a
  prose-only earn criterion, a graphical criterion, an implied choice, a step count, or a label
  naming a quantity in words). A separate data file was used rather than
  `data/staging/*.json` and `tools/merge_staging.py`, because that tool fully replaces a matched
  record rather than merging fields, and re-authoring all 76 rich, sourced `scoring_points.json`
  records through a staging file to add one field risked corrupting or silently dropping sourced
  content the labelling pass did not touch; the label is also a judgement about the grader's
  design, not a fact about the rubric the registry otherwise records. `qa/15_determinism_labels.py`
  asserts every active BC-PT record carries exactly one label with a reason and that the file and
  the registry agree on the id set; verified red on a record deleted from the labels file, green
  restored. `tools/cost_model.py` gained `MEASURED_MODEL_JUDGED_POINT_RECORDS = 28` and wired the
  Claude-only tier's grader line to it, `role_cost("grader", ...)` at 2 samples with a third on
  disagreement over 442 of 1,200 judged points, $12.44 against the $33.32 worst case every point
  reaching the model, a saving of $20.88; the worst-case figures stay priced alongside it as
  `grader.worst_case_conditional_third_cycle` and `tier.hundred_claude_only.worst_case_cycle`
  because this file never overwrites a figure a document has already quoted. The Claude-only tier
  now totals $108.07, an overrun of $8.07 against the $100.00 ceiling, down from $128.95 and
  $28.95. `docs/plan/14-token-economy.md` "The $100 tier, line by line" and open question 2 are
  rewritten to the measured figures and to state why no further sourced lever closes the
  remaining $8.07 (see Known defects); `docs/plan/11-phased-delivery.md`'s P3 entry criterion is
  updated from "all 76 records are labelled" as an open task to the closed count. `tests/tools/test_cost_model.py`
  gained `test_claude_only_tier_grader_line_reads_the_labelling_pass`, pinning the tier at $108.07
  and the grader line at $12.44, verified red against the reverted worst-case grader line and
  green restored; `docs/plan/14-token-economy.md` also joined the `DOCUMENTS` tuple the
  hand-figure regression test already runs over 13 and the operator cost doc.
  `tools/cost_model.py --check docs/plan/14-token-economy.md` exits 0. No live Anthropic call was
  made; no test, gate, threshold or fixture was loosened.
- Nineteenth session, 2026-09-23, two review findings against the eighteenth session's uncommitted
  slice 3 work fixed. First, `app/db/models.py` `skills_state.credited_observation_count` was
  `NOT NULL` with no `server_default`, so `app/db/migrate.py apply_additive_migrations` raised
  `SchemaDriftError` on any database created before the column existed; `_column_definition`
  confirmed the message quotes exactly that shape. Fixed with `server_default=text("0")`, matching
  the pattern the other additive columns on `attempts` already use. A bare server default was not
  enough: every row already in the table would then read 0, and `app/engine/fringe.py serve_stage`
  reads `credited_observation_count > 0` to decide whether the stored `fading_stage` wins over the
  `p_A_knowledge` bands, so a 0 backfill would silently undo a student's fading progress on the
  first migrated read. `app/db/migrate.py` gains `_backfill_credited_observation_count`, run inside
  `apply_additive_migrations`'s own transaction immediately after this one column is added (a new
  `BACKFILLS` map keyed by `"table.column"`, so no other column's migration is touched): it replays
  `app/engine/update.py credit_for` over every `attempts.per_skill_states` entry, for every session
  with `updates_mastery = 1` (a rehearsal session never reached `apply_observation` and contributes
  nothing), and writes the count per `(user_id, skill_id)`. This is an exact replay of the counting
  rule `apply_observation` itself uses (`is_credited_success = c_credit > 0.0`,
  `is_credited_failure = f_credit > 0.0 or is_gap`), not an approximation from the counters that
  reset (`consecutive_successes`/`consecutive_failures`) or the ones a `prerequisite_gap` credit of
  `(0.0, 0.0)` never moves (`credited_successes`/`credited_failures`), which is why the backfill
  reads history from `attempts` rather than from any column already on `skills_state`.
  `tests/db/test_migrate.py::test_credited_observation_count_is_backfilled_from_attempt_history`
  seeds two sessions (one `updates_mastery = 1`, one `= 0`) and three attempts across them, drops
  the column, migrates, and asserts the recomputed per-skill counts; red with the backfill call
  stubbed out (both skills read back 0 against an expected 1), green restored, confirmed by
  temporarily replacing the `BACKFILLS.get(name)` call with a no-op and rerunning.
  Second, `app/runtime/bank.py served_steps` let a stage `example` item under the 2-step minimum
  degrade to showing every step, the final, un-blanked answer step included, while the stage still
  grades and credits whatever the student submits; two such items would meet 02's 2-consecutive-
  credited-successes rule and advance a skill out of `example` with no work from the student, since
  the answer was already on screen. Fixed by dropping the degrade path entirely: both `example` and
  `completion` now raise the same `a stage needs at least 2 worked steps to blank the last one`
  `ValueError` below the minimum, and `app/session/service.py resolve_served_stage` (renamed from
  its narrower completion-only form) rewrites a slot at either stage to `unsupported` when its item
  is under the minimum, so `served_item` never calls `served_steps` on a stage that cannot blank.
  This replaces the completion-only fallback the eighteenth session's slice built: an item too
  short for a completion blank now falls all the way to `unsupported` rather than stopping at
  `example`, because `example` no longer has room to blank a step either.
  `tests/api/test_served_steps.py::test_completion_below_the_two_step_minimum_is_served_at_unsupported`
  (renamed and re-asserted) and the new
  `::test_example_below_the_two_step_minimum_is_served_at_unsupported` cover both entry points; red
  against the eighteenth session's code (asserted stage `unsupported`, got `example`), green after,
  confirmed by stashing `app/runtime/bank.py` and `app/session/service.py` and rerunning.
  `docs/plan/11-phased-delivery.md` Q16 is corrected in place: "served at stage unsupported only",
  with the old "example and unsupported only" reading quoted and dated. No live API call; full
  pytest run, client `306 passed`, `tsc --noEmit`, and `qa/12_report.py` all clean (see the
  verification lines below this entry). `tests/e2e/test_exit_criteria_mastery.py::test_mastery_path_across_days_and_unmastery`
  reconfirmed at 30/30 clean runs in a dedicated loop this session, on top of the eighteenth
  session's fix, which this session did not touch.
- Eighteenth session, 2026-09-23, slice 3: how a skill leaves stage example, and the flaky mastery
  e2e test. The operator's ruling (Known defects, fourteenth session, first entry) is that stage
  `example` collects a graded answer: the worked example is shown with its final step left for the
  student, the student commits an answer, a confidence rating is collected after the answer and
  before feedback exactly as at completion and unsupported, and the server grades and credits it
  under 02's existing rules. `app/runtime/bank.py` `served_steps` now blanks the last step at
  `example` too, gated on the same 2-step minimum as `completion` (`supports_completion`); below
  the minimum `example` degrades to showing every step given, unblanked, rather than refusing the
  slot, which is the same fallback shape the existing below-minimum completion test already
  exercises. `app/session/service.py` `collects_confidence` now returns true for every stage, and
  `record_confidence` no longer refuses a rating at `example`; `_check_rating` in
  `app/feedback/render.py` picks this up unmodified, since it already read `collects_confidence`
  generically. Client: `app/web/src/session/Item.tsx` blanks the last worked step at `example` the
  same way as `completion` (`requiredServedStepCount`, `blanksAStep`), collects an answer at every
  stage (`collectsAnswer = true`), and asks for a rating at every stage
  (`collectsConfidence` returns true unconditionally); `EXAMPLE_LABEL` and its "I have explained
  this" commit copy are removed, since every stage now commits the same way. `SessionScreen.tsx`
  needed no change: `commit`, `rateConfidence` and `awaitsRating` already read `collectsConfidence`
  generically rather than special-casing example, so flipping the one function was enough to route
  example's answer and rating through the same path as completion. `docs/plan/11-phased-delivery.md`
  implementer decision 3 is withdrawn in place, its old text quoted and the new rule stated.
  02's internal inconsistency (line ~404's "credited observation" against line ~407's
  `observation_count > 0`, which line 56 says counts uncredited observations too) is resolved by a
  new field, `credited_observation_count` on `SkillState` (`app/engine/state.py`), incremented in
  `app/engine/update.py` `apply_observation` on the same `is_credited_success or is_credited_failure`
  event that already drives `move_counters`; `app/engine/fringe.py` `serve_stage` reads it instead
  of `observation_count`, `app/db/models.py`/`app/session/repository.py`/`app/content/reconcile.py`
  carry the new column (additive, picked up by `app/db/migrate.py` with no migration script), and
  02's schema table and `serve_stage` pseudocode are edited to name the field. New test
  `tests/engine/test_selection.py::test_serve_stage_ignores_observation_count_and_reads_credited_observation_count`
  proves the distinction: broken against `observation_count` and watched red (asserted
  `!= UNSUPPORTED` failed, since the stale `observation_count`-only check honoured a stage no
  credited observation had set), restored and green. Server tests updated for the new blanking and
  rating rule: `tests/api/test_served_steps.py`, `tests/api/test_ungraded_flow.py`,
  `tests/feedback/test_render.py`; fixtures that force a stage via `observation_count = 1`
  (`tests/api/conftest.py`, `tests/session/test_service.py`, `tests/session/test_serve_format.py`)
  now also set `credited_observation_count = 1`, since `serve_stage` gates on the new field.
  Client tests: `app/web/src/session/Item.test.tsx`, `app/web/src/session/SessionScreen.test.tsx`
  rewritten off the withdrawn decision; the one test that had no analogue left ("offers Next item
  after a worked example, whose attempt the server leaves ungraded") is deleted rather than
  loosened, because the ruling makes its premise false. Flake:
  `tests/e2e/test_exit_criteria_mastery.py::test_mastery_path_across_days_and_unmastery` failed
  once in 10 runs of the base branch before this session's changes (`UNIQUE constraint failed:
  audit_log.id`, confirming the shape once a naive fix was tried; the true fix is below) and 8 of 8
  clean runs otherwise. Root cause: `app/session/preview.py` `user_assembly_rng` seeds session
  assembly's tie-breaking draw from the process seed (fixed at 7 by the `world` fixture), the user
  id and the day; the user id is a fresh `uuid.uuid4().hex` from `app/auth/service.py new_id`
  minted fresh on every test's registration call, so which archetype the draw serves, and so which
  skill this test masters and un-masters, changed from run to run though nothing else did. Fixed by
  monkeypatching `auth_service.new_id` for the one `"USER"` prefix only, to a fixed id, leaving
  every other prefix (`AUD`, `PKC`, `CHL`, ...) on the real generator; an earlier attempt that
  pinned every prefix to the same fixed string broke on the second `write_audit` call inside one
  test run (`UNIQUE constraint failed: audit_log.id`), which is the artifact quoted above. Proof:
  36 consecutive runs with 0 failures (6 immediately after the fix, 30 more in a dedicated loop,
  `for i in $(seq 1 30); do .venv/bin/python -m pytest -q tests/e2e/test_exit_criteria_mastery.py::test_mastery_path_across_days_and_unmastery; done`,
  every exit code 0). No live API call; `app/providers/replay.py` cassette only.
- Seventeenth session, 2026-09-23, slice 2 of the token economy: a Claude-only $100 tier, priced
  and wired, plus a guard fix from the previous review. `tools/cost_model.py` gains
  `tier.hundred_claude_only`, additive next to `tier.hundred`: the verifier prices on
  `claude-haiku-4-5` batch (`verifier.on_haiku_batch_cycle`, $26.94, uncached because its 1,100
  token prefix sits below Haiku 4.5's 4,096 token cache minimum, the same reasoning 14 already
  gives the tutor); the template author prices on `claude-opus-5-5` (`template.cycle_on_opus_5_5`,
  $13.87 against $17.37, saving $3.50); the grader prices at 2 samples with a third on
  disagreement over the full 1,200 judged points, `grader.conditional_third_cycle` ($33.32), not
  the 17-of-76 field bound, because that bound is a lower bound on the model share and not a
  measurement and pricing the tier on it would be inventing the labelling pass's answer. New
  `CLAUDE_ONLY_ROLE_MODELS` names each role's model for the Claude-only tier; the existing
  `ROLES`/`PRICES`/`tier.hundred` figures are untouched, because `13-ai-engineering.md` and
  `docs/operator/ai-operating-costs.md` still quote the $95.03 Gemini-verifier tier and this file
  never patches a figure a document has already quoted. Total: $128.95, an overrun of $28.95
  against the operator's $100.00 hard stop. `docs/plan/14-token-economy.md`'s "The $100 tier, line
  by line" table, "Per role model choice" section, the "Proposed edits" table and open questions 2
  and 7 are rewritten to match and to report the overrun rather than close it by assumption;
  question 7 is answered, the ceiling is a hard stop with no margin, direction 7 taken now.
  `python3 tools/cost_model.py --check docs/plan/14-token-economy.md` exits 0.
  `tests/tools/test_cost_model.py` (13 and ai-operating-costs.md, unchanged) stays green.
  `app/providers/model_routing.py` is new: `ROLE_MODELS`, the same per-role Claude model choice
  restated for the application, read by `app/feedback/tutor.py` (`TUTOR_MODEL = model_for("tutor")`,
  replacing the hardcoded string). `tests/providers/test_model_routing.py` asserts `ROLE_MODELS`
  and `tools.cost_model.CLAUDE_ONLY_ROLE_MODELS` agree role by role, every role names a Claude
  model, and the tutor path reads from the shared table; a mismatch introduced by hand (grader
  changed to `claude-opus-5-5` on the app side only) turned it red before the fix and was reverted
  to confirm green. Guard fix: `app/providers/guard.py` `_settle` called `_dev_reconcile` from
  inside `_reconcile`'s own try block, so a `_dev_reconcile` failure (a corrupt dev-spend ledger
  file, `json.JSONDecodeError`, a `ValueError` subclass) was caught by `_settle`'s
  unreadable-result handler, which double-counted `settled_calls` and wrote a false
  `provider_result_unreadable` audit row for a provider result that had, in fact, read fine and
  already been settled onto the budget row. `_reconcile` now returns what the true-up needs instead
  of calling it, and `_settle` calls the new `_dev_reconcile_safely`, which isolates
  `_dev_reconcile`'s own exceptions behind a new audit action,
  `dev_spend_ledger_reconcile_failed` (added to `app/audit/vocabulary.py`), bounded once per user
  per day the same way the other refusal rows are.
  `tests/providers/test_dev_spend_guard.py::test_a_dev_ledger_failure_on_true_up_does_not_double_charge_the_budget_row`
  and `::test_a_dev_ledger_failure_on_true_up_is_recorded_under_its_own_action` reproduce it with a
  `LedgerThatFailsOnTrueUp` double whose `add()` raises `ValueError` only on the true-up call (the
  reservation call still succeeds); both red before the fix (`settled_calls` 2 instead of 1, zero
  `dev_spend_ledger_reconcile_failed` rows), green after, confirmed by `git stash` of
  `app/providers/guard.py` alone and rerunning. No live Anthropic call was made. Suite at close:
  pytest full run clean, client `308 passed`, `tsc --noEmit` clean, `qa/12_report.py` exit 0 (see
  the verification lines below this entry).
- Sixteenth session, 2026-09-23, two review findings against the fifteenth session's persistent
  developer spend cap fixed. `DevSpendLedger.spent()` and `.add()` in `app/providers/guard.py` were
  an unlocked read-modify-write of one JSON file, with `write_text` truncating before writing;
  concurrent reservations under the sync FastAPI route's threadpool could lose an update, and a
  reader could land on a truncated file mid-write. Fixed with an `fcntl.flock` on a `.lock` sidecar
  file held for the whole read-modify-write, and an atomic write (`tempfile.mkstemp` in the same
  directory, then `os.replace`) so a reader never observes a half-written file.
  `test_dev_spend_ledger_add_is_safe_under_concurrent_writers` reproduces the race with two threads
  and a monkeypatched `_read` that widens the read-to-write window; red without the lock (final
  total 1.0 instead of 3.0, one writer's update lost), green with it, confirmed by temporarily
  stripping the lock and rerunning. Separately, `dev_worst_case_usd` priced every prompt token at
  the base input rate regardless of `request.cache`, while `dev_actual_usd` charges a reported cache
  write at `write_1h` (2x input), so a cold-cache reservation could sit below the reconciled cost and
  let the cap be crossed. Fixed: a request whose `cache` is set now reserves its prompt at
  `max(input, write_1h)`, falling back to `input` for a model with no `write_1h` row.
  `test_dev_spend_reservation_prices_a_cached_request_at_the_write_rate` sets the cap just above the
  uncached worst case and asserts the call is refused; red without the fix (call went through,
  `DID NOT RAISE DevSpendCapExceeded`), green with it, confirmed by temporarily reverting to the
  input-only rate and rerunning. No live Anthropic call was made. Suite at close: pytest full run
  clean, client tests and `tsc --noEmit` clean, `qa/12_report.py` exit 0 (see the verification lines
  below this entry).
- Fifteenth session, 2026-09-23, slice 1 of the persistent developer spend cap. `tools/cost_model.py`
  PRICES gains `claude-opus-5-5` (input 4.00, write_5m 5.00, write_1h 8.00, read 0.20, output 20.00,
  the operator's console announcement, tagged [inferred] rather than [verified] since it is not an
  independent reading of the pricing page). `app/providers/guard.py` adds `DevSpendLedger`, a JSON
  counter under `var/dev_spend_ledger.json`, and `DevSpendCapExceeded`; `GuardedProvider` reserves
  the worst case against it before a live call, reconciles to the reported usage after, and refuses
  with an audit row (`dev_spend_cap_refused`, one row per day) when the projection would cross
  `GROWTH_DEV_SPEND_CAP_USD` (default $15.00). Pricing for the cap comes from
  `tools/cost_model.py`'s PRICES table, including its batch discount, not from the guard's own
  MODEL_PRICES. Tracking is off unless the caller passes `dev_spend_track=True`; the only caller
  that does is `app/api/routes/sessions.py`, from `isinstance(settings.tutor, AnthropicProvider)`,
  so replay and every Provider test double the suite already wires never touch the ledger, and a
  future double added to some unrelated test cannot start writing to it by accident either. `tools/dev_spend.py`
  is a read-only reporter over the same ledger. tests/providers/test_dev_spend_guard.py: refusal
  before the wire, persistence across a fresh `DevSpendLedger` instance pointed at the same file,
  reconciliation from the worst-case reservation to reported usage, replay leaving the ledger and
  its file untouched, tracking off unless `dev_spend_track=True` even over a double that reports
  real usage, the real `AnthropicProvider` class engaging the cap with no key and no socket opened,
  and the Opus 5.5 price. Suite at close: pytest full run clean (no FAILED entries; a single
  `test_a_pathological_comparison_on_the_main_thread_is_unsettled_within_the_bound` failure earlier
  in the session did not reproduce standalone or on a clean rerun and is unrelated, a timing bound
  test sensitive to host load per its own comment), client `308 passed`, `tsc --noEmit` exit 0,
  `qa/12_report.py` exit 0. No live Anthropic call was made.
- Fourteenth session, 2026-09-23. Suite at close: pytest `803 passed`, client `308 passed`, tsc
  clean, tests/e2e plus tests/api `151 passed` on four repeat runs, `qa/12_report.py` exit 0.
  Opened at `746 passed` and `286 passed`.
- R7, R8, R9 from the thirteenth session, reviewed fresh this session and closed with the repairs
  below: tests/api/test_ungraded_flow.py, tests/items/test_bound_child_failure.py,
  tests/design/test_contrast_floors.py, app/web/src/styles/app.test.ts.
- Child death while grading (R8 finished): `ChildDiedError` is re-raised through
  `app/items/grade.py` instead of being caught as ungraded, and POST /sessions/{id}/attempts
  answers 503 with no attempt row, so the resubmit is graded.
  test_a_child_death_while_grading_writes_no_attempt_and_the_resubmit_is_graded (red
  `assert 200 == 503`), plus three grade-level re-raise tests, each red under its own mutant.
- Provider seam: `ProviderResult.finish_reason` replaces `stop_reason`; a cassette that still
  carries `stop_reason` is refused; `output_config.effort` is refused on Haiku 4.5.
  test_result_names_finish_reason, test_a_cassette_carrying_stop_reason_instead_of_finish_reason_is_refused,
  test_every_committed_cassette_replays_its_finish_reason, test_effort_is_refused_on_haiku_4_5,
  test_haiku_4_5_without_effort_reaches_the_wire.
- Account: `GET /auth/status` answers `{"user_exists": bool}` and the account screen shows only
  register or only sign-in; `POST /auth/passkey/add/begin|finish` add a second passkey under the
  session cookie, excluding the credentials already stored; `AddPasskeyControl` is mounted on
  settings. tests/api/test_auth_status.py, tests/auth/test_add_authenticator.py (including
  test_a_challenge_issued_to_one_user_cannot_finish_under_another_users_session, red `assert 409
  == 403` with the guard mutated off, and test_adding_an_authenticator_excludes_the_passkeys_already_stored),
  test_registration_options_exclude_the_credentials_already_stored against the real py_webauthn,
  App.test.tsx "offers a signed-in student a second passkey on settings and nowhere else".
- Key audit: a verdict outside the sample is refused (`VerdictOutsideSample`), a second verdict
  through `record_item_audit_verdict` is refused (`VerdictAlreadyRecorded`), the denominator is
  the sample size, and no rate is published until every sampled item has exactly one verdict.
  test_a_verdict_outside_the_sample_is_refused, test_a_second_verdict_on_an_audited_item_is_refused,
  test_an_incomplete_sample_publishes_no_rate, test_a_complete_sample_publishes_its_rate,
  test_check_verdicts_refuses_a_verdict_outside_the_sample.
- Units in grading (03 check 4): notation credit only for the same unit written differently, SI
  conversion factor exactly 1; a different unit of any dimension is wrong; symbols are
  case-sensitive except where the submission reads as no unit at all and matches the key in
  another case (" M/Sec " against m/sec); physical constants are not units.
  test_a_different_unit_earns_no_notation_credit (11 cases),
  test_the_same_unit_written_differently_keeps_notation_credit,
  test_a_speed_in_metres_per_second_against_a_key_in_feet_per_second_is_wrong,
  test_unit_symbols_are_case_sensitive, test_a_physical_constant_is_not_a_unit,
  test_units_that_name_no_known_unit_are_ungraded.
- Gate 23 seed independence: the gate's loop runs until both screens arrived and every
  cold-start-reachable archetype was served (no assertion changed; seeds 0 to 49 all pass),
  `serve_as_mcq` publishes its own sibling item, and `second_wrong_answer` in
  tests/api/test_settings_routes.py makes the stage and format certain. The session and preview
  rng is seeded by process seed, user id and day through `preview.user_assembly_inputs`, and the
  old `assembly_inputs` is deleted. test_two_users_on_the_same_day_get_different_draws,
  test_the_process_seed_still_moves_the_draw, test_the_same_user_on_the_next_day_gets_a_different_draw,
  test_the_preview_and_the_session_both_draw_from_the_signed_in_users_rng (red `assert [] ==
  ['USER-...']`).
- test_next_item_never_carries_the_answer_key reads its forbidden fields from 04's output schema
  and 06's items table; red on each of four leaks mutated into `_as_item_dict`.
- Error note cap of 500 (operator decision 2026-09-20): `ERROR_NOTE_MAX_CHARACTERS`, 422 over it.
  test_error_note_route_refuses_a_note_over_500_characters, test_a_note_of_exactly_500_characters_is_stored
  (red `assert 422 == 200` with `>` mutated to `>=`); the client field's maxLength test scans the
  server constant (red `expected 501 to be 500`).
- A malformed `today` answers 422 on GET /progress, POST /sessions and the other session routes,
  with nothing written.
- Design: the contrast floor tested at exactly 4.5 (red with `<` mutated to `<=`); the accent tint
  range parsed from 08; `css.py` emits a `:root:not([data-theme])` fallback, light by default and
  dark under `prefers-color-scheme: dark`, derived from theme.ts, so the first paint carries tokens.
- Session screen: `rateConfidence` catches a refused rating and releases the in-flight guard; the
  example-stage mock returns what the server returns (correct null, confidence null).

Session 2026-09-23 (thirteenth), P1 exit criteria, the provider seam defects 13 enumerates, the
sign-in screen, and the design. Suite line at open `512 passed in 70.40s (0:01:10)`, at the last
close `746 passed in 148.85s (0:02:28)`. Client `Tests 286 passed (286)`, `npx tsc --noEmit`
exit 0, `npx vite build` succeeds. Style gate exit 0 on 77 changed Python and Markdown
files at the pre-wave-3 check. `qa/12_report.py` exit 0; `data/`, `research/`, `cache/` and `qa/`
untouched. `tools/gate_status.py --phase P1` reads `P1: 31 gates, 28 present, 3 missing, 28
passing`. Nothing committed.

- Gate 26 `test_contrast_floors` closed (`tests/design/test_contrast_floors.py`). The palette is
  `app/design/growth-tokens.json`, "Graphite, revised", chosen by the operator on 2026-09-23 from
  three directions and then four Slate variants rendered as mockups. `tools/check_tokens.py`
  exits 0 on it; the lowest pair is focus-ring on surface-sunken at 4.91:1 and the lowest text
  role is 5.60:1. Cross-checked against the WebAIM Contrast Checker API
  (https://webaim.org/resources/contrastchecker/, api mode, queried 2026-09-23): every text,
  state and focus pair passes AA in both themes. The six border-hairline rows read AA fail and
  AA-large pass at 3.02 to 3.57; 08 sets a 3:1 working floor only for the mastery map and the
  calibration curve, and holding input edges to it is the implementer's extension.
  Deviations the operator accepted by choosing it: 08 asks for warm neutrals and Graphite is a cool
  grey; the file carries 08's named neutral tokens and the two semantic base colours, not a
  separate nine-step ramp or semantic tint ramps, because the vocabulary names none.
- Gate 22 `test_prompt_cache_prefix_length` closed. The tutor renders
  `prompts/feedback/elaborated_v2.md`, whose static prefix measures 1,470 tokens on
  claude-sonnet-5 by `POST /v1/messages/count_tokens` with the operator's key on 2026-09-23 (v1
  measured 485). The prefix grew only with 13:246's content: guardrail rules, notation and
  rendering rules, interface-writing rules; P1 has no persistent misconception list, so none was
  added. The measurement is bound to the prefix bytes by sha256 in
  `tests/fixtures/prompt_token_counts.json`; `tools/count_prompt_tokens.py` re-measures. P1 now
  reads 28 of 31.
- Exit criteria 5 and 6: `tests/e2e/test_exit_criteria_mastery.py`,
  `test_unit2_session_changes_mastery_state` and `test_mastery_path_across_days_and_unmastery`,
  over the real HTTP app with the six D2 conditions recomputed from `attempts` rows.
- Exit criterion 8 instrument: `tools/serving_cost.py <db> [--user id]` prints served items, median
  tutor cost per served item (all items, and items that made a call) and the cache read share from
  attempts and from budgets, each with its denominator and exclusions. New attempts columns
  `tutor_calls`, `tutor_cost_usd`, `tutor_tokens_in`, `tutor_tokens_cached_read`,
  `tutor_cached_read_reported_calls`.
- 13's guard items 3 to 7 and its missing hard-stop rows (`app/providers/guard.py`): a call that
  reached the wire is charged the worst case, a `RefusedBeforeWire` is refunded; a refusal names
  every crossed cap; null and zero cached counts kept apart through `settled_calls` and
  `cached_*_reported_calls`; `ProviderCallFailed` carries no message text; an unconfigured role is
  refused and audited once a day; only a raise of every stopping cap above the day's spend clears
  a stop, through the guard and `PUT /settings/budgets` alike; `CallAccounting` and
  `last_accounting`. Price table carries Haiku 4.5, Flash-Lite and dated Gemini 3.8 Flash.
- Anthropic adapter: allowlisted `provider_options` (thinking disabled, effort), the key never a
  local on a raising frame, redirects refused, SSE stream mapped per 06 with usage returned,
  `reasoning_tokens` read, Opus 5 family rule.
- Tutor: 13's configuration (thinking disabled, effort low, 600 output tokens) and ceilings of 20
  calls per session and 3 per item, counted from the database, pre-wire failures not counted.
  Startup caps default to 12's row, $1.00 and 250,000 tokens, and refuse non-finite values.
- Audit detail bound (`app/audit/detail.py`) on every writer, checked per constructor by AST.
- CSP and CORS middleware; Secure cookie decided by request host, plain http on a non-loopback
  host refused.
- SymPy bounded on every thread for equivalence, numeric check, expression comparison and parse;
  a SymPy exception on student input is ungraded instead of a 500.
- Client: account screen (register, sign in, recovery code) over real WebAuthn; `data-theme` from
  the system preference; `app/web/src/styles/app.css` from the chosen mockup; inline style
  overrides removed; one main landmark per screen.
- Reviewer D's findings fixed: an example-stage or ungraded attempt no longer 409s on feedback or
  confidence, so the student always gets Next item and mastery stays unchanged
  (`tests/api/test_ungraded_flow.py`, feedback kind `ungraded`); a grader child that dies before
  answering raises `ChildDiedError` instead of reading as unsettled; gate 26 pins focus-ring and
  both state colours on every surface; app.css's `:focus-visible` rule, one main landmark per
  screen, an h1 on the account screen and the recovery-code input's `autocomplete="off"` and focus
  return are tested.
- Tests strengthened: the tutor receives only its selected fields (sentinels in every other
  field), prompt templates carry sha256 goldens, the cookie refusal reads the database.
- py_webauthn landed in `pyproject.toml` and 06; `LibraryVerifier` builds real options.
  `uvicorn` is installed in `.venv/` only, on the operator's yes, to run the app locally.

Session 2026-09-22 (twelfth), the server routes and client wiring for the three P1 screens. Suite
line at open `405 passed in 57.78s`, at close `512 passed in 60.71s (0:01:00)`. Client suite
`Tests 228 passed (228)`, `npx tsc --noEmit` exit 0, `npx vite build` succeeds. Style gate exit 0 on
all 64 changed or new files. `qa/12_report.py` exit 0 and `qa/last_report.json` restored. `data/`,
`research/` and `cache/` untouched. `tools/gate_status.py --phase P1` still reads 26 of 31: every
remaining gate is operator content or a live key. Nothing committed.

- A, session payload. `GET /sessions/{id}/next` carries `served_steps` (every worked step at
  example, all but the last at completion, null at unsupported, index and text only) and
  `self_explanation_prompt` at example. `POST /sessions/{id}/attempts/{aid}/self-explanation`
  writes `attempts.self_explanation` once, and only for a worked example or a corrected attempt.
  `attempts.response` keeps only `mathjson`, `option_id` and `units`, so a client-claimed
  `correct` or `step_outcomes` is no longer stored or trusted. Step marks are computed on the
  server in `worked_solution` numbering: given steps `given: true, correct: null`, the completion
  blank carries the server's verdict. A completion slot below Q16's 2-step minimum is served at
  example. Tests `tests/api/test_served_steps.py`, `tests/api/test_self_explanation.py`, the
  strengthened `test_next_item_never_carries_the_answer_key`, and the rewritten
  `tests/feedback/test_render.py::test_step_verification_at_example_and_completion`.
- B then A, home queue preview. `GET /progress` returns `skills_due_for_review`, `frontier_skills`,
  `corrected_items_returning`, `forecast_minutes` and `session_in_progress`, writes nothing, and
  derives its day and rng from `preview.assembly_inputs`, the same function `POST /sessions` now
  uses, so the forecast is the queue the student opens. Coverage-gap audit rows deduped per user,
  archetype and day. Tests `tests/session/test_queue_preview.py`,
  `tests/api/test_progress_route.py` including
  `test_progress_predicts_the_queue_post_sessions_assembles`.
- C, settings and budgets. `GET` and `PUT /settings` (exam date and purge date),
  `GET /settings/providers` (six roles from `guard.ROLES`, no key material), `GET` and
  `PUT /settings/budgets` behind re-authentication with a `budget_cap_changed` audit entry. Caps
  live on `budgets` rows and carry forward day to day once a PUT is made; before that the startup
  caps apply and a lowered one still binds on today's row (the committed
  `test_a_lowered_cap_binds_on_the_existing_row` passes unchanged). Tests
  `tests/api/test_settings_routes.py`, `tests/providers/test_cap_change_binds.py`.
- D, export. `POST /export` behind re-authentication and `GET /export/{id}`, a JSON archive of
  every user-owned table classified from the SQLAlchemy metadata, with secret-bearing columns
  dropped, written 0600, replaced new-file-first, 503 on an in-memory database. Tests
  `tests/export/test_export.py`.
- P, purge repair. Purge now removes the export archive and its `jobs` row, uses the export's
  ownership classification instead of a hand-typed table list, and burns a wrong reauth token.
  Gate 24 unedited and green. Tests `tests/session/test_purge.py` (three new),
  `tests/api/test_purge_route.py`.
- E, spacing. `SPACING_TOKENS` holds 08's nine values as `space-<px>`, emitted in a `:root` block,
  and `stylesheet_from_token_file(path)`. Test `tests/design/test_spacing.py`.
- F, ASGI mount. `app/main.py` serves `app/web/dist/assets` through `StaticFiles`, `index.html` at
  `/` only, and `/growth-tokens.css` from `GROWTH_TOKENS_PATH` read per request (404 when unset).
  `application` is built on first attribute access, so importing `app.main` writes nothing.
  Tests `tests/api/test_static_mount.py` (19, including three traversal encodings).
- G, hygiene. Resolution audit logs the row's own kind; `resolve_item_audit_row` resolves exactly
  the named row and refuses a resolved one; the key error rate divides by eval 29's sample of 100;
  `verify_item` splits options on `is_key` and refuses inconsistent records.
- H, client. Home, session and settings are mounted over real calls; the "not built yet" panels
  and the invented required props are gone. `ServedItem` and `SessionQueue` are checked by exact
  field-set equality against the server source. Dates print as 08 writes them. Every settings
  action reports failure by leaving its control re-enabled with no success state.

Session 2026-09-21 (eleventh), the P1 client and gate 25. Suite line at open `388 passed in 64.09s`,
at close `405 passed in 174.52s`. Client suite `133 passed`, `npx tsc --noEmit` exit 0 and
`npx vite build` succeeds. Style gate
exit 0 on every changed Python and Markdown file. `qa/12_report.py` exit 0. `data/`, `research/`
and `cache/` untouched, `git status --porcelain` over the three empty. `qa/last_report.json`
restored. Nothing committed.

- Gate 25 `test_reduced_motion_replaces` closed, which takes P1 from 25 of 31 passing to 26 of 31.
  `tools/gate_status.py` reports `P1 25 test_reduced_motion_replaces present passing`. The three
  previous sessions filed this gate as human-only on the ground that it waits on the design token
  file. That reading is corrected: the gate's property is the motion contract and the presence of
  five affordances, it reads no hex value, and 11 P1 scope items 8, 11 and 17 put `app/web/` inside
  P1. See Plan corrections.
- `app/web/`, new, the P1 client. React 18, TypeScript and Vite, which
  `docs/plan/06-architecture.md` line 93 names, plus KaTeX and MathLive from the same sentence.
  `npm` lockfile committed, `node_modules/` ignored.
- `app/web/src/affordances.ts`, the five gate-25 affordance names as one object with
  `affordanceProps`. Gate 25 and the session tests range over that object, so no hand-copied list
  is checked against another hand-copied list.
- `app/web/src/api/types.ts` and `client.ts`, the typed fetch layer over the routes
  `app/api/routes/` already exposes. `client.test.ts` scans the FastAPI decorators from disk and
  asserts every path the client issues is a path the server declares, and, after the wave-1
  review, scans the route return-dict literals, `bank.STUDENT_OPTION_FIELDS`, `render.as_dict` and
  `dress_item` and asserts twelve payload types by exact field-set equality.
- `app/web/src/styles/motion.css` and `motion.ts`, the motion contract. One duration and one
  easing, both derived from 08's single number. `motion.test.ts` walks the real stylesheet through
  the CSSOM and fails a reduce block that deletes a transition instead of cross-fading it.
- `app/web/src/input/MathField.tsx` and `McqControl.tsx`. MathField exports MathJSON, not LaTeX.
  McqControl takes its option count from the item's own options array and leaks no key: its test
  compares attribute name and value pairs across the radios, excluding the legitimately varying
  ones, which is what caught a `data-is-key` mutation that a name-only comparison had missed.
- `app/web/src/session/`, the session screen: the three fading stages, backward fading with the
  last step blanked, the five feedback affordances, and the item-to-feedback-to-next-item flow.
  Colour independence holds: every correct or incorrect state carries a word and a glyph.
- `app/web/src/home/HomeScreen.tsx` and `settings/SettingsScreen.tsx`, with home's three states
  (queue ready, queue empty, session in progress) and settings restricted to the five sections
  11 P1 scope 17 names. The settings test parses that scope sentence out of 11 rather than typing
  the list. Purge refuses without the typed confirmation.
- `tests/web/test_reduced_motion.py`, gate 25 in pytest so `tools/gate_status.py` finds it and the
  operator's one suite command runs it. It shells out to vitest and asserts on the JSON reporter,
  not the exit code: every `it(...)` title scanned out of the tsx source must be reported passed,
  the passed count must equal the declared count, and a run matching zero files fails. It never
  skips.
- `app/design/css.py`, the only bridge from the operator's token file to the client. The client
  references `var(--growth-<token>)` and contains no hex value anywhere.
- The three non-blocking defects carried since the eighth session are fixed.
  `app/items/verify.py` now holds one comparison and error-path core that both
  `verify.distractor_checks` and `distractor_paths.distractor_path_violations` call, with the two
  deliberately different unsettled policies preserved and named in each caller.
  `tests/design/test_tokens.py`'s floor test now finds the greys astride the floor with
  `contrast.contrast_ratio` instead of asserting black on white at 21:1, and the accent tint range
  is parsed from 08's own sentence instead of typed.

Session 2026-09-20 (tenth), the token economy. Suite line at open `388 passed`, at close
`388 passed, 1 warning in 56.96s`. Style gate exit 0 on every file written. `qa/12_report.py` exit
0. `data/`, `research/` and `cache/` untouched, `git status --porcelain` over the three empty.
Nothing committed.

- `docs/plan/14-token-economy.md`, new. The operator set a ceiling of $100.00 to exam day against
  the recommended tier's $348.05. Ten directions are ranked by dollars saved, each with the quality
  instrument that would detect its loss and the measurement that settles it, plus rejected
  directions with the floor that rejects each, proposed constant changes, open questions and
  unsourced claims. The tier lands at $95.03, Anthropic $82.31 and Google $12.71, with $4.97 of
  headroom.
- `tools/cost_model.py`, additive only. `gemini-3.5-flash-lite` prices read off the pricing page on
  2026-09-20, a `template` role priced from measured prompt and artifact sizes, the grader's model
  share, the diagnostician's recurrence share, the golden set 2 canary, and the `tier.hundred`
  lines. No existing constant moved, so the superseded configuration stays priced beside the new
  one and the four tests stay green. Positive control on the new document: a stray `$999,999.99`
  appended to a scratch copy gives `14-control.md:535: $999,999.99 is not a figure in
  tools/cost_model.py` and exit 1; the clean file gives 0 unknown figures and exit 0.
- What was measured in this session, with the command. 139 active archetypes and a mean
  `build_prompt` of 1,582.3 characters over all of them; `INSTRUCTIONS` at 4,420 characters and
  `TEMPLATE_SCHEMA` at 2,280, both from `tools/template_trial.py`; the 26 template artifacts under
  `var/` at a mean 2,412.1 characters of compact JSON, median 2,372.5, min 1,910, max 3,212; and 76
  active BC-PT records in `data/scoring_points.json` of which 59 answer no to
  `justification_required`, `interpretation_required` and `hypotheses_required`, 14 require
  justification, 3 interpretation and 3 hypotheses.
- Eight of the ten directions were written into the plan on the operator's instruction: 13 gains a
  fourth tier, a Flash-Lite verifier row, two price rows, a second per-role table, rewritten eval
  schedule rows, six tunables and five decisions; 07's D8 verifier row and the paragraph above it;
  04's re-solve routing and a paragraph on what the unit of generation does to caching, batching and
  bank cost; 10's golden set 1 onto the template gate, golden set 2's sampling split, which point
  types reach the grader, and the P3 and P4 gates; 03 gains a section on when the diagnostician is
  called at all and the rule-based section is renamed from "unavailable" to "does not run"; 11 gains
  the BC-PT labelling pass as a P3 entry criterion and the calculator boundary on the template gate;
  12 gains ten tunables rows; and the operator guide's settings, spend, tiers, eval schedule, credit
  arithmetic and the 2026-12-31 calendar note.
- Two directions deliberately not taken, on the operator's instruction: grader thinking off at
  $25.20 and a third grader sample drawn only on disagreement at $11.02. Each asserts a quality
  decision with no evidence behind it, each has a settling measurement named in 13, and together
  they are the remedy if the grader line comes in at its worst case of $44.34, which would put the
  tier at $129.25.
- The tier's single point of failure, recorded because it is not a defect and will read like one
  later. The grader line of $10.11 rests on 17 of 76 BC-PT records, which is a lower bound on the
  share of judged points reaching a model and not the share, because 03 adds a second condition the
  data does not carry. The labelling pass that settles it is offline, free and is now a P3 entry
  criterion.
- No application code was written. `app/generation/` still does not exist and the grader, the
  diagnostician and the transcriber are still unbuilt, so every direction landed as a plan change
  and a cost model line rather than as behaviour.

Session 2026-09-20 (ninth), the AI layer follow-through. Suite line at open `341 passed`, at
close `388 passed, 1 warning in 63.34s`. Style gate exit 0 on every file written. `qa/12_report.py` exit 0.
`data/`, `research/` and `cache/` untouched, `git status --porcelain` over the three empty.
Nothing committed. Five tasks in order, each verified before the next.

- The live 400. `app/providers/anthropic.py` sent `"temperature": request.temperature` on
  every call and `ProviderRequest` defaulted it to 0.0; a non-default temperature is a 400 on
  Opus 5 and Sonnet 5 at any value. The key left the wire body and the field left
  `ProviderRequest` entirely rather than becoming optional, because no routed model accepts it
  and an optional field invites sending it again. `tests/providers/test_anthropic.py` now asserts
  `"temperature" not in body`; shown red by re-adding the key
  (`AssertionError: assert 'temperature' not in {... 'temperature': 0.0 ...}`), restored,
  `tests/providers` 31 passed. `/code-review` over the four files: no findings.
- The cost model. `tools/cost_model.py` emits every figure `docs/plan/13-ai-engineering.md` and
  `docs/operator/ai-operating-costs.md` quote, from named price, token, call-count and survival
  constants, and `--check <file>` lists every dollar figure in a file that the model does not
  emit. `tests/tools/test_cost_model.py` (4 tests): the tutor cycle against the formula 13
  states, the effort lever against the thinking difference, and the two documents against the
  emitted set with a positive control that a stray `$999,999.99` is flagged. Red under mutation:
  charging every call as a prefix write gives `assert 15.588 == 5.01308`; a hand-patched
  `$123.45` in the operator guide gives `prints dollar figures the calculator does not emit:
  [(168, '123.45')]`. Both restored. What the recompute moved: golden set 2 was priced without
  the grader's 700 thinking tokens, so its run is $6.48 not $3.33 and the recommended tier is
  $348.05 not $319.70; effort high in the uncapped tier now applies to every thinking role by
  the generator's 2,500 to 1,200 ratio, so that tier is $1,145.55 not $880.29; five passages
  still priced the bank at 40 generated per archetype and now read 56 (staging waves of 28,
  batch queue 7,784 and 6,227, spend avoided $5.09 to $19.70, Sonnet comparison $71.05, effort
  lever $126.49). 24 bare `[measured]` tags were each given a command, retagged `[verified]`
  where the evidence was a code read at a named line, or `[single-source]` where the run is not
  in the repository. Two grep claims written for those tags were false as first written and
  were corrected before landing: `self_explanation` matches a prompt shown to the student, and
  `REPEAT_WINDOW_DAYS` is named by 13 itself.
- The template gate. `tools/template_trial.py` gained `contract_check` (declared
  representation from the archetype's list; figure spec required for BC-REP-02, 03, 07 and
  08; every distractor `error_path` an active BC-ERR id; every `point_type_id` a BC-PT id;
  exactly four options) and `incidental_check` (every parameter declares `radical` or
  `incidental`; each incidental is varied alone over its domain and the structure of every step
  and the key must hold). Schema, prompt and defect feedback carry all of it, and the prompt
  now lists the BC-ERR ids reachable from the archetype's skills. `tests/tools/test_template_trial.py`
  grew from 32 to 43 tests, one mutation of `tests/fixtures/template_trial/clean_02011.json` per
  check plus the clean-fixture absence claims; the fixture gained a representation, three
  resolving distractors and honest roles (`a` incidental, `b` and `c` radical because a zero
  deletes a term). Every check shown red by disabling it in the code, and the gate wiring shown
  red by dropping each clean flag from `passes_bar`; all restored, 43 passed. Measured over the
  26 templates in `var/` with the eleven-check gate: 0 of 26 pass; 12 of 26 on the six old
  checks. Failures by check: representation undeclared 26, error path unresolved 26, four
  distractors 14, key copied from the last step 13, point type unresolved 6, key disagreement 1.
  The role declaration is absent on all 26 by construction. The earlier "6 of 18" and "7 of 8"
  claims are superseded by that line.
- The radicals declaration. 13 gained "Radicals and incidentals" with the five primary
  sources, the contract consequence and the gate above, and the difficulty-prior decision:
  02 keeps one prior per archetype and accepts a known centre-ward bias, with the measurement
  that adds a variance term recorded (facility spread above 0.15 over at least 5 instantiations
  on 30 or more attempts). 02 and 04 carry the surgical corrections listed under Plan
  corrections.
- The migration. 13 gained "Template architecture and the migration" with the file-by-file
  map and the seam decision: instantiate at build time into `items`, never at serve time,
  because `attempts.item_id` is a permanent reference at `app/session/repository.py:129` and
  `app/api/routes/sessions.py:154` and `:207`, verification and the duplicate gate are per
  item, the requeue serves the same id again, and the least-recently-served draw needs stable
  ids. `app/generation/`, `prompts/generator/` and `prompts/verifier/` do not exist, so 11's
  P4 items 7 and 11 were corrected to name the template module and prompt. No application
  code for the migration was written this session.

Session 2026-09-20 (eighth), suite line at open `230 passed in 34.85s`, at close
`341 passed in 44.31s`. Style gate exit 0 on all 28 changed files, fed the hook its JSON payload
on stdin, confirmed to bite with a positive control (`style_gate: probe.py: em dash present`,
exit 2). `qa/12_report.py` exit 0. `data/`, `research/`, `schemas/` and `cache/` untouched,
confirmed with `git status --porcelain` over all four. The phase stayed P1, because 11's P2 entry
criterion is "P1 merged with all gates green" and six P1 gates are still open. The slice was every
P1 deliverable buildable without the operator, plus the operator unblock kit for the six that are
not. `python3 tools/gate_status.py --phase P1` now reads `P1: 31 gates, 25 present, 6 missing,
25 passing`, and the six missing are exactly the human-only list: 17, 22, 25, 26, 29 and 30.

- Integrator, gate table: `tools/gate_status.py`, `tests/tools/test_gate_status.py` (17 tests).
  Reads the gate list out of 11 for every phase, uses the plan's own item numbers for P1 and a
  running index for the later phases, scans `tests/` for each gate's definition, and reads
  outcomes from a JUnit report the tool writes itself. It exits 1 when any gate is missing or
  failing, so a caller can use it as a check. Two defects found in it during review and fixed: the
  outcome column was asserted by no test, and `run_suite` used `sys.executable`, which under
  `python3 tools/gate_status.py` is the system interpreter with no pytest, so the run failed
  silently and every gate read unknown. The tool now runs the repository's own `.venv` interpreter
  and says on stderr when a run produced no report.
- Agent M2, schema drift: `app/db/migrate.py`, `tests/db/test_migrate.py`,
  `tests/db/test_engine_migrates.py`, wired into `make_engine` in `app/db/models.py`.
  `missing_columns`, `apply_additive_migrations` and `SchemaDriftError`. This closes the
  `attempts.tutor_sentence` defect: an existing `var/growth.db` no longer raises on the first
  feedback read. Every ALTER is built and validated before the transaction opens, so a blocking
  column aborts before any write. A column that is NOT NULL with no server default refuses, and so
  does a column declared unique or indexed, because ALTER TABLE ADD COLUMN carries neither and the
  migrated database would otherwise diverge from a fresh one while reporting no drift. A database
  with no drift opens no write transaction at all.
- Agent M3, the unreadable provider result: `app/providers/guard.py`, `app/audit/vocabulary.py`,
  `tests/providers/test_guard_settle.py` (7 tests). A new audit action
  `provider_result_unreadable`, deduped on the budget row id, which is already one per user per
  role per day, so two roles give two rows and a day rollover records again. The detail carries
  the role, the model and the exception type name and nothing else.
- Agent M4, gate 26's arithmetic: `app/design/contrast.py`, `tests/design/test_contrast.py`
  (14 tests). WCAG 2.2 relative luminance and contrast ratio, `TEXT_CONTRAST_FLOOR` 4.5 and
  `LARGE_TEXT_CONTRAST_FLOOR` 3.0, both taken from 08 and 11. No hex value is authored anywhere.
- Agent M5, gate 30's property: `app/items/distractor_paths.py`,
  `tests/items/test_distractor_paths.py` (8 tests). `error_ids_for_skills` computes the BC-ERR set
  over the P1 skills rather than typing 40, and it is 40. An unsettled symbolic comparison is
  reported as its own violation and never reads as clean.
- Agent M6 and the integrator, the error note: `app/api/routes/sessions.py`,
  `tests/api/test_error_note.py`, `app/session/service.py`,
  `tests/session/test_error_note_service.py`. One note per corrected attempt, refused with 409
  rather than silently overwritten, and a note containing a line break refused with 400, because
  03 says the student writes one line. No length cap, because 03 and 06 give none. The guard was
  moved into `record_error_note` so every caller gets it, not only the route, and the route now
  maps `ErrorNoteAlreadyWritten` and `ErrorNoteNotOneLine` onto its two status codes.
- Agent M7, gate 29's shape: `app/review/verdicts.py`, `tests/review/test_verdicts.py` (14 tests).
  `verdict_violations` and `audit_completeness`. The verdict vocabulary is imported from
  `app/review/audit.py` and asserted identical rather than retyped.
- Agent M8, gate 26's vocabulary: `app/design/tokens.py`, `tools/check_tokens.py`,
  `tests/design/test_tokens.py` (12 tests), `docs/operator/design-tokens.template.json`. The nine
  type tokens and the seventeen colour tokens, both parsed out of 08 inside the test rather than
  compared against a second hand-typed list. The template is every token name at null, and a null
  is reported as missing rather than skipped.
- Agent M9, the operator's own checks: `tools/check_items.py`, `tools/check_audit_verdicts.py`,
  `tests/tools/test_operator_clis.py` (8 tests). `python3 tools/check_items.py <directory>` runs
  gate 17's and gate 30's checks over a directory of records and prints a per-archetype count;
  `python3 tools/check_audit_verdicts.py <verdicts.json> <sample.json>` prints the key error rate
  or says why it cannot be published. Over `tests/fixtures/items_p1/` the first reports 36 records,
  36 clean, exit 0, with six archetypes at 6 records each and the other seven at 0.
- Agent M10, the work orders: `docs/operator/README.md`, `items.md`, `key-audit.md`,
  `design-tokens.md`, `provider-key.md`. What the operator has to produce, in what shape, and the
  command that checks it, with every field list read out of the code rather than recalled.
- Integrator, the unsettled distractor: `app/items/verify.py`, `app/items/ingest.py`,
  `tests/items/test_unsettled_distractor.py` (5 tests). `_equals_key` collapsed an unsettled
  symbolic comparison into not-equal, so a distractor the checker could not compare against the
  key read as distinct from it and the item reached status `verified`. It is now
  `INDETERMINATE`, which leaves the item a draft and routes it to review, which is what ingest's
  own docstring already claimed. Red: `assert 'pass' == 'indeterminate'`.
- Integrator, gate 23 strengthened: `tests/e2e/test_session_login_to_feedback.py`. Membership in
  the 13 is a subset check that a regression serving one archetype passes. The gate now also
  computes, from the engine's own `outer_fringe` and `candidates` over the freshly seeded state,
  every archetype open at cold start, asserts there is more than one, and asserts every one of
  them was actually served.
- Integrator, the archetype lists: `tests/tools/test_p1_archetype_list.py` (4 tests). The 13 ids
  were typed in three places and checked against 11 in none. The plan text is now the source and
  every copy is compared against it. Red under mutation: dropping one id from
  `tools/build_p1_fixture.py` gives `AssertionError: assert {...} == {...}`.
- Integrator, after the fresh review, which raised two blocking findings and both reproduced.
  `audit_completeness` published a rate over a sample that was complete by id but not by verdict:
  100 sample ids, 98 clean, one verdict `mostly_fine` and one `None` gave `missing_ids []` and
  `key_error_rate 0.0`, which is what gate 29 and exit criterion 4 forbid. It now folds
  `verdict_violations` in, reports `invalid_ids` and `unidentified_records`, and returns `None`
  for the rate unless every verdict in the sample exists and is well formed (red:
  `assert 0.0 is None`). And a record with no `item_id` raised `TypeError` out of a `sorted()`
  rather than being reported; it is now counted. `app/design/tokens.py` checked
  `accent-contrast-text`, `state-correct` and `state-incorrect` against nothing, so a token whose
  role is text could hold any value and pass gate 26; the validator now checks
  `accent-contrast-text` against the accent base and its four tints and each semantic colour
  against each surface (red: `these do: ['accent-contrast-text']`).

Session 2026-09-20 (seventh), suite line at open `191 passed in 23.36s`, at close `230 passed in 46.12s`.
Style gate exit 0 on every touched file; `qa/12_report.py` exit 0; `data/`, `research/`, `schemas/`
and `cache/` untouched, confirmed by `git status --porcelain` over all four. The slice was the
provider seam of 07 plus gate 23, which were the last two pieces of P1 scope needing no key, no
screen and no hand-authored item. A fresh reviewer found ten defects over the first integration;
eight were fixed in session by two repair agents and the integrator, and the two that remain are
under Known defects.

- Agent A, the provider seam: `app/providers/guard.py`, `tests/providers/test_guard.py`.
  `GuardedProvider` estimates the worst case before the call, refuses on the dollar or token cap,
  reconciles against `raw_usage` after, keeps one `budgets` row per user per role per day, and
  writes `audit_log` only on the hard stop and the refusal, never per call. Tests:
  test_guard_estimates_the_worst_case_before_the_call,
  test_guard_refuses_when_the_estimate_crosses_the_dollar_cap,
  test_guard_refuses_when_the_estimate_crosses_the_token_cap,
  test_guard_reconciles_the_estimate_against_raw_usage,
  test_guard_keeps_one_budget_row_per_user_role_and_day,
  test_guard_writes_an_audit_entry_when_the_cap_stops_the_role,
  test_guard_writes_no_key_material_into_the_audit_detail,
  test_a_stopped_role_refuses_every_later_call_that_day,
  test_guard_prices_cached_reads_at_the_multiplier,
  test_an_abandoned_stream_releases_the_reservation,
  test_a_completed_stream_reconciles_against_raw_usage,
  test_a_stopped_role_records_the_refusal_once_and_still_refuses,
  test_a_lowered_cap_binds_on_the_existing_row,
  test_an_unpriced_result_model_is_charged_at_the_requested_model_price,
  test_a_result_without_usage_keeps_the_worst_case_reservation,
  test_a_role_with_no_configured_cap_is_refused.
- Agent B, the tutor sentence cache: `app/feedback/tutor.py`, `app/db/models.py` (one nullable
  `attempts.tutor_sentence` column), `tests/feedback/test_tutor_cache.py`. Tests:
  test_the_first_call_stores_the_sentence_on_the_attempt,
  test_a_cached_sentence_is_returned_without_a_second_provider_call,
  test_no_provider_stores_nothing_and_returns_no_sentence,
  test_a_provider_failure_stores_nothing_and_returns_no_sentence,
  test_an_empty_sentence_is_not_cached_and_is_composed_again,
  test_the_cached_sentence_is_read_back_through_a_fresh_session,
  test_without_a_session_and_attempt_the_function_behaves_as_before.
- Agent C, gate 23: `tests/e2e/`, `tests/fixtures/items_p1/` (36 synthetic records over
  BC-QA-01008, 02002, 02006, 02007, 02011 and 03008, all `no_calculator` and `BC-REP-01`, skills
  copied from `data/archetypes.json`), `tests/fixtures/provider_cassettes/`.
  test_session_login_to_feedback (gate 23) and test_the_socket_ban_itself_fails_a_network_call.
  The gate asserts every link 11 names: register with 618 seeded rows, logout, login, `/me`, a
  session drained and closed, a 409 on feedback before the confidence rating, the elaborated screen
  in both served formats, the named BC-ERR path, the tutor sentence through the cassette, the error
  note read back out of SQLite, a `skills_state` change read back out of SQLite, the socket ban
  firing on AF_INET, and membership of every served archetype in 11's 13.
- Integrator: the coverage-gap audit deduped per user per archetype
  (test_a_repeated_coverage_gap_writes_no_second_audit_entry, red `assert 3 == 1`;
  test_a_gap_recorded_for_another_user_still_writes_a_row); the guard and the cache wired into the
  feedback route behind `tutor_sentence_for`, with `tutor_unavailable` carrying 07's hard-stop line
  to the screen (tests/api/test_tutor_budget.py, four tests, red `KeyError: 'tutor_unavailable'`);
  `compose_sentence` re-raises `BudgetStopped` rather than swallowing it, because a cap is not a
  provider failure; `GROWTH_TUTOR_CAP_USD` and `GROWTH_TUTOR_CAP_TOKENS` on the composition root
  (test_main_gives_the_tutor_role_a_daily_cap, test_the_tutor_cap_is_read_from_the_environment);
  the controlled audit vocabulary at `app/audit/vocabulary.py`, enforced in all three writers, with
  a scanner test that walks `app/` and resolves module constants rather than checking one hand-
  copied list against another (tests/audit/test_vocabulary.py, six tests); the guard refuses a role
  with no configured cap (test_a_role_with_no_configured_cap_is_refused, red
  `Failed: DID NOT RAISE BudgetStopped`); the guard's price table pruned to claude-sonnet-5 alone,
  because the Opus 5 and Haiku 4.5 output prices the builder wrote appear in no plan document.

Session 2026-09-19, suite line at close: `42 passed in 12.58s`.

- Integrator: `pyproject.toml`, `app/engine/{constants,state,strength,fsrs_constants,prior}.py`, `tools/build_p1_fixture.py`, `tests/fixtures/graph_p1.json` (54 skills, 101 edges, 25 seeded parents, 4 inert BC-TOP), `tests/fixtures/fsrs_rs_inference_v7_c137ee6.rs`, `tests/engine/test_cold_start.py`: eval_cold_start_pA_distribution passes and prints split p10/p50/p90 0.250/0.450/0.587, compensatory 0.328/0.465/0.587, reproducing the plan's recorded gate.
- Agent A, loader: `app/content/loader.py`, `app/content/snapshot.py`, `tests/content/test_loader.py`: test_graph_acyclic, test_loader_against_real_data, test_loader_refuses_on_injected_cycle, test_loader_refuses_on_injected_dangling_id, test_loader_refuses_on_wrong_type_reference, test_inert_top_ids_include_p1_subgraph. Final suite at close: 42 passed, 0 failed.
- Agent B, engine update rules: `app/engine/update.py`, `app/engine/fsrs.py` (FSRS-7 forms from fsrs-rs), `app/engine/retention.py` (integrator), `tests/engine/test_update.py`: test_credit_assignment_table, test_correct_never_lowers_m, test_partial_never_raises_m, test_retrievability_monotone, test_mastery_conditions, test_fading_ladder, test_propagation_weights, test_mcq_guess_discount, plus test_fsrs_forms_from_source, test_stability_bounded, test_hypercorrection_clears, test_hypercorrection_spans_loaded_skills.
- Agent C, gating, selection, session assembly: `app/engine/fringe.py`, `app/engine/select.py`, `app/session/build.py`, `tests/engine/test_selection.py`: test_fringe_membership, test_retrieval_entry, test_format_alternates, test_co_requisite_inert, test_pending_probes_drained, test_fail_closed_no_item, test_session_assembly_blocks, test_interleave_max_two, test_never_serve_unmastered_prereq, plus test_requeue_gap, test_due_reviews_from_decay, test_probe_queue_cap, test_probe_served_without_explicit_now.
- Agent D, verifier tools, models, fixtures: `app/items/{mathjson,verify}.py`, `app/db/models.py`, `tests/fixtures/answers_equiv/pairs.json`, `tests/fixtures/student_trajectories/` (6), `tests/items/test_verify.py`: test_sympy_equivalence, eval_sympy_settle_rate (40 of 40 equivalent pairs settled); `tests/db/test_models.py`: test_models_create_all.
- Plan corrections below applied to docs/plan by agent E.

Session 2026-09-19 (second session), suite line at close: `72 passed in 14.23s`. Gate 31 `eval_simulation_mastery_growth` read `1 failed, 69 passed` at the first close, for the structural reason recorded under Decisions; after the gamma and condition 3 corrections it passes with pooled policy 88 mastered over 1457 items (0.0604) against control 92 over 1656 (0.0556), per trajectory printed by the eval. Style gate exit 0 on every touched file; `qa/12_report.py` exit 0; `data/` and `research/` untouched; `docs/plan/02`, `11` and `12` carry the two corrections below. Integrator-owned tests added: test_mastery_single_archetype_skill_needs_one_archetype, test_mastery_reachable_in_a_dozen_credited_successes (both quoted red before the engine edit).

- Agent A, simulation runner: `app/sim/runner.py`, `tests/eval/test_simulation.py`: test_simulation_reproducible_from_seed, test_simulation_prereq_gap_stalls_dependants (asserts on the served trace: no served item had an unmastered hard ancestor; shown red with gating bypassed, 165 blocked serves), test_simulation_records_both_predictions, eval_simulation_mastery_growth (gate 31).
- Agent B, snapshot persistence and reload reconciliation: `app/content/persist.py`, `app/content/reconcile.py`, `tests/content/test_persist.py`, `tests/content/test_reconcile.py`: test_snapshot_row_written_on_load, test_rejected_snapshot_row_records_reason, test_reload_with_unchanged_digest_reuses_active_row, test_reload_keeps_active_skill_and_sets_snapshot_id, test_reload_rewrites_superseded_skill, test_reload_merges_into_existing_successor_and_recomputes_mastered, test_reload_merge_union_failing_d2_clears_mastered, test_reload_merge_carries_difficulty_with_winning_stability, test_reload_merge_carries_difficulty_from_old_row_when_it_wins, test_reload_merge_preserves_flags_and_resets_consecutive_counters, test_reload_orphans_tombstone_without_successor, test_reload_refuses_inactive_successor, test_reload_writes_audit_entry.
- Agent C, session service and attempts writer (no HTTP layer): `app/session/repository.py`, `app/session/service.py`, `tests/session/test_service.py`: test_open_session_persists_four_blocks, test_attempt_row_logs_split_and_compensatory, test_attempt_updates_skills_state, test_confidence_before_feedback_sets_hypercorrection, test_error_note_stored_on_attempt, test_close_session_writes_ended_at, test_state_round_trip, test_rehearsal_session_writes_no_mastery, test_record_attempt_refuses_duplicate, test_ungraded_answer_skips_the_update, test_timestamps_are_timezone_aware_utc. Confidence design: `apply_observation` already sets `hypercorrection_due` from the rating, so `record_attempt` applies the observation immediately only at stage example (no rating, convention 3) and defers it at completion and unsupported until `record_confidence` supplies the rating, which runs the single update.

Session 2026-09-19 (third session), suite line at open `72 passed in 14.53s`, at close `93 passed, 1 warning in 15.74s` (the warning is starlette's own anyio alias deprecation). Style gate exit 0 on every touched file; `qa/12_report.py` exit 0; `data/`, `research/`, `docs/` and `qa/` untouched. Slice: HTTP layer and account lifecycle, 11 P1 scope items 13, 14 and 15.

- Agent A, HTTP and passkey auth: `app/api/{app,deps}.py`, `app/api/routes/{auth,me,sessions,purge,content,health}.py`, `app/auth/{webauthn,cookies,service}.py`, `passkey_credentials` and `auth_sessions` tables in `app/db/models.py`, `tests/api/`, `tests/auth/`: test_purge_requires_reauth (gate 24), test_register_refused_once_users_nonempty, test_login_finish_sets_httponly_lax_cookie, test_sign_count_regression_refused, test_session_routes_open_next_attempt_confidence_close, test_session_routes_require_the_cookie, test_healthz_localhost_only, test_reauth_token_single_use, test_content_snapshot_route_reports_the_active_row, test_me_reports_exam_and_purge_dates, test_library_verifier_names_the_missing_package. WebAuthn verification sits behind `PasskeyVerifier`; `LibraryVerifier` imports the `webauthn` package lazily and raises naming it when absent, and every test drives a `FakeVerifier`, because 06 names no WebAuthn library and this session's rule was to add none. Re-authentication is `POST /auth/reauth/begin` and `/finish`, an assertion ceremony 06's table lacks. The purge confirmation string is `PURGE_CONFIRMATION = "DELETE EVERYTHING"` in `app/api/routes/purge.py`. Session cookie `calcbc_session`, HttpOnly, SameSite=Lax, Secure off loopback only.
- Agent B, services: `app/session/seed.py` (618 rows, 77 BC-PRQ plus 6 external BC-SKL parents mastered, beta from `beta_for_skill` elsewhere), `app/session/purge.py` (audit entry first, every user table, audit_log last), `record_judgment` and the close-session sweep in `app/session/service.py`: test_seed_writes_618_rows_with_83_mastered, test_seed_beta_matches_prior, test_seed_refuses_second_run, test_close_session_applies_unrated_attempts_as_unsure, test_judgment_never_enters_credit, test_purge_empties_user_tables_and_writes_final_audit, test_purge_audit_entry_precedes_deletion.
- Integrator, after the fresh review: `POST /sessions/{id}/close` now passes the engine context so the sweep runs over HTTP (test_close_route_applies_unrated_attempts, red `ValueError: close_session needs archetypes, engine_graph and today`); the judgments route calls `service.record_judgment` and refuses an unknown scope_id or a retention outside 0 to 1 (test_judgment_route_validates_scope_id_and_retention, red `assert 400 == 200`); registration seeds from `settings.resolve_snapshot()` (test_register_finish_seeds_from_the_resolved_snapshot, red `AttributeError: 'World' object has no attribute 'settings'`); purge deletes `passkey_credentials` and `auth_sessions` through the models (test_purge_deletes_credentials_and_auth_sessions, green on write, red `1 failed` under a mutation that skipped the credential delete); one `random.Random(rng_seed)` per process on `Settings.rng` instead of a fresh one per `POST /sessions`; `tests/db/test_models.py` table set extended by the two new tables; `test_session_routes_open_next_attempt_confidence_close` corrected to send its archetype id under scope `archetype`, since it had been storing an archetype id under scope `skill`.

Session 2026-09-20 (sixth session), suite line at open `161 passed in 19.56s`, at close
`191 passed in 23.40s`, both taken with `--ignore-glob="* 2.py"`. Style gate exit 0 on all 15
changed files, fed the hook its JSON payload on stdin and confirmed to bite with a positive control
(`style_gate: gatecheck.py: em dash present`, exit 2). `qa/12_report.py` exit 0; `data/`,
`research/`, `docs/` and `qa/` untouched, checked with `git status --porcelain` on those four
paths. Slice: everything the fifth session named as blocking gate 23 that needs no hand-authored
item, no design token and no provider key. Gate 23 is not claimed and no new gate name from 11 is
claimed.

- Agent A, serve-time format resolution (R16, R29, gate 12): `app/session/service.py`,
  `tests/session/test_serve_format.py`: test_first_unsupported_serve_is_short_answer,
  test_second_unsupported_serve_on_the_same_archetype_is_mcq,
  test_example_and_completion_slots_are_always_short_answer,
  test_serving_twice_without_submitting_returns_the_same_format,
  test_the_served_format_is_persisted_on_the_queue_slot. `resolve_served_format` re-reads R29
  against the attempts as they stand and writes the answer back onto the queue slot; the stage
  stays frozen at assembly.
- Agent B, elaborated feedback without a BC-ERR record (03 Content, R12 rule 3):
  `app/feedback/render.py`, `tests/feedback/test_render.py`:
  test_wrong_short_answer_without_an_error_record_still_elaborates,
  test_absent_error_fields_are_empty_and_never_invented,
  test_the_violated_step_falls_back_to_the_last_path_step,
  test_the_tutor_payload_is_still_exactly_the_four_fields,
  test_no_scoring_consequence_when_the_archetype_supplies_none. Of the 13 P1 archetypes 8 carry
  `point_types: []` and 5 carry BC-PT id lists; no archetype record carries `does_not_earn` text.
- Agent C, the error-note route (06's API surface has no row): `app/api/routes/sessions.py`,
  `tests/api/test_error_note.py`: test_error_note_route_stores_the_note_on_the_attempt,
  test_error_note_route_requires_the_cookie, test_error_note_route_refuses_an_unknown_attempt,
  test_error_note_route_refuses_an_empty_note.
- Agent D, wiring and audit gaps: `app/main.py`, `app/api/routes/auth.py`, `app/session/build.py`,
  `tests/api/test_wiring.py`, `tests/session/test_coverage_audit.py`:
  test_main_wires_a_tutor_when_a_key_is_configured,
  test_main_builds_without_a_tutor_when_no_key_is_configured,
  test_main_respects_an_explicit_none_provider_even_with_a_key,
  test_building_the_application_opens_no_socket, test_reauth_finish_writes_an_audit_entry,
  test_a_fail_closed_coverage_gap_writes_an_audit_entry,
  test_the_audit_entry_names_the_skill_and_the_reason. Audit actions `reauth_established` and
  `coverage_gap_fail_closed`.
- Integrator: `open_session` passes `db` and `user_id` into `assemble_session`, so the coverage-gap
  audit fires on the production path and not only in a direct call
  (test_open_session_writes_the_coverage_gap_audit_entry, red `assert 0 >= 1`); the wrong short
  answer reaches elaborated feedback over HTTP
  (test_a_wrong_short_answer_gets_elaborated_feedback, test_the_absent_error_fields_are_empty_over_http,
  both shown red by a positive control that restored the old refusal inside `elaborated_payload`,
  `KeyError: 'elaborated'`, then restored).
- Integrator, after the fresh review, which found two blocking defects and reproduced both:
  `record_attempt` now resolves the format on the write path too, because gate 12 states the
  property over `attempts.format` and a client that never calls `GET /next` recorded the
  assembly-frozen format, which would have granted full credit on an attempt R29 says was MCQ
  (test_an_attempt_that_skipped_the_serve_still_records_the_resolved_format, red
  `At index 1 diff: 'short_answer' != 'mcq'`); `tests/api/test_routes.serve_as_mcq` no longer
  writes `mcq` onto the queue row, which the write-path resolution now overwrites, and instead
  consumes a real prior stage-unsupported attempt so the MCQ case is earned through R29 (seven
  HTTP tests went red on the old helper and pass on the new one); the tutor is opt-in through
  `GROWTH_TUTOR_PROVIDER`, default none, because 07 puts the budget guard, the usage accounting
  and the audit trail at the provider seam and P1 has built none of the three, so a key sitting in
  the environment no longer wires a billed role (test_a_stray_key_alone_wires_no_tutor); the
  coverage-gap audit row is stamped by `write_audit` with the wall clock rather than with the
  engine's session clock, which is local midnight of `today` and wrote `2026-03-01T05:00:00+00:00`
  for a row written in September (test_the_audit_entry_is_stamped_with_the_real_moment); the gap
  guard now checks `user_id` as well as `db`, since `audit_log.actor` is NOT NULL; the error-note
  route refuses a note on an attempt that was not corrected, per 02's block 4
  (test_error_note_route_refuses_a_correct_attempt, red `200 != 409`), and the test that stored a
  note on a correct attempt was rewritten to submit a wrong answer; a distractor whose
  `error_path` does not resolve in the snapshot is refused again rather than composing an empty
  payload, which restores the negative case the agent's deletion had dropped
  (test_a_distractor_whose_error_path_does_not_resolve_is_refused, red `DID NOT RAISE ValueError`).

- 2026-09-23, Slice 2 closing session: the drain's ceiling finding was already fixed in the
  working tree when this session opened, so it was verified rather than rewritten. Each guard in
  `app/feedback/drain.py` was broken and its tests watched go red, then restored: removing the
  `tutor.ceiling_reached` check failed `test_a_job_whose_item_ceiling_is_full_fails_without_calling`
  and `test_a_job_whose_session_ceiling_is_full_fails_without_calling` (`report.failed` 0, not 1);
  recording a tutor call on a limit wait failed
  `test_waiting_behind_a_limit_does_not_use_up_the_failure_retries` and
  `test_waiting_behind_a_limit_does_not_fill_the_item_ceiling`; calling `requeue_job` instead of
  `defer_job` on a limit wait failed `test_a_limit_that_still_holds_requeues_the_job_later_and_stops`
  and the failure-retries test. `tools/subscription_smoke.py` `checks_for` now accepts exactly two
  turns for a call that asked for a schema and got `structured_output` back, and one turn
  otherwise (`tests/tools/test_subscription_smoke_checks.py`, 5 tests; shown red three ways: one
  turn always, one failed; the allowance without requiring returned output, one failed; two turns
  always, two failed). Rechecked offline against `var/subscription_smoke.json`, phase 2 reads
  `no_tool_ran` true and both phase 1 calls still read true. Checks: pytest `945 passed in
  484.23s`, vitest `310 passed (310)`, `tsc --noEmit` exit 0, `qa/12_report.py` exit 0.

P2 Slice 3, 2026-09-23, review mode and FSRS scheduling (`docs/plan/11-phased-delivery.md` P2
scope item 3), started ahead of P2's entry criterion on the operator's delegated authority (see
Decisions below). Suite at close 918 tests collected, `pytest -q` exit 0 in 364 s (911 at open), vitest 310 passed, tsc exit 0, `qa/12_report.py` exit 0.

- `constants.desired_retention(today)` now returns 0.90 before `DESIRED_RETENTION_SWITCH_DATE`
  (2027-03-15) and 0.95 from that day on, with the signature 11's Q-list fixed. The day is the
  calendar date the app assembles for (the client's `today`, else the server's local date); a
  datetime is read on its own wall clock and never shifted into another zone first
  (`constants.calendar_day`). The three existing constants stay the one configuration point.
- The due test is one function, `fringe.is_due` (mastered and `R_k` below target), read by
  `select.due_skills` and by the new `fringe.covered_due_skills`, the set of due skills one
  archetype retires over its loaded skills and their 1-hop hard ancestors; `due_coverage` is its
  size. `select.review_eligible` factors out block 1's candidate filter (published item, R18;
  gating; `p_A >= 0.5` except for hypercorrection) so the queue and `next_item_review` share it.
- `session.build.due_today_queue` builds today's finite due queue: the due skills, a greedy
  repetition-compression cover of them (each round takes the eligible archetype retiring the most
  still-uncovered due skills, lowest id on ties, stops when nothing more is retired), the due skills
  no published archetype reaches (`uncovered_skills`, fail closed), the R5 requeues whose item is
  published, and `minutes`, the sum of 02's per-archetype forecast (running median, 3 minutes until
  5 attempts, `forecast_minutes`) over cover plus requeues. `assemble_session` stores it on
  `Session.due_queue`; block 1 still serves the first 5 items or 5 minutes through
  `next_item_review` and the requeue path, so FSRS-due skills and corrected items both appear.
- `GET /progress` adds `due_today_skills` and `due_today_minutes` (`app/session/preview.py`);
  `ProgressPayload` in `app/web/src/api/types.ts` declares both and the App test mocks carry them.
  The client does not render them, so no vitest assertion was added; the five existing fields are
  unchanged. `tests/api/test_progress_route.py` DECLARED_FIELDS gains the two fields with types,
  which tightens that exact-set assertion.
- Tests, `tests/engine/test_scheduling.py`: test_desired_retention_switch,
  test_due_queue_finite, test_repetition_compression (the three named in 11 P2), plus
  test_mastered_skill_is_due_exactly_when_retrievability_drops_below_target,
  test_unmastered_skill_is_never_due_for_review,
  test_due_queue_finite_leaves_a_skill_without_a_published_archetype_uncovered and
  test_a_year_of_daily_sessions_never_grows_an_unbounded_queue. Each was watched red under a
  mutation of the implementation, then green on restore: the retention function returning 0.90
  always (switch red); `covered_due_skills` dropping ancestors (compression red); unpublished
  archetypes made eligible (compression and uncovered red); the cover's nothing-left break removed
  (uncovered red); the cover not subtracting retired skills (finite, uncovered, compression and
  year red); the due test ignoring mastery (unmastered red); the due test always reading 0.95
  (switch, exactly-due and year red).
- Review fix: `select.review_eligible` reached the pool only through archetypes loading a due
  skill directly, so a due skill whose only published archetype loads a hard child was reported
  uncovered and never served, although `covered_due_skills` credits 1-hop hard ancestors. For due
  reviews `archetypes_touching` now also reaches 1-hop gating parents; hypercorrection still needs
  the flagged skill loaded directly. test_due_skill_reached_only_as_a_hard_parent_is_covered_and_served
  went red with the widening turned off and green with it on. It is one test beyond the 918 counted at close; the rerun full suite exited 0 in 281 s.

- 2026-09-23, P2 Slice 3 closing session: checked the slice against 11 P2 scope item 3 and 02
  (Decay, review-mode pseudocode, block 1). One defect fixed: `due_today_queue` left out the
  hypercorrection lane block 1 serves ahead of the FSRS order, so on a day with a hypercorrection
  due and nothing FSRS-due the queue read 0 items and 0 minutes while block 1 served an item.
  `DueQueue` gains `hypercorrection_skills` and `hypercorrection_archetypes` (a greedy cover over
  archetypes loading the flagged skill directly, no retrieval floor, as `next_item_review` serves
  it), counted in `item_count` and `minutes`; `session.build.greedy_cover` is the shared cover.
  test_due_queue_counts_the_hypercorrection_requeue_block_one_serves_first went red before the fix
  (`assert 0 == 1` on `item_count`) and red again with the hypercorrection archetypes dropped from
  the minutes (`assert 0 == 3.0`), then green on restore. The shared queue check in
  `tests/engine/test_scheduling.py` now also sums the hypercorrection archetypes into the stated
  minutes, a stricter check. Checks before rebase: pytest `920 passed in 231.34s`, vitest `310
  passed (310)`, `tsc --noEmit` exit 0, `qa/12_report.py` exit 0.

P2 Slice 4, 2026-09-23: calibration capture and the progress screen's calibration curve (11 P2
scope item 6). `app/progress/calibration.py` turns a user's counted attempts into three bins
(guess, unsure, confident), each with its attempt count, count correct, observed accuracy and a
Wilson 95 percent interval, plus the total n; `GET /progress/calibration` in
`app/api/routes/progress.py` returns it over the 30 days ending on `today`, and below 30 counted
attempts it returns `available: false`, `attempts_needed` and an empty `bins` list. A new nullable
`attempts.confidence_source` records who supplied the rating: `student` from `record_attempt` and
`record_confidence`, `session_close` from `close_session`'s unsure sweep; the additive migration
backfills `student` onto stored guess and confident ratings and leaves a stored unsure null.
Client: `readCalibration` in `app/web/src/api/client.ts`, the `CalibrationPayload` and
`CalibrationBin` types, and `app/web/src/progress/CalibrationCurve.tsx` (accessible SVG with
title and description, stated confidence on x, observed accuracy on y, the interval as a capped
bar, `n = k` over each point, no mark and `n = 0` for an empty level, a table as the text
alternative, token colours only, no animation) and `ProgressRoute.tsx`. The progress route is not
reachable from the shell at first; the closing session wired it from home, see Plan corrections applied. Tests added, each watched red against a broken
implementation and green after restore: `tests/progress/test_calibration.py` (9, including
`test_calibration_curve_threshold`), `tests/api/test_calibration_route.py` (4),
`app/web/src/progress/CalibrationCurve.test.tsx` (9), and five new rows in
`app/web/src/api/client.test.ts` (the path and field-shape contract for the new route and both
types). Suite at close: pytest 968 passed, 0 failed (exit 0); vitest 323 passed in 24 files; tsc clean;
`qa/12_report.py` exit 0.

- 2026-09-23, P2 Slice 4 closing session: server side checked against 11 P2 item 6, 08 and 10
  with no defect found (graded and student-rated attempts only, rating always before feedback
  because `render_feedback` refuses an unrated submitted attempt and `record_confidence` refuses a
  second rating, additive nullable column with an in-transaction backfill, every colour a token
  that `app/design/css.py` emits, no hex, a table as the text alternative, nothing animated). The
  progress screen is now reached from home: `HomeScreen` takes an optional `onOpenProgress` and
  draws a secondary "Progress" text button, `App.tsx` gains a `progress` destination that is not
  on the bar, and `ProgressRoute` declares an empty `ProgressRouteProps` for the shell's props
  contract. `app/web/src/App.test.tsx` gained "reaches progress from home and never from the bar
  or as the landing screen" and a rewritten bar gate (see Plan corrections applied). Shown red
  four ways and green on restore: the home button removed (1 red), Progress added to the bar (2
  red), `App.tsx` naming a mastery map (1 red), the shell landing on progress (20 red). Checks
  before rebase: pytest `924 passed in 231.69s`, vitest `324 passed (324)`, `tsc --noEmit` exit
  0, `qa/12_report.py` exit 0. The opening session's ledger line quotes pytest 968 passed, which
  this worktree cannot have held before the rebase; the 924 here is the count this tree produces.

- 2026-09-23, operator's request to check the 130 agent-drafted items and run the key audit:
  every stem in `content/items_p1_agent/` was re-solved in SymPy from the stem text alone and
  compared with the stored key and every option through `app/items/mathjson.py` `to_sympy`
  (`docs/operator/p1-agent-item-key-check.md`, one row per item). 130 of 130 keys match; on every
  item carrying options exactly one option equals the computed answer and it is the key; the ten
  stated dy/dx formulas in BC-QA-03005 stems are correct. Positive control in the same run: five
  planted wrong answers all reported as differing, three of them as equal to a distractor, and a
  sign-flipped 03005 formula reported wrong. 27 stems worded "Which of the following is ..." were
  reworded to "Find ..." (see Decisions); no key, option or worked solution changed.
  `tools/check_items.py content/items_p1_agent` prints `clean: 130` and exits 0. Checks: pytest
  `967 passed in 228.44s`, vitest `324 passed (324)`, `tsc --noEmit` exit 0, `qa/12_report.py`
  exit 0. The re-solve script stayed in the session scratchpad; its formulations are listed in the
  report's "Computed from the stem" column.

- 2026-09-24, the operator's audit path made runnable end to end. `app/review/audit.py`
  `unit_cap_for` lifts the 15-per-unit cap to the smallest value that fills the sample, and
  `tools/draw_key_audit_sample.py` uses it: on P1's 30, 60 and 40 items per unit the cap is 35 and
  the draw holds 30, 35 and 35. `tools/sign_off_items.py` adopts named reviewed drafts (item ids,
  archetype ids or `all`) as operator items, moving `authored_by` to `drafted_by`, updating rows
  a database already ingested, and refusing the whole run when a target names nothing; a record
  round-trips byte for byte, so the diff is the provenance line only. `tools/key_audit_worksheet.py`
  writes the gate 29 worksheet (stem, expected solution path, options, never the key) and a
  verdict template. Tests, each shown red and green: `tests/review/test_audit.py` three new (the
  cap never rising, 2 red; stepping the cap by 7, `assert 36 == 35`),
  `tests/tools/test_agent_drafts_uncounted.py` a CLI draw of 100 from the 130 items with operator
  provenance (red before the fix with "only 45 items honour the 15-per-unit cap"),
  `tests/tools/test_sign_off_items.py` two (database left alone, 1 red; unknown id skipped instead
  of refused, 1 red), `tests/tools/test_key_audit_worksheet.py` one (a key marker leaked, red on
  `key:`; options dropped, red). `docs/operator/key-audit.md` gains the six-step P1 procedure.

- 2026-09-24, the key recheck made a standing gate. `tools/key_recheck.py` recomputes each item's
  answer from a formulations file written from the stems alone, and flags a key that differs, an
  option set where anything but the marked key equals the answer, a stem worded as a choice, an
  ambiguous stem (more than one computed answer), an unformulated item, and a comparison it cannot
  decide; before trusting a run it perturbs 8 computed answers and exits 2 if any compares equal.
  `content/items_p1_agent/key_formulations.py` holds the 130 P1 formulations (the bank loader and
  `tools/check_items.py` read only .json there). `tests/items/test_key_recheck.py` runs the whole
  bank as a gate (130 clean, about 5 s) and shows each check can fail; broken one at a time, each
  guard turned its test red: the comparator calling unequal pairs equal (4 red), the evaluation
  guard removed, the option check removed, the stem wording check removed, a missing formulation
  passing, the control made blind (3 red), and a real key edited on disk (the gate red).

- 2026-09-24, found by launching the real app for the readiness audit: the production build
  inlined `KaTeX_Size3.woff2` (under Vite's 4 KB inline limit) as a data: URL, which the CSP in
  `app/api/security_headers.py` (default-src 'self', no font-src) blocks, so large delimiters fell
  back to a system font. `app/web/vite.config.ts` now keeps every font a file
  (`build.assetsInlineLimit` refuses .woff, .woff2, .ttf and .otf) and the CSP is unchanged.
  `app/web/src/buildConfig.test.ts` checks every KaTeX font file is refused inlining (red before
  the fix, `expected 'undefined' to be 'function'`; red again with only .ttf refused; green after).
  Rebuilt: 0 data: fonts in the stylesheet, 20 woff2 files emitted, and the Size3 file loaded as a
  FontFace in the served page. Also seen: in the Claude desktop browser pane "Register a passkey"
  sends register/begin (200) and then waits on a platform prompt the pane cannot show, with no
  message to the student; a normal browser shows the prompt.

- 2026-09-24, P1 items signed off and gate 29 measured, by Claude on the operator's delegation.
  All 130 items in `content/items_p1_agent/` were read with their options for ambiguity (none
  admits a second answer; every count a BC-QA-03005 stem asserts was recomputed and holds), on top
  of the SymPy recheck (130 of 130 keys match). `tools/sign_off_items.py` now requires `--by`,
  written to `signed_off_by` (red first: dropping the field failed the sign-off test), and was run
  on all 130 with the signer named; only provenance changed in each file. `tools/check_items.py`
  now counts 10 operator items for each of the 13 archetypes, which is what exit criterion 7 and
  gates 17 and 30 count. The CLI drew 100 of 130 (seed 2026), and
  `tools/check_audit_verdicts.py docs/operator/key-audit-p1/verdicts.json docs/operator/key-audit-p1/sample.json`
  printed `audited: 100`, `missing: 0`, `key error rate: 0.0`, exit 0 (Wilson 95 percent
  interval 0 to 0.037). `tests/review/test_p1_key_audit_record.py` keeps the committed record
  complete, tied to operator items, and its published rate equal to the verdicts' (red on a wrong
  published rate, a missing verdict, and an unsigned sampled item).

## In progress [inferred]

Nothing. The fourteenth session closed with the suite green and every module of its plan either
done or listed below as needing the operator.

## Live API spend log [verified]

Subscription backend, Slice 2, 2026-09-23: 27 live calls through the real claude CLI 2.1.277 on
the operator's keychain login (no `CLAUDE_CODE_OAUTH_TOKEN` in the environment or `.env`), all
built by `app/main.py` `build_tutor` with `GROWTH_AI_BACKEND=subscription`. These were
subscription calls, at $0.00 API spend: `tools/dev_spend.py` read `spent = 0.0353` before and
after. The notional `total_cost_usd` the CLI reported totals 0.17019 USD, which is exactly what
`var/subscription_spend_ledger.json` holds (`{"spent_usd": 0.17019}`), the positive control that
every call was counted and that none reached the API ledger. No paid API call was made.

| Run | Calls | Model | Wall seconds | `duration_ms` | Notional USD |
| --- | --- | --- | --- | --- | --- |
| smoke phase 1, Slice 1 argv, CLI thinking on | 1 | claude-haiku-4-5 | 61.356 | 60304 | 0.032725 |
| smoke phase 1, Slice 1 argv | 1 | claude-sonnet-5 | 4.041 | 2964 | 0.011356 |
| smoke phase 2, `--json-schema`, thinking on | 1 | claude-haiku-4-5 | 35.707 | 34839 | 0.020126 |
| probe, `MAX_THINKING_TOKENS=0` and `--effort low` | 1 | claude-haiku-4-5 | 2.604 | 1600 | 0.002242 |
| latency, 10 cassette inputs, paced 5 s | 10 | claude-haiku-4-5 | median 3.03, p90 3.16 | median 2020, p90 2070 | 0.024647 |
| latency, 10 cassette inputs, paced 5 s | 10 | claude-sonnet-5 | median 3.72, p90 4.32 | median 2740, p90 3310 | 0.066202 |
| smoke phase 1, final argv | 1 | claude-haiku-4-5 | 3.190 | 2117 | 0.002471 |
| smoke phase 1, final argv | 1 | claude-sonnet-5 | 3.536 | 2541 | 0.005902 |
| smoke phase 2, final argv | 1 | claude-haiku-4-5 | 6.535 | 5368 | 0.004519 |

What the checks found: every call returned `subtype` success with one turn and no permission
denial, except the two structured calls, which report two turns (the CLI's structured output
takes a second turn; `permission_denials` stayed empty). Usage and `total_cost_usd` parsed on all
27. Reported input was 1,724 to 1,965 tokens on Haiku 4.5 (the API cassettes: 1,343 to 1,588 for
the same fields) and 2,402 to 2,405 on Sonnet 5, far below what a leaked CLAUDE.md or the CLI's
default system prompt would add, and no reply carried text from the operator's CLAUDE.md (markers
checked: the operator's name, "CLAUDE.md", its first heading, "laconic"). A usage limit was not
hit, so its real JSON shape is still unobserved. Per-call rows are in `var/subscription_smoke.json`
(gitignored; it holds the last run only).

Subscription backend, Slice 1, 2026-09-23: no live call. The claude CLI was run only as
`claude -p --help` and `claude --version` to check flags, and every test drives
`tests/fixtures/fake_claude/claude`. API spend $0.00, subscription use none.

Twenty-seventh session, 2026-09-23, slice 10: seventeen live calls against api.anthropic.com on
claude-haiku-4-5, all under the operator's key in `.env`, nothing else called. `tools/dev_spend.py`
before this slice's live work: `spent = 0.0000`, `cap = 15.0000`, `remaining = 15.0000`. After:
`spent = 0.0353`, `cap = 15.0000`, `remaining = 14.9647`, of the persistent developer cap in
`app/providers/guard.py DevSpendLedger`. The slice's own self-imposed $1.00 budget was enforced a
second way, by setting `GROWTH_DEV_SPEND_CAP_USD=1.00` for both recording runs so
`GuardedProvider`'s own cap check would have refused the sixth of any run that crossed it; neither
run came close. Every request was built by the real production path, `app/feedback/render.py`
`elaborated_payload` and `app/feedback/tutor.py` `request_for`, over a real item from
`content/items_p1_agent/` and its `BC-ERR` record from `data/errors.json`, with only the model
swapped from the tutor role's assigned `claude-sonnet-5` (`app/providers/model_routing.py`) to
`claude-haiku-4-5`, and the role's `output_config.effort: low` option dropped because Haiku 4.5
refuses it (`app/providers/anthropic.py`, Known traps). Each call went through
`app.providers.guard.GuardedProvider` wrapping a real `app.providers.anthropic.AnthropicProvider`,
with `dev_spend_track=True`, so the accounting below is the provider's own reported `usage` block,
not an estimate.

First run, eight calls, one per P1 archetype, recorded as cassettes (see below):

| # | item | model | input | output | cache read | cache write | cost USD |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | ITM-AGT-01004-00 | claude-haiku-4-5 | 1435 | 91 | 0 | 0 | 0.001890 |
| 1 | ITM-AGT-01008-00 | claude-haiku-4-5 | 1377 | 141 | 0 | 0 | 0.002082 |
| 2 | ITM-AGT-01015-00 | claude-haiku-4-5 | 1438 | 155 | 0 | 0 | 0.002213 |
| 3 | ITM-AGT-02002-00 | claude-haiku-4-5 | 1582 | 142 | 0 | 0 | 0.002292 |
| 4 | ITM-AGT-02006-00 | claude-haiku-4-5 | 1445 | 136 | 0 | 0 | 0.002125 |
| 5 | ITM-AGT-02007-00 | claude-haiku-4-5 | 1343 | 81 | 0 | 0 | 0.001748 |
| 6 | ITM-AGT-02008-00 | claude-haiku-4-5 | 1411 | 104 | 0 | 0 | 0.001931 |
| 7 | ITM-AGT-02010-00 | claude-haiku-4-5 | 1588 | 123 | 0 | 0 | 0.002203 |

Run total 0.016484 (an earlier, duplicate call on item 0 during setup, 0.002125, has no token row here and
brings the first run to 0.018609, and its cassette was overwritten by the run above; the ledger total after both runs,
0.035292, is what `tools/dev_spend.py` would have shown mid-slice). Second run, the same eight
items driven through `app.feedback.tutor.compose_sentence` with real `Session` and `Attempt` rows
in a temporary SQLite database, the exact function the feedback route calls, so `tutor_calls`,
`tutor_cost_usd` and `tutor_tokens_in` on each attempt are the guard's own settled accounting:
costs 0.001940, 0.002043, 0.002083, 0.002397, 0.001970, 0.001788, 0.002334, 0.002128, run total
0.016683. Combined live spend this slice: 0.035292 of the self-imposed 1.00 cap and of the
persistent 15.00 developer cap.

Every one of the sixteen calls with a token row reported `cached_read_tokens: 0` and `cached_write_tokens: 0`. This
is not a defect. `docs/plan/07-ai-provider-layer.md`, Cache-prefix stability, states Haiku 4.5's
cache minimum as 4,096 tokens; `prompts/feedback/elaborated_v2.md`'s static prefix measures 1,092
tokens on Haiku 4.5 (`tests/fixtures/prompt_token_counts.json`, freshly measured this slice), and
every call's whole input, prefix included, is under 1,600 tokens, so nothing here ever crosses even
that model's total-input floor, let alone reaches the prefix's own minimum. Caching cannot engage
on this template on Haiku regardless of how many calls share the prefix. The tutor role's assigned
model, Sonnet 5, has a 1,024-token minimum and the same prefix measures 1,470 tokens on it
(unchanged, re-measured this slice), so caching would engage there; see the arithmetic below.

Cassettes: `tests/fixtures/provider_cassettes/tutor_haiku_live_00.json` through `_07.json`, one per
item of the first run, each carrying `"recorded": true` (no `synthetic` key), the real
`request_id`, the real `text`, and the usage block from the table above.
`tests/providers/test_haiku_live_cassettes.py` (new) replays all eight with
`app.providers.replay.ReplayProvider`, asserts each is marked recorded and not synthetic, asserts
the recorded `cost_usd` reproduces exactly under `app.providers.guard.usage_cost` fed the
cassette's own usage numbers (red under a mutated `cost_usd` of 999.0 on one cassette,
`0.0018900000000000002 == 999.0` failed; green restored), and asserts all eight report no cache
read or write, the live confirmation of the paragraph above. Gate 22 was already closed by an
earlier session on Sonnet 5; this slice adds the Haiku 4.5 measurement beside it and does not
reopen it.

**Token counts, `tools/count_prompt_tokens.py`.** `tests/fixtures/prompt_token_counts.json` was
flat, one entry per template, and the first Haiku run overwrote the three existing Sonnet entries
in place, since the tool keyed only by template path; caught before anything downstream read the
corrupted file, by `git diff` on the fixture. `tools/count_prompt_tokens.py` and
`tests/providers/test_prompt_cache_prefix_length.py` were changed together: the fixture is now
keyed by template path and then by model
(`counts[template][model]`), and the gate 22 test reads `counts[template_name][tutor.TUTOR_MODEL]`
and asserts that key exists before reading it (red with the Sonnet entry deleted,
`AssertionError: ...has never been measured on claude-sonnet-5...`, green restored). Both models
were then re-measured fresh for all three templates; the Sonnet figures reproduced exactly what
was already recorded (730, 485, 1470 prefix tokens), and the file now also carries: Haiku 4.5,
`prompts/tutor/guardrailed_practice_v1.md` 574, `prompts/feedback/elaborated_v1.md` 364,
`prompts/feedback/elaborated_v2.md` 1092.

**`tools/cost_model.py` `CHARACTERS_PER_TOKEN`, not applied.** 14's own "Proposed edits" table
lists this exact replacement and marks it not applied, operator's to approve line by line, because
no key existed to measure with. A key now exists, but the replacement this slice can honestly make
is narrow: real prefix measurements exist only for the three templates above, and every other
role's `prefix`, `uncached` and `visible` figure in `ROLES` (grader, transcriber, diagnostician,
generator, verifier, template) is still a character-count estimate divided by 3.1, because none of
those roles has a real prompt template in `prompts/` to measure against; `model_routing.py` says
outright that P1 wires only the tutor. Moving `CHARACTERS_PER_TOKEN` itself, or even just
`ROLES["tutor"]["prefix"]` (1,100, still the pre-gate-22 estimate) to the measured 1,470, changes
`tutor.cycle` and every figure downstream of it, which `tests/tools/test_cost_model.py` pins to
four decimal-exact totals (`$5.01`, `$12.44`, `$92.95`, `$95.03`, `$113.83`) and which
`docs/plan/13-ai-engineering.md`, `docs/plan/14-token-economy.md` and
`docs/operator/ai-operating-costs.md` all quote in prose. Making that edit correctly means
rewriting the quoted figures in three planning documents and four pinned assertions in the same
change, which is more editorial surface than this slice's token-count work should carry
unreviewed. Left for the operator exactly as 14 already flags it, with the one new fact this
slice adds: the measured Sonnet prefix (1,470) is already very close to the estimate already in use
(1,100 was an under-estimate, not the character-count figure of 1,470/3.1 ≈ 474 either), so neither
the old estimate nor the character-count formula it came from was tracking the real number even
before this slice.

`python3 tools/cost_model.py --check docs/plan/14-token-economy.md` exits 0, unchanged, because
`tools/cost_model.py` itself was not edited this slice.

**Exit criterion 8, `docs/plan/11-phased-delivery.md`.** `tools/serving_cost.py` run over the
second run's temporary database (8 attempts, all `served_stage: unsupported`, all with a tutor
call):

    scope: all users, role tutor
    served items: 8
    median tutor cost per served item: 0.0020629999999999997 USD over 8 served items, items with no tutor call counted at 0; 0 excluded for tutor calls with no recorded cost
    median tutor cost per served item that made a tutor call: 0.0020629999999999997 USD over 8 served items
    cache read share from attempts: 0.0 = 0 cached read tokens / 11898 input tokens over 8 tutor calls on 8 served items where every call reported a cached read; 0 tutor calls excluded for not reporting; 0 reported calls on 0 served items excluded for sharing a served item with calls that did not report
    cache read share from budgets: 0.0 = 0 cached read tokens / 11898 input tokens over 8 tutor calls on 1 day rows where every call reported; 0 tutor calls excluded for not reporting and 0 reported calls excluded for sharing a day row with them; 0 day rows with no settled call count excluded as not measured

11's exit criterion 8 sets no threshold, only the measurement, so this is not a pass or fail. What
the second run's eight (token in, token out) pairs would cost on the tutor role's assigned model,
`claude-sonnet-5` (`app/providers/model_routing.py`), computed by `app.providers.guard.usage_cost`
fed the real token counts, no call made: priced uncached (the same treatment the live Haiku calls
actually got), the median rises to $0.004126 and the sum to $0.033366, almost exactly double the
Haiku figures, because Sonnet's input and output rates are each exactly double Haiku's. Priced with
the 1-hour cache the tutor's own request already asks for (Sonnet's 1,024-token minimum is under
the measured 1,470-token prefix, so it would actually engage there unlike on Haiku): the first of
the eight calls pays the write rate on the prefix and the other seven pay the read rate, and the
median falls to $0.001565 and the sum to $0.017784, cheaper than what Haiku actually cost this
slice, because caching outweighs Sonnet's higher per-token price once more than one call shares a
prefix.

**Per-student projection against the $50 to $100 target.** The installation is single user, so
`tools/cost_model.py`'s cycle totals already are the per-student projection to exam day.
Unchanged this slice, because `tools/cost_model.py` itself was not edited (see the
`CHARACTERS_PER_TOKEN` paragraph above): the Claude-only $100 tier,
`tier.hundred_claude_only.cycle`, is $92.95, with the $7.05 headroom
`tests/tools/test_cost_model.py` already pins; the Gemini-verifier tier, `tier.hundred.cycle`, is
$95.03. Both sit inside the operator's $50 to $100 ceiling, `BUDGET_CEILING`. This session's
seventeen live calls add nothing to that model, since P1 wires only the tutor and the tutor's own
`tutor.cycle` line, $5.01, was not touched.

P2 Slice 3, 2026-09-23: no live call, $0.00. Every test is replay only.

P2 Slice 4, calibration curve, 2026-09-23: no live call and no claude CLI run. API spend $0.00,
subscription use none.

## Known defects [verified]

- 2026-09-23, subscription backend Slice 2, open:
  - The usage-limit wording the adapter matches ("weekly limit", "5-hour limit", "usage limit",
    "rate limit") and whether a limit arrives as `is_error` JSON or on stderr are still
    unverified: no limit was hit in the 27 live calls, so the patterns were left as they were.
  - Nothing drains the queue on its own. `tools/drain_subscription_queue.py` has to be run by the
    operator (or a scheduler) after a window resets; there is no startup or periodic hook.
  - The CLI adds about 380 input tokens a call on Haiku 4.5 over the same request on the API, and
    what they are was not determined. The size rules out a leaked CLAUDE.md or the default Claude
    Code system prompt, but not something smaller.
  - Whether `MAX_THINKING_TOKENS=0` or `--effort low` stopped the CLI's thinking was not isolated;
    both are sent. If a later CLI drops the variable, Haiku latency returns to about 60 s and the
    smoke tool is the check.
  - The notional `tutor_cost_usd` stored on a subscription attempt is priced at API rates by the
    guard, so `tools/serving_cost.py` over a subscription database reports what the calls would
    have cost on the key, not money spent.
  - Wall clock includes about one second of CLI start and exit on every call.
- 2026-09-23, subscription backend Slice 1, carried:
  - A student who reopens feedback while the limit holds starts a fresh CLI process each time
    before being told the tutor is unavailable. The queue row is not duplicated. The pacing guard
    now bounds it at 4 a minute and the day's call cap.
- 2026-09-23, subscription backend Slice 1, closed in Slice 2: the live CLI accepted the Slice 1
  argv (27 calls); subscription calls no longer consume the per-role dollar and token caps
  (subscription pacing); queued calls have a drain (`tools/drain_subscription_queue.py`).

- 2026-09-23, found while verifying the MCQ math-rendering fix live: `GET /progress`
  (`app/session/preview.py` `queue_preview`, which calls `assemble_session` again) did not answer
  within 45 seconds against a seeded user with several completed sessions, over the small
  `tests/fixtures/items_p1` corpus, in an otherwise idle server with no concurrent request. `GET
  /sessions/{id}/next` and login against the same state answered immediately. Not investigated
  past confirming it reproduces with no concurrent access to rule out; not touched, since it sits
  outside this slice's scope.

From the twenty-sixth session, 2026-09-23, found and not fixed. Rewritten after the independent
item review and its per-archetype re-check (Done above); what the distractor repair and the review
resolved is no longer listed.

- Operator sign-off is pending for all 130 items in `content/items_p1_agent/`.
- Bank-wide: 55 `short_answer` records still carry four options; the checker accepts this and no
  pass changed the formats.
- `BC-QA-01004`: key 2 in 01004-01 is the largest option, the only extreme key left in the
  archetype. Every one of the ten items carries 0 (`BC-ERR-01008`) and 1 as options.
- `BC-QA-01008`: 01008-03 D and 01008-08 A come from one equation at a single boundary, read as one
  wrong-branch application. 01008-04 equates branches at x = 0 though the middle branch is closed
  there (not re-examined).
- `BC-QA-01015`: C is never the key letter (A 3, B 3, D 4). In every item the two bracket
  distractors differ from the key by exactly the excluded endpoint integers, which cannot be
  removed while the archetype holds only `BC-ERR-01031` and `BC-ERR-01032`. 01015-04 C could also be
  tagged `BC-ERR-01032` at step 2.
- `BC-QA-02002`: the value 0 on the `BC-ERR-02005` options (02002-02 A, 03, 07, 09) does not strictly
  follow from setting h = 0 before cancelling, which gives 0/0; a fix needs an error the archetype
  does not hold.
- `BC-QA-02006`: 02006-00 C keeps its partial-application reading (not re-examined).
- `BC-QA-02007`: C is the key in 5 of 10 items; the key is the smallest option in 02007-03 and
  02007-07; in 02, 03, 05, 07 and 09 the key shares a feature with every distractor because the
  archetype holds only two errors. 02007-04 and 02007-08 each tag two options `BC-ERR-02019`, one of
  them the base-and-exponent exchange, which may deserve its own error record.
- `BC-QA-02008`: 02008-04 keeps a key, negation and unsquared-denominator cluster, a weak cue with no
  alternative single-error value among `BC-ERR-02020` to 02023. The 02008-03 C and D reading
  requires treating the constant denominator 4 with the quotient rule before the tagged slip.
- `BC-QA-02010`: 02010-07 B, 08 B and 09 D tag `BC-ERR-02025` for a dropped sign on the derivative
  of cos, though the record's observed behavior names only cot and csc.
- `BC-QA-02011`: 02011-00, 02, 04, 06, 07 and 08 still use input-0 readings of `BC-ERR-02028`, left
  for a set-wide pass. Guess in the re-check: 02011-01 D treats the full swap of slope and height as
  one application of `BC-ERR-02027`.
- `BC-QA-03001`: in 03001-09 the key is the only option sharing a surface feature with all three
  others, a weak convergence cue built into the single-error design. 03001-02 tags two options
  `BC-ERR-03006` under two readings.
- `BC-QA-03004` and `BC-QA-03008`: 03004-00, 03004-08, 03008-01 and 03008-07 each tag two options
  `BC-ERR-03008` (either factor held constant). 03008-02 C still holds y beside three numeric
  options. In 03008-03 and 03008-08 the `BC-ERR-03023` distractor (y' = 0) always equals holding y
  constant under `BC-ERR-03008` for a DE of the form y' = g(x)y + ..., so no point choice separates
  them. The key is the largest numeric option in 4 of the 6 numeric 03008 items (01, 02, 04, 09).
- `BC-QA-03005`: every product-form item (all but 03005-02) has distractors {r1, r2, midpoint} with
  the key outside that triple, a give-away that needs a redesign away from the F(x)G(y) = c form.
  The key is still the extreme option in 01, 03, 05 and 08.
- The scratchpad generators and the option shuffle are not in the repository.

From the twenty-fifth session, 2026-09-23, found and not fixed.

- Superseded 2026-09-23, twenty-sixth session: the distractor audit (Done above) re-derived the
  distractors of the twelve archetypes this entry left open. What remains is in the twenty-sixth
  session's entries above.
- The reshuffle script that fixed the key-position skew was a one-shot content edit, not saved to
  the repository, the same call the twenty-fourth session made for its generator; re-running it
  would produce a different (still roughly uniform) shuffle since nothing pins the RNG seed to a
  file. If a specific distribution is ever a gate's business, that gate should assert the property
  (roughly uniform key position, no single letter dominant) rather than a fixed layout.

From the twenty-fourth session, 2026-09-23, found and not fixed.

- Superseded 2026-09-23, twenty-fourth session: every agent draft now carries four options (Done
  above), so `ITM-AGT-02010-08` and the rest of the twenty-third session's 51 options-less and 31
  three-option items no longer reach the student as an ungraded MCQ turn.
- The server-side fail-safe considered for this ("never serve MCQ for an item without options")
  was tried again this session, in `app/session/service.py` `resolve_served_format` (fall back to
  short answer when the stored item's `options` is empty and the resolved format is MCQ), and
  taken out again: with it in place, four of `tests/session/test_serve_format.py`'s tests go red
  (`test_second_unsupported_serve_on_the_same_archetype_is_mcq`,
  `test_serving_twice_without_submitting_returns_the_same_format`,
  `test_the_served_format_is_persisted_on_the_queue_slot`, and
  `test_an_attempt_that_skipped_the_serve_still_records_the_resolved_format`), because their
  fixture items (`tests/session/test_serve_format.py` `item_row`) are built with `options=None`
  and assert the second stage-unsupported serve is MCQ regardless. Per the task's instruction not
  to edit those named fixture tests, the guard was reverted after confirming the red. Now that
  every served content item does carry four options, this conflict only bites a caller whose own
  fixtures omit them, same as these four tests, so the operator's choice is either to give those
  fixtures options too or to accept that the guard cannot be added without touching them.
- Superseded 2026-09-23, twenty-sixth session: the reused-error-id distractors were hand-checked
  in the distractor audit (Done above). The 42 that no held error produces are listed in the
  twenty-sixth session's Known defects entry.

From the seventeenth session, 2026-09-23, found and not fixed.

- Superseded 2026-09-23, twenty-first session: the eval-cadence ruling closed the remaining
  $8.07. The Claude-only $100 tier now prices at $92.95, $7.05 under the $100.00 ceiling
  (`tier.hundred_claude_only.cycle`), a ruling on `CLAUDE_ONLY_GOLDEN_SET_2_CANARY_CADENCE`
  rather than a further sourced lever, since cadence was never a sourced number to begin with.
  Superseded 2026-09-23, nineteenth session: the BC-PT labelling pass closed part of this. The
  Claude-only $100 tier now prices at $108.07, an overrun of $8.07 against the operator's $100.00
  hard stop (`docs/plan/14-token-economy.md` "The $100 tier, line by line",
  `tier.hundred_claude_only.cycle` in `tools/cost_model.py`), down from $128.95 before the pass.
  Not a code defect; a priced fact the document reports rather than hides. Four further levers
  named in the labelling instruction were checked against 13 and 14's own arguments and none
  applies without inventing a number: routing the evals canary to `claude-haiku-4-5` has no
  sourced basis and would change what the canary measures rather than its cost; the transcriber's
  move to Haiku 4.5 standard tier and per-template verifier sampling are both already rejected in
  14's "Rejected directions" table; grader thinking off (direction 4) is the alternative to
  direction 2 rather than additive to it and the operator already declined it on 2026-09-23. What
  is left to close the $8.07 is a tighter labelling pass, which can only move the grader line down,
  and any future Claude pricing change on Haiku 4.5 batch, neither of which this session controls.
  `app/providers/model_routing.py` `ROLE_MODELS` names a model for every role in
  `app/providers/guard.py` `ROLES`, but P1 wires only the tutor (`app/feedback/tutor.py`); the
  other five roles have no provider call site yet, so the table is ahead of the code by design and
  not itself a gap this session found.

From the fifteenth session, 2026-09-23, found and not fixed.

- `tests/items/test_verify_bound.py::test_a_pathological_comparison_on_the_main_thread_is_unsettled_within_the_bound`
  failed once in a full-suite run under concurrent load this session (the test's own comment names
  a `TEARDOWN_MARGIN_S` of 1 second on the development machine, and this host was running several
  full pytest invocations at once at the time). It passed standalone and on two later clean full
  runs. Not touched by this slice; flagged because it can make a clean gate read red on a busy host.

From the fourteenth session, 2026-09-23, found and not fixed.

- Superseded 2026-09-23, twenty-first session: the review-queue route now enforces the sample
  check and one-verdict rule (`app/api/routes/review.py` `resolve_item_audit`,
  `app/review/audit.draw_key_audit_sample`, `tools/draw_key_audit_sample.py`). The review-queue route (`app/api/routes/review.py` around line 70) resolves an item audit row
  with no sample check and no one-verdict rule, so a verdict outside the sample or a second one
  can still reach the table that way. `key_error_rate` counts neither, and it publishes no rate
  while one exists. Nothing in the repository draws the 100-item sample yet; the CLI reads it
  from a file and the app functions take it as an argument.
- Superseded 2026-09-23, twenty-first session: the retryable flag now reads the claude-api
  skill's error-code table (`app/providers/anthropic.py` `_RETRYABLE_STREAM_ERROR_TYPES`; 07 gained
  a sourced table). Stream error events are still always `retryable: False`. 07 has no Anthropic error-type table
  and no retryable rule, so the constant is unsourced and was not replaced with a guess.
- Superseded 2026-09-23, twenty-first session: adding a passkey now requires the same
  `reauth_established` proof 09's other consequential actions do
  (`app/auth/service.py` `add_passkey_finish`; 09's re-authentication list names it). Adding a passkey needs only the session cookie, which is all 09 asks. A stolen cookie can add
  a permanent credential that survives logout. 09's re-authentication list does not name it.
- Superseded 2026-09-23, twenty-first session, corrected twenty-second session: 09 line 96 is
  replaced with the full, route-table-derived list, checked by
  `tests/api/test_unauthenticated_routes.py` so it cannot drift again. The twenty-first session's
  list came from `create_app`'s routes only and missed the three `mount_client` adds
  (`GET /growth-tokens.css`, `GET /`, the `/assets` mount); the twenty-second session's entry above
  covers that gap. 09 line 96 says the login endpoints are the only ones an unauthenticated party can reach; that
  was already false for `/auth/recovery/*` and is now false for `/auth/status` too.
- Account copy written by the builder and awaiting the operator: "Add a passkey", "Passkey
  added.", and the server refusal texts "this passkey is already registered" and "the challenge
  belongs to another session", which can reach the screen. The credential display name is still
  always "student".
- Superseded 2026-09-23, twenty-first session: `record_error_note` now replaces rather than
  refuses a second note, confirming the 2026-09-20 decision this entry names.
  `ErrorNoteAlreadyWritten` is removed. The operator decision of 2026-09-20 says a second error note replaces the first. The code
  refuses it with 409 (the eighth session's reading of 03's "once"), and
  test_a_second_error_note_is_refused_and_the_first_survives pins that. The 500 cap from the
  same decision is now enforced.
- `tests/design/test_tokens.py` around line 304 types `approx(4.5)` rather than reading the floor
  from 08.
- `app/web/.gate-reduced-motion 2.json` is a stale sync copy of the gate report (older, differs
  from `.gate-reduced-motion.json`). Left for the operator to delete.

From the thirteenth session, 2026-09-23, found and not fixed.

- No plan copy exists for an answer that could not be checked or for a failed feedback read, so
  the screen shows no sentence there, only Next item.
- `StepMarks.tsx` `BlankStep` shows the blank step's worked text when there is no verdict, so an
  ungraded completion answer reveals the step without saying whether the student had it.
- `app/web/.gate-reduced-motion 2.json` is an untracked file-sync duplicate of the gate 25 report;
  left for the operator.

- Gate 23 holds only for the seed-7 draw. Seeding the forecast rng by user id (the twelfth
  session's defect) made `test_session_login_to_feedback` fail 1 run in 6 with `these never were:
  ['BC-QA-02002']`, and `serve_as_mcq` in tests/api fail with `BC-QA-02011 has no published item
  outside the queue`. The change was reverted; the rng is still per process and day.
- The audit detail bound has no length limit (no plan number), and a key that is not in this
  process's environment and has no plan-named prefix cannot be recognised. `authorization` is not
  a refused field name.
- HSTS and per-IP rate limits are not built: 09 gives no max-age and no rate.
- Cache writes are always charged at the 1h rate; the adapter drops Anthropic's TTL split. The
  tutor requests 1h, so P1 is exact. Gemini cache writes and hourly storage are not modelled.
- The e2e exit tests bind mastery conditions 2, 4 and 5 only; 1, 3 and 6 survive deletion from the
  engine there (gate 7 covers them). Condition 6 cannot bind in P1 because `evaluate_mastery` runs
  at elapsed 0.
- `COMPARISON_TIMEOUT_S = 5` has no plan source. A short-answer grade can take 15 s on a sync
  worker. SIGALRM cannot interrupt one long C call on the main thread (ingest CLI). Forkserver
  children are unbounded in number and re-import an unguarded `__main__`.
- A budgets row that spans the migration day mixes unreported sums with counted calls.
- `stop_reason` versus 07's `finish_reason`: readers in replay.py, several tests and the cassette.
- Superseded 2026-09-23, twenty-first session: retryable now reads the claude-api skill's
  error-code table, see above. Stream error events are always `retryable: False`. Effort on Haiku 4.5 is not refused.
- Superseded 2026-09-23, twenty-first session: `GET /growth-tokens.css` now defaults to
  `app/design/growth-tokens.json`; the three assertions were changed on the operator's own
  instruction (this slice). `GET /growth-tokens.css` 404s unless `GROWTH_TOKENS_PATH` is set; a default to
  `app/design/growth-tokens.json` needs three assertions in tests/api/test_static_mount.py changed,
  which only the operator may approve.
- No Inter font is bundled, so the system font renders. `letter-spacing` and numeric weights are
  unset (08 gives none). The page renders once without colour tokens before JS sets `data-theme`.
- Account screen: no route says whether a user exists, so both buttons show; the credential name is
  always "student"; adding a second authenticator is not built (09 asks registration to prompt for
  one); copy strings on the account screen were written by the builder and await the operator.
- `finish_*` against the real py_webauthn has never run; that needs a real authenticator.
- `test_next_item_never_carries_the_answer_key` derives forbidden columns from the code under test.

Resolved in the thirteenth session from the list below: no `data-theme` ever set (D33), hand-typed
`INSTANT_CLASSES`, stream parsed as JSON, thinking refused and options dropped, unbounded
equivalence off the main thread, the tutor "only four fields" and prompt golden tests, Secure flag
from bind_host, no CSP, webauthn not installed, `test_library_verifier_names_the_missing_package`
depending on the package being absent.

From the twelfth session, 2026-09-22, found and not fixed.

- Superseded 2026-09-23, twenty-first session: the purge confirmation phrase is ruled
  (`"delete my data"`) and wired into `App.tsx`; purge is reachable from settings. Purge is unreachable from the served app. 08 gives no purge confirmation phrase, so `App.tsx`
  passes `null` and the purge controls stay disabled with the gap named on screen. Failure
  scenario: 30 days after the exam the student cannot purge from settings.
- No plan copy exists for a failed request anywhere in the client. Screens stay silent on a 500
  or a dropped connection; a refused next-item request leaves feedback on screen to retry.
- The empty-queue action "Add a 15 minute practice set" opens an ordinary session. No route
  assembles a 15-minute set, so on an empty queue the button opens an empty session.
- 08's "daily minute target" and "daily cap, all roles" have no column in 06, so neither is served
  or shown.
- Provider key storage (`PUT /settings/providers/{provider}` and its test call) is not built. 09
  requires libsodium secretbox under a memory-hard KDF, and no libsodium binding is installed or
  named by package in 06.
- After the first cap change through settings, the environment cap no longer binds for that role.
  Stated in `app/providers/guard.py`. A PUT is detected from the `budget_cap_changed` audit entry.
- The home forecast rng is seeded from `GROWTH_RNG_SEED` and the day, not the user, so two users
  on one day would share a draw. Harmless while P1 is single user.
- `test_importing_app_main_leaves_the_repository_database_untouched` cannot fail when the
  repository database already matches; `test_importing_app_main_opens_no_database` is the one that
  proves the guarantee.
- Export audit scope names the actors `worker`, `system` and `operator` as the student's in a
  single-student deployment; purge deletes the same set. Multi-user (P8) needs a real owner.
- `format_version = 1` in the export is a label with no plan source, and the `export` job type is
  taken from 06's API surface row, not from its jobs type list.
- Purge deletes archive files before its transaction commits. A failed commit leaves the rows and
  loses the files, which is the privacy-safe side.
- If more audit verdicts are recorded than the sample holds, `verdicts_complete` reads true and the
  key error rate can exceed 1. No plan rule decides it.
- The passkey JSON the client sends to the reauth and purge routes has been tested against mocks
  only. The `webauthn` package is not installed in `.venv/`, so `LibraryVerifier` has never run.

Resolved this session: the served-steps, pre-submission self-explanation prompt and
self-explanation persistence defects; `record_attempt` storing a client-claimed `correct`; the
three unmounted screens; the unserved token stylesheet; the missing spacing vocabulary;
`ServedItem` omitting `is_probe` and the loosely typed queue; the review audit kind, the wrong-row
resolution and the key error denominator; `verify.py`'s null `error_path` split; coverage gaps
missing from `audit_log` per day; `test_next_item_never_carries_the_answer_key` asserting only a
string. The reauth audit entry was already written by the route.

Two review rounds ran against this session's own diff, and both found blocking defects that were
reproduced and fixed before close.

- Wave 1 review, blocking, fixed. `app/design/css.py` emitted colour tokens and silently dropped
  all nine type tokens on the one path the operator will take: filling
  `docs/operator/design-tokens.template.json` and calling `stylesheet_from_tokens` produced 34
  declarations, none of them `--growth-type-*`, while `CUSTOM_PROPERTIES` advertised 26 names. The
  module now refuses a missing token of either kind, validates type values for the characters that
  would end a declaration or a rule block, and the template carries the nine type tokens as nulls
  so the operator can fill them. `tests/design/test_css.py` now exercises the real template rather
  than only a hand-built full token file.
- Wave 1 review, blocking, fixed. `app/items/distractor_paths.py` duplicated the comparison and
  error-path core of `app/items/verify.py`, proven by replacing `verify._compare` and watching
  `test_distractor_paths.py` stay green. One core now serves both callers and two monkeypatch
  tests prove a change to it reaches both.
- Wave 2 review, blocking, fixed, and the most serious finding of the session. Gate 25 could be
  defeated by `it.skip`. The reviewer skipped the cross-fade case and rewrote every reduce block
  to `transition: none`, which is the implementation 08 explicitly calls wrong, and the gate still
  reported `1 passed`: the title regex matched only `it(`, so a skipped case left both sides of
  the count, and nothing read `numPendingTests`. The scan now captures the modifier and refuses
  `.skip`, `.todo`, `.only`, `.fails` and `.concurrent`, and the gate asserts `numPendingTests`
  and `numTodoTests` are 0. The same attack now fails at `test_reduced_motion.py:52`. Everything
  else thrown at the gate already failed correctly: absent `node_modules`, a renamed test file, a
  glob matching zero files, broken reduce blocks, a stripped affordance and a stale report.
- Wave 2 review, blocking, fixed. The client had no entry point. `index.html` named
  `/src/main.tsx`, which did not exist, so `npx vite build` failed, and nothing imported
  `motion.css`, so gate 25 asserted a property of a stylesheet no browser loaded. `main.tsx` and
  `App.tsx` now exist, `main.tsx` imports the motion stylesheet, the build succeeds, and
  `tests/web/test_client_builds.py` runs the production build so the gap cannot reopen unnoticed.
  No P1 gate ran the build, which is why this was invisible.
- Wave 2 review, three plan deviations in the session screen, fixed. The confidence rating could
  be skipped although 11 P1 scope item 10 says it is collected before feedback on every item; the
  error note was optional and was prompted after correct answers although the plan says one note
  per corrected item; and a double-clicked `Next item` stranded the student on the server's 409
  with nothing said. `commit` now reads the rating back off the attempt row the server wrote
  rather than off local state, the note field renders only on the corrected path and is required
  there, and one in-flight guard released in a `finally` covers all three submissions.
- Wave 2 review, a vacuous test, fixed. `HomeScreen.test.tsx`'s colour scan caught only hex
  literals, so `rgb(255, 0, 0)` and `red` passed, and its "only" test was an at-least-one match
  inside a loop with no count guard. The scan now decides whether a value names a colour by
  assigning it to a DOM node and asking whether the CSS parser kept it, subtracting the seven
  CSS-wide and context keywords by name, so no colour list is hand-typed anywhere.

From the eleventh session, 2026-09-21, found and not fixed.

- The three screens are built and tested but are not mounted in the bundle. `App.tsx` routes
  between home, session and settings and, for each, renders a panel headed "This screen is not
  built yet" naming every required prop no client route supplies, because mounting a screen with
  `[]`, `null` or `0` would render a queue claiming no work is due and a budget claiming nothing
  was spent, which is a fabricated figure wearing the screen's real layout. A test asserts no
  rendered route contains a digit at all, so a default cannot be slipped back in quietly. The
  consequence to carry: gate 25's "still reaches the student" is asserted at component level, not
  through a served page, and it closes one screen at a time as routes land.
- Nothing calls `app/design/css.py` and nothing writes a generated stylesheet into the client, so
  every `var(--growth-*)` resolves to the browser default. `App` probes `--growth-surface-page` at
  render and shows a `role="status"` notice when it is absent. What is still owed once the
  operator's token file lands: a build or startup step that reads it, calls
  `stylesheet_from_tokens`, writes the result where the client imports it, and a `main.tsx` import
  of that stylesheet beside the motion one.
- No plan document gives copy for an in-session request failure. A rejected `submitAttempt`,
  `submitConfidence` or `submitErrorNote` leaves the student on the same screen with nothing said.
  The double-click case is closed by the in-flight guard, but a 500 or a dropped connection is
  not, and the sentence was not invented. It needs a line in 08-design-brief.md's Interface
  writing before it can be built.
- `purgeConfirmationPhrase` has no client source. 08 gives the claudebox acknowledgement string
  verbatim but gives no phrase for purge, so the settings screen takes it as a required prop and
  the only value anywhere is a fixture in `SettingsScreen.test.tsx`.
- The consolidation in `app/items/verify.py` changed one outcome beyond the duplication fix. The
  old `_equals_key` collapsed an unsettled comparison into "not equal", so such an item reached
  `verified`; it now lands in review. That is the safer reading and it is a behaviour change worth
  knowing.
- `tests/web/test_client_builds.py` runs `vite build` rather than `npm run build`, because the
  latter chains `tsc --noEmit` and a type error in a module the bundle never loads would read as a
  client that cannot be served. `tsc --noEmit` is still run separately and is clean.
- The client cannot draw a worked example or a completion problem from what the server sends.
  `GET /sessions/{id}/next` returns `ServedItem` from `app/runtime/bank.py:_as_item_dict`, which
  deliberately withholds the worked solution before submission, so it carries `stem` and no step
  list. Stages `example` and `completion` both need one. Failure scenario: a student opens a
  session, block 2 serves a stage-example item, and the screen has nothing to render above the
  answer field. `Item.tsx` takes `workedSteps` as a required prop with no default and
  `SessionScreen` requires `workedStepsFor(item)` from its caller, so nothing is fabricated, but
  no route supplies it. What the route owes, for stages example and completion only:
  `served_steps: [{index, text}]`, all steps at example, the first n-1 and never the last at
  completion.
- `FeedbackPayload.self_explanation_prompt` arrives only after submission, but the example stage
  shows the self-explanation prompt before any submission. `SessionScreen` requires
  `selfExplanationPromptFor(item)` for that reason. The same pre-submission payload should carry
  it.
- Nothing persists the self-explanation answer. `POST /sessions/{id}/attempts/{aid}/error-note` is
  the error note only. Failure scenario: a student types an answer to "which rule justifies step
  k, and why does it apply here" at the example stage and it is dropped when the item advances.
- A student whose MathLive chunk fails to load is stuck on that item. `Item.tsx` now tells them
  the problem cannot take an answer and withdraws the confidence prompt and the commit button, but
  the only way forward is `Next item`, which lives behind feedback, and feedback needs an attempt.
  No plan section specifies a skip or reload path, so none was invented. Worth a decision before
  P1 ships.
- Nothing in the client suite exercises real MathLive. Its package exports map answers the "node"
  condition with a server-side bundle that omits `MathfieldElement`, and Vitest resolves that
  condition under jsdom. Adding `resolve.conditions` to `vite.config.ts` was tried and broke seven
  other test files, so the seam is tested against an honest stub custom element instead. Nothing
  proves `MathfieldElement` registers, that `<math-field>` upgrades, that a real keystroke emits
  an `input` event, or that the real `getValue("math-json")` returns parseable MathJSON. The
  failure path is exercised through a mocked rejecting module, so the browser's real rejection
  shape is assumed rather than observed. A browser-level check is the only thing that closes this.
- The consolidation in `app/items/verify.py` changed one behaviour. The shared core is `verify`'s
  comparison, which re-runs `numeric_check` after `equivalence`. For every settled comparison that
  is identical to what `distractor_paths` did, because `numeric_check` is seeded. The one case
  that can now decide differently is when `equivalence` hits its 5 second SIGALRM timeout:
  previously the checker called that unsettled, now the unbounded `numeric_check` may settle it
  either way. Nothing tests that path.
- `types.ts` `ServedItem` omits `is_probe`, which `app/engine/select.py` `dress_item` writes onto
  every served slot, so the client's `ServedItem` gate is one-directional rather than exact
  equality. `SessionPayload.queue` is typed `Record<string, ServedItem[]>`, but
  `service.queue_payload` returns `block1` to `block4`, `forecasts`, `coverage_gaps` and
  `interleaving_satisfied`, so three of those values are not item arrays and no gate covers them.
- `app/design/css.py` emits only `[data-theme="..."]` selectors, with no `:root` default and no
  `prefers-color-scheme` block. A document rendered before the shell sets `data-theme` resolves
  every `var(--growth-*)` to empty. 08 requires no default, so this is an interface note rather
  than a deviation.
- Entry criterion 5 names a nine-value spacing scale alongside the nine type-scale steps.
  `app/design/tokens.py` carries no spacing vocabulary at all, so the template offers no spacing
  slot and `CUSTOM_PROPERTIES` advertises none. The names were not invented. The operator kit
  still owes a `SPACING_TOKENS` table, its nulls in the template and its emission in `css.py`.
- The `var(--growth-*)` role assignments on the home and settings screens, meaning which text sits
  on `text-secondary` against `text-muted` and which control is `accent-base` against
  `surface-sunken`, were chosen by the builder. 08 fixes token names and roles in the abstract but
  gives no screen-by-screen mapping. This is a first pass, not a spec-derived assignment, and a
  design review should confirm it.
- `motion.ts`'s `INSTANT_CLASSES` is a hand-typed list of the six repeated-keystroke paths 08
  names, checked against a hand-authored stylesheet. The six do match 08, and
  `TRANSFORM_MOTION_CLASSES` is correctly derived from `P1_FEEDBACK_AFFORDANCES`, but nothing
  parses 08 for them the way `test_tokens.py` parses it for the type scale. A seventh path added
  to 08 would fail no test.
- `app/web/src/api/client.ts` issues `POST /sessions/{id}/attempts/{aid}/error-note`, which is not
  in 06's API surface table. The route predates this session and 06 was never updated. The client
  conformance test scans the FastAPI decorators, so it catches client and server drift but cannot
  catch server and plan drift.
- The style gate blocks U+2600 to U+27BF, so tick and cross glyphs are unusable. The correct and
  incorrect glyphs are the ASCII strings `ok` and `x`, the second matching 08's own wireframe. Real
  tick glyphs would need a gate exemption or inline SVG.

- Resolved 2026-09-20 (ninth): the unconditional `temperature` on every Anthropic call, which
  was a 400 on every routed model. See Done.
- From the ninth session, not fixed. The 26 templates in `var/` all fail the extended gate,
  and every one of them was generated before the schema carried `representation`, `figure`,
  `role` or the allowed BC-ERR list, so the 0 of 26 is a contract measurement and not yet a
  model measurement. A fresh paid run against the new prompt is the next measurement and is
  not taken without the operator.
- From the ninth session, not fixed. `tools/template_trial.py` `structure` treats degree,
  head, function set, arity and zero-ness as the whole of a solution path's shape. A radical
  that changes which theorem applies without changing any of those, such as a sign pattern
  that switches an integrand between two antiderivative rules, passes the incidental check.
  The check is a floor, not a proof.

- From the eighth session's review, not fixed, not blocking. `app/items/distractor_paths.py`
  reimplements the two comparison loops and the error-path resolution of
  `app/items/verify.py`'s `distractor_checks`, although its own docstring says it does not. The
  two now disagree on policy by design: the checker reports an unsettled comparison as a
  violation, while `ingest.distractor_distinct_check` returns indeterminate and routes to review.
  Failure scenario: a future change to 04's rejection rule 5 has to land in two files and a
  reviewer editing one will not see the other.
- From the eighth session's review, not fixed, not blocking.
  `tests/design/test_tokens.py::test_a_filled_pair_at_the_floor_is_accepted` does not test the
  floor. Its fixture sets every checked pair to black on white, which is 21:1, and the boundary
  the code tests with `ratio < TEXT_CONTRAST_FLOOR` is never exercised at exactly 4.5.
- From the eighth session's review, not fixed, not blocking. `tests/design/test_tokens.py` reads
  the colour token names out of 08 but types out the `accent-tint-1` to `accent-tint-4` range. If
  08 said "1 through 6" the test would build four names, `COLOUR_TOKENS` holds four, and it would
  pass.
- From the eighth session, not fixed. Gate 22, `test_prompt_cache_prefix_length`, has no test
  function anywhere under `tests/`. It cannot be written honestly without a key, because it
  asserts a token count of the tutor template's static prefix.
- From the eighth session's review, not fixed, and worth the operator's eye.
  `provider_result_unreadable` is a sixth action in `app/audit/vocabulary.py` that 09's prose does
  not enumerate. So is `app/db/migrate.py` itself: 06 names no migration mechanism at all, and its
  only migration prose is Postgres through SQLAlchemy at phase 8, so the additive migrator is an
  implementer-invented seam.
- From the eighth session, a gap in the evidence rather than a defect. The gate 23 strengthening
  could not be shown red by a mutant: a copy of the repository under the scratchpad does not run
  the end-to-end test green even unmutated, because the cassette and content paths do not resolve
  outside the working tree. The strengthening rests instead on two assertions that are both live,
  that more than one archetype opens at cold start and that every one of them was served.
- From the seventh session's review, accepted rather than fixed and still true. Six of the 13 P1
  archetypes are unreachable at cold start because each one's primary skill has a hard prerequisite
  that is an ordinary BC-SKL rather than one of the 25 seeded assumed-mastered parents, and
  BC-QA-01004's gating parent BC-SKL-01028 is one of BC-QA-01004's own skills, so it can never
  open. That last one looks like a library shape worth a question rather than a test defect. Gate
  23 no longer accepts a one-archetype regression, but it still cannot reach those six.
- From the seventh session, a behaviour change to note. `compose_sentence` now returns `None` where
  it used to return `""` when a provider returns an empty string, on the uncached path as well.
  Nothing in the suite depended on the old reading and the route treats a missing sentence as the
  degradation case.

- The error note still takes any length. 03 and 06 set no cap, so none was invented. The repeat
  POST and the multi-line note are fixed as of the eighth session.
- `scoring_consequence` is empty on every wrong short answer, so feedback carries two of 03's three
  required parts on that path. See Plan corrections for why the BC-PT branch was not implemented.

- From the fifth session's review, not fixed. Session assembly freezes `format` on every queue slot
  at assembly time, so the R16 alternation never happens inside one session: every item of a fresh
  session is served as short answer, and an MCQ case exists over HTTP only when a test rewrites the
  queue row. Because R12 rule 3 gives a wrong short answer no error path, and
  `elaborated_payload` refuses to compose without a BC-ERR record, elaborated feedback is
  unreachable through the natural P1 flow. These two together are what block gate 23
  `test_session_login_to_feedback`, along with two smaller gaps: no HTTP route writes the error
  note that gate 23 names, although `service.record_error_note` exists, and
  `tests/fixtures/provider_cassettes/` does not exist, so "no network calls outside the recorded
  cassettes" has no cassettes to replay. `app/main.py` also sets no `settings.tutor`, so the one
  wired role is wired only in tests.
- The static prefixes of both prompt templates are far short of the 1,024-token minimum that binds
  on claude-sonnet-5: `guardrailed_practice_v1.md` is 2,473 characters and `elaborated_v1.md` is
  1,641, which is roughly 620 and 410 tokens. Gate 22 would fail on length, not merely be
  unmeasurable, and the plan's own trap is that a short prefix is processed uncached with no error.
- `AnthropicProvider.stream` sets `"stream": true` and then parses the body as JSON, so the first
  real streaming call raises a decode error on the `text/event-stream` response. No test covers it
  because every test feeds a dict back. 07 gives no concrete SSE to normalised event mapping that
  could be validated without a key.
- `app/providers/anthropic.py` refuses `thinking` in `provider_options` outright, including the
  adaptive form 07 names as the correct one for Claude 4.7 and later, and drops `provider_options`
  rather than passing it through. Defensible for a tutor that needs none, a deviation for the P4
  generator. The result field is `stop_reason` where 07's shape names `finish_reason`.
- The tutor is called from the feedback route on every GET, so re-reading the screen re-spends and
  returns a different sentence, and the `usage` block is discarded, so nothing feeds a budgets row,
  the cache hit rate or `audit_log`. 07 puts the budget guard, the usage accounting and the audit
  trail at the provider seam.
- A BC-ERR record whose skills are all outside the archetype leaves `error_path_skills` empty, and
  `rule_based_mastery_states` then falls back to blaming the primary skill, which is R12 rule 3's
  behaviour for an answer with no error path. The fallback predates this session; the grader is
  what starts feeding it real error paths.
- `equivalence` now returns without a bound when it runs off the main thread, which is where a sync
  FastAPI route runs. The `signal` crash is fixed and the timeout is not replaced, so a
  pathological submission can pin a worker thread. The exposure is one authenticated user on their
  own installation.
- `record_attempt` persists the submitted body verbatim in `attempts.response`, so a claimed
  `"correct": true` is stored beside the server verdict that overrode it.
- `audit.write_resolution_audit_entry` hard-codes the `item_audit` kind, so resolving a row of any
  other kind is logged as an item audit. `resolve_item_audit` passes `row.ref_id` rather than the
  row, so `record_item_audit_verdict` re-looks-up the open row by item id and would resolve the
  wrong one if two were open for the same item.
- `_misnotated` treats any units mismatch as `notation_only` with correct true, which credits 0.25
  for an answer whose units are dimensionally wrong. 03's check 4 asks for units present and
  dimensionally correct; R12 rule 4 is loose enough to permit the reading.
- Three tests assert less than their names claim, and none of them is a gate from 11:
  `test_next_item_never_carries_the_answer_key` checks only that the literal string `answer_key` is
  absent and never checks `is_key` or `error_path`, which are what identify the key;
  `test_the_tutor_receives_only_the_four_selected_fields` proves no "only" and never inspects
  `request.system`; `test_prompt_templates_are_versioned_and_golden` holds no snapshot or digest,
  so any rewrite of either template passes it.
- The working tree carries 24 untracked files whose names end in `" 2.py"`, copies made by a file
  sync. pytest collects them and reports `200 passed` instead of `161 passed`, so every count in
  this ledger is taken with `--ignore-glob="* 2.py"`. They are the operator's to delete.


- From the fourth session's review, not fixed: `close_session` sweeps graded, unrated attempts and
  applies them with `Confidence.UNSURE`, which is an observation the student never rated entering
  `c_k`, `distinct_archetypes_succeeded` and `success_days`; it rests on the operator's second
  session instruction, not on a plan sentence, and `close_session` now raises `ValueError` (409)
  when no engine bundle is supplied, so a caller without one cannot close a session at all.
  `reauth_finish` writes no audit entry although 09 records "a session established from a new
  authenticator". `app/review/audit.py` divides the key error count by the verdicts recorded
  rather than by the sample size, which reads correctly only because `verdicts_complete` ships
  beside it. Coverage gaps from the fail-closed rule go into `sessions.queue` rather than
  `audit_log`, which 06's traceability row asks for; pre-existing, and live now that the real bank
  is wired. `app/items/verify.py` still splits options on a null `error_path`; only the ingestion
  path was corrected to read `is_key`.
- Recovery issues a replacement code after a successful recovery. 09 says a code is "generated once
  at registration", so this is a deviation; without it a recovered account has no recovery path
  left. The plaintext replacement is returned once in the finish response.
- `app/runtime/bank.py` decides what a served item may carry. Anything a later phase adds to the
  `items` row is withheld from the student by default and has to be added to `_as_item_dict`
  deliberately.

- From the third session's review, not fixed: registration issues no recovery code (09 Recovery requires one, hashed, shown once); purge leaves `review_queue`, `jobs`, `items`, `item_verifications` and `content_snapshots` untouched because they carry no `user_id`, and it empties `audit_log` globally, so the purge audit entry itself does not survive; no ASGI entrypoint builds `Settings`, resolves the snapshot and the `SessionContext` for a real run, so `create_app` is reachable only from tests; `LibraryVerifier`'s calls into the `webauthn` package have never executed; challenges live in a per-process `ChallengeStore` with a 300 second TTL; the Secure flag derives from `bind_host` rather than the request scheme; audit actions `session_established` and `session_closed` are not in 09's vocabulary; no per-IP rate limit, CSP or HSTS middleware.
- `test_purge_requires_reauth` drives a purge double, so no HTTP test runs the real `purge_user`; the real one is covered in `tests/session/test_purge.py` only.
- Gate 31 margin is thin: pooled 0.0604 against 0.0556 on the fixed per-trajectory seeds, and on ceiling and slipper the control arm scores higher per item than the policy. The pooled win comes from the policy serving fewer items on absent_30_days and floor (block 1 requeues), not from faster mastery. A different seed set could flip it. The eval asserts pooled only, as written.
- Dependants of BC-SKL-02025 do reach mastery in the prereq_gap trajectory as secondary loaded skills of archetypes whose primary is ungated (BC-SKL-02044, 02045 via BC-QA-02010; BC-SKL-03006 via BC-QA-03001). Invariant 3 gates on the primary skill only, so this is plan-conformant; `test_simulation_prereq_gap_stalls_dependants` asserts that no mastered dependant was credited by an archetype whose primary is itself a dependant. Whether secondary loading should be gated too is a 02 question.
- `test_simulation_prereq_gap_stalls_dependants` asserts gating on the served trace and is load-bearing; its second clause (dependants of BC-SKL-02025 unmastered) is vacuous until mastery is reachable.
- `app/sim/runner.py` reads `tests/fixtures/graph_p1.json` and `tests/fixtures/student_trajectories/` by path and synthesises 10 published items per archetype because `tests/fixtures/items_p1/` does not exist; when the 130 items land, the bank should be read from them.
- Session service: an attempt at stage completion or unsupported whose confidence rating never arrives is never applied, and nothing sweeps abandoned sessions. Stage example fabricates `Confidence.UNSURE` because `grade_for` requires a rating and convention 3 collects none there. `transcription_confirmed` is not enforced as a precondition on the update (P1 has no transcription). `constants.LAMBDA` is 0 in P1, so the retrievability passed into the logged predictions is inert until the lambda arm turns on. Nothing seeds the 618 `skills_state` rows at account creation; tests seed from the fixture.
- Reconciliation: consecutive counters are zeroed on merge, an inferred choice recorded in `ReloadReport.notes`; a `skills_state` row whose id is neither active nor in `ids.json` refuses the reload (folded into the pseudocode's final else). Orphaned rows are surfaced only through the report and `audit_log` (`skill_orphaned`); nothing in selection excludes them yet.
- Resolved 2026-09-19: `data/prereq_edges.csv` carried a cycle over the full typed edge set (BC-SKL-05020 to BC-SKL-05021 hard_prerequisite, BC-SKL-05021 to BC-SKL-06023 supporting, BC-SKL-06023 to BC-SKL-05020 supporting) because one supporting row was stored in the reverse direction. The row was flipped (see Decisions); `tools/graph_check.py` reports 0 cycles, test_graph_acyclic and test_loader_against_real_data pass, and the helper test that removed the cycle from a temporary copy was deleted as obsolete. A full `tools/merge_staging.py` replay after the flip regressed unrelated evidence links in archetypes, scoring_points and skills, so those three registries and `data/staging/sync-dependents.json` were restored to HEAD; the replay order in that tool lets older staging files overwrite later link-evidence merges, which the library owner should look at before the next merge.
- FSRS-7 forms: docs/plan/02 transcribes stability and difficulty updates with parameter indices that do not match the shipped model (the plan's w7 as an exponent on S made stability explode by about 500x per review; its difficulty step had the sign inverted). Per R28 the forms are copied from the reference implementation instead, fsrs-rs at commit c137ee6e096f9217632397a8fb2bdb6f6e1b92ae, `src/model_v7.rs` and `src/inference_v7.rs`, cross-checked against srs-benchmark `models/fsrs_v7.py`; the source is recorded in `app/engine/fsrs.py` and the vector's source file is committed as `tests/fixtures/fsrs_rs_inference_v7_c137ee6.rs` with its sha256 in `app/engine/fsrs_constants.py`. The awesome-fsrs wiki page R28 names documents only v0 to v6.
- FSRS-7 carries a second, fast stability per card that the P1 schema does not store; `app/engine/fsrs.py` reconstructs it as 0.8 times the long stability, which is the source's own SM-2 bridge. A `fast_stability` column is a P2 schema decision.
- The mastery corroboration test `test_stability_bounded` shows stability saturating at the source's 36500-day clamp after about 12 successive Good reviews at elapsed = S; retrievability still decays below 0.90 at large elapsed times. Whether that clamp is acceptable for an exam horizon of months is unexamined.
- `drain_probe_queue` in `app/engine/fringe.py` still takes `now` as a required positional; every public entry point supplies it through `session_now`, so only a direct call without it raises. `session_now` accepts a datetime `today`, but the rest of the selection path compares dates, so pass a date.
- `qa/last_report.json` is regenerated whenever `qa/12_report.py` runs and is restored with `git checkout -- qa/last_report.json` at session close, so the library's committed report does not drift because of build sessions.

- 2026-09-23, Slice 2 closing session: `var/subscription_smoke.json` is gitignored and was not
  re-run, so the file on disk still holds `no_tool_ran: false` for phase 2 from the old check. The
  two-turn allowance rests on the CLI 2.1.277 forcing its internal StructuredOutput tool for
  `--json-schema`; a later CLI that answers a schema in one turn, or takes more than one extra
  turn, will read `no_tool_ran` false in the smoke run and needs a look before the check is
  changed.

- 2026-09-23, P2 Slice 3, open:
  - `due_today_minutes` estimates the whole due queue through a deterministic cover; block 1 serves
    only 5 items or 5 minutes of it with a random draw, so the rest carries to later days and
    the served items can differ from the cover. Home does not show either new number; whether it
    should is a design-brief question for the operator.
  - A due skill with no published archetype (`DueQueue.uncovered_skills`) stays due every day and
    is not written to `audit_log`; block 2's coverage gaps are audited, block 1's are not.
  - In a fresh worktree `qa/12_report.py` exits 1 on `00_manifest` (97 "pdf missing") because
    `cache/pdf/` is not in the checkout, and `git status` shows `cache/pdf` as untracked rather
    than ignored. This session linked the main checkout's `cache/pdf` read-only for the QA run and
    removed the link afterwards; an orchestrator that links it must not commit the link.

- 2026-09-23, P2 Slice 4, open:
  - The curve omits 08's ideal diagonal and its "overconfident on confident by 18 points"
    sentence, and reports no Brier score or confidence minus accuracy, because all four need each
    rating mapped to a probability and no plan document fixes that mapping (see Decisions).
  - A legacy unsure rating stored before `attempts.confidence_source` existed stays unattributed
    and never counts, because nothing in the row tells a student's unsure from the close sweep's.
    On a database with P1 history the curve can therefore under-count the unsure level.
  - The 1.4.11 non-text contrast ratio is still unfetched (08, 11 P8 item 4), so the axis stroke
    uses `text-muted` and the marks `accent-base` without a measured non-text ratio.
  - `app/session/service.py` carries four one-line edits (two constants and three
    `confidence_source` assignments), inside the area Slice 3 also edits; they touch only
    `record_attempt`, `record_confidence` and `close_session`, not session assembly.

- 2026-09-23, P2 Slice 4 closing session: `app/progress/calibration.py` `counted_attempts` takes
  the day of each attempt from the UTC `submitted_at` string, while the window's end is the
  client's calendar day. An attempt made in the evening in a zone behind UTC can fall one day
  later than the student's own date, so at the window's two edges the count can differ by the
  attempts of one evening. Not fixed: no stored field records the student's zone.

- 2026-09-23, gate 29 cannot be drawn as specified. `app/review/audit.py`
  `draw_key_audit_sample` caps each unit at 15 items (`MAX_ITEMS_PER_UNIT`, from 10's "no unit
  contributes more than 15 items") and asks for 100 (`EVAL_29_SAMPLE_SIZE`), but P1's items span
  three units, so at most 45 can be drawn. Run over the 130 agent items as candidates it refuses
  with "only 45 items honour the 15-per-unit cap; 100 were requested", and with the cap lifted it
  draws 100, so the cap is the cause. Independently, `tools/draw_key_audit_sample.py` offers only
  provenance `operator` items and there are none, so today it refuses at "only 0 candidate items".
  Either the cap is waived for P1's three units or the P1 sample shrinks to 45; both loosen the
  gate as written, so the operator rules. Not changed.
- 2026-09-23, `var/growth.db` held no items when the 27 stems were reworded, so the new wording
  reaches the app on first ingestion. A database that ingested the old records keeps the old
  wording, because `app/items/ingest.py` skips a record whose id is already stored.

- 2026-09-24, `GET /progress` slowness not reproduced. A probe built the real composition root
  (`app/main.py` `build_application`, the live content snapshot, the subscription backend off)
  with the test passkey verifier, registered one user and ran a session a day, answering every
  served item. Over 10 days with `tests/fixtures/items_p1` as the bank it answered in 0.05 to
  0.15 s each day, and over 5 days with `content/items_p1_agent` in 0.14 to 0.35 s. The 45 s
  report above came from a seeded state that was not kept, so the cause is unknown; the probe
  stayed in the session scratchpad and nothing was changed.

## Plan corrections applied [verified]

Session 2026-09-23 (fourteenth). No plan file was edited. Readings applied in code:

- 03 check 4 "dimensionally correct" read as "the same unit": a unit of the same dimension at a
  different scale (cm against m, m/s against ft/s) is wrong, because the value is compared
  without conversion. The builder's first reading, same dimension is notation, credited 12.5 m/s
  against a key of 12.5 ft/s.
- 11 exit criterion 4, "measured rather than estimated": no key error rate is published while any
  sampled item lacks exactly one verdict. Two assertions written earlier expected a partial rate
  (0.2 and 0.5); they now expect none.
- One assertion written this session, `"M"` against a key of `m` ungraded, was changed to credit
  it, to agree with the committed `" M/Sec "` case in test_units_declared_but_absent_is_notation_only.
- 13 line 60 says a truncated tutor call returns `stop_reason: "max_tokens"`; true of Anthropic's
  raw response, and the normalised result now carries it as `finish_reason`.
- 06's API table has no rows for `GET /auth/status` or `POST /auth/passkey/add/begin|finish`.

Session 2026-09-23 (thirteenth).

- `docs/plan/09-security-and-privacy.md` CSP paragraph: adds `style-src-attr 'unsafe-inline'`.
  Old reading: styles restricted to self with per-build hashes. Reason: MathLive lays out formulas
  through run-time style attributes; under the old policy a fraction rendered collapsed with 121
  blocked-style errors, verified in a browser.
- `docs/plan/02-adaptive-engine.md` lines 733 and 734: gamma 0.4 and rho -0.2 in the tunables
  table corrected to 1.0 and -0.5, which lines 130 and 131 and the code already use.
- `docs/plan/06-architecture.md`: attempts gains the five tutor accounting columns; budgets gains
  `settled_calls`, `cached_read_reported_calls`, `cached_write_reported_calls` and `stopped_by`,
  with the rule that a count of 0 means the cached sum is not a measurement; line 93 names
  py_webauthn.
- 11 entry criterion 5 and implementer decision 6: the token file is the implementer's, not the
  operator's. The eighth to twelfth sessions filed it as human-only. The operator chose the
  palette; the implementer produced and checked the values.
- 11 P1 Goal against scope 17: the onboarding account screen (passkey registration) is in P1,
  because the Goal has a student register and scope 17 excludes only the diagnostic onboarding.
- `app/design/tokens.py`: `accent-contrast-text` is no longer checked on `accent-base`, approved by
  the operator. 08 gives the button text its own token, `text-on-accent`, still checked.
- 13 item 4 with 07's "No further tutor calls today": the stop latches; its refusal names the cap
  that stopped it. Three tests in tests/providers/test_guard.py were rewritten on 13 items 3 and 4:
  the abandoned stream now asserts the worst-case charge (old `tokens_in == 0`, `cost_usd == 0.0`),
  and the two latch tests assert one refusal row naming `usd` (old `len(refusals) == 2`, `reasons ==
  {"usd", "hard_stopped"}`).
- 13 "raising a cap clears the stop": read as every stopping cap raised, none lowered, all above
  the day's spend.
- 13 item 6: charged at the 1h write rate because the result carries no TTL split.
- 07 "the adapter passes it through": replaced by an allowlist, because 13 line 20 makes
  temperature a 400 and a passthrough let model and max_tokens bypass the guard.
- 07:145 thinking form: only `{"type": "disabled"}` is accepted, per 13:22 and 13:60; the adaptive
  form 07 names for the generator stays refused until P4 needs it.
- 09 "refuses a Secure-less cookie on a non-loopback origin": origin read as the request host.
- 06 "the verifier stays in-process with SymPy": read as in the application, not a separate
  service; the child process is a time bound.
- 11 exit criterion 8 "per served item": items with no tutor call count at cost 0 (06's
  `tutor_calls` DEFAULT 0); both medians are printed.
- 13's per-session tutor ceiling: reaching it returns no sentence rather than "unavailable for the
  rest of today", which 07 writes for the daily cap.

Session 2026-09-22 (twelfth). None of these edits docs/plan.

- 06 API surface, `GET /progress`, listed as "mastery map, calibration, due counts". The progress
  screen is not P1, but home's three counts and minute forecast need a route, so P1 serves only
  the due-count part there. Old reading: a progress-screen route. Reason: 08 home needs the counts
  and 06 names no other route that carries them.
- 06 API surface has no self-explanation route. `POST /sessions/{id}/attempts/{aid}/self-explanation`
  is added beside the error-note route, which also predates 06's table. Reason: 06 defines the
  `attempts.self_explanation` column and 11 P1 scope 10 requires the answer.
- 11 P1 entry criterion 5 lists the spacing scale among values the implementer produces. 08 already
  fixes the nine values, so they are emitted from 08 directly and are not operator input. Names
  are `space-<px>` because 08 gives none.
- 07 Budget caps, "stored in budgets". Read as: the cap in force is on today's budgets row, carried
  forward from the latest earlier row once the operator has changed it through settings.
- 09, "an extension is an explicit act". Read as: a changed exam date never moves `purge_after`.
- 11 Q16, "served at stages example and unsupported only". The server serves such a completion slot
  at example, keeping the support the engine chose.
- 11 Remaining implementer decision 3 (no answer at example). Read as: step marks at example carry
  no verdict; every step is marked given.

From the eleventh session, 2026-09-21.

- `docs/plan/11-phased-delivery.md` gate 25 and the previous three sessions' Next candidates. The
  old reading filed `test_reduced_motion_replaces` as human-only, waiting first on the design token
  file and then on screens. The new reading is that gate 25 reads no hex value: its property is the
  reduced-motion contract plus the presence of five affordances, and 11's own P1 scope items 8
  (`app/web/session/Item.tsx`), 11 (`app/web/input/`) and 17 (home, session and settings screens)
  put the client inside P1. The gate is closed this session with the token file still unwritten.
  The token file still blocks gate 26, which does read hex values, and that remains human-only.
- `docs/plan/06-architecture.md` line 93 names React 18, TypeScript, Vite, KaTeX and MathLive, and
  names no client test runner, exactly as it names no Python test runner. Vitest with jsdom and
  @testing-library/react are therefore the implementer's choice on the same footing as pytest,
  hypothesis and httpx2, which 06 also does not name. `@types/node` was added for the same reason.
  Recorded here rather than treated as a dependency not named in 06.
- `docs/plan/08-design-brief.md` Motion rules gives one number, "under roughly 300 ms", and states
  that Material 3's numeric duration and easing tokens could not be loaded, so specific millisecond
  values are unknown. `motion.css` uses 300ms as the single duration and cites it as the stated
  ceiling rather than as a token value. This is a bound used as a value and is flagged rather than
  hidden.
- `BUILD-LEDGER.md`'s eighth-session finding on the accent tint range does not reproduce as
  written. It said a brief reading "1 through 6" would leave the test green against a four-name
  `COLOUR_TOKENS`. In fact the old parser's range regex stops matching under that mutation and the
  interior names vanish, so the old test also went red, for an incidental reason. The fix is still
  correct and the endpoints are now derived from 08, but there was no false pass to point at.

Session 2026-09-20 (ninth).

- `docs/plan/02-adaptive-engine.md`, Variant adjustment. Read as if instantiations of one
  template share the archetype's difficulty. A paragraph now records that they do not, per the
  sources in 13, that the prior gains no variance term and accepts a centre-ward bias, and the
  measurement that would add the term. Reason: Tian and Choi (2023) and Sam et al. (2023), as
  summarised in 13.
- `docs/plan/04-item-generation.md`, the parameter spec bullet for `role`. Read `role` (`safe`
  or `difficulty`) with no check behind it. It now maps `safe` to a declared incidental and
  `difficulty` to a declared radical, states that the declaration is checked by structural
  invariance of the solution path, and that distractor composition is always a radical.
  Reason: Embretson and Daniel (2008), distractor evaluation b = 0.999.
- `docs/plan/11-phased-delivery.md`, P4 scope items 7 and 11. Read `app/generation/generate.py`
  and `prompts/generator/symbolic_v1.md`, per-item generation. Now read
  `app/generation/template.py`, `app/generation/instantiate.py` and
  `prompts/generator/template_v1.md`. Reason: the template architecture decided in 13; none
  of the named files existed, so no code moved.
- `docs/operator/ai-operating-costs.md`. Read `app/providers/anthropic.py:79 sends one today
  and must stop`; now records the fix. Every dollar figure re-derived from
  `tools/cost_model.py`, see Done.

Session 2026-09-20 (AI layer research pass). No application code, no tests and no `app/` change.
`docs/plan/13-ai-engineering.md` and `docs/operator/ai-operating-costs.md` are new. Every number
in both was fetched from a provider page on 2026-09-20 or measured in this repository; the
unsourced ones are listed in 13 under "Claims I could not source". `data/` and `research/` were
read and not written; `git status --porcelain` on both is empty. `qa/12_report.py` exit 0.
`tools/style_gate.py` exit 0 on every file written.

- `docs/plan/07-ai-provider-layer.md`, the D8 routing table, three rows. The verifier read
  `Anthropic claude-opus-5`, the same model as the generator, which maximises the correlated
  generator-verifier failure that 04 guards against with "a second model, on a different provider"
  and that 10 calls "the worst case"; it now reads `Gemini 3.8 Flash (batch, paid tier)` with
  `claude-sonnet-5` on batch second. The diagnostician read `Anthropic claude-opus-5` while the
  same document justifies Anthropic-first by naming the grader, the verifier and the transcriber
  as the roles whose errors reach a student directly, which does not include the diagnostician,
  and while the grader, which it does name, runs on Sonnet; it now reads `claude-sonnet-5`. The
  transcriber read `Anthropic claude-haiku-4-5`, which sits in the standard vision tier at a
  1568 px long edge and 1568 visual tokens against the high-resolution tier's 2576 px and 4784 on
  Claude 4.7 and later, on the one role whose dominant failure mode is misreading; it now reads
  `claude-sonnet-5`, at a cost difference of $0.008 a page. A paragraph under the table records
  each reason and points at 13.
- `docs/plan/07-ai-provider-layer.md`, the Anthropic Known traps paragraph. It recorded that
  `thinking: {type: "enabled"}` returns 400 on Opus 5 and Sonnet 5 and left the reader with the
  impression that not sending a thinking parameter leaves thinking off. It does not: thinking is
  on by default on both models and its tokens are billed as output. The paragraph now records the
  default, the explicit `thinking: {"type": "disabled"}` form and its per-model availability, and
  the `output_config.effort` parameter, whose default is `high` and whose resolved value
  invalidates the prompt cache. Leaving either at its default is the largest avoidable cost in the
  tutor role: $14.92 against $5.01 over the cycle at 12 calls a session.
- `docs/plan/07-ai-provider-layer.md`, the batch paragraph. It recorded the discount, the size
  limits and the expiry and not the two facts that change how a batch is built: batch results come
  back in any order and must be matched by `custom_id`, and prompt caching inside a batch is best
  effort at a reported 30 to 98 percent because requests process concurrently. Both are now
  recorded, with the mitigation the documentation itself gives.
- `docs/plan/07-ai-provider-layer.md`, the cache-prefix stability paragraph. It named 4,096 on
  Haiku 4.5 as a minimum a role had to clear. With the transcriber moved off Haiku 4.5 no role
  routes there, so the binding minima are 512 on Opus 5 and 1,024 on Sonnet 5.
- `docs/plan/07-ai-provider-layer.md`, the fallback chain example. Its `diagnostician` block still
  named `claude-opus-5` as the order 1 deployment after the routing table moved that role to
  `claude-sonnet-5`. Corrected to match the table.
- `docs/plan/07-ai-provider-layer.md`, the Gemini adapter table and its Known traps paragraph. The
  table's Data policy row read "unknown from the loaded pages" and the trap paragraph said the
  unknown policy "is itself a reason it is a secondary rather than a default". Both were true on
  2026-09-19 and are false now. The row carries the paid-tier and unpaid-tier statements with their
  URLs, and the paragraph says the tier rather than the provider is what the router checks, that an
  unpaid Gemini deployment is refused for the four roles carrying student text, and that the
  verifier carries only a generated stem, which is one reason it is the role routed to Gemini first.
- `docs/plan/07-ai-provider-layer.md`, "Why Gemini 3.8 Flash second, by cost" and the sentence
  "Since Gemini is the secondary for every role". Gemini is now the primary for the verifier, so
  both read wrong. The heading names the split and the trap paragraph records that the verifier's
  own prefix of about 1,100 tokens does not clear Gemini's 4,096 implicit minimum, so the verifier
  is priced uncached in `13-ai-engineering.md`.
- `docs/plan/04-item-generation.md`, the output schema `required` list. It read
  `["stem", "key", "worked_solution", "metadata"]`. `metadata` is entirely an echo of the
  generation request, it was 32.0 percent of the emitted characters on a measured full-schema
  record, and a model that restates a provenance field wrongly corrupts an item's provenance for
  no benefit. It now reads `["stem", "key", "worked_solution"]` and the backend writes the block.
- `docs/plan/04-item-generation.md`, rejection rules. None of rules 1 to 14 checked that a
  worked-solution step is mathematically correct, so the key was verified three ways while the
  worked solution a student reads on the feedback screen was unverified model output. Rule 15 is
  added: a step carrying a `sympy` expression must follow from the previous step's under the rule
  it names, checked with `app/items/verify.py` `equivalence`, and a step that is an identity under
  the drawn parameters is vacuous and is rejected.
- `docs/plan/04-item-generation.md`, the independent re-solve paragraph. It said D8 routes the
  verifier to `claude-opus-5`, which is now wrong and was always in tension with the same
  paragraph's own "a second model, on a different provider". It now names the corrected routing
  and states decorrelation as a property of the routing alongside key-blindness as a property of
  the prompt.
- `docs/plan/04-item-generation.md`, the Monte Carlo family pass. It read as a per-item check in a
  list of per-item checks. It is a property of the parameter spec, so running it per item repeats
  one archetype's work forty times; it now says it runs once per archetype per spec version before
  any item is generated, and points at 13 for the cheapest-first ordering of all five checks.
- `docs/plan/12-open-questions.md`, the Gemini data-policy entry. It said Gemini stays second tier
  until the policy is read. The policy was read on 2026-09-20: the paid tier does not use prompts
  or responses to improve Google products, the unpaid tier does and human reviewers may read the
  content, and default log retention is 55 days configurable to 7. The entry now records the
  resolution, and the free-tier limits entry is moot because the free tier is unusable for any
  role carrying student work.
- `docs/plan/12-open-questions.md`, the OpenRouter tool-calling entry. Closed as not applicable,
  since no role uses tools.
- `docs/plan/12-open-questions.md`, the tunables register. Item bank size moved from "30 to 60" to
  40, generated 20 first and topped up on measurement, conditional on the draw rule becoming least
  recently served. The client token estimate divisor is superseded by the free
  `POST /v1/messages/count_tokens` endpoint, with 3.1 rather than 4 surviving as the offline
  fallback. The tutor token cap moved from unset to 250,000 a day, which binds within a few calls
  of the $1.00 cap at the corrected configuration. Six new rows were added for the settings 13
  creates: thinking per role, effort per role, max output tokens per role, cache TTL per role, the
  bank draw rule and the distinct-item corroboration rule.

Session 2026-09-20 (eighth). None of these edits docs/plan; each is recorded here for the operator
to carry into the named file.

- 06 names no migration mechanism. Its only migration prose is Postgres replacing SQLite through
  the same SQLAlchemy models at phase 8, and `Base.metadata.create_all` never alters an existing
  table, so a column added to a model after a database existed never reached it. The build adds
  `app/db/migrate.py` and calls it from `make_engine`. It is additive only: it adds a nullable
  column or one with a server default, and refuses a NOT NULL column with no default and a column
  declared unique or indexed, because ALTER TABLE ADD COLUMN carries neither constraint. A type
  change and a dropped table are not detected, which is the documented scope.
- 09's audit vocabulary has no entry for a provider result the guard cannot read. The build writes
  `provider_result_unreadable`, deduped on the budget row, which the operator should carry into
  09's list or rename there. 07 puts usage accounting at the provider seam and says nothing about
  a result the seam cannot parse.
- 03's "The student's one-line error note" says the student writes one line and gives no length.
  The build enforces both halves mechanically, one note per corrected attempt and no line break in
  it, and enforces no length at all, because a character cap would be a number in no plan
  document.
- 04's rejection rule 5 asks whether a distractor equals the key. An unsettled symbolic comparison
  has not established that it does not, so `app/items/verify.py` no longer collapses unsettled
  into not-equal and `distractor_distinct_check` returns indeterminate for it, which leaves the
  item a draft and routes it to review rather than verifying it. That is what
  `app/items/ingest.py`'s own docstring already claimed of an indeterminate check.
- 08 fixes token names and roles and no hex values, and says the floors are stated over text.
  `accent-contrast-text` is a text role and 08 does not say which background it sits on; the
  validator checks it against the accent base and all four accent tints. `state-correct` and
  `state-incorrect` are checked against every surface. 08 names tint ramps for both semantic
  colours without enumerating their steps, so no ramp step names were invented.
- 11's P1 gate 26 reads the hex values out of a token file the implementer produces. That file
  does not exist and the build authors no part of it: `docs/operator/design-tokens.template.json`
  is every token name at null, and a null reads as a missing value rather than as a skip.
- 11's P1 scope names the 13 archetypes and three files in the repository typed the list
  independently. `tests/tools/test_p1_archetype_list.py` now parses the ids out of 11 and compares
  every copy against it.

Session 2026-09-20 (seventh).

- `docs/plan/06-architecture.md`, the `attempts` table: a `tutor_sentence` nullable column was
  added to the field list. The sentence is one-to-one with the attempt, dies with it under purge
  and carries the same retention as `error_note` and `self_explanation`, so a separate table would
  buy nothing and would need its own purge join. Without the column a re-read of the feedback
  screen spends a second tutor call against the daily cap 07 sets.
- `docs/plan/06-architecture.md`, the API surface row for
  `GET /sessions/{id}/attempts/{aid}/feedback`: the model role read `diagnostician`, which
  contradicts R35 and 11's P1 scope, where the tutor writes the P1 sentence and no diagnostician is
  wired until P3. It now reads tutor in P1, diagnostician from P3, and names the `tutor_unavailable`
  field the route returns when the cap has stopped the role.
- `docs/plan/09-security-and-privacy.md`, the Audit log Recorded sentence: extended with the role
  stopped by its budget cap, the call refused by it and the fringe archetype excluded for want of a
  published item, and with the statement that an ordinary provider call is not recorded because its
  accounting lives in `budgets`. The vocabulary is now enumerated in code at
  `app/audit/vocabulary.py` and a write outside it is refused, so the word controlled is true of the
  code and not only of the prose.
- `docs/plan/12-open-questions.md`, the tunables table: two rows added. The tutor daily cap at $1.00
  with the token cap unset, and the client token estimate divisor at 4 characters per token. 07 sets
  no number for either and the guard cannot run without both, so each is inferred here with what
  settles it. The divisor in particular is the unsafe direction: 07 records the Claude 4.7 tokenizer
  producing about 30 percent more tokens for the same text, so 4 likely under-estimates.


- 03 Content part 2 gives the scoring consequence as the BC-PT `does_not_earn` text when no error
  matched. `app/content/loader.py` does read `data/scoring_points.json` and the archetypes carry
  BC-PT ids, but that text answers which point the response failed to earn, and naming one of an
  archetype's several point types needs the per-point decision 03 puts behind mechanic 6, which P1
  has no component to make. The field stays empty rather than naming a guessed exam consequence.
- 06's API surface has no row for the error note although the `attempts` table carries the column.
  The build adds `POST /sessions/{id}/attempts/{aid}/error-note`, refused unless the attempt was
  corrected, per 02's Session assembly block 4.
- 09's audit vocabulary has no entry for re-authentication or for a fail-closed coverage gap. The
  build writes `reauth_established` and `coverage_gap_fail_closed`, which the operator should carry
  into 09's list or rename there.
- 11 gate 12 states the alternation over `attempts.format`, so R29 is resolved both when a slot is
  served and when the attempt is written. A format frozen at assembly was the only thing any test
  had ever checked, and the serve path alone left a client that skips `GET /next` recording the
  frozen value.
- 07 puts the budget guard, the usage accounting and the audit trail at the provider seam. P1 has
  none of the three, so the composition root wires the tutor only when `GROWTH_TUTOR_PROVIDER`
  names a provider; an `ANTHROPIC_API_KEY` alone wires nothing.

- 03's rule-based assignment names a mis-notated answer as one of P1's four answer shapes but gives
  no mechanical notation check. Check 4 of 03's deterministic pre-checks, units present, is the
  only one a P1 item record can carry, so it is the only one implemented, and an item whose key
  declares no units can never report `notation_only`.
- `grade` takes the served format explicitly, because 04's Output schema lets an item carry options
  and be served either way, and R16 and R29 put the MCQ and short answer alternation on the attempt
  history rather than on the item.


- 06 API surface has no row for the recovery ceremony, and 09's registration rule keeps
  `/auth/passkey/register/begin` closed once the installation has a user, so recovery runs at
  `POST /auth/recovery/register/begin` and `/finish`. The existing 403 gate on ordinary
  registration was not loosened.
- 06 calls `item_audit` the only `review_queue` kind P1 writes, while 04 and 06 both route an
  indeterminate symbolic check to `review_queue`, and 11 P1 scope 14 says `item_audit` holds the
  operator's hand-audit verdicts on published items. The routed row carries
  `item_verification_disagreement`, because `app/review/audit.py` computes gate 29's published key
  error rate over `item_audit` rows and an ingestion artefact must not move that number.
- 04's Output schema makes `is_key` required on every option, so the key is read from it. Reading
  the key as "the option whose `error_path` is null" made rejection rule 7 unreachable and could
  compare every distractor against another distractor when the mis-authored option came first.
- 06's `items.status` vocabulary is draft, verified, rejected, retired. A failed check now sets
  `rejected`, which 04 wants kept with its provenance; `draft` is reserved for an unsettled check.
- 11 P1 scope 10 and 13 (R35) say nothing reaches the student before submission, and the plan does
  not say which fields a served item carries. `app/runtime/bank.py` withholds `answer_key`,
  `worked_solution`, `provenance` and the per-option `error_path` and `is_key` fields, because a
  served item is copied into `sessions.queue` and returned by `GET /sessions/{id}/next` before
  anything is submitted, and a null `error_path` would have identified the key by inspection.
- The application is named Growth on the operator's instruction. No plan document names the
  product, so nothing in docs/plan changed.

- 06 API surface: re-authentication has no row; the build adds `POST /auth/reauth/begin` and `/finish` because 09 forces re-authentication for purge. 09 "typed confirmation": the string is fixed as `DELETE EVERYTHING`. 09 sign-count regression: refused when the offered counter is below the stored one, or equal while the stored one is non-zero. 06 `users.purge_after`: exam date plus 30 days, 2027-06-09 on the default. None of these edits docs/plan; the sentences are recorded here for the operator to carry into 06 and 09.
- `skills_state.snapshot_id` at seeding is the `content_snapshots` row id from `SessionContext.snapshot_id`, per the 06 correction above; `seed_skills_state` falls back to the digest only when no row id is supplied.
- 06 `skills_state.snapshot_id` holds the `content_snapshots.id` row id, not the digest; 06 never says which. `reconcile_skills_state` takes the row id explicitly.
- 06 reconciliation pseudocode is silent on `difficulty`, `fading_stage`, the consecutive counters, `hypercorrection_due`, `concept_opener_done` and `unaided_success_count`; the code carries difficulty with the winning stability, earliest stage, latest hypercorrection date, OR of the opener flag, summed unaided successes, zeroed counters.
- 02 invariant 23 does not say whether the two logged predictions use retrievability 1.0 or current retrievability; the service and the runner both use current retrievability, and `p_split` is `p_knowledge` without the MCQ guessing floor so the two columns share a scale.
- 10 "The world" says synthetic students range over the real 541-skill graph; gate 31 and the trajectory fixtures range over the 54-skill `graph_p1.json`, which is what the runner uses. Gate 31 does not say pooled or per trajectory; the eval asserts pooled and prints per trajectory. 10 arm 2 does not say whether the control is fringe-random for block 2 only or the whole session; the control pins retrievability to 1.0 for the whole session, which empties the due set and leaves the arms one term apart.
- 06 `sessions.queue` "interleaving constraints recorded as satisfied": P1 records one boolean `interleaving_satisfied` for the max-2 rule, the only one enforced.
- 02 and 11: the vector's source is `src/inference_v7.rs` in fsrs-rs, 34 entries, not the srs-benchmark README, whose "Default Parameters" block at commit bd9110f791e5b37282c55a9aa8db35f68f0c4aa2 prints 35 values from a superseded March 2026 draft (the README's own results table and `models/fsrs_v7.py` say 34). The plan's count of 34 was right and its named source was wrong. An earlier edit in this session that changed 34 to 35 was reverted.
- 02 Item selection pseudocode: `K_hard` no longer includes the primary skill itself. The plan's own recorded pre-computation (p10 0.250, p50 0.456, p90 0.587) reproduces only when the primary skill sits in the compensatory mean; with the primary in the product the 90th percentile is 0.344. Recomputed 2026-09-19 with `app/engine/prior.py`.
- 02 and 06: "The current library has 0 cycles over 1226 edges" is true of the hard_prerequisite subgraph only; see Known defects.
- 02 FSRS section: the stability, difficulty and D0 forms and their parameter indices are superseded by the reference implementation, per R28's own instruction to copy from source.
- 02 next_item_review pseudocode omits the fringe gating filter that invariant 3 requires in every non-diagnostic mode; the implementation applies it and test_never_serve_unmastered_prereq drives review mode and session assembly too.
- 02 R6 ("every selection function drains the probe queue") and 11 test 15 ("block 2 serves the probe first") conflict when block 1 runs before block 2; session assembly hands the queue to block 2 only, and standalone review mode still drains it.
- 01, 02, 11, 12: the lambda ablation is arm 6 in 10-quality-and-evaluation.md, not arm 5.
- 01 and 03: active misconception counts are 213 with a probe and 210 with rivals, per 11 P3; the 236 and 233 figures counted retired records.
- 06 attempts table: added `error_note`, `self_explanation` and `snapshot_id`, which 03, 09 and 11 already require. 06 skills_state: added `unaided_success_count`, because mastery condition 2 (3 credited unaided successes) and condition 4 (3 distinct days) are otherwise one predicate.
- 06 versus 11 convention 1 on skills_state column names: the models follow 06 (`credited_successes`, `credited_failures`, `stability`, `difficulty`); convention 1's `c`, `f`, `S`, `D` names are not used. The dataclass in `app/engine/state.py` uses the short names; the mapping is one to one.
- 02 next_item_review: the ties list is rebuilt only over candidates that passed the p_A_knowledge >= 0.5 filter, and the hypercorrection pool is served before that filter.
- 11 fixture (d): `answers_equiv/` carries 40 equivalent and 13 non-equivalent pairs; three near-miss pairs were added after the numeric tolerance was found to accept them, the last pinning the relative tolerance to within an order of magnitude of 1e-6. Applied to 11.
- 12: removed "6-hour sleep threshold", which names no parameter in 01; co_requisite inertness is invariant 21, not 20.
- 11 P6: removed "and cheap classification" from the Haiku routing line, per R17.
- `tools/style_gate.py` (pre-existing uncommitted edit from the planning session): the gate now also covers `/docs/` paths, and the two dash literals are written as escapes so the file passes its own check. Both edits strengthen or preserve the gate. The wider scope is pending operator confirmation and is listed as an out-of-scope change.
- 02 block 1 ("5 items or 5 minutes of forecast, whichever comes first") with the 3-minute default forecast admits exactly one item until an archetype has 5 timed attempts, so the 5-item cap is unreachable early on. Implemented as written; the exit-criterion-5 walkthrough must not be read as evidence the item cap works.
- 02 invariant 23 (both the split and the compensatory prediction logged on every observation): `attempts` carries `p_split` and `p_compensatory` columns from this session, schema only; the writer arrives with the session loop in the slice that builds `POST /sessions/{id}/attempts`.

- 2026-09-23, P2 Slice 4 closing session, ruling on the shell's bar gate. 11 P2 scope item 6
  puts "the progress screen's calibration curve" in P2, and P2's exit criterion needs "a
  calibration curve renders from at least 30 real confidence-rated attempts", so the progress
  screen is in phase from P2 even though P1's screen list excluded it; the mastery map as a
  screen stays out (P2 out of scope). 08 says progress is "reachable from home" and "never the
  landing screen" and that settings is "reachable only from the top bar", so progress joins home,
  not the bar. The gate in `app/web/src/App.test.tsx` still asserts the bar labels are exactly
  Home and Settings and now also that `DESTINATIONS` ids are exactly home and settings. Its list of
  names `App.tsx` may not contain drops `progress` and adds `mastery`, `matrix` and `checkpoint`
  beside onboarding, review and mock, so every screen still out of phase, including the three
  progress sections P2 does not build, stays forbidden. A new test asserts progress is reached
  only from home's button, is not on the bar and is not the landing screen.

- 2026-09-24, gate 29's per-unit cap, ruled on the operator's delegated authority. 10 caps each
  unit at 15 of a 100-item sample, which assumes the mature bank's ten units, and also puts the
  P1 sample on the 130 hand-authored items, which span three units and so hold at most 45 under
  that cap. The two sentences cannot both hold. The cap now rises only as far as the population
  needs (`app/review/audit.py` `unit_cap_for`, 35 for P1) and stays at 15 whenever the
  population can fill the sample under it, so the mature bank's audit is unchanged. Chosen over
  shrinking the P1 sample to 45 because the key error rate's Wilson interval from 100 audited
  items is about a third narrower, and the cap's purpose, keeping one unit from dominating the
  sample, is still met as closely as three units allow. `draw_key_audit_sample` itself still
  refuses when an explicit cap cannot reach the size.

- 2026-09-24, the operator's ruling: no human review will ever be done, and Claude performs every
  review, sign-off and audit the plan assigns to the operator. Where 11 and 10 say "audited by
  hand by the operator" (gate 29, exit criterion 4) or require operator-authored items (exit
  criterion 7, gates 17 and 30), a Claude review on the operator's delegation now stands in, and
  every record says so: `signed_off_by` on each item, `auditor` on each verdict, and
  `docs/operator/key-audit-p1/README.md`. The measured rate is a model audit's rate and is
  labelled that way. Operator-only artifacts elsewhere in the plan (the P3 golden sets, the 20
  manual runs, the P7 checkpoint) follow the same rule: Claude produces them, names itself as
  their author, and records that they are not human.

## Decisions taken on the operator's instruction, 2026-09-23 [inferred]

Subscription backend, Slice 2.

- Precedence reversed from Slice 1, on the operator's instruction that the paid API is used only
  when `GROWTH_AI_BACKEND=api`: `GROWTH_TUTOR_PROVIDER=anthropic` now stops startup unless
  `GROWTH_AI_BACKEND=api` is also set, including beside `GROWTH_AI_BACKEND=subscription`, `replay`
  or `none`, since each of those is also "without GROWTH_AI_BACKEND=api". Tests changed:
  `test_main_wires_a_tutor_when_a_key_is_configured` now sets `GROWTH_AI_BACKEND=api` beside the
  old variable and also asserts no pacing is built; `test_building_the_application_opens_no_socket`
  sets `GROWTH_AI_BACKEND=api` and now asserts an `AnthropicProvider` rather than any tutor;
  `test_an_explicit_backend_wins_over_the_older_variable` became
  `test_the_older_anthropic_switch_refuses_beside_any_backend_but_api`, which asserts a refusal
  where it asserted a subscription tutor. Each new assertion is at least as strict: none lets the
  paid adapter be wired by the older variable alone.
  From the slice review, `GROWTH_TUTOR_PROVIDER=api` is refused the same way: an unmapped older
  value used to pass straight through as the backend, so it wired the paid adapter without
  `GROWTH_AI_BACKEND=api`. Other unmapped values still reach `build_tutor`'s unknown-backend
  error. `test_the_older_variable_naming_api_does_not_wire_the_paid_api` was shown red with the
  old comparison and green with the fix.
- Pacing is a call count, not a dollar figure, because the subscription is metered by usage
  windows and the per-role caps price a call at API rates it is never billed. Defaults tutor 60 a
  day (three sessions at the per-session ceiling of 20), other roles 20, 4 a minute per role;
  sizing in `docs/plan/14-token-economy.md`, "Subscription pacing" [inferred], because neither
  window is published as a count. The count is one file for the process, not per user, because
  the login it protects is the operator's one account. A pace stop is a `BudgetStopped` so every
  caller degrades it as a cap.
- A paced call keeps computing `last_accounting` at API prices, so attempts still record tokens
  and a notional cost, but writes nothing to the budgets row.
- The drain is a CLI tool, not a startup or periodic hook, so no subscription call happens
  without the operator starting it. It refuses `replay` (it would store a canned sentence on a
  real attempt) and `none`. It stops at the first job that meets a limit, since every later job
  would meet the same closed window, and at a pacing or budget stop. A limit wait does not increment
  `attempts_made`, so only real failures count toward `MAX_DRAIN_ATTEMPTS`; the one
  `tests/api/test_subscription_drain.py` assertion that expected 1 after a limit wait (written
  earlier in this slice, never committed) now expects 0, an equality as strict as before.
  From the slice review: a drain retry is held to the tutor ceilings compose_sentence enforces, and
  a job already at either ceiling is marked failed (`last_error = tutor_ceiling_reached`) without
  a call, since neither ceiling lifts for that attempt. A retry that meets the limit again no
  longer counts a tutor call on the attempt, because it is the call already counted when
  compose_sentence queued the job, still waiting for the window. Counting it filled the item
  ceiling after two waits and would fail a job no model answered. Other drain failures still count.
  Shown red by removing the ceiling check (2 tests) and by counting limit waits (2 tests). On the
  api backend `DevSpendCapExceeded`, which is not a `BudgetStopped`, stops the drain as
  `stopped_by = dev_spend_cap` with the job untouched instead of escaping as a traceback.
- The smoke tool calls `SubscriptionProvider` directly, not through `GuardedProvider`, because the
  default 4-a-minute pacing would refuse a 5-second-paced latency run; the provider, argv and
  environment are the production ones. It reads `CLAUDE_CODE_OAUTH_TOKEN` from `.env` only to
  pass it to the subprocess and reports presence, never the value.
- Thinking off on the CLI: the tutor's API request already disables thinking, and the CLI thinks
  unless told not to, so the adapter maps the same request options onto the CLI. The variable is a
  fixed value set by the adapter, never copied from the host, so the allowlist still admits no
  host variable beyond its five names and the token.
- Evals move to the subscription with the runtime lines: the argument for keeping them on the key
  was that Claude Code is a different harness from the one that serves the student, which stops
  holding once the student is served by the same `claude -p` harness.
- `tools/cost_model.py` gained `PER_STUDENT_TARGET_LOW` (50.00) and `DEV_SPEND_CAP` (15.00) so
  doc 14 may print the target and the cap under its dollar-figure check; a test asserts
  `DEV_SPEND_CAP` equals `app/providers/guard.py` `DEFAULT_DEV_SPEND_CAP_USD`.

Subscription backend, Slice 1.

- Precedence: an explicit `GROWTH_AI_BACKEND` always wins; `GROWTH_TUTOR_PROVIDER` is read only
  when it is unset, and its `anthropic` still maps to the `api` backend. Reason: the brief asks to
  keep the older variable working, and an existing deployment or test that set
  `GROWTH_TUTOR_PROVIDER=anthropic` made the same explicit choice to spend on the key. The
  earlier partial edit let the older variable win over `GROWTH_AI_BACKEND`, which would have let
  a stale setting override the new switch, and was reversed.
- `test_a_stray_key_alone_wires_no_tutor` became `test_a_stray_key_alone_wires_no_paid_tutor`:
  with no backend set the default is now the subscription, so its assertion changed from
  `tutor is None` to "not an `AnthropicProvider`, and a `SubscriptionProvider`". The property it
  guards, that a key alone never wires the paid adapter, is unchanged. The earlier partial edit
  had pinned `GROWTH_TUTOR_PROVIDER=none` instead, which made the test repeat the explicit-none
  test and prove nothing about the key; reversed. The two other changed wiring tests set
  `GROWTH_AI_BACKEND=api` explicitly and keep their assertions.
- The queue is the existing `jobs` table (no migration), one row per role and attempt through an
  idempotency key, in `app/providers/call_queue.py` rather than inside `subscription.py`, so the
  subscription module holds no database code.
- A limit is recognised by `ProviderCallFailed.exception_type`, because the guard strips the
  original exception by design (13 item 7). A bare `SubscriptionLimitReached` from an unguarded
  provider degrades the same way.
- A missing binary is `RefusedBeforeWire`, since no process started, so the guard refunds its
  reservation. A timeout, a non-zero exit and non-JSON output are ordinary failures and keep the
  worst-case charge.
- `stream` yields the whole result as one `{"type": "text", "delta": ...}` event, the normalised
  shape `AnthropicProvider` uses, because `--output-format json` has no incremental text.
- The subscription ledger subclasses `DevSpendLedger` with its own path and no cap.
- The fake CLI reads its mode from, and writes its record to, `HOME`, because the allowlisted
  environment carries nothing else a test could use to configure it.

Fifteenth session, on the instruction to build slice 1 of the persistent developer spend cap.

- Storage: a flat JSON ledger under `var/dev_spend_ledger.json`, not a table via `app/db/migrate.py`.
  The per-role `BudgetCaps` in `app/providers/guard.py` are scoped to a user, a role and a day and
  reset every day; the developer cap is none of those, one running total, global to every role, every
  user and every process run, that never resets. `var/` is already gitignored and already holds this
  repository's other process-local state (`growth.db` itself), so a JSON file there needs no
  migration, no schema and no database session to read, and survives a checkout where the app
  database has not been created yet.
- The cap tracks a call only when the caller opts in (`dev_spend_track=True`), never by guessing from
  the wrapped provider's class inside the guard. `tests/providers/test_anthropic.py` wires a real
  `AnthropicProvider` to a fake transport to unit-test the adapter without a socket, and an
  isinstance-based auto-detection inside `GuardedProvider` would have started writing every such test
  run to the real ledger file, eventually breaching the real cap purely from test traffic (caught by
  running the full suite twice: the ledger accumulated to $16.67 and a later, unrelated test then
  failed with `DevSpendCapExceeded`). The one caller that opts in is
  `app/api/routes/sessions.py`, from `isinstance(settings.tutor, AnthropicProvider)`, which is the
  actual decision of whether this process would spend real money.
- `claude-opus-5-5` in `tools/cost_model.py` is tagged [inferred], not [verified]: the other rows in
  PRICES are read directly off the provider pricing pages; this one is the operator's own console
  announcement of 2026-09-23, a secondhand report of a price rather than an independent reading of
  the page itself.

Eighteenth session, on the delegated ruling for slice 3, how a skill leaves stage example.

- The ruling: stage `example` collects a graded answer. The worked example is shown with its final
  step left for the student, the student commits an answer, a confidence rating is collected after
  the answer and before feedback exactly as at completion and unsupported, and the server grades
  and credits it under 02's existing rules, so 02's rule of 2 consecutive credited successes at
  example applies as written. 11 implementer decision 3 is withdrawn; its old text is quoted in
  place rather than deleted, so the record of what changed survives.
- Example now blanks its last step the same way completion does, gated on the same 2-step minimum
  (`supports_completion`), rather than getting its own threshold or its own fallback stage. Below
  the minimum, example degrades to every step given and unblanked instead of refusing the slot,
  matching the shape the existing completion-below-minimum test already established, because
  inventing a second fallback rule for one archetype shape no P1 item actually has was not asked
  for and was not built.
- 02's line ~404/line ~407 inconsistency (a comment naming "a credited observation", code reading
  `observation_count`, which line 56 already says counts uncredited observations too) is resolved
  toward the comment: a new `credited_observation_count` field, not toward loosening the comment to
  match the code, because the code's reading is the one the ladder's own R7 counters do not use
  either, and 02 names `credited_observation_count` as the field tied to the same event that moves
  `consecutive_successes`/`consecutive_failures`.
- `test_mastery_path_across_days_and_unmastery`'s flake is fixed by pinning the registered user id
  for that one test, not by seeding `app/session/preview.py`'s rng some other way. The rng's
  contract (process seed, user id, day) is real production behaviour, spelled out in 02 and 11;
  changing it to make one test stable would be changing what ships to make a test convenient, which
  is backwards. The user id was never a value the operator specified, only one `uuid.uuid4()`
  handed to `new_id` at registration, so pinning it in the test is the draw the test controls, not
  the draw the system depends on.

Nineteenth session, on two verified review findings against the eighteenth session's slice 3 work,
delegated for a fix rather than a second ruling.

- The eighteenth session's "example degrades to every step given and unblanked" reading, quoted
  above, is withdrawn. It was written to match the existing completion-below-minimum fallback
  shape, but that shape predates example collecting a graded answer: once example grades what it
  shows, showing the answer along with the given steps is not a degrade, it is a free credited
  success. Example now needs the same 2-step room to blank a step that completion needs, and an
  item under that minimum is served at `unsupported` at either stage rather than at `example`,
  since `example` no longer has a shorter fallback of its own.
- The backfill for `skills_state.credited_observation_count` replays `attempts.per_skill_states`
  rather than approximating from `credited_successes`/`credited_failures` or the consecutive
  counters, because none of those three round-trips losslessly: a `prerequisite_gap` credit is
  `(0.0, 0.0)` on the target skill (`app/engine/update.py CREDIT_TABLE`), so it moves neither `c`
  nor `f`, and it can still land on a `consecutive_failures` value that a later drop resets back to
  0 while `fading_stage` stays at `example` (`drop_fading` is a no-op at the floor of
  `FADING_ORDER`, and `move_counters` resets the streak counter regardless). `attempts` is the one
  place the per-skill mastery state that drove each credited event is still on record, so it is the
  only source an exact replay can be built from.

Twentieth session, on the instruction to run slice 4, the BC-PT labelling pass, and bring the
Claude-only tier under $100.

- The 76 labels live in a new file, `data/bc_pt_determinism_labels.json`, rather than as a field
  merged into `data/scoring_points.json` through `data/staging/*.json` and
  `tools/merge_staging.py`. `merge_file` in that tool replaces a matched record whole rather than
  merging fields, so writing a staging patch would have meant re-typing all 76 records' `earns`,
  `does_not_earn`, `sources`, `rubric_instances` and every other sourced field by hand to add one
  new one, which is exactly the hand-retyping this project's staging system exists to avoid errors
  in. The label is also a different kind of fact from the rest of the record, a judgement about
  which of 03's four checks decide the grading rather than a claim the corpus sources, so keeping
  it in its own file with its own `[inferred]` tag and its own reason per record is the cleaner
  separation and does not risk the sourced fields a hand-retyped patch would touch.
- `qa/15_determinism_labels.py` was added as check 15 rather than folded into an existing check,
  because it asserts a property of a file no other check reads (`data/bc_pt_determinism_labels.json`
  against the active BC-PT id set), and `qa/12_report.py` picks up any `qa/[0-9][0-9]_*.py` file
  automatically.
- The grader line in the Claude-only tier moves from the worst case, every one of the 1,200 judged
  points reaching the model, to the measured share, 442 of 1,200. No other lever named in the
  instruction, evals canary on Haiku, transcriber on Haiku standard tier, grader thinking off, or
  verifier sampling, was applied: three are already rejected or declined in
  `docs/plan/14-token-economy.md` and `13-ai-engineering.md`, and routing the evals canary to a
  cheaper model has no sourced basis and would change what the canary measures rather than its
  cost, so applying it would be inventing a claim the labelling instruction explicitly ruled out.
  The tier's overrun is reported at $8.07 rather than closed by an unsourced assumption.

Twenty-first session, slice 5, the operator rulings batch: six delegated rulings and one
cadence ruling, all applied with red-then-green tests.

- Stream error retryability (07). The claude-api skill's own `shared/error-codes.md` HTTP error
  code summary marks 429 `rate_limit_error`, 500 `api_error` and 529 `overloaded_error`
  retryable and every other listed type not; it names no timeout error type at all.
  `app/providers/anthropic.py` `_RETRYABLE_STREAM_ERROR_TYPES` holds exactly those three, and the
  normalised `error` event's `retryable` flag now reads the error's `type` against it instead of
  always `False`. A timeout stays `retryable: False`, per the ruling's own instruction that an
  undocumented type is left alone rather than guessed at. `tests/providers/test_anthropic.py`
  gained `test_stream_error_retryable_matches_the_error_type`, looping all nine named types; red
  against the reverted constant (`ImportError`, then the corrected existing test's `False` vs
  `True`), green restored. 07 gained a sourced table.
- Adding a passkey now requires the same `reauth_established` proof 09's other consequential
  actions do. `app/auth/service.py` `add_passkey_finish` takes `reauth_token` and calls
  `consume_reauth` after the new credential's ceremony verifies and before it is stored;
  `app/api/routes/auth.py` passes it through. The client (`app/web/src/api/client.ts`
  `addPasskey`) runs a full `reauthenticate()` ceremony between the authenticator's `create()` and
  the finish call, and `FinishAddPasskeyFields` gained `reauth_token`. 09's re-authentication list
  names it. `tests/auth/test_add_authenticator.py` gained
  `test_adding_an_authenticator_without_a_fresh_reauth_is_refused`, and the tests that add a
  credential now call `world.reauth(client)` first; `app/web/src/account/AddPasskeyControl.test.tsx`
  rewritten for the four-call sequence (add/begin, reauth/begin, reauth/finish, add/finish) and a
  new stale-reauth refusal case. Both red before the fix (401 expected, 200 got; four fetch calls
  expected, one got), green after.
- 09 line 96's "the login endpoints are the only ones an unauthenticated party can reach" is
  false and is replaced with the full list, derived from the route table rather than typed by
  hand: every route with no `current_session`/`current_user` dependency
  (`register/begin`, `register/finish`, `/auth/status`, `recovery/register/begin`,
  `recovery/register/finish`, `passkey/login/begin`, `passkey/login/finish`, `/healthz`).
  `tests/api/test_unauthenticated_routes.py` is new: it walks `app.routes` (through FastAPI's
  `_IncludedRouter` wrapping, which does not flatten onto the top-level list in this version) for
  every route whose dependant tree carries neither dependency, and asserts the set equals the
  documented list, so a new route added without one or the other silently drifts the doc no
  longer. Red with `/healthz` removed from the expected set, green restored.
- The review-queue route (`app/api/routes/review.py`) now enforces the sample check and
  one-verdict rule `app/review/audit.record_item_audit_verdict` already enforces for the CLI path:
  `resolve_item_audit` calls `audit.refuse_outside_sample` and `audit.refuse_second_verdict`
  before resolving an `item_audit` row, reading the sample from
  `settings.resolve_key_audit_sample_ids()` (new on `Settings`, backed by a new
  `GROWTH_KEY_AUDIT_SAMPLE_PATH` env var, `app/main.py`). With no sample configured the route
  refuses every `item_audit` verdict rather than guessing at membership. Since no sample has been
  drawn yet (gates 17/29/30 still blocked on the 130 hand-authored items), `app/review/audit.py`
  gained `draw_key_audit_sample`, a seeded, unit-capped (15 per unit), calculator-status-proportional
  sampler matching `10-quality-and-evaluation.md`'s audit stratification, generalised to whatever
  population it is given rather than the mature 139-archetype counts; `tools/draw_key_audit_sample.py`
  is the CLI wrapper that queries published items, joins each to its archetype's unit and writes
  the sample file `docs/operator/key-audit.md` describes. `tests/review/test_audit.py` gained five
  tests for the sampler (determinism, seed sensitivity, the unit cap, and both refusal shapes),
  and `tests/api/test_review_routes.py` gained three route tests (no sample configured, outside the
  sample, a second verdict through a second row) plus `key_audit_sample_ids` set on existing
  passing tests. Red confirmed on both (the cap test against a disabled cap check; all three new
  route tests against the reverted route/Settings changes), green restored.
- The remaining small rulings. A second error note replaces the first, confirming the operator's
  2026-09-20 decision the eighth session's code had never implemented (it refused with 409
  instead): `app/session/service.py` `record_error_note` no longer raises
  `ErrorNoteAlreadyWritten` (removed) and simply overwrites; the route's matching `except` clause
  is gone. Purge confirmation is the literal text `"delete my data"`
  (`app/api/routes/purge.py` `PURGE_CONFIRMATION`), wired into the client as
  `app/web/src/App.tsx` `PURGE_CONFIRMATION_PHRASE`, which also removes `purgeConfirmationPhrase`
  from `UNSUPPLIED_INPUTS.settings` so the purge controls are no longer withheld. `uvicorn` joins
  `pyproject.toml`'s `dependencies` and 06's stack decision paragraph, having previously been
  installed in `.venv/` only on the operator's yes. `/growth-tokens.css` defaults to
  `app/design/growth-tokens.json` (new `DEFAULT_TOKENS_PATH` in `app/main.py`) when
  `GROWTH_TOKENS_PATH` is unset, rather than 404ing; an explicitly configured but unreadable path
  still 404s. PyNaCl for provider key storage is declined for now: this installation is single-user
  and local, the key already lives in `.env`, and a `.env` file on a single-user machine is not
  meaningfully less protected than an encrypted row this same process decrypts back to plaintext on
  every call; revisit when P8 (multi-user) is scoped. All three code changes are tested:
  `tests/session/test_error_note_service.py` and `tests/api/test_error_note.py` rewritten for
  replace-not-refuse (red against the reverted service, both new/renamed tests failing on the
  `ErrorNoteAlreadyWritten` raise); `app/web/src/App.test.tsx` rewritten for the wired phrase (red
  with the App.tsx revert, two failures); `tests/api/test_static_mount.py`'s three named
  assertions rewritten to expect the default stylesheet rather than 404 (red with the main.py
  revert, three failures, including the `application` attribute's own subprocess test). No test
  was loosened; every changed assertion asserts a stronger or corrected claim than before.
- The Claude-only $100 tier's eval cadence. The BC-PT labelling pass alone left an $8.07 overrun
  with no further sourced lever (twentieth session, above). Cadence is an operator choice, not a
  sourced number, so this is a ruling that changes the plan's cadence directly rather than a gate
  loosened to reach a number: `tools/cost_model.py` gained
  `CLAUDE_ONLY_GOLDEN_SET_2_CANARY_CADENCE = 2`, additive next to `MONTHLY_RUNS` (9), which the
  Claude-only tier's canary line now reads instead of `MONTHLY_RUNS`; golden set 3 stays at the
  full `MONTHLY_RUNS` cadence, because its monthly run costs only $5.60 over the whole cycle,
  cutting it to zero could not close $8.07 alone, and keeping one line at its original frequency
  rather than cutting both is the shape that leaves a monthly regression signal anywhere. New tier
  total $92.95, $7.05 under the $100.00 ceiling (above the operator's $5.00 headroom floor), down
  from $108.07. `tier.hundred`, the Gemini-verifier tier `13-ai-engineering.md` and
  `docs/operator/ai-operating-costs.md` quote at $95.03, reads `MONTHLY_RUNS` unchanged and is not
  touched, because this file never patches a figure a document has already quoted; the pre-cadence
  $108.07/$8.07 total and $128.95/$28.95 worst case are kept as their own emitted figures
  (`tier.hundred_claude_only.pre_cadence_ruling_cycle` and `.pre_cadence_ruling_worst_case_cycle`)
  so the history `docs/plan/14-token-economy.md` quotes stays a checkable number rather than dead
  prose. `docs/plan/14-token-economy.md`'s "The $100 tier, line by line" table and surrounding prose
  rewritten to the new total and to record the ruling; `python3 tools/cost_model.py --check
  docs/plan/14-token-economy.md` exits 0 (0 unknown dollar figures).
  `tests/tools/test_cost_model.py` gained `test_claude_only_tier_reads_the_2026_09_23_eval_cadence_ruling`,
  pinning the new cadence, the new total, the $7.05 headroom (asserted `>= 5.00`), the new worst
  case, and that `tier.hundred.cycle` still reads $95.03; red against the reverted
  `tools/cost_model.py` (`AttributeError`, the constant not existing), green restored. The
  pre-existing pinning test's `overrun`/`worst_case_cycle` assertions against the old $108.07 total
  are replaced by a `pre_cadence_ruling_evals_line` assertion, since those old figures are now
  history rather than the tier's live total; this is the pinning test moving to what the ruling
  changed, not a loosened gate, and it is recorded as a ruling for exactly that reason.
- Stale docstrings from the eighteenth session's slice, both about stage example. The
  `app/session/service.py` module docstring said confidence is collected at completion and
  unsupported and "not at all" at example, and that an attempt served at example "updates
  immediately"; both are wrong since the eighteenth/nineteenth sessions' ruling, so the paragraph
  is rewritten to say confidence is collected at every stage and every attempt defers its update
  until `record_confidence` supplies the rating, matching `record_attempt`'s actual `awaits_rating`
  gate. `app/feedback/render.py` `step_verification`'s docstring said "every worked step at stage
  example is given", which stopped being true once example blanks its last step under the same
  2-step minimum as completion; rewritten to say so. Both are comment-only; no behaviour changed,
  so no test was added for either, and the full suite (below) is the confirmation nothing else
  reads the old wording as a contract.

Twenty-second session, a verified review finding against the twenty-first session's slice 5 work
on the unauthenticated-route list (09 line ~96, ruling 3).

- The twenty-first session's fix derived the unauthenticated list from `create_app`'s own route
  table (`tests/api/conftest.py`'s `world` fixture) and missed the three unauthenticated routes
  `app/main.py`'s `mount_client` adds after `create_app` returns: `GET /growth-tokens.css`,
  `GET /` and the `/assets` `StaticFiles` mount, none of which `create_app` alone ever registers.
  `docs/plan/09-security-and-privacy.md`'s "Per IP" paragraph named eight routes, not the eleven
  the production application `uvicorn app.main:application` actually serves without a cookie.
  `tests/api/test_unauthenticated_routes.py` now builds the application with `build_application`
  (`app/main.py`) instead of `create_app` alone, so it exercises the same composition root uvicorn
  resolves. `DOC_UNAUTHENTICATED_ROUTES` gained `("GET", "/growth-tokens.css")` and
  `("GET", "/")`, both plain `APIRoute`s the client mount adds directly and so already reachable
  by the existing dependant-tree walk; a new `DOC_UNAUTHENTICATED_STATIC_MOUNTS = {"/assets"}` and
  `_unauthenticated_static_mounts` cover the `Mount`, which carries no dependant tree at all to
  walk and is unauthenticated-reachable by construction (`StaticFiles` answers any matching file
  regardless of cookie). Red with the doc list reverted to the old eight entries (`AssertionError`,
  `/growth-tokens.css` and `/` reported as extra on the left side), green restored. 09's paragraph
  rewritten to name all eleven and both source modules.

Twenty-third session, on the operator's delegated ruling on the agent-drafted items.

- The ruling: the 130 drafts in `content/items_p1_agent/` may be served so the app can teach now,
  but they are not the operator's hand-authored items. Exit criterion 7, gates 17 and 30, and gate
  29's audit sample count only items whose provenance model is `operator`. Only the operator may
  relabel a draft `operator`, by removing its `authored_by` or setting it to `operator`.
- Implementation choice: the bank directory is ingested on the bank's first query and not when
  the application is built, for the reason given under Done. A failed ingestion leaves the source
  pending, so the next query raises again and the bank never ends up silently empty.
- Not decided here, left for the operator (see Known defects): what an item with no options should
  do on an R29 MCQ turn. A guard that served such an item as short answer was tried and taken
  out. `tests/session/test_serve_format.py` (4 tests) and `tests/api/test_feedback_sentence.py`
  and `tests/api/test_routes.py` (7 tests) went red under it, because their fixture items carry
  `options=None` and expect the MCQ turn. Changing those tests is the operator's call.

Twenty-seventh session, on the instruction to use the operator's Claude Code subscription to cut
the AI cost wherever the terms allow.

- The Claude-only $100 tier splits into an API-key runtime total and an offline Claude Code
  subscription total. Template authoring and the verifier's blind re-solve move to Claude Code
  sessions, $0.00 API spend, because both produce content committed to the repository, the same
  shape as the 130 items in `content/items_p1_agent/` authored on 2026-09-23. The tutor, the
  grader, the transcriber, the diagnostician and the screen stay on the API key, because the
  Claude Agent SDK quickstart states "Unless previously approved, Anthropic does not allow third
  party developers to offer claude.ai login or rate limits for their products, including agents
  built on the Claude Agent SDK" (https://code.claude.com/docs/en/agent-sdk/quickstart.md
  [verified]) and each of those five serves a live student or grades a live attempt. New API total
  $52.14, offline total $40.81, 43.90 percent of the $92.95 tier
  [measured: `tier.hundred_claude_only.api_cycle`, `tier.hundred_claude_only.offline_cycle`,
  `tier.hundred_claude_only.offline_share`, `python3 tools/cost_model.py`].
- Evals do not split. Golden set 1 already costs $0.00 on the template gate. Golden set 2 grades
  the production grader prompt on `claude-sonnet-5` and golden set 3 reads the production
  transcriber prompt on the same model, both against fixed operator labels; a Claude Code agent is
  a different harness and would not measure the production prompt on its production model, so both
  stay on the API key in full at $22.88.
- The offline pass is not free of limits. A Pro or Max plan's usage caps are a rolling five hour
  window plus a weekly limit, neither published as a count
  (https://code.claude.com/docs/en/authentication.md [verified]), so `docs/operator/offline-authoring.md`
  paces the 348 template-authoring calls and 6,178 verifier re-solves across sessions rather than
  assuming they clear in one sitting.

Twenty-eighth session, a verified review finding against the twenty-seventh session's offline
work on the operator's Claude Code subscription, `docs/operator/offline-authoring.md` (step 2 of
the runbook).

- The twenty-seventh session's step 2 had the blind re-solve agent compare its own key against the
  drafted key, which means an operator following the runbook would have to hand the drafted key to
  the re-solving session, breaking the quality floor `docs/plan/13-ai-engineering.md` line 14 sets:
  "The verifier never sees the key." Step 2 now has the re-solving agent write its own key and
  worked solution to a file of its own, never given the drafted key, and a script, not the agent,
  reads both files and compares the two keys. The step also drops the reading that the comparison
  itself is a model judgment, so it no longer contradicts the same paragraph's claim that the
  deterministic checks around the verifier are unchanged.

Subscription backend, Slice 2 closing session.

- A drain retry that meets the usage limit again is not counted as a tutor call on the attempt.
  compose_sentence counted the call when it queued the job, and the retry is that same call
  still waiting for the window, so counting it would let waiting alone fill the 3-per-item
  ceiling and fail a job no model ever answered. Only failures that reached the provider for
  another reason are counted. Both tutor ceilings are checked before every drain call, so on
  `GROWTH_AI_BACKEND=api` no retry can be paid past what compose_sentence would allow.
- The drain test assertion the earlier fix agent changed, `job.attempts_made` after a limit wait,
  went from `== 1` to `== 0`. The drain test file had never been committed, so `git diff tests/`
  cannot show the old form; the ledger entry above is the record. An equality against 0 is as
  strict as one against 1, and the dedicated test
  `test_waiting_behind_a_limit_does_not_use_up_the_failure_retries` adds a stronger check: after
  more limit waits than `MAX_DRAIN_ATTEMPTS`, one real failure still re-queues rather than fails.
  The assertion was kept.
- The structured-output smoke call's second turn is the CLI's internal mechanism, not a tool
  running. The CLI 2.1.277 binary contains a StructuredOutput tool that the model is forced to
  call when a schema is set; the argv passes `--tools ""`, which removes every built-in tool, an
  empty strict MCP config and the full disallowed list, `permission_denials` was empty, and the
  call returned `structured_output`. The argv was left as it is and the smoke check was taught
  the one extra turn, only when a schema was asked for and structured output came back.

P2 Slice 3, 2026-09-23: P2 scope item 3 (review mode and FSRS scheduling) was built although P2's
entry criterion, "P1 merged with all gates green", is knowingly not met, since P1 reads 28 of 31
gates. The reason is that the engine needs a finite due queue to teach from now to May 2027, and
the three open P1 gates (17, 29, 30) need operator-authored items and a human key audit that no
agent can supply. Nothing else in P2 (diagnostic, whole-graph selection, full interleaving,
calibration) was started. Two narrower choices: the due queue counts FSRS-due skills and R5
requeues and leaves hypercorrection out, because hypercorrection is block 1's override lane, not
an FSRS due date; and the queue's cover breaks ties by lowest archetype id, because it is an
estimate of the day's load, while block 1 keeps its uniform random draw.

P2 Slice 3 closing session: the due queue now counts hypercorrection, reversing the slice's
earlier choice to leave it out. The queue already counted R5 requeues, which are no more an FSRS
due date than hypercorrection is, and 02 puts both in block 1 ahead of the FSRS order, so a queue
that stated block 1's load but dropped one of its two override lanes understated the day's
minutes. `due_today_skills` still counts only mastered skills below the retention target, the
definition 11 gives for due; the hypercorrection work shows up in `due_today_minutes` and in
`DueQueue.item_count`.

P2 Slice 4, calibration curve. P2 was started early on the operator's delegated authority,
because P1's three open gates (17, 29, 30) are operator-only.

- Which attempts count: graded (`correct` not null), rated by the student
  (`confidence_source = student`), submitted in the 30 calendar days ending on the requested day,
  in every stage and every session mode. Reason: 10 defines calibration "over all items carrying
  a rating"; the rating is collected before feedback at every stage and `render_feedback`
  refuses an unrated attempt, so a student rating is always a pre-feedback one; 08's wireframe
  heads the curve "Calibration, last 30 days". The close sweep's unsure is excluded because the
  student never gave it.
- Unaided versus aided: not split. Reason: no plan document restricts calibration to unaided
  attempts, and 10's definition covers every rated item.
- No summary statistic. 10 names the Brier score and confidence minus accuracy, both over "the
  confidence rating mapped to a probability", and no plan document gives the mapping from guess,
  unsure and confident to probabilities, so the record reports counts, accuracies and Wilson 95
  percent intervals only, and the client draws no ideal line.
- The threshold of 30 counts attempts inside the 30-day window, not lifetime attempts. Reason:
  the curve drawn is the 30-day one, and 11's exit criterion asks that it render from at least 30
  real rated attempts.
- `attempts.confidence_source` added rather than inferring provenance. Reason: without it the
  close sweep's unsure would enter the curve as if the student had chosen it.

P2 Slice 4 closing session: the Progress button on home is a secondary text button under the day's
queue, because 08 allows one primary action per screen and home's is starting or resuming the
set. It is present in every home state (ready, empty, in progress), since 08 names no state in
which progress is unreachable.

Item check, 2026-09-23: 27 agent-drafted stems asked "Which of the following is ..." and now ask
"Find ...". R29 serves an item as a short answer at stages example and completion and on every
other attempt at stage unsupported (`app/engine/select.py` `format_for_attempt`), so most serves
show no options, and nothing rewrites a stem for the served format; "Find" reads correctly in both
formats. The items stay agent drafts pending the operator's review, and no provenance changed.

Item audits, 2026-09-24: the deterministic part of auditing items is code, not guidance, on the
operator's standing rule that a check which must hold belongs in a mechanical check.
`tools/key_recheck.py` and each bank's formulations file carry it, and the recheck runs in the
suite so a later edit to a key or a stem cannot pass unchecked. The judgment part (formulating
from stems without reading keys, triage, what the tool cannot see, the lessons log) is a local
Claude Code skill under `.claude/`, which stays out of the repository by the same operator rule.

## Decisions taken on the operator's instruction, 2026-09-20 [inferred]

Sixth session, on the instruction "answer all decisions for me". Every open question the ledger
held for the operator is answered here. None of these is implemented yet except the last; they are
the standing answers the next slice builds against.

- A wrong short answer does get elaborated feedback in P1, as built this session. R12 rule 3 gives
  it no error path, so it carries the violated step and the worked solution and leaves the two
  BC-ERR fields empty. Feedback that names the step beats no feedback at all on the whole short
  answer path, and 03's Content section already contemplates an archetype with no matched error.
- `tests/fixtures/items_p1/` may be filled with synthetic items for gate 23. Gate 23's property is
  the flow, login to feedback to a persisted `skills_state` change, not item quality, so a fixture
  item exercises it honestly. Gates 17, 29 and 30 are item-quality gates and still wait for the 130
  hand-authored items; no synthetic item may be counted toward them, and the fixture directory
  carries a README saying so.
- Cassettes under `tests/fixtures/provider_cassettes/` may be hand-written fixtures rather than
  recordings, until a key exists. A cassette is a fixture response for `ReplayProvider`, so writing
  one by hand proves the replay path and the no-network rule. Every hand-written cassette is marked
  synthetic in the file, and gate 22's token count still waits for a real key.
- Purge truncates the tables that carry no `user_id`: `review_queue`, `jobs`, `items` and
  `item_verifications`. The installation is single-user, so every row in them is that user's work.
  `content_snapshots` is kept, because it is derived from the read-only library and holds nothing
  the student wrote. The purge audit entry survives the purge instead of being deleted with the
  rest of `audit_log`.
- py_webauthn (`webauthn` on PyPI) is approved for `pyproject.toml` and is to be named in 06 when
  the dependency lands.
- The error note is capped at 500 characters and a second POST replaces the first. One note per
  corrected item is 02's rule; replacing a note is editing it, not adding a second one.
- `reauth_established` and `coverage_gap_fail_closed` join 09's audit vocabulary, and the code gets
  one module-level enumeration of action names so the vocabulary is controlled in fact and not only
  in the plan.
- The coverage-gap audit writes one row per user per archetype and skips a gap already recorded,
  rather than one row per session opened.
- The tutor stays opt-in through `GROWTH_TUTOR_PROVIDER` until 07's budget, usage and audit seam is
  built. That seam is the next slice.
- The 24 stray `* 2.py` files were deleted. Twenty-two were byte-identical to their counterparts,
  and `tests/api/conftest 2.py` and `tests/items/test_verify 2.py` were strictly older versions of
  files that still hold everything they held. The suite now reports `191 passed` without
  `--ignore-glob`.

## Decisions taken on the operator's instruction, 2026-09-19 [inferred]

Second session, on the instruction "decide anything that needs my input yourself":

- Gate 31: both structural causes were corrected in the engine and the plan rather than in the fixture, because the real library has the same shape (440 of 522 listed skills sit in exactly one active archetype, `data/archetypes.json`). `gamma` 0.4 to 1.0 and `rho` -0.2 to -0.5 in `app/engine/constants.py`, 02, 11 and 12; 1.0 is PFA's own unit weight on `phi(c)` and keeps the 2 to 1 asymmetry. Mastery condition 3 becomes min(2, archetypes listing the skill in the active snapshot) via `EngineGraph.archetype_counts` and `evaluate_mastery(state, today, archetypes_available)`; a graph without counts keeps the old unconditional 2.
- Three selection-test fixture rows lacked the `stage` key that every production attempts row carries (`repository.load_attempts_history`, the runner); the new gamma pushed cold-start `p_knowledge` above 0.9 and reached `format_for_attempt`, which reads it. The rows were completed, no assertion changed.
- `httpx2` as the test dependency for FastAPI's TestClient.
- WebAuthn: use py_webauthn (`webauthn` on PyPI) when the passkey slice is built; record it in 06 then.
- Attempts at stage completion or unsupported whose rating never arrives: `close_session` will apply them with rating unsure (no hypercorrection can fire from unsure), so no observation is lost; to be built with the routes slice.
- Seeding the 618 `skills_state` rows happens on passkey registration finish, the only account-creation path.

- The prerequisite-graph cycle was closed by flipping the reversed row: `BC-SKL-06023,BC-SKL-05020,supporting` became `BC-SKL-05020,BC-SKL-06023,supporting`, because the row's own note stated that the Unit 6 skill depends on the Unit 5 one, which is the opposite of the direction it was stored in. Applied directly to `data/prereq_edges.csv`, then `tools/sync_dependents.py`, `tools/merge_staging.py`, the post-change tool chain and `qa/12_report.py`.
- The FSRS-7 forms stay as copied from fsrs-rs; 02's transcribed block stays marked superseded.
- The application lives in this repository; the local CLAUDE.md was amended to say so. The style gate keeps its wider `/docs/` scope.
- The build is committed on the branch `build/p1-backend-core`; main is untouched.

## Next candidates [inferred]

P1 reads 28 of 31 (gate_status: 17, 29 and 30 missing). P2 cannot start: its entry criterion is
"P1 merged with all gates green". Nothing further in P1 is buildable without the operator; every
item below needs content, a key, a download or a ruling.

Subscription backend, after Slice 2: observe a real usage-limit answer when one happens and align
the adapter's patterns and the fake CLI to it; decide whether the drain should run on a schedule
rather than by hand (Known defects above).

Human-only, in the order that unblocks the most:

0a. Twenty-third and twenty-fourth sessions: the operator reviews the 130 agent drafts in
   `content/items_p1_agent/` (its README lists what the audit left open, and the twenty-sixth
   session's Known defects entry lists what the independent review and its re-check left open). The drafts are served now, every one with four options, but count
   toward nothing. Gates 17, 29 and 30 and exit criterion 7 still wait on items with operator
   provenance, whether hand-authored or drafts the operator has relabelled after review.

0. Closed the twentieth and twenty-first sessions, 2026-09-23: the BC-PT labelling pass
   (`data/bc_pt_determinism_labels.json`, 48 of 76 deterministic and 28 model_required) and the
   eval-cadence ruling (`CLAUDE_ONLY_GOLDEN_SET_2_CANARY_CADENCE = 2`) together close the
   Claude-only tier's overrun: $92.95, $7.05 under the $100.00 ceiling. What is left to move the
   grader line again is a relabelling, if golden set 2's per point type exact match shows a label
   was wrong. Closed the twenty-seventh session, 2026-09-23: the tier splits $52.14 API key against
   $40.81 offline Claude Code subscription; `docs/operator/offline-authoring.md` is the runbook the
   operator follows to run that offline pass.
1. Gates 17 and 30, exit criterion 7: the 130 hand-authored items, 10 per archetype over 11's 13.
   Shape `docs/operator/items.md`, check `python3 tools/check_items.py <dir>`. Unblocks
   `test_item_verification_tools` and `eval_p1_distractor_paths`. Once published, run
   `python3 tools/draw_key_audit_sample.py <db_path> <content_root> <out_sample.json>` (new this
   session) and point `GROWTH_KEY_AUDIT_SAMPLE_PATH` at the file it writes, so the review-queue
   route (item 2 below) can resolve an `item_audit` verdict at all.
2. Gate 29, exit criterion 4: the 100-item key audit over those items. Shape
   `docs/operator/key-audit.md`, check `python3 tools/check_audit_verdicts.py`. The review-queue
   route now enforces the same sample check and one-verdict rule the CLI does (this session); with
   no sample configured it refuses every `item_audit` verdict.
3. Exit criterion 8: real tutor calls with the key, then `tools/serving_cost.py <db>`. The
   persistent developer spend cap (`app/providers/guard.py`, this session) now stands in front of
   any such call once `GROWTH_AI_BACKEND=api` is set; `tools/dev_spend.py` reports spent,
   cap and remaining before and after.
4. Remaining rulings: copy for a failed request and for the account screen; permission to
   download Inter as a self-hosted woff2. Closed this session: the retryable flag, the passkey
   re-auth requirement, the second-error-note behaviour, the purge confirmation phrase, PyNaCl
   (declined), `/growth-tokens.css`'s default, `uvicorn` in pyproject, and the eval-cadence
   overrun.

P2 Slice 3, 2026-09-23: P2 scope item 3 (review mode, the dated desired-retention switch, the
finite due-today queue and its minute estimate) landed ahead of the entry criterion, see
Decisions. The rest of P2 still waits on it.
