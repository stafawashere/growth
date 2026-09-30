---
title: Security and privacy
research_date: 2026-09-19
status: draft
purpose: State the threat model, the key and data handling rules, the injection and rate-limit defences, the password authentication flow, and the retention and deletion policy for a single minor learner.
---

# Security and privacy

This document covers the application described in `06-architecture.md` and `07-ai-provider-layer.md`. It is a planning document and contains no application code.

The posture is D10, amended 2026-09-27 on the operator's instruction: a username and password as the only authentication (D10 said passkeys; see the ruling under "Authentication with a password"), local-first single user, provider keys encrypted at rest, model output treated as untrusted data, the tutor holding no tools, generated items sanitised before rendering, rate limits per role and per IP, and a default purge 30 days after the exam date with an export first.

Two framing statements before the detail. First, the learner is a minor, which raises the cost of every data decision and lowers the tolerance for storing anything the product does not need. Second, this is not legal advice; where a question is legal rather than technical it is written below as an open question and carried into `12-open-questions.md` rather than answered.

## Threat model

Assets, ranked by what their loss costs.

| Asset | Where it lives | Loss consequence |
| --- | --- | --- |
| Provider API keys | `provider_configs`, encrypted | Financial loss to the operator, unbounded until noticed; abuse of the operator's account |
| The student's work and mastery history | `attempts`, `gradings`, `diagnoses`, `skills_state` | A detailed record of a named minor's academic weaknesses over a year |
| FRQ images | Object storage referenced from `attempts` | Handwriting, and whatever else is on the photographed page |
| Session credentials | Browser cookie; the scrypt hash in `users.password_hash` and the recovery code hash in `users.recovery_code_hash` | Full access to everything above |
| Content snapshot integrity | In-memory graph from `data/` | Corrupted mastery attribution, which is silent |
| Grading integrity | `gradings` | A student trusts a wrong score, or distrusts a right one |
| Operator's Claude subscription credential | Outside this application entirely, see `07-ai-provider-layer.md` | Account suspension; terms exposure |

Actors.

**The student.** Not an adversary in the usual sense, but the party whose mistakes matter most: a shared device, a screenshot, a misunderstood export. The student is also the party most able to damage their own learning by finding a way to see answers early, which is a product-integrity concern rather than a security one.

**The operator.** The person running the deployment and holding the keys. Trusted with everything, which is why every consequential action they take is recorded in `audit_log` rather than being invisible.

**A remote attacker.** Anyone who can reach the listening port. In the default deployment that is nobody, because the service binds to loopback. The moment it is exposed, this actor becomes the reason for TLS, CORS, CSP, rate limits and the password controls below.

**A malicious or compromised provider response.** The actor most specific to this product. Model output is data that arrives from outside the trust boundary and is rendered to a student, and a generated item stem is text the application itself asked a model to write and then displays. This actor also covers the case of injected instructions arriving inside a student-uploaded image, which the transcriber reads and passes on.

STRIDE, with the control that answers each row.

| Threat | Instance in this system | Control |
| --- | --- | --- |
| Spoofing | Someone authenticating as the student | Changed 2026-09-27 from WebAuthn passkeys: a password hashed with scrypt, a per-account lockout, a per-IP limit on the three sign-in routes, and a Host, Origin and plain-http check before any password is read. Weaker than a passkey against phishing and reuse, which the ruling below accepts |
| Spoofing | A process claiming to be the job worker | The worker shares the database file and the process boundary, not a network identity; no network auth to spoof because there is no network hop |
| Tampering | Modifying a mastery state or a grade directly | Database file permissions; `audit_log` records every state rewrite the engine did not initiate |
| Tampering | Modifying the content library between snapshots | Digest recorded on `content_snapshots`; a reload that changes the digest is an audited event |
| Repudiation | A grade with no explanation of how it was reached | `gradings` stores the samples, the deciding path and the rationale; `items.provenance` stores the model and prompt template version |
| Information disclosure | A key in a log, an error page or a URL | Keys never leave `provider_configs` except into a request-scoped buffer; no key in any log, URL, error or `audit_log` detail |
| Information disclosure | FRQ images served without authorisation | Images are served only through an authenticated endpoint scoped to the owning attempt; no public or guessable URL |
| Information disclosure | Student data leaving to a third party | No third-party analytics, no external fonts or scripts beyond what the CSP allows, provider choice constrained by the data policies below |
| Denial of service | A runaway loop spending the budget | Per-role daily caps checked before the call, inside the provider layer, outside the fallback chain |
| Denial of service | Request flooding | Per-IP, per-session and per-role rate limits with backoff |
| Elevation of privilege | Injected instructions causing an action | The tutor has no tools; no model output is ever executed, interpreted as an instruction, or used to select a code path |

The last row is the one that most often gets under-specified, so it is expanded in its own section below.

## Key handling

**Encryption at rest.** Provider keys are stored as libsodium secretbox ciphertext with a per-record nonce in `provider_configs`, under a key derived from an operator passphrase with a memory-hard KDF and a per-installation salt. The passphrase itself is never stored in any form, including a hash, because nothing in this system needs to verify the passphrase independently of decrypting with it: a wrong passphrase produces a failed decryption, which is the check.

