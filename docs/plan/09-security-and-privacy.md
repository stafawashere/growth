---
title: Security and privacy
research_date: 2026-09-19
status: draft
purpose: State the threat model, the key and data handling rules, the injection and rate-limit defences, the passkey authentication flow, and the retention and deletion policy for a single minor learner.
---

# Security and privacy

This document covers the application described in `06-architecture.md` and `07-ai-provider-layer.md`. It is a planning document and contains no application code.

The posture is D10: passkeys as the only authentication, local-first single user, provider keys encrypted at rest, model output treated as untrusted data, the tutor holding no tools, generated items sanitised before rendering, rate limits per role and per IP, and a default purge 30 days after the exam date with an export first.

Two framing statements before the detail. First, the learner is a minor, which raises the cost of every data decision and lowers the tolerance for storing anything the product does not need. Second, this is not legal advice; where a question is legal rather than technical it is written below as an open question and carried into `12-open-questions.md` rather than answered.

## Threat model

Assets, ranked by what their loss costs.

| Asset | Where it lives | Loss consequence |
| --- | --- | --- |
| Provider API keys | `provider_configs`, encrypted | Financial loss to the operator, unbounded until noticed; abuse of the operator's account |
| The student's work and mastery history | `attempts`, `gradings`, `diagnoses`, `skills_state` | A detailed record of a named minor's academic weaknesses over a year |
| FRQ images | Object storage referenced from `attempts` | Handwriting, and whatever else is on the photographed page |
| Session credentials | Browser cookie, WebAuthn credential | Full access to everything above |
| Content snapshot integrity | In-memory graph from `data/` | Corrupted mastery attribution, which is silent |
| Grading integrity | `gradings` | A student trusts a wrong score, or distrusts a right one |
| Operator's Claude subscription credential | Outside this application entirely, see `07-ai-provider-layer.md` | Account suspension; terms exposure |

Actors.

**The student.** Not an adversary in the usual sense, but the party whose mistakes matter most: a shared device, a screenshot, a misunderstood export. The student is also the party most able to damage their own learning by finding a way to see answers early, which is a product-integrity concern rather than a security one.

**The operator.** The person running the deployment and holding the keys. Trusted with everything, which is why every consequential action they take is recorded in `audit_log` rather than being invisible.

**A remote attacker.** Anyone who can reach the listening port. In the default deployment that is nobody, because the service binds to loopback. The moment it is exposed, this actor becomes the reason for TLS, CORS, CSP, rate limits and passkeys.

**A malicious or compromised provider response.** The actor most specific to this product. Model output is data that arrives from outside the trust boundary and is rendered to a student, and a generated item stem is text the application itself asked a model to write and then displays. This actor also covers the case of injected instructions arriving inside a student-uploaded image, which the transcriber reads and passes on.

STRIDE, with the control that answers each row.

| Threat | Instance in this system | Control |
| --- | --- | --- |
| Spoofing | Someone authenticating as the student | WebAuthn passkeys, origin-bound and phishing-resistant; no password to steal or reuse |
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

**Memory handling.** The derived key exists only while the application is unlocked, and unlocking is an explicit action rather than an implicit startup step. A plaintext key is materialised into a request-scoped buffer, passed to the adapter for one call, and not retained on any adapter object between calls. This costs a decryption per call and buys the property that a heap dump taken between calls contains no key.

**No keys in logs or URLs.** Absolute. No log line, error message, stack trace, exception payload, URL path, query string or `audit_log` detail field contains a key or any part of one, including a masked prefix, because a masked prefix is still a disclosure. `GET /settings/providers` returns configuration without key material. The provider layer's structured logs record provider and model, never credentials, and never the raw provider response body.

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

**Per IP.** Request-rate limits on the API, strictest on the unauthenticated endpoints. `POST /auth/passkey/login/begin` and `/finish` carry the tightest limit, because they are the only endpoints an unauthenticated remote party can reach. In the default loopback deployment this layer is inert; it exists so that exposing the service does not require adding it later under pressure.

