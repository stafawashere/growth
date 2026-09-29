---
title: Memory of one learner for the live tutor
research_date: 2026-09-29
status: draft
purpose: Survey how long-lived assistants keep and grow memory of one person, state what Growth already holds about the learner, and recommend the memory layer the live tutor should add.
---

# Memory of one learner for the live tutor

This file covers one strand of the live tutor research. It surveys the published memory designs of MemGPT and Letta, the generative agents architecture, Anthropic's memory and context features, Claude Code's auto memory, ChatGPT memory, Mem0, Zep and Graphiti, and the open learner model literature. It then reads what Growth already stores about the student and recommends what a memory layer should add, and what it must never hold.

## Constraints this file takes as given [inferred]

These hold whatever the evidence below says, and every recommendation is written inside them.

- The tutor role is never routed to claudebox, and the single-user rule of the subscription backend holds.
- No student-written text reaches a system prompt. Every field substitutes below the `<!-- prompt-variables -->` marker (`app/providers/base.py`, `render_template`), and plan 13 Safety adds that untrusted fields are JSON-encoded into the user message, that an untrusted-content policy block sits in the cached prefix, and that untrusted output is screened.
- No tool definitions are sent to a model unless research shows a need that app-composed context cannot meet. The default is app-composed context plus structured output.
- Plan 03 guardrail. During practice the agent never states the answer, never receives the unsubmitted answer or the key, never evaluates in-progress work on an unsupported or exam-shaped item, and asks before it tells. Nothing the agent says or the student types writes mastery evidence.
- No study advice, no schedules, no quotas, no praise copy, and no talk about what the exam will hold, in any template or interface copy.
- Plan 09 privacy for a minor learner. Every new datum gets a retention-table row, purge and export cover it, and the student can view and delete it.
- Every agent call goes through `app/providers/guard.py` and pacing caps, under its own role and caps. Consolidation runs off the interactive path, through the jobs table and its drain or through batch.

## MemGPT and Letta [single-source]