Ruled 2026-09-23: PyNaCl (the libsodium binding this section needs) is declined for now, so `provider_configs`, `PUT /settings/providers/{provider}` and everything above stay unbuilt rather than gaining a weaker substitute. This installation is single-user and local, the key already lives in `.env` (read by `ANTHROPIC_API_KEY` per `docs/operator/provider-key.md`), and a `.env` file on a single-user machine is not meaningfully less protected than an encrypted row this same process decrypts back to plaintext on every call; adding PyNaCl now would spend a real dependency and a passphrase-unlock UX on a threat model, a shared or multi-tenant install, this project does not yet have. The decision is revisited when P8 (multi-user) is scoped, at which point a second user's key sitting in another user's readable `.env` is the actual gap this section exists to close.

**Memory handling.** The derived key exists only while the application is unlocked, and unlocking is an explicit action rather than an implicit startup step. A plaintext key is materialised into a request-scoped buffer, passed to the adapter for one call, and not retained on any adapter object between calls. This costs a decryption per call and buys the property that a heap dump taken between calls contains no key.

**No keys in logs or URLs.** Absolute. No log line, error message, stack trace, exception payload, URL path, query string or `audit_log` detail field contains a key or any part of one, including a masked prefix, because a masked prefix is still a disclosure. `GET /settings/providers` returns configuration without key material. The provider layer's structured logs record provider and model, never credentials, and never the raw provider response body. Added 2026-09-27: the same absolute rule covers the login password and the recovery code, a password or any part of one included, and a 422 on an `/auth/*` path is returned without FastAPI's echoed `input` and `ctx`, so a malformed sign-in body never comes back in the response.

**Rotation.** `PUT /settings/providers/{provider}` with a new key requires passphrase re-entry, writes a new ciphertext and nonce, records the rotation in `audit_log` with a timestamp and no key material, and invalidates any cached client holding the old key. There is no key history, because a retained superseded key is a liability with no benefit.

**The desktop keychain option.** Where the application runs as a desktop app, the derived key may be held in the OS credential store instead of re-derived at each start. This is a convenience trade, stated as one in the settings screen: it removes a passphrase prompt and moves the trust boundary to the operating system account. Offered, never defaulted.

**What is stored for claudebox.** The loopback base URL and the `CLAUDEBOX_API_KEY` bearer token, encrypted like any other secret. The operator's Claude subscription OAuth token is never read, written, copied or transported by this application. See `07-ai-provider-layer.md` for the full restriction.

## Prompt injection from model output and from student-uploaded images

The rule is one sentence: model output is data. Everything below follows from it.

**Rendering.** Model output is rendered as text or as KaTeX-typeset math. It is never inserted as HTML, never evaluated as JavaScript, never passed to a template engine that interprets it, and never written to a context where a browser would parse it as markup. KaTeX is rendered with untrusted input settings, meaning macro expansion and any command that can emit raw HTML are disabled. A figure in a generated item is a declarative specification that the client renders from a fixed vocabulary of shapes, axes and labels; it is not SVG the model wrote, because SVG is a markup language and accepting it would reintroduce exactly the injection surface this rule closes.

**Never instructions.** No model output is parsed for directives, used to choose a code path, used to construct a subsequent prompt's instruction block, or fed back into another role's system prompt. The diagnostician's output selects a next item only through a validated BC-QA identifier that must exist in the content snapshot; a string the model invented resolves to nothing and the selection falls back to the ordinary policy. This is the structural version of the rule: model output influences the system only through validated identifiers and schema-constrained fields, never through free text that some component interprets.

**The tutor has no tools.** No tool definitions are sent on a tutor call, so there is no action for injected text to induce. This is also a learning decision (D1) and a small cost saving, but the security value stands alone: a model with no tools has no reach.

**Generated items are sanitised.** Before an item reaches `status = 'verified'` it passes a sanitisation gate: the stem and options are checked against an allowed character and command set for KaTeX, the figure specification is validated against its schema, the options are checked for the distractor properties in `04-item-generation.md`, and the whole item is checked against the duplicate gate. An item that fails sanitisation is rejected, not repaired, because a repaired item has an unclear provenance.