**Backoff.** A client that exceeds a limit receives 429 with `Retry-After`. The client honours it rather than retrying immediately. On the outbound side, the provider layer honours a provider's own `Retry-After` in preference to its configured cooldown, which matters because LiteLLM's default cooldown of 5 seconds (https://docs.litellm.ai/docs/routing [verified]) is shorter than a typical rate-limit retry window. OpenRouter returns 429 with `X-RateLimit-*` headers and `Retry-After`, and 402 on credit exhaustion (https://openrouter.ai/docs/api-reference/limits [verified]); the adapter distinguishes them, because 402 is not retryable and retrying it wastes the cooldown budget.

## Authentication with passkeys

WebAuthn passkeys are the only authentication method. No password, no email link, no recovery question.

The learning-impact argument for this is thin, so the honest ordering is different here: this is a security and convenience decision. A minor's study record, a set of provider keys with real spending power, and a single-user deployment together make a stolen or reused password the highest-probability compromise path, and a passkey removes it. It is also less friction daily, which matters for a product whose whole value depends on the student opening it most days.

**Registration.** `POST /auth/passkey/register/begin` returns a challenge with the relying party identifier bound to the deployment's origin. The authenticator creates a credential; `POST /auth/passkey/register/finish` verifies the attestation and stores the credential identifier, public key and sign count. In the single-user deployment, registration is available only while `users` is empty, so the first registration claims the installation and every later one is refused. The student is encouraged to register at least two authenticators, for example a platform authenticator on the study device and a second on a phone.

**Login.** `POST /auth/passkey/login/begin` returns an assertion challenge; `/finish` verifies the signature against the stored public key, checks the sign count for regression, and establishes a session cookie that is HttpOnly, Secure when not on loopback, and SameSite=Lax. Session lifetime is long enough that daily study does not mean daily re-authentication, with re-authentication forced for the consequential actions: setting or rotating a provider key, changing a budget cap, enabling claudebox, exporting, and purging.

**Recovery.** This is where passkey-only designs usually fail, so it is specified rather than assumed. Three mechanisms, in order of preference. A second registered authenticator is the primary answer, which is why registration prompts for one. A recovery code, generated once at registration, shown once, and stored as a hash, which authenticates a new registration and is then consumed. And the operator's local fallback: on a deployment the operator controls, an operator with filesystem access can clear the credential table and re-register, which is not a backdoor so much as an acknowledgement that filesystem access is already total access. Every recovery path writes to `audit_log`.

**Later multi-user.** The credential model already supports multiple users; what changes is that registration stops being first-come and becomes an invitation issued by the operator, sessions carry a user identifier that every query scopes on, and rate limits move from per IP to per user. Nothing in the passkey flow itself changes. Two things do not become available under multi-user: claudebox, which refuses to start with more than one user record, and any shared view of one student's work by another student.

## Data retention and what is stored about a minor learner

Everything stored, why, for how long, and whether the student can delete it.

| Datum | Table or store | Purpose | Retention | Deletable |
| --- | --- | --- | --- | --- |
| Display name | `users` | Address the student in the interface | Until purge | Yes, editable to anything |
| Exam date | `users` | Schedule spacing to the criterion date; default 2027-05-10 per `research/exam/exam-structure.md` [single-source] (R19) | Until purge | Editable, not removable; the scheduler needs it |
| WebAuthn credentials | auth store | Authentication | Until purge or revoked | Yes, per credential |
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

What is deliberately not stored: no free-text chat history beyond the student's own error notes, because the tutor is guardrailed and turn-based rather than a conversation to be archived; no location; no device fingerprint; no contact details; no third-party analytics identifiers of any kind. There are no third-party analytics at all, which is a D10 rule and also removes an entire category of data-sharing question.

**FRQ images are deletable individually and immediately.** `DELETE /attempts/{aid}/images/{iid}` removes the object and writes an `audit_log` entry. Grading already completed is retained, because the per-point rationale stands on its own; the image was the input, not the record. This matters because a photograph of a page is the most personal artefact the product holds and the student should never have to accept keeping it.

**Default purge 30 days after the exam date, with an export first.** The product's purpose ends on exam day. Thirty days after it, the retained data has no use to the student and is pure liability. The sequence is: a notice ahead of the purge date, then `POST /export` producing a complete archive of everything in the table above in an open format, then `POST /purge` behind a typed confirmation and re-authentication. The purge is destructive and irreversible, and the interface says so in those words. The date is stored per user in `users.purge_after` and is editable, because a student retaking in a later year has a legitimate reason to extend it, and an extension is an explicit act rather than a default.

**Parental access, stated as open questions.** These are genuinely unsettled and this document does not answer them, because answering them would be giving law advice this project is not positioned to give. Whether a parent has a right to see a minor's study record here, and whether the product should provide a distinct parental view rather than sharing the student's credential, is open. Whether the student should be told when a parent views their record, and what that does to the student's willingness to record a confident wrong answer honestly, is open, and it has a real learning consequence: calibration data is only useful if the student answers the confidence prompt truthfully. Which jurisdiction's minor-data rules apply to a self-hosted single-student deployment is open. Whether an operator who is also the parent changes any of this is open. All four are carried in `12-open-questions.md`.

One design position that is not open, because it follows from the mechanics rather than from law: if a parental view is built, it shows mastery and effort rather than per-item transcripts. The per-item record exists so the engine can adapt and so the student can review their own errors, and turning it into a surveillance feed would change what the student is willing to enter, which would degrade the estimate the whole product runs on.

## Transport and hosting

**Localhost first.** The default deployment binds to loopback. Nothing is reachable from the network, which makes most of this section inert by default and is the reason the default is what it is.

**TLS when exposed.** Any non-loopback binding requires TLS, and the application refuses to set a Secure-less session cookie on a non-loopback origin. HSTS is set when exposed. Self-signed certificates are acceptable for a private deployment; no certificate at all is not.

**CORS.** No cross-origin access. The API and the client are same-origin, served by the same process, so the CORS policy is an empty allowlist rather than a permissive one. There is no reason for a third-party origin to call this API and no configuration option to permit one.

**CSP.** A strict policy: `default-src 'self'`, no `unsafe-inline` and no `unsafe-eval` for scripts, styles restricted to self with per-build hashes, `img-src 'self' blob:` for camera capture, `connect-src 'self'` so the client never talks to a provider directly, `frame-ancestors 'none'`, `object-src 'none'`, `base-uri 'none'`. The `connect-src` restriction is structural: every provider call goes through the server, which is what makes the budget guard and the audit trail unbypassable, and the CSP is what enforces it at the browser.

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

Recorded: a provider key set, rotated or removed; claudebox enabled or disabled, with the acknowledgement text version; a budget cap changed; a content snapshot reloaded, with the digest before and after; a `skills_state` row rewritten by a tombstone merge, naming both library IDs; an FRQ image deleted; an export produced; a purge run; a review queue item resolved; a grading re-run; a passkey registered, removed or used for recovery; a session established from a new authenticator.

Not recorded: any key or any part of one; the passphrase; a raw provider response body; the student's response text, which lives in `attempts` and does not need duplicating into a second store with a different retention.

Each entry carries the timestamp, the actor (user identifier, worker, or system), the action from a controlled vocabulary, the subject as a table and row identifier, and a JSON detail field bound by the exclusions above. The request identifier from `06-architecture.md` propagates into the entry, so a consequential action traces back to the request that caused it.

The log is readable by the operator through the same authenticated surface as everything else. It is deleted only by the full purge, and the purge writes itself as the final entry before the store is emptied.

## Traceability

| Security element | Mechanic in `01-learning-model.md` | Rule in `02-adaptive-engine.md` | Plan document |
| --- | --- | --- | --- |
| Passkey-only authentication | Daily engagement, since friction at login costs sessions | none | `06-architecture.md` API surface |
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