MemGPT frames long-term memory as an operating-system problem. The abstract describes "virtual context management", which moves data "between fast and slow memory" to give the appearance of a larger context (https://arxiv.org/abs/2310.08560, accessed 2026-09-29). The full paper splits the prompt into system instructions, a working context the agent edits, and a first-in first-out message queue. Two stores sit outside the prompt. Recall storage holds the full message history, and archival storage holds arbitrary long-term text. The agent moves data with its own function calls (`core_memory_append`, `core_memory_replace`, `archival_memory_search`, `conversation_search`). A memory-pressure warning fires at about 70 percent of the context, and at the limit the queue is flushed with a recursive summary (https://arxiv.org/pdf/2310.08560, accessed 2026-09-29). These details come from a summarised read of the PDF, so the 70 percent figure should be checked against the paper before anyone relies on it.

Letta is the product built on MemGPT. Its documentation defines core memory as labelled blocks with four fields (label, description, value, and a character limit) plus an optional `read_only` flag. Blocks are prepended to the prompt so they are always visible without retrieval, and the agent edits them with built-in tools (https://docs.letta.com/guides/agents/memory-blocks, accessed 2026-09-29). The memory overview lists the tool names `memory_replace`, `memory_insert`, `memory_rethink`, `archival_memory_insert`, `archival_memory_search` and `conversation_search`, and says the important "core" memories are injected into the context window while the rest is retrieved on demand (https://docs.letta.com/guides/agents/memory, accessed 2026-09-29).

Letta's sleep-time agents, now called dreaming, move consolidation off the interactive path. Background subagents "review recent conversations, consolidate useful lessons, and update memory", and they run either after a set number of completed agent steps or when the context is compacted. An optional second pass reviews proposed updates before they apply, at extra token cost (https://docs.letta.com/guides/agents/sleep-time-agents, accessed 2026-09-29). The page does not say which model runs them.

The lesson for Growth is the split between a small always-in-prompt block and a larger store read on demand, and the choice to consolidate in the background. The part Growth cannot copy is the agent editing its own memory through tools, which conflicts with the no-tools default.

## Generative agents and reflection [single-source]

Park et al keep a memory stream, a complete natural-language record of an agent's observations (https://arxiv.org/abs/2304.03442, accessed 2026-09-29). Retrieval scores each memory on three terms. Recency decays exponentially with a factor of 0.995 per game hour since last access. Importance is a 1 to 10 score the model assigns at write time, from mundane to poignant. Relevance is the cosine similarity between the memory's embedding and the query's. The three are min-max normalised and summed with equal weights of 1 (https://arxiv.org/html/2304.03442, accessed 2026-09-29).

Reflection runs when the summed importance of recent events passes 150, which in the simulation happened two or three times a game day. The agent asks for the three most salient high-level questions its recent records can answer, retrieves evidence for each, and writes insights that cite the memories they rest on. Reflections can cite earlier reflections, which gives a tree with observations at the leaves (https://arxiv.org/html/2304.03442, accessed 2026-09-29). The paper's ablation found that observation, planning and reflection each contribute to believability.

Two points carry over. Reflection is triggered by accumulated importance rather than by a clock, and every higher-level entry cites its evidence. The second is directly useful for a student-facing memory view, because an entry that cites the conversation it came from is an entry the student can judge.

## Anthropic's memory and context features [single-source]

The memory tool has the type `memory_20250818` and the name `memory`, and it is client-side. Claude requests file operations under `/memories` and the application executes them against storage it controls, with the commands `view`, `create`, `str_replace`, `insert`, `delete` and `rename` (https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool, accessed 2026-09-29). When the tool is present the API adds a system instruction telling Claude to view its memory directory before anything else. The security section makes path traversal the application's problem, recommends capping file sizes, and suggests periodically deleting memory files that have not been accessed in a long time. It also notes that Claude usually refuses to write sensitive information but that stronger guarantees need the application's own validation. The page says the tool needs no beta header.

Context editing clears old content by rule. `clear_tool_uses_20250919` clears the oldest tool results once input passes a trigger (default 100,000 input tokens), keeps the last 3 tool uses by default, and takes `clear_at_least` so a clearing is large enough to justify the cache invalidation it causes. `clear_thinking_20251015` does the same for thinking blocks. Both need the `context-management-2025-06-27` beta header (https://platform.claude.com/docs/en/build-with-claude/context-editing, accessed 2026-09-29). Compaction replaces older turns with a server-written summary, either on demand under the `compact-2026-09-04` beta header or at a token threshold, and the memory tool page recommends pairing compaction with memory so the facts that must survive summarisation are held outside the conversation (https://platform.claude.com/docs/en/build-with-claude/compaction, accessed 2026-09-29).

Managed Agents memory stores are workspace-scoped collections of text documents, mounted into the session sandbox and edited with the ordinary file tools, under the `agent-memory-2026-07-22` beta header. Each memory is capped at 100 kB and a store at 10,000 memories. Every change writes an immutable memory version, versions are kept for 30 days, and a version can be redacted to scrub content while keeping the audit trail, which the page names as the route for user deletion requests (https://platform.claude.com/docs/en/managed-agents/memory, accessed 2026-09-29). The page warns that a `read_write` store exposed to untrusted input lets a prompt injection write content that later sessions read as trusted memory. Dreams are the consolidation job. A dream reads a store and up to 100 session transcripts and writes a new store with duplicates merged and contradicted entries replaced by the latest value, and it never modifies the input store, so the output can be reviewed and discarded (https://platform.claude.com/docs/en/managed-agents/dreams, accessed 2026-09-29). Dreaming is a research preview and runs on `claude-opus-5`, `claude-fable-5`, `claude-opus-4-8`, `claude-opus-4-7`, `claude-sonnet-5` or `claude-sonnet-4-6`.

For Growth the relevant ideas are the write-then-review consolidation that never edits in place, the version trail with redaction, and the explicit warning about injection into writable memory. The mechanisms themselves (a tool, a mounted sandbox) are out of scope under the no-tools default and the subscription backend.

## Claude Code auto memory [single-source]

Claude Code keeps two layers (https://code.claude.com/docs/en/memory, accessed 2026-09-29). CLAUDE.md files hold instructions the user writes. Auto memory holds notes Claude writes itself, in `~/.claude/projects/<project>/memory/`, with a `MEMORY.md` index of one line per memory and one topic file per memory. Each memory file carries a `type` in its frontmatter (`user`, `feedback`, `project` or `reference`), and Claude Code stamps a `modified` timestamp on each write so a reader can see how current a fact is. Only the first 200 lines or 25 KB of `MEMORY.md` load at session start, whichever comes first. Topic files load on demand when Claude decides it needs them. When the index nears the limit, Claude Code tells Claude to keep one line per entry, move detail into topic files and merge or drop stale entries. Everything is plain Markdown the user can open, edit or delete through `/memory`, and the page states that Claude skips anything it can derive from the code or that CLAUDE.md already says.

The pattern that transfers is the index of short pointers with a hard size bound, typed entries, a write timestamp on every entry, and a rule against storing what another source already holds. That last rule maps directly onto Growth, where the engine tables are the source of truth for mastery and memory must not duplicate them.

## ChatGPT memory [single-source]

The OpenAI help pages returned HTTP 403 to direct fetches (https://help.openai.com/en/articles/8590148-memory-faq and https://openai.com/index/memory-and-new-controls-for-chatgpt/, both attempted 2026-09-29), so this section rests on the help-centre text as a search engine returned it, and should be re-read when the pages are reachable. That text describes two mechanisms. Saved memories are details the user asked ChatGPT to remember or that it saved as useful, stored separately from chat history. Reference chat history lets ChatGPT draw on past conversations, and what it derives from them can change as ChatGPT updates what it finds useful. The user can delete individual saved memories, clear all of them, or turn memory off. Deleting a saved memory stops its future use but does not remove mentions from past chats, and deleting a chat does not delete a saved memory created from it. Turning reference chat history off schedules what was remembered for deletion within 30 days, and OpenAI may keep logs of deleted saved memories for up to 30 days. Temporary Chat stays out of history (https://help.openai.com/en/articles/8914046-temporary-chat-faq/, search result, accessed 2026-09-29).

The design principle that transfers is that memory is a separate, listable, per-entry deletable object, distinct from the conversations it came from. The ChatGPT detail that deleting a chat leaves its derived memory in place is the behaviour Growth should avoid, because a student deleting something should see it gone from every place it shaped.

## Mem0 [single-source]

The Mem0 paper splits memory into an extraction phase and an update phase (https://arxiv.org/html/2504.19413, accessed 2026-09-29). Extraction takes the newest message pair, a stored conversation summary and the previous m messages (m = 10 in the experiments) and asks a model for a set of salient candidate facts. Update retrieves the s most similar stored memories by embedding (s = 10) and has the model pick one operation per candidate. ADD creates a memory when nothing equivalent exists, UPDATE augments an existing one, DELETE removes a memory the new fact contradicts, and NOOP leaves the store alone. The graph variant Mem0g detects conflicting relationships and marks them invalid rather than removing them, to keep temporal reasoning possible. On LOCOMO the abstract reports a 26 percent relative gain in the LLM-as-a-judge metric over OpenAI's memory, about 2 percent more for the graph variant, 91 percent lower p95 latency and over 90 percent lower token cost than full context (https://arxiv.org/abs/2504.19413, accessed 2026-09-29). The paper reports about 7,000 memory tokens per conversation for Mem0 and about 14,000 for Mem0g against about 26,000 for full context.

The current documentation describes a different default. The `add` page says new memories are added "without overwriting or deleting existing memories", and that `infer=True` runs the extraction while `infer=False` stores raw messages (https://docs.mem0.ai/core-concepts/memory-operations/add, accessed 2026-09-29). The memory-types page organises memory by scope (`user_id`, agent, `run_id` for a session) and by function (preferences, decisions, plans, feedback) rather than by the episodic, semantic and procedural split (https://docs.mem0.ai/core-concepts/memory-types, accessed 2026-09-29). Whether the product still runs the paper's DELETE path is unknown from these pages.

The ADD, UPDATE, DELETE, NOOP vocabulary is a good shape for a structured-output consolidator, because each proposal names exactly one operation against one entry and an application can validate it. The drift between paper and product also shows that silent model-driven deletion is the part vendors back away from.

## Zep and Graphiti [single-source]

Zep's Graphiti engine stores memory as a temporal knowledge graph with three tiers. An episode subgraph keeps the raw input non-lossily for citation, a semantic entity subgraph holds extracted entities and facts, and a community subgraph clusters entities with summaries (https://arxiv.org/html/2501.13956, accessed 2026-09-29). Every fact edge carries four timestamps on two timelines. `t_valid` and `t_invalid` record when the fact held in the world, and `t'_created` and `t'_expired` record when the system learned and retired it. When a new fact contradicts an old one over an overlapping period, Graphiti sets the old edge's `t_invalid` to the new edge's `t_valid` rather than deleting it. Retrieval combines cosine similarity, BM25 and breadth-first graph search, with reranking by reciprocal rank fusion, maximal marginal relevance, mention frequency or a cross-encoder. The abstract reports 94.8 percent against MemGPT's 93.4 percent on Deep Memory Retrieval, up to 18.5 percent accuracy gains on LongMemEval and about 90 percent lower latency (https://arxiv.org/abs/2501.13956, accessed 2026-09-29).

Supersession by invalidation rather than deletion appears independently in Mem0g above, in Managed Agents' immutable versions and in Zep, so the principle is well supported for the system's own edits. It does not answer what happens when the person asks for deletion, and for a minor learner that answer has to be real deletion of the content.

## Open learner models and tutoring memory [single-source]

In intelligent tutoring, the learner model has long been the memory of the student, and the open learner model tradition argues it should be visible to them. Bull's survey of students names four types of open learner model. An inspectable model is for viewing only, a co-operative model shares modelling tasks between student and system, an editable model lets the student change the contents at will, and a negotiated model has student and system discuss the contents and agree. Students in that survey preferred co-operative (45 percent) and editable (50 percent) models, and between 32 and 48 percent were undecided about each type (Bull, "Supporting Learning with Open Learner Models", https://www.etpe.gr/custom/pdf/etpe4.pdf, accessed 2026-09-29). The same paper argues that negotiation serves both accuracy and reflection, because the student has to justify a change.

Bull and Kay's SMILI framework, "Student Models that Invite the Learner In", was revised in 2016 as a guide for designers of interfaces to learning data, covering what is open, how it is presented and who controls access (https://api.semanticscholar.org/graph/v1/paper/DOI:10.1007/s40593-015-0090-8, abstract, accessed 2026-09-29). The Springer page at https://link.springer.com/article/10.1007/s40593-015-0090-8 redirected to a sign-in and was not read. A secondary summary lists the original framework's four elements and notes the tension between letting learners update their model and letting them overstate their skill (https://edutechwiki.unige.ch/en/Open_learner_model, accessed 2026-09-29).

Recent LLM tutor work adds persistent memory to this frame. DeepTutor keeps a three-part profile of session history, a weakness inventory with each gap marked active or resolved, and self-reflection notes on which explanations worked. A gap is marked resolved after correct application in at least two later sessions and reverts to active if the error returns. Removing memory cost 7.11 percentage points of overall quality on the authors' TutorBench (Zhao et al, https://arxiv.org/html/2604.26962v1, accessed 2026-09-29). LOOM builds a learner memory graph from everyday LLM conversations and names its own weakness, that LLM inference can overgeneralise what the learner knows after one interaction, and that learners could respond to proposals but not edit the structure (Cui, Pu and Grossman, https://arxiv.org/html/2511.21037, accessed 2026-09-29). Both are single author-group preprints with self-built evaluations.

For Growth the transferable points are that a memory of the student should be open to the student, that the editable form is the one students in Bull's survey wanted most, and that an LLM-inferred claim about what a student knows is the weakest kind of evidence and must not stand in for the engine's measured state.

## Sycophancy and over-personalisation [verified]

Two independent studies find that memory about the user makes models agree with the user more. Jain et al found that user memory profiles were associated with the largest increases in agreement sycophancy, for example +45 percent for Gemini 2.5 Pro, using two weeks of interaction data from 38 users (https://arxiv.org/abs/2509.12517, accessed 2026-09-29). PersistBench tested 18 models on 500 human-validated samples and found a median 97.8 percent failure rate on memory-induced sycophancy and a median 53 percent failure rate on cross-domain leakage, where a memory from one area bends an answer in another, against 16.5 percent failure on the control set of beneficial memory use. The authors report that doing well on beneficial use does not predict robustness to harmful use (Pulipaka et al, https://arxiv.org/html/2602.01146v2, accessed 2026-09-29).

For a mathematics tutor the risk is concrete. A memory that says the student believes a sign rule would, on this evidence, raise the chance the tutor lets a wrong step pass. So memory entries must be about how to help the student, never about what the student believes to be mathematically true, and the tutor prompt must state that no memory entry changes whether a step is right. A search also surfaced 2026 preprints on over-personalisation and persistent sycophancy in stateful agents (https://arxiv.org/html/2608.08300 and https://arxiv.org/html/2607.01071v1, search results only, not read), which are not relied on here.

## How the surveyed systems answer the design questions [inferred]

The table condenses the sections above. Each cell restates what the cited source says, and the last column is this file's reading for Growth.

| Question | What the surveyed systems do | Reading for Growth |
| --- | --- | --- |
| Episodic, semantic, procedural split | MemGPT and Letta split in-prompt core blocks from recall (episodes) and archival stores. Zep keeps episodes non-lossily beside extracted facts. DeepTutor separates session history, weaknesses and notes on what explanations worked, which is a procedural layer. Claude Code types entries as user, feedback, project, reference. | Keep three kinds. Episodic is a short-lived per-session summary. Semantic is durable facts about the student as a learner. Procedural is how to tutor this student (explanation style, hint pace). |
| When summarisation and reflection run | Generative agents reflect when importance passes 150. Letta dreams after N steps or at compaction. Managed Agents dreams are an explicit job over up to 100 sessions. Mem0 extracts on every message pair. | Run at the end of each tutor session and as a nightly sweep, never per turn, so no memory model call sits on the interactive path. |
| Retrieval per turn | Letta keeps core blocks always in prompt and searches the rest. Generative agents rank by recency, importance and relevance. Claude Code loads a bounded index and reads topics on demand. Zep fuses cosine, BM25 and graph search. | With one student and tens of entries, a deterministic rank on screen skills, kind and recency does the job without embeddings. |
| How much to inject | Claude Code caps its index at 200 lines or 25 KB. Letta caps each block by characters. Mem0's paper averages about 7,000 memory tokens per conversation. | A fixed cap of about 6 entries and about 300 tokens per turn (see Token cost). |
| Contradiction and supersession | Zep invalidates edges with bi-temporal stamps. Mem0g marks relationships invalid. Managed Agents writes immutable versions. Dreams replace contradicted entries in a new store. | The consolidator proposes SUPERSEDE, the old row gets `superseded_by` and `invalid_at`, and the new row cites it. |
| Forgetting and decay | Generative agents decay recency at 0.995 per hour. The memory tool page suggests expiring unaccessed files. Managed Agents keeps versions 30 days. DeepTutor marks gaps resolved. ChatGPT schedules deletion within 30 days when chat reference is off. | Per-kind expiry, resolution of confusions when the engine shows the linked skills mastered, and hard deletion of superseded content after a short window. |
| User-visible and editable memory | ChatGPT lists and deletes per entry and clears all. Claude Code memory is plain files the user edits. Managed Agents exposes API edit and redact. Bull's students preferred editable models. | A memory view in settings with per-entry delete, per-entry edit for conversation-derived entries, full clear, and a pause switch. |
| Memory that must never influence grading | None of the general assistants has a grading path. Growth already keeps checkpoints and probes out of the engine (`app/db/models.py` module docstring). | The same rule, enforced in code and by test, applied to memory. |
| Sycophancy and over-personalisation | Jain et al and PersistBench measure large increases in agreement driven by user memory. | No entry may record a mathematical belief as the student's position, and the prompt says memory never changes correctness. |
| Token cost | Mem0 and Zep both report large savings against full context. Context editing and compaction exist to bound context growth. | Memory is a small fixed add-on to each tutor turn (see Token cost). |

## Token cost of memory in the prompt [inferred]

Prices are from https://platform.claude.com/docs/en/about-claude/pricing (accessed 2026-09-29). Claude Sonnet 5 is $2 per MTok input, $10 per MTok output, $0.20 per MTok for cache hits, and $2.50 per MTok for 5-minute cache writes. Claude Haiku 4.5 is $1 input and $5 output per MTok. The Batch API halves both input and output, giving $1 and $5 for Sonnet 5 and $0.50 and $2.50 for Haiku 4.5. The model ids Growth routes to are `claude-sonnet-5` and `claude-haiku-4-5` (docs/plan/07-ai-provider-layer.md).

Per turn, a cap of 6 entries at about 40 to 50 tokens each plus JSON framing is about 300 input tokens. Uncached on `claude-sonnet-5` that is 300 × $2 / 1,000,000 = $0.0006 per turn, or $0.60 per 1,000 turns. Memory changes only between sessions, so within one tutor session the memory block is stable, and if it sits in the first user message behind a cache breakpoint the repeat reads cost 300 × $0.20 / 1,000,000 = $0.00006 per turn after a first write of 300 × $2.50 / 1,000,000 = $0.00075. Whether a cache breakpoint placed after a JSON-encoded user block holds across turns in Growth's adapter is untested, and the fixture `tests/fixtures/prompt_token_counts.json` has no measured tutor figure yet, so these are estimates.

Per consolidation, an input of about 3,000 tokens (the session's turn buffer, the current active entries and the prompt) and an output of about 500 tokens on `claude-haiku-4-5` is 3,000 × $1 / 1,000,000 + 500 × $5 / 1,000,000 = $0.0055, or $0.00275 on batch. At one consolidation per tutor session and a few sessions a day, that is under $0.02 a day. On the subscription backend the dollar figure does not apply, and the binding limit is the per-role pacing cap in `app/providers/guard.py`, which is why consolidation needs its own role and its own cap rather than spending the tutor's calls.

The comparison that matters is against the alternative of replaying past conversations. Mem0's paper puts full-context conversations at about 26,000 tokens, which on `claude-sonnet-5` is $0.052 per turn uncached, roughly 90 times the memory block.

## What Growth already holds about the learner [verified]

Read from the files named, on 2026-09-29. The tag here means read in the repository, not cross-checked on the web.

| What | Where | Written by | Notes |
| --- | --- | --- | --- |
| Mastery per skill (beta, credited successes and failures, FSRS stability and difficulty, fading stage, mastered flag and date, consecutive runs, unaided success count, hypercorrection due date, concept opener flag) | `skills_state`, `app/db/models.py` `SkillState` | The engine | The adaptive mechanism itself. Deletable only by full purge (plan 09). |
| Every attempt, with the response, confidence and its source, elapsed time, correctness, served fading stage, format, per-skill states at serve time, transcription, grading state and credit record | `attempts`, `Attempt` | Session and grading services | Plan 09 lists the response text as a thing never to log. |
| The student's one-line error note | `attempts.error_note` | The student, after corrective feedback (plan 03, "The student's one-line error note") | Shown on the review screen (`app/review/screen.py` `error_notes`) and editable there. Plan 13 Safety measured that no prompt builder reads it. |
| The student's self-explanation | `attempts.self_explanation` | The student, prompted by `app/feedback/render.py` `self_explanation_prompt` | No plan 09 retention row names it separately. |
| The tutor's feedback sentence and per-attempt tutor usage | `attempts.tutor_sentence`, `tutor_calls`, `tutor_cost_usd`, token columns | `app/feedback/drain.py` and `app/api/routes/sessions.py` `tutor_sentence_for` | Model-written text about one attempt. |
| Diagnoses (observed errors, misconception hypotheses as a distribution, non-conceptual causes, prerequisite gap, mastery states, matched signal, scheduled probe, who diagnosed) | `diagnoses`, `Diagnosis`, keyed by attempt | Rules in P2, the diagnostician in P3 (plan 03) | Plan 03 Feedback policy forbids naming a misconception as established. |
| Pending discriminating probes | `pending_probes` | The diagnostician path | Expire after 7 days. |
| Per-point FRQ gradings with evidence quotes | `gradings` | The grader | Disputes reverse engine credit. |
| Judgments of learning | `judgments` | The student | Never enter credit assignment (plan 09). |
| Session records (mode, queue, whether the session updates mastery) | `sessions` | Session builder | |
| Lesson reading state and events | `lesson_state`, `lesson_events`, `lesson_check_responses` | Lessons layer | Lesson check answers never reach `attempts` (plan 15, invariant L2). |
| Checkpoint scores, probe responses, assessment parts and responses (including the student's own notes and highlights in a timed part), mock results | `checkpoints`, `checkpoint_scores`, `probe_*`, `assessment_*`, `mock_results` | Assessment and evaluation paths | The engine never reads checkpoints or probes, so a measurement cannot train what it measures (`app/db/models.py` docstring). |
| The if-then implementation intention, one line in the student's own words | `users.study_plan` | The student, through `/settings/study-plan` (`app/settings/preferences.py`) | Plan 01, "Implementation intention and queue-bound streak". Student-written text that no memory entry should copy. |

Purge and export already reach any table that carries `user_id`, `session_id` or `attempt_id`, by reading the schema rather than a list (`app/export/archive.py` `owner_clause`, `app/session/purge.py` `purge_user`). A new memory table with a `user_id` column is therefore exported and purged with no further code, and its secret-column rule would not strip it, since no column name would carry a secret word.

The tutor prompt already has a persistent slot. `prompts/tutor/guardrailed_practice_v1.md` takes `{{ misconception_list }}` below the marker so that a nudge does not repeat a correction the student has needed before. A search of `app/` finds no code that fills `misconception_list` today, so the slot exists in the template and its tests only. Plan 07 (Prompt templates, cache-prefix stability) says the misconception list sits in the cached prefix, while the template puts it below the marker, so the plan and the template disagree and the template is the one that satisfies the no-student-text-in-system-prompt rule.

Plan 09 states what is deliberately not stored: "no free-text chat history beyond the student's own error notes, because the tutor is guardrailed and turn-based". Plan 03 calls the error note "the only free text the app stores about the student beyond their own work". A live tutor with memory changes both statements, so either needs a recorded amendment before a memory table ships.

## What a memory layer adds beyond this [inferred]

Everything in the table above is measurement. It says what the student got right, how sure they were, and what error the diagnostician inferred. None of it records how this student likes to be helped, and none of it keeps the student's own words about their confusion beyond the single error-note line. The items below are the gap, and each is information a human tutor would carry from one week to the next.

- How the student prefers explanations. For example, a graph before the algebra, or a short answer before a long one, or the student asked the tutor to stop restating the question.
- Recurring confusions in the student's own words. For example, "I never know when to use the chain rule on the inside". This is different from a `diagnoses` row, which names a library misconception with a probability. The student's phrasing is what lets the tutor recognise the same confusion next time and address it in the student's terms.
- Representations the student reaches for. For example, the student sketches a sign chart for every increasing and decreasing question, or avoids tables. Plan 03's one-translation rule picks a representation from the item and the misconception, and this would tell the tutor which of the two the student finds easier to read.
- What the student said they found hard, as the student said it, kept apart from what the engine measured.
- Preferred pace of hints. Whether the student wants a question back first or wants to be left alone longer before a nudge, inside the limits the guardrail level sets.
- A short episodic note of the last tutor session, such as the topic discussed and where the conversation stopped, so the next session can pick up without the student repeating themselves.

Each of these is about the interaction and not about correctness, and none is derivable from the engine tables. That is the test for whether something belongs in memory, taken from Claude Code's rule of skipping anything another source already holds.

## What must never be a memory [inferred]

- Any answer the student gave or is working on, submitted or not, and any fragment of one.
- Any answer key, option key, worked solution or step of a worked solution.
- Any statement of mastery, readiness or progress ("has mastered related rates", "is weak on series"). The engine owns that and it already has the measured version.
- Any correctness judgement about a past attempt, and any grade, point or score.
- Any record of a mathematical claim as the student's belief ("thinks the derivative of a product is the product of derivatives"). That is a misconception hypothesis, which belongs in `diagnoses` with a probability, and as memory it is the shape PersistBench and Jain et al show raising sycophancy.
- Confidence ratings and judgments of learning, which already have tables and feed calibration.
- Anything about exam predictions, schedules, study plans or quotas.
- Personal information beyond learning: family, health, location, contact details, other people. The student may mention these in conversation and the consolidator must drop them.
- Any text written as an instruction to the tutor ("always give me the answer"). A preference that would breach the guardrail is not stored, because stored memory is read in later sessions as context and the Managed Agents page names exactly this route for injected content to become trusted.

## Proposed store, consolidator output and retention rows [inferred]

This section gives the concrete shapes the recommendations below refer to. It is a proposal for a plan amendment, not a settled design.

`tutor_memories`, one row per entry.

| Column | Type | Meaning |
| --- | --- | --- |
| `id` | text, primary key | `MEM-` plus a random hex id |
| `user_id` | text | Owner. Makes export and purge reach the row through `owner_clause` |
| `kind` | text | One of `preference`, `confusion`, `stated_difficulty`, `episode` |
| `text` | text, nullable | At most 200 characters. Null on a tombstone |
| `skill_ids` | text (JSON list) | Library skill codes as attributes. Empty for most `preference` entries |
| `source` | text | `conversation` or `own_notes` |
| `source_session_id` | text, nullable | The tutor session the entry was consolidated from |
| `evidence_count` | integer | How many sessions supported the entry |
| `created_at`, `updated_at` | text | ISO timestamps, as every Growth table carries |
| `last_confirmed_at` | text | Last consolidation that returned UPDATE or NOOP on it |
| `last_used_at` | text, nullable | Last time retrieval put it in a prompt |
| `expires_at` | text, nullable | Set for `episode` (14 days) and refreshed by use for the others (60 days) |
| `superseded_by` | text, nullable | The id of the entry that replaced it |
| `invalid_at` | text, nullable | When supersession took effect |
| `resolved_at` | text, nullable | When the engine showed every linked skill mastered |
| `edited_by_student` | integer | 1 when the student has edited the text, which the consolidator may not overwrite |
| `deleted_at` | text, nullable | Set on a student deletion, with `text` erased |

`tutor_turn_buffer`, one row per turn of the live tutor, holding `id`, `user_id`, `tutor_session_id`, `role` (student or tutor), `text`, `screen_ref` (the structured screen state id, never the draft answer), `created_at`, `consolidated_at`. Rows are hard-deleted when their session is consolidated, and a sweep deletes any row older than 7 days whatever its state.

The consolidator returns a list of proposals under a strict schema. Each proposal has these fields.

```json
{
   "operation": "ADD | UPDATE | SUPERSEDE | NOOP",
   "target_id": "MEM-... or null for ADD",
   "kind": "preference | confusion | stated_difficulty | episode",
   "text": "at most 200 characters",
   "skill_ids": ["library skill codes"],
   "evidence_turn_ids": ["tutor_turn_buffer ids the proposal rests on"]
}
```

The application, not the model, applies a proposal. It refuses an UPDATE or SUPERSEDE against a row with `deleted_at` set or with `edited_by_student` set, refuses any proposal whose `evidence_turn_ids` do not all belong to the session being consolidated, and runs the content checks listed in recommendation 7 before writing.

Rows for the plan 09 retention table, in its column order.

| Datum | Table or store | Purpose | Retention | Deletable |
| --- | --- | --- | --- | --- |
| Tutor memory entries | `tutor_memories` | Let the live tutor carry the student's stated preferences and recurring confusions across sessions | Episodes 14 days, other entries 60 days from last use, superseded and resolved entries 30 days, all at purge | Yes, individually, and all at once, with no mastery consequence |
| Tutor turn buffer | `tutor_turn_buffer` | Input to consolidation only | Until the session is consolidated, at most 7 days, and at purge | Yes, with the full memory clear, and by full purge |

Neither table touches the "What is deliberately not stored" paragraph's other exclusions (location, device fingerprint, contact details, third-party analytics), and both keep the plan 09 rule that the student's response text is never logged, because neither table holds an item response.

## What this means for Growth [inferred]

Ranked by consequence if it is got wrong.

1. **Memory never reaches grading, diagnosis, the engine or selection, and this is enforced in code.** The memory table is read by exactly one prompt builder, the tutor's. A test walks the import graph and fails if `app/engine`, `app/grading`, `app/feedback` (other than the tutor path), `app/session/build.py` or any diagnostician or grader template builder imports the memory module. A second test runs the engine over a fixed attempt sequence twice, once with a populated memory table and once empty, and asserts byte-identical `skills_state`. This matches the existing rule that checkpoints and probes never train the engine. Alternative rejected: letting the diagnostician read the student's own phrasing to sharpen its distribution. It would let unverified model-summarised text move mastery evidence, which breaks the plan 03 guardrail, and the diagnostician already reads the observed work directly.

2. **Record the plan amendments before building.** Plan 09's "no free-text chat history" and plan 03's "only free text" sentences need rewriting, plan 09 needs retention rows for the new tables, and plan 07 needs an R17 decision adding a seventh role for consolidation, because plan 07 allows six roles only and `app/providers/guard.py` `ROLES` lists six. Alternative rejected: running consolidation under the diagnostician's role. The house rule is that every agent call has its own role and caps, and borrowing another role's cap would let memory work starve grading-adjacent work on the subscription pacing limit.

3. **Two tables, one durable and one short-lived.** `tutor_memories` holds entries with `id`, `user_id`, `kind`, `text` (at most 200 characters), `skill_ids` (library codes as attributes, never keys), `source` (`conversation` or `own_notes`), `source_session_id`, `evidence_count`, `created_at`, `last_confirmed_at`, `last_used_at`, `expires_at`, `superseded_by`, `invalid_at`, `resolved_at`, `edited_by_student`, `deleted_at`. `tutor_turn_buffer` holds the live tutor's turns for one user until the consolidation job for that session has run, and never longer than 7 days, and is then hard-deleted. Both carry `user_id`, so the existing export and purge rules reach them with no code change. Alternative rejected: keeping full transcripts as MemGPT recall storage. Plan 09 names chat history as deliberately not stored for a minor learner, and the consolidated entries carry what a later session needs. Alternative rejected: a graph store after Zep. At one student and tens of entries a graph adds a dependency and buys nothing a `skill_ids` column does not.

4. **Entry kinds and their provenance are fixed.** Four kinds, all from conversation or from the student's own error notes and self-explanations. `preference` (explanations, hint pace, representation habits), `confusion` (a recurring confusion in the student's words, with `skill_ids`), `stated_difficulty` (what the student said was hard), and `episode` (a one-to-two sentence summary of the last tutor session, expiring after 14 days). Engine signals are not copied into memory. The prompt builder reads the misconception list, the current skills and the mastered flags live from `diagnoses` and `skills_state` at call time, which keeps one source of truth. Alternative rejected: writing engine-derived entries such as "struggles with series" into memory. That duplicates the engine as an unmeasured, stale copy, and it is the mastery claim the previous section forbids.

5. **Supersession by invalidation for the system, real deletion for the student.** When the consolidator finds a newer entry that contradicts an older one, the old row gets `superseded_by` and `invalid_at` and drops out of retrieval, and superseded rows are hard-deleted 30 days later. When the student deletes an entry, its `text` is erased at once and the row stays as a tombstone with `kind`, `skill_ids` and `deleted_at` only, so an in-flight consolidation job that proposes an UPDATE against it is refused instead of resurrecting it. Full clear deletes every row including tombstones and empties the turn buffer. Alternative rejected: keeping deleted text in an audit version as Managed Agents does. For a minor learner a delete has to remove the words, and the audit log can record that a deletion happened without its content.

6. **Retrieval per turn is deterministic, capped at 6 entries and about 300 tokens.** Candidates are active entries (not superseded, not deleted, not expired). Rank first all `preference` entries by `last_confirmed_at`, capped at 3. Then `confusion` and `stated_difficulty` entries whose `skill_ids` intersect the skills of what is on screen, then the latest `episode`, then remaining entries by `last_confirmed_at`. Stop at 6 entries or 300 tokens. The block is JSON-encoded into the user message below the marker, under the untrusted-content policy in the cached prefix, and the prompt states that memory describes how to help this student and never changes whether a step is right. Alternative rejected: embedding search with generative-agents scoring. With tens of entries and screen context that already names skills, embeddings add a model dependency and an extra call per turn for no measurable gain. Alternative rejected: a memory tool the tutor calls. The no-tools default holds because app-composed context meets the need.

7. **Consolidation runs as a job, off the interactive path, on a cheap model with structured output.** A `memory_consolidate` job is enqueued when a tutor session ends (idle for 30 minutes or the student leaves the screen) and a nightly sweep catches any session left unconsolidated. The drain calls the new role on `claude-haiku-4-5` (batch when on an API key, pacing-capped when on the subscription) with the session's turn buffer, the student's error notes and self-explanations from that session, and the active entries. The output is a strict schema of proposals, each one of ADD, UPDATE (with `evidence_count` incremented), SUPERSEDE (with the id replaced) or NOOP, carrying the kind, the text and the source turn ids. The model never deletes. The application validates each proposal before writing: kind in the allowed list, text within 200 characters, no digits-and-operator strings that could be an answer, no item or archetype ids, no mastery words from a fixed deny list, no instruction-shaped text, and a Haiku screen with a strict schema for injection as plan 13 already uses for the transcriber. Alternative rejected: per-turn extraction as Mem0 does. It puts a second model call on every tutor turn, which is latency on the interactive path and doubles the subscription call count. Alternative rejected: a reflection trigger on accumulated importance. A session boundary is a natural and predictable trigger for a tutor, and importance scores from a model are one more unmeasured number.

8. **Decay and resolution.** `episode` entries expire after 14 days. A `confusion` entry is marked `resolved_at` by the consolidation job when every skill in its `skill_ids` is `mastered` in `skills_state`, and a resolved entry leaves retrieval and is hard-deleted 30 days later. This is memory reading the engine, which is allowed, and never the engine reading memory. Any entry not retrieved for 60 days expires. Everything goes at the plan 09 default purge. Alternative rejected: an exponential recency decay as in generative agents. A fixed expiry is explainable to the student in one line and testable, and a decay constant would be another untuned number.

9. **A student-facing memory view with per-entry delete, full clear and a pause.** Settings gets a "What the tutor remembers" page listing active entries grouped by kind, each with a plain provenance line naming the date of the conversation it came from, a delete control, and an edit control on `preference` and `confusion` entries, which is Bull's editable model. A "clear all" control sits behind a typed confirmation like the purge, and a pause switch stops both retrieval and consolidation while leaving entries in place. The tutor never announces that it saved something mid-conversation, and the view is where the student finds out. Copy on the page carries no praise and no advice. Alternative rejected: a negotiated model where the system argues back when the student edits. That is right for a mastery model where overstatement is a risk, but these entries are about preference, and the student is the authority on their own preferences.

10. **Evaluate the failure modes before shipping.** Build a small eval set in the PersistBench shape. Cases where a stored confusion must not make the tutor accept a wrong step, cases where a memory about one skill must not colour help on an unrelated one, and cases where a stored preference must not loosen the guardrail. Run it on every change to the tutor template or the consolidator schema. Alternative rejected: relying on the general sycophancy behaviour of the model. The two independent studies above show memory makes that behaviour worse, not better.

One point is left for the operator to decide. Consolidation could also read `attempts.error_note` and `attempts.self_explanation` from sessions where the live tutor was never opened, which would let memory learn recurring confusions from the review loop alone. That widens what a model reads of the student's own text, so it is a choice about the privacy line rather than a technical one.

## Sources [verified]

- https://arxiv.org/abs/2310.08560, accessed 2026-09-29
- https://arxiv.org/pdf/2310.08560, accessed 2026-09-29
- https://docs.letta.com/guides/agents/memory-blocks, accessed 2026-09-29
- https://docs.letta.com/guides/agents/memory, accessed 2026-09-29
- https://docs.letta.com/guides/agents/sleep-time-agents, accessed 2026-09-29
- https://docs.letta.com/guides/agents/architectures/sleeptime, accessed 2026-09-29
- https://arxiv.org/abs/2304.03442, accessed 2026-09-29
- https://arxiv.org/html/2304.03442, accessed 2026-09-29
- https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool, accessed 2026-09-29
- https://platform.claude.com/docs/en/build-with-claude/context-editing, accessed 2026-09-29
- https://platform.claude.com/docs/en/build-with-claude/compaction, accessed 2026-09-29
- https://platform.claude.com/docs/en/managed-agents/memory, accessed 2026-09-29
- https://platform.claude.com/docs/en/managed-agents/dreams, accessed 2026-09-29
- https://platform.claude.com/docs/en/about-claude/pricing, accessed 2026-09-29
- https://code.claude.com/docs/en/memory, accessed 2026-09-29
- https://help.openai.com/en/articles/8590148-memory-faq, attempted 2026-09-29, HTTP 403, content taken from search results
- https://help.openai.com/en/articles/8983136-what-is-memory, attempted 2026-09-29, HTTP 403
- https://help.openai.com/en/articles/8914046-temporary-chat-faq/, search result, accessed 2026-09-29
- https://openai.com/index/memory-and-new-controls-for-chatgpt/, attempted 2026-09-29, HTTP 403
- https://arxiv.org/abs/2504.19413, accessed 2026-09-29
- https://arxiv.org/html/2504.19413, accessed 2026-09-29
- https://docs.mem0.ai/core-concepts/memory-operations/add, accessed 2026-09-29
- https://docs.mem0.ai/core-concepts/memory-types, accessed 2026-09-29
- https://arxiv.org/abs/2501.13956, accessed 2026-09-29
- https://arxiv.org/html/2501.13956, accessed 2026-09-29
- https://www.etpe.gr/custom/pdf/etpe4.pdf, accessed 2026-09-29
- https://api.semanticscholar.org/graph/v1/paper/DOI:10.1007/s40593-015-0090-8, accessed 2026-09-29
- https://link.springer.com/article/10.1007/s40593-015-0090-8, attempted 2026-09-29, redirected to sign-in, not read
- https://edutechwiki.unige.ch/en/Open_learner_model, accessed 2026-09-29
- https://arxiv.org/html/2604.26962v1, accessed 2026-09-29
- https://arxiv.org/html/2511.21037, accessed 2026-09-29
- https://arxiv.org/abs/2509.12517, accessed 2026-09-29
- https://arxiv.org/html/2602.01146v2, accessed 2026-09-29
- https://arxiv.org/html/2608.08300, search result only, not read, 2026-09-29
- https://arxiv.org/html/2607.01071v1, search result only, not read, 2026-09-29