**Image OCR text is untrusted.** The transcriber reads a photograph of a page the student wrote on. That page could contain anything, including text addressed to the model. The transcription is therefore handled with the same rules as any other model output, and with one addition: it is shown back to the student as rendered math for confirmation before any grading call uses it, which means a human sees it before it propagates. Per R10 that path runs only inside a unit check, a part drill, a mock or the six-week checkpoint, so the exposure is a handful of sessions rather than a daily one; micro-session grading is deterministic and sends no image anywhere. That confirmation step exists for accuracy reasons first (the 2026 AIED study found roughly 87 percent of residual grading errors were transcription failures rather than rubric misapplication, https://arxiv.org/abs/2605.19043 [single-source]), and the security benefit is a second reason to keep it rather than the reason it exists.

**Uploaded images themselves.** Images are validated by content sniffing rather than by filename or declared type, re-encoded before storage and before transmission to a provider, and bounded in size before any model call. The provider bounds that apply are Anthropic's 10 MB per image and 32 MB per request (https://platform.claude.com/docs/en/build-with-claude/vision [verified]) and Gemini's 20 MB total request size for inline base64 (https://ai.google.dev/gemini-api/docs/image-understanding [verified]). The image quality gate from `05-assessment-modes.md` runs before any of this, so a blurred or badly cropped page is rejected before it costs a call.

## Rate limits

Three layers, each answering a different failure.

**Per role, per day.** The budget caps in `07-ai-provider-layer.md`. These bound cost rather than abuse, and they degrade support before correctness.

**Per session.** A ceiling on model calls per session and on tutor invocations per item, both `[inferred]` tunables. The per-item tutor ceiling exists for a learning reason as much as a cost one: repeatedly asking for help on one item is the behaviour the guardrail exists to bound.

**Per IP.** Request-rate limits on the API, on the unauthenticated endpoints that take a credential. Corrected 2026-09-23, with the route names brought up to date on 2026-09-27: the set of unauthenticated routes is not whatever a list says, and neither is the set of routes `create_app` builds the only source of them. Every route with no `current_session` or `current_user` dependency (`app/api/deps.py`) is reachable without a cookie: `POST /auth/signup`, `POST /auth/login`, `POST /auth/recovery/reset`, `GET /auth/status`, and `GET /healthz` (which restricts itself to loopback callers inside its own handler rather than through a session dependency). The production application `app/main.py`'s `build_application` serves, not just the routers `create_app` registers, adds three more that carry no session dependency either, because `mount_client` adds them after `create_app` returns: `GET /growth-tokens.css`, `GET /` (the built client's index page), and the `/assets` `StaticFiles` mount, which answers any file under `app/web/dist/assets` and carries no dependant tree at all to check. That is eight, down from the eleven the passkey routes made. `tests/api/test_unauthenticated_routes.py` builds the application with `build_application` rather than `create_app` alone, derives the route and mount sets from that live table on every run, and fails if a new unauthenticated route or mount is added without joining this list, so it cannot drift again.

Narrowed 2026-09-27 on the operator's instruction, replacing the 2026-09-23 rule that all eleven unauthenticated routes carry the tightest limit: the per-IP limit covers only `POST /auth/signup`, `POST /auth/login` and `POST /auth/recovery/reset`, the three routes a stranger can reach that take a credential and spend a scrypt hash. It is `app/auth/limiter.py`, a sliding window of 10 requests per peer address per 60 seconds (`GROWTH_AUTH_RATE_LIMIT`, held on `Settings`), in process memory, with at most 1,024 tracked addresses. It keys on the peer address, `request.client.host`. On the default loopback bind every caller is `127.0.0.1`, so the limit works as one global bucket. Behind the reverse proxy this document requires once the service is exposed, uvicorn's proxy headers (on by default, trusting `127.0.0.1`) replace the peer with the proxy's `X-Forwarded-For` address, so each remote client gets its own window, provided the proxy sets that header. That is the reason for the narrowing: on the shared loopback key, a limit on `GET /`, `/assets` or `/growth-tokens.css` would lock the client out of its own page and static files after ten loads. `GET /auth/status` and `GET /healthz` read no credential and do no hashing. The cost of one bucket on loopback is that any local caller can hold sign-in refused for up to 60 seconds at a time; the Host and Origin checks under "Authentication with a password" stop another web page from doing it through the student's own browser. The limit is checked inside the route after the body has parsed, so a cross-site `text/plain` post that FastAPI refuses with 422 never spends it, and a limited request is answered before any scrypt work or database write. Being in memory, the window resets when the process restarts and is not shared between worker processes; the per-account lockout below is stored on the `users` row and survives both. `POST /auth/reauth`, `POST /auth/password/change` and `POST /auth/logout` need a session and are not per-IP limited; a wrong password on the first two counts toward the lockout instead.

**Backoff.** A client that exceeds a limit receives 429 with `Retry-After`. The client honours it rather than retrying immediately. On the outbound side, the provider layer honours a provider's own `Retry-After` in preference to its configured cooldown, which matters because LiteLLM's default cooldown of 5 seconds (https://docs.litellm.ai/docs/routing [verified]) is shorter than a typical rate-limit retry window. OpenRouter returns 429 with `X-RateLimit-*` headers and `Retry-After`, and 402 on credit exhaustion (https://openrouter.ai/docs/api-reference/limits [verified]); the adapter distinguishes them, because 402 is not retryable and retrying it wastes the cooldown budget.

## Authentication with a password

A username and a password are the only authentication method. No passkey, no email or magic link, no OAuth sign-in, no second factor, no recovery question.

Ruled 2026-09-27 on the operator's instruction, and reversing D10's passkey-only rule for this installation: passkeys are removed entirely and the student signs in with a username and a password. `app/auth/webauthn.py`, the `passkey_credentials` table, every `/auth/passkey/*`, `/auth/recovery/register/*` and `/auth/reauth/begin` and `/finish` route, and the `webauthn` dependency are gone; the hash is `hashlib.scrypt` from the standard library, so no dependency replaces it. What the ruling gives up: a passkey is bound by the authenticator to the relying party id and the origin, cannot be typed into a lookalike page, and cannot be reused from a breach elsewhere, which is why D10 chose it; a password has none of those properties. The server now does the origin binding itself (the request checks below), and the lockout and the per-IP limit bound online guessing, but nothing in this application stops a reused password or a phished one. The paragraphs below replace the passkey registration, login and recovery flows; every other part of D10 stands.

D10's argument, kept as the record of what the ruling reversed: the learning-impact argument for passkeys is thin, so this was a security and convenience decision. A minor's study record, a set of provider keys with real spending power, and a single-user deployment together make a stolen or reused password the highest-probability compromise path, and a passkey removes it. It is also less friction daily, which matters for a product whose whole value depends on the student opening it most days.

**Request checks.** A password is not bound to an origin, so every route that takes a credential, `POST /auth/signup`, `/auth/login`, `/auth/recovery/reset`, `/auth/reauth`, `/auth/password/change` and `/auth/logout`, first runs `app/auth/guard.py` `refuse_untrusted_auth_request`, before any password is read, in this order. The Host must be one the installation serves: `127.0.0.1`, `localhost` and `::1`, plus the one name in `GROWTH_PUBLIC_HOST` for an installation behind a reverse proxy; any other Host gets 400, which refuses a DNS-rebound page. A request whose `Sec-Fetch-Site` is `cross-site`, or whose `Origin` is present and is not the origin the request reached, gets 403, which is the cross-site request check a passkey ceremony made unnecessary. A non-loopback request over plain http gets the 400 the session-cookie rule under "Transport and hosting" gives, now before the password is processed rather than when the cookie is set. Signup, login and recovery then pass the per-IP limit under "Rate limits". Every refusal on these routes is returned rather than raised, because `app/api/deps.py` `get_db` rolls back on an exception and would take a lockout count with it.

**Passwords and usernames.** A password is 12 to 128 characters and at most 512 bytes of UTF-8, with no composition rule. It is stored in `users.password_hash` as `scrypt$n$r$p$salt$hash` in hex, with a 16-byte random salt and a 32-byte key (`app/auth/passwords.py`), at n=2^14, r=8 and p=5 by default, about 16 MiB of memory per hash, set by `GROWTH_SCRYPT_N`, `GROWTH_SCRYPT_R` and `GROWTH_SCRYPT_P`. One hash took 276 ms on the development machine on 2026-09-27 [single-source, one measurement]. The parameters live in each hash, so a hash made under lower parameters is rehashed at the next sign-in, and the comparison is constant time. A username is 3 to 32 ASCII letters, digits or underscores and is stored lowercase, so sign-in ignores case; non-ASCII is refused rather than folded, which rules out lookalike names. There is no unique index on `users.username`: SQLite refuses to drop an indexed column, and the migration tests drop every nullable column, so uniqueness rests on the single-user claim below. Multi-user needs that index. `display_name` stays "student".

**Sign-up.** `POST /auth/signup` with a username and password is open only while `users` is empty. The claim is one statement, `INSERT ... WHERE NOT EXISTS (SELECT 1 FROM users)`, so two sign-ups at once cannot both claim the installation; the loser gets 403, as does every later attempt. Sign-up seeds `skills_state`, opens a session, audits `account_created`, and returns a recovery code once.

**Login.** `POST /auth/login` answers every failure, an unknown username, a wrong password, a migrated user with no password yet and a locked account, with the same 401, "username or password is incorrect". An unknown user, a user with no password and a locked user still run scrypt, against a dummy hash built at startup from the current parameters, so the reply takes about as long as a real check. A success clears the failure count and establishes a session cookie that is HttpOnly, Secure when not on loopback, and SameSite=Lax, and audits `session_established` with the subject `users:<id>`. Session lifetime is long enough that daily study does not mean daily re-authentication.

**Session lifetime.** Ruled 2026-09-29 on the operator's instruction, which was that the student is never signed out in normal use. A session ends 90 days after its last request rather than 30 days after sign-in: `app/api/deps.py` `current_session` calls `app/auth/service.py` `renew_session`, which moves `expires_at` to 90 days from now whenever that gains at least an hour (`SESSION_RENEW_INTERVAL_SECONDS`, so a burst of requests writes the row once), and `app/api/session_renewal.py` then sends the cookie again with the matching max-age. Sessions live in the database, so a restart or a rebuild keeps them. The cookie name carries the port when the origin names one (`growth_session_8000`), because a browser keys cookies on the host and not the port: every server on `localhost` used to share one `growth_session` cookie, and signing in to a second local server replaced the first server's token, which is what signed the student out. The bare name is still read, so a cookie set before the change keeps working and moves to the port name at its next renewal. A session still ends on sign-out, on a password change (the other sessions only), on a recovery reset, at purge, and after 90 idle days, and re-authentication for the consequential actions above stays a prompt that never signs the student out. What the ruling gives up: a stolen cookie stays useful for as long as it keeps being used, where the fixed 30 days capped it; HttpOnly, SameSite=Lax and the loopback-first hosting rule are what bound that risk. The client keeps only non-secret profile fields (username and display name) in localStorage so a reload renders signed in while `/me` revalidates; the token never leaves the HttpOnly cookie, and only a 401 from `/me` shows the sign-in form, never a network error or a 5xx.

**Lockout.** The count lives on the users row, in `failed_login_count` and `locked_until`, so it survives a restart. Four failures are free; the fifth locks the account for 30 seconds, and each failure after a lock has ended doubles the next lock, to at most 15 minutes. There is never a permanent lock. An attempt is counted before the password is checked, in one `UPDATE ... RETURNING` that matches only while the account is unlocked and that sets `locked_until` in the same transaction when the attempt uses up the free four, so parallel guesses cannot check more passwords than the free four and the locking one. An attempt during a lock counts nothing and does not extend the lock; it runs the dummy hash and gets the same generic 401, not a 429 with `Retry-After`, so a lock does not tell a stranger that the username exists. The cost is that a locked-out student is told only that the password is incorrect. `login_failed_lockout` is audited once per lock, when the locking attempt fails, with the count and `locked_until` only. A wrong password at `/auth/reauth` or `/auth/password/change` counts toward the same lockout. Unknown usernames keep no state, so only the per-IP limit covers them. Recovery has no lockout, because the code carries about 100 bits and the per-IP limit bounds its cost; a successful recovery clears the lock.

**Re-authentication.** Re-authentication is forced for the consequential actions: setting or rotating a provider key, changing a budget cap, enabling claudebox, exporting, purging, and changing the password. `POST /auth/reauth` takes the password on a live session, runs the same count and check as login, and on success mints the single-use `reauth_established` proof, valid for 300 seconds, that the consumers read as `reauth_token`. The key-derivation passphrase under "Key handling" stays a separate secret from the login password and is never derived from it: when `PUT /settings/providers/{provider}` is built it takes both the passphrase and this re-authentication.

**Password change.** `POST /auth/password/change` takes the current password, the new one and a `reauth_token`. The token is spent first, then the current password is checked (counting toward the lockout), then the new one is validated and hashed. Every other session of the user is signed out and the current one is kept; the recovery code is unchanged. It audits `password_changed`.

**Recovery.** Two mechanisms, in order of preference. A recovery code, 20 characters from a 32-symbol alphabet, generated at sign-up, shown once and stored as a PBKDF2 hash: `POST /auth/recovery/reset` with the code and a new password sets the password, signs every session out, clears the lockout, spends the code with one conditional `UPDATE` so two resets racing with it cannot both succeed, opens a new session, and shows a replacement code once. A reset sets the username only when none is stored, and then requires one; it never renames an account. And the operator's local fallback: `python -m app.auth.issue_recovery_code --db <path>` prints a fresh code for the installation's one user, replacing any earlier one, and audits `recovery_code_issued` with the actor "operator". That rests on the same acknowledgement D10 made, that filesystem access is already total access: whoever can run it can already read or replace every row. Every recovery path writes to `audit_log`.

**Accounts that had a passkey.** On first start after the change, `app/db/migrate.py` `retire_tables` copies the database to `backups/growth-before-retiring-passkey_credentials-<stamp>.db` beside it, then drops `passkey_credentials` and deletes every `auth_sessions` row in one transaction, so no session made with a passkey outlives it. The user row is kept with a NULL `password_hash`, which is the "must set a password" state; `current_session` refuses any session whose user has none. The migration logs a warning naming the operator command above for any user with neither a password nor a recovery code. Such a user sets a password through the recovery reset. `GET /auth/status` answers `{"user_exists"}` to everyone and adds `needs_password` only to a loopback caller, so the client can route a migrated student to the reset form without advertising the migration window to the network.

**Residuals the ruling accepts.** A known username always commits a write (the attempt count, then its clear or keep) and an unknown one does not, a difference of a few milliseconds of disk sync that could tell a patient caller which username exists; accepted because the installation has one user, the per-IP limit bounds the attempts, and the design does not treat the username as a secret. The backups under `backups/`, the 14 dated copies and the pre-retirement copy, hold the password hash and recovery code hash of their day, so restoring one restores that day's password and recovery code. The per-IP limit is one global bucket on the default loopback bind (see "Rate limits").

**Later multi-user.** The credential model already supports multiple users; what changes is that registration stops being first-come and becomes an invitation issued by the operator, sessions carry a user identifier that every query scopes on, rate limits move from per IP to per user, and `users.username` gains a unique index. Two things do not become available under multi-user: claudebox, which refuses to start with more than one user record, and any shared view of one student's work by another student.

## Data retention and what is stored about a minor learner

Everything stored, why, for how long, and whether the student can delete it.

| Datum | Table or store | Purpose | Retention | Deletable |
| --- | --- | --- | --- | --- |
| Display name | `users` | Address the student in the interface | Until purge | Yes, editable to anything |
| Exam date | `users` | Schedule spacing to the criterion date; default 2027-05-10 per `research/exam/exam-structure.md` [single-source] (R19) | Until purge | Editable, not removable; the scheduler needs it |
| Username, password hash and failed-login state | `users.username`, `users.password_hash`, `users.failed_login_count`, `users.locked_until` (replaced WebAuthn credentials on 2026-09-27) | Authentication and the lockout | Until purge | The password is changeable at any time; the rest only by full purge |
| Recovery code hash | `users.recovery_code_hash` | Recovery | Until spent, replaced or purged | Replaced at each recovery reset or operator issue |
| Provider keys | `provider_configs` | Model calls | Until rotated or removed | Yes |
| Mastery state per skill | `skills_state` | The entire adaptive mechanism | Until purge | Only by full purge; deleting one skill's state corrupts the graph-propagated estimates around it |
| Hypercorrection due date | `skills_state.hypercorrection_due` | Reschedules a high-confidence error to the next day | Until purge, and self-clearing once the retry is served | With the row, so only by full purge |
| Productive-failure opener flag | `skills_state.concept_opener_done` | Stops a concept's opener being served twice | Until purge | With the row, so only by full purge |
| Judgments of learning | `judgments` | Calibration curve and the metacognition metric; never enters credit assignment | Until purge | Yes, individually, with no mastery consequence |
| Pending discriminating probes | `pending_probes` | Holds at most 3 recommended probes per user and drains into the next selection | Expires 7 days after enqueue, or at purge, whichever is first | Yes, individually; a dropped probe only means the probe is not served |
| Attempts with responses | `attempts` | Credit assignment, retention measurement, calibration | Until purge | Yes, per attempt, with the mastery consequence stated |
| Confidence ratings | `attempts` | Hypercorrection routing, calibration metrics | Until purge | With the attempt |
| Timing per item | `attempts` | Pacing metrics; FSRS grade mapping | Until purge | With the attempt |
| FRQ images | Object store | Transcription and grading | Until purge, or earlier | Yes, individually, at any time |
| Transcriptions | `attempts` | Grading input, and the student's own record of their work | Until purge | With the attempt |
| Per-point gradings | `gradings` | Feedback, dispute trail, grader calibration | Until purge | With the attempt |
| Diagnoses | `diagnoses` | Feedback, misconception tracking | Until purge | With the attempt |
| Student error notes | `attempts` | The only free text the student writes; self-explanation | Until purge | Yes, individually |
| Session records | `sessions` | Interleaving constraints, session history | Until purge | By full purge |
| Generated items | `items` | The shared bank; not personal data | Indefinite | Not personal data, so not subject to the student's deletion |
| Token and cost usage | `budgets` | Budget enforcement | Until purge | By full purge |
| Audit log | `audit_log` | Explaining state changes and key actions | Until purge | By full purge, and the purge itself is the last entry written |
| Calculator drill records: task draw, typed result, typed setup, correctness, elapsed time, which Desmos variant was open (added 2026-09-29) | `calculator_drills` | Fluency measurement per calculator capability; never enters credit assignment | Until purge | Yes, individually, with no mastery consequence |

What is deliberately not stored: no free-text chat history beyond the student's own error notes, because the tutor is guardrailed and turn-based rather than a conversation to be archived; no location; no device fingerprint; no contact details; no third-party analytics identifiers of any kind. There are no third-party analytics at all, which is a D10 rule and also removes an entire category of data-sharing question.

**FRQ images are deletable individually and immediately.** `DELETE /attempts/{aid}/images/{iid}` removes the object and writes an `audit_log` entry. Grading already completed is retained, because the per-point rationale stands on its own; the image was the input, not the record. This matters because a photograph of a page is the most personal artefact the product holds and the student should never have to accept keeping it.

**Default purge 30 days after the exam date, with an export first.** The product's purpose ends on exam day. Thirty days after it, the retained data has no use to the student and is pure liability. The sequence is: a notice ahead of the purge date, then `POST /export` producing a complete archive of everything in the table above in an open format, then `POST /purge` behind a typed confirmation and re-authentication. The purge is destructive and irreversible, and the interface says so in those words. The date is stored per user in `users.purge_after` and is editable, because a student retaking in a later year has a legitimate reason to extend it, and an extension is an explicit act rather than a default. Ruled 2026-09-23: the typed confirmation is the literal text "delete my data" (`app/api/routes/purge.py` `PURGE_CONFIRMATION`, `app/web/src/App.tsx` `PURGE_CONFIRMATION_PHRASE`), since this document names none.

**Parental access, stated as open questions.** These are genuinely unsettled and this document does not answer them, because answering them would be giving law advice this project is not positioned to give. Whether a parent has a right to see a minor's study record here, and whether the product should provide a distinct parental view rather than sharing the student's credential, is open. Whether the student should be told when a parent views their record, and what that does to the student's willingness to record a confident wrong answer honestly, is open, and it has a real learning consequence: calibration data is only useful if the student answers the confidence prompt truthfully. Which jurisdiction's minor-data rules apply to a self-hosted single-student deployment is open. Whether an operator who is also the parent changes any of this is open. All four are carried in `12-open-questions.md`.

One design position that is not open, because it follows from the mechanics rather than from law: if a parental view is built, it shows mastery and effort rather than per-item transcripts. The per-item record exists so the engine can adapt and so the student can review their own errors, and turning it into a surveillance feed would change what the student is willing to enter, which would degrade the estimate the whole product runs on.

## Transport and hosting

**Localhost first.** The default deployment binds to loopback. Nothing is reachable from the network, which makes most of this section inert by default and is the reason the default is what it is.

**TLS when exposed.** Any non-loopback binding requires TLS, and the application refuses to set a Secure-less session cookie on a non-loopback origin. HSTS is set when exposed. Self-signed certificates are acceptable for a private deployment; no certificate at all is not.

**CORS.** No cross-origin access. The API and the client are same-origin, served by the same process, so the CORS policy is an empty allowlist rather than a permissive one. There is no reason for a third-party origin to call this API and no configuration option to permit one.

**CSP.** A strict policy: `default-src 'self'`, no `unsafe-inline` and no `unsafe-eval` for scripts, styles restricted to self with per-build hashes, `img-src 'self' blob:` for camera capture, `connect-src 'self'` so the client never talks to a provider directly, `frame-ancestors 'none'`, `object-src 'none'`, `base-uri 'none'`. One exception, corrected 2026-09-23: `style-src-attr 'unsafe-inline'`. MathLive, which 06 names for input, lays out every rendered formula through inline `style` attributes computed at run time, so no per-build hash can cover them, and under `style-src 'self'` alone a fraction renders collapsed with one blocked-style error per box [verified in a browser against the installed MathLive on 2026-09-23]. The exception covers style attributes only; `<style>` elements, stylesheets and every script directive stay as above. A second exception, added 2026-09-27 on the operator's instruction: `frame-src https://www.desmos.com`, so a calculator question can open the Desmos graphing calculator inside the page. The frame is a different origin and cannot read the app, and no other origin may be framed. The `connect-src` restriction is structural: every provider call goes through the server, which is what makes the budget guard and the audit trail unbypassable, and the CSP is what enforces it at the browser.

**The client never holds a provider key.** It has no need to, because it never calls a provider. This is worth stating because the alternative architecture, where a client calls a provider directly with a key, is common and would make every control in `07-ai-provider-layer.md` advisory.

## Provider data policies and the choice they drive

| Provider | Policy | Source |
| --- | --- | --- |
| OpenRouter | Prompts and completions are not logged by default. Opting into logging gives a 1 percent discount. Providers that log, or that lack a confirmed privacy policy, are not routed to unless the training toggle is on | https://openrouter.ai/docs/faq [verified] |
| OpenAI | Responses API stores by default | https://developers.openai.com/api/docs/guides/migrate-to-responses [verified] |
| Anthropic | Zero data retention is available on PDF and other surfaces | https://platform.claude.com/docs/en/build-with-claude/pdf-support and the track 4 comparison table [verified] |
| Gemini | Unknown from the pages loaded in track 4 | https://ai.google.dev/gemini-api/docs [verified as absent from the loaded pages] |
| Ollama | Fully local; nothing leaves the machine | https://docs.ollama.com/api/openai-compatibility [verified] |

What that drives, in the project's priority order.

Learning impact is neutral across these, so the decision falls to privacy and then cost. OpenAI is off by default, and the reason is the storage default on Responses: a minor's handwritten work and a record of their misconceptions should not be stored by a third party as a side effect of a default. Enabling OpenAI surfaces that statement in the settings screen rather than burying it.

Anthropic stays the default partly because zero data retention is available, which gives the operator a lever the other defaults do not. Whether ZDR is enabled on this deployment is an operator setting, and it is recorded in `audit_log` when changed.

Gemini's policy being unknown from the loaded pages is a genuine gap and it is why Gemini sits as a secondary rather than a default despite being the cheapest capable option at $0.75 in and $3.75 out per 1M through 31 December 2026 (https://ai.google.dev/gemini-api/docs/pricing [verified]). Cost lost to privacy uncertainty is the correct trade here. The gap is carried in `12-open-questions.md` as something to resolve by reading the policy rather than by guessing.

OpenRouter's no-logging default is good, and the adapter sets `data_collection: "deny"` explicitly rather than relying on the default (https://openrouter.ai/docs/features/provider-routing [verified]). The 1 percent discount for opting into logging is declined, which is the cheapest privacy decision in the whole document.

Ollama is the only option where nothing leaves the machine, which is a genuine privacy advantage and is why the offline fallback is worth having beyond its availability role. It does not become a grading peer for that reason, because the quality argument in `07-ai-provider-layer.md` is separate and stands.

The FRQ image path deserves a specific note, because it is the most sensitive payload the system sends anywhere. A photograph of a minor's handwritten page goes to a provider for transcription. The controls are: the image is never sent to a provider whose logging posture is unknown or permissive, it is re-encoded and bounded before sending, and it is deletable at any time afterwards. If the operator wants that payload never to leave the machine, the typed MathLive path from D6 exists and is the mode that satisfies it, at a cost in criterion fidelity that the product states plainly rather than hiding.

## Audit log

`audit_log` is not the application log. It is a durable, queryable record of consequential actions, and it survives log rotation.

Recorded: a provider key set, rotated or removed; claudebox enabled or disabled, with the acknowledgement text version; a budget cap changed; a content snapshot reloaded, with the digest before and after; a `skills_state` row rewritten by a tombstone merge, naming both library IDs; an FRQ image deleted; an export produced; a purge run; a review queue item resolved; a grading re-run; an account created, a session established, a lockout engaged, a password changed, a password reset through a recovery code and a recovery code issued by the operator (these six replaced the passkey actions on 2026-09-27); a role stopped by its budget cap and a call refused by it, which are the same class of event as a cap changed; a fringe archetype excluded from selection for want of a published item. An ordinary provider call is not recorded here: its accounting lives in `budgets`, and a row per call would flood a record this section describes as durable and queryable. The vocabulary is enumerated in code at `app/audit/vocabulary.py`, and a write whose action is outside it is refused.

Not recorded: any key or any part of one; the passphrase; a password or any part of one, and a recovery code; a raw provider response body; the student's response text, which lives in `attempts` and does not need duplicating into a second store with a different retention.

Each entry carries the timestamp, the actor (user identifier, worker, or system), the action from a controlled vocabulary, the subject as a table and row identifier, and a JSON detail field bound by the exclusions above. The request identifier from `06-architecture.md` propagates into the entry, so a consequential action traces back to the request that caused it.

The log is readable by the operator through the same authenticated surface as everything else. It is deleted only by the full purge, and the purge writes itself as the final entry before the store is emptied.

## Traceability

| Security element | Mechanic in `01-learning-model.md` | Rule in `02-adaptive-engine.md` | Plan document |
| --- | --- | --- | --- |
| Password authentication with a lockout (passkey-only until 2026-09-27) | Daily engagement, since friction at login costs sessions | none | `06-architecture.md` API surface |
| Tutor with no tools | No chat box beside an unsolved problem; guardrailed support at parity with no tutor rather than minus 17 percent | none | `07-ai-provider-layer.md` |
| Model output rendered, never executed or interpreted | All feedback mechanics, which depend on rendering model text to a student | Item selection algorithm, which is influenced only by validated BC-QA identifiers | `07-ai-provider-layer.md` |
| Transcription confirmed before grading | Criterion-shaped rehearsal on the real artefact | Update rules, whose credit assignment reads a graded point vector | `05-assessment-modes.md` |
| Generated items sanitised before publication | All practice mechanics | An unverified or unsanitised item is never served | `04-item-generation.md` |
| Per-role and per-session rate limits | Bounds repeated help-seeking on one item | none | `07-ai-provider-layer.md` budget caps |
| Encrypted keys, never in a log or URL | none | none | `07-ai-provider-layer.md` |
| claudebox single-operator guard, tutor not routable | Tutor latency would break the session loop | none | `07-ai-provider-layer.md` |
| Individually deletable FRQ images | Willingness to photograph real work, which the capture mode depends on | none | `05-assessment-modes.md` |
| Purge 30 days after the exam date, export first | The product's horizon is the exam date, which is also the spacing horizon | Decay, whose desired-retention schedule ends at exam day | `06-architecture.md` data model |
| No third-party analytics | none | none | `10-quality-and-evaluation.md`, whose metrics are all derived from local tables |
| Audit log | none directly | Every engine-external state rewrite is explainable | `06-architecture.md` observability |
| CSP `connect-src 'self'` | none | none | `06-architecture.md`, since it is what makes the budget guard unbypassable |

## Calculator fluency, 2026-09-29 [inferred]

Data. One table, `calculator_drills`, owned through its `user_id` column, so `owner_clause` puts it under export and purge with no code change; its retention row is in the inventory above. Nothing from inside the Desmos frame is stored, because the app never receives the graph state.

CSP. No directive changes. The drills and the calculator items open https://www.desmos.com/testing/collegeboard/graphing, which is the same origin as the calculator the 2026-09-27 exception already names, so `frame-src https://www.desmos.com` covers it and tests/api/test_security_headers.py is unchanged. The embedded Desmos API was considered and not adopted: it would need `script-src https://www.desmos.com` (every script is self-hosted here) and an API key from an account only the operator can create; the API terms' free Trial Tier permits personal, non-commercial use, so the licence alone would not have blocked it [single-source, BC-SRC-desmos-api-terms p.1]. The decision and what would reverse it are in [../calculator/research/synthesis.md](../calculator/research/synthesis.md).

Terms. The desmos.com Terms of Service state that the Desmos Tools may not be framed or mirrored without Desmos's prior consent [single-source, BC-SRC-desmos-terms p.1]. The frame exists on the operator's instruction; the code carries a one-constant switch to opening the same URL in a new window, and the ruling is recorded in 12.
