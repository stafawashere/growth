---
title: Anki and FSRS, how it teaches
research_date: 2026-09-29
status: draft
purpose: Record how Anki, FSRS, the mnemonic medium, Orbit, RemNote and SuperMemo schedule review, so the lesson redesign can borrow spacing mechanics and avoid their known limits for procedural mathematics.
---

# Anki and FSRS

This file reads the subject as a spacing reference. Anki teaches nothing itself, it schedules retrieval of material someone else wrote.


## Who it serves [inferred]

Anki is a general flashcard program with no stated audience in its manual. A study of first-year medical students exists in the literature (https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12662189/, accessed 2026-09-29, seen as a search result only, not read). Quantum Country serves readers of one essay on quantum computing (https://numinous.productions/ttft/, accessed 2026-09-29). RemNote targets students and reports FSRS as the recommended scheduler (https://help.remnote.com/en/articles/9124137-the-fsrs-spaced-repetition-algorithm, accessed 2026-09-29).

## Lesson anatomy [single-source]

A card moves through four states: new, learning, review and relearning (https://docs.ankiweb.net/studying.html, accessed 2026-09-29). The learner sees the front, recalls, reveals the back, and presses Again, Hard, Good or Easy. The manual says Again is used about 5 to 20 percent of the time and Good 80 to 95 percent. Each button shows the next due date.

Learning steps are a list of short delays, for example "1m 10m 1d". Good advances one step, Again returns to the first step, and after the last step the card graduates to a review interval set by the graduating interval. Easy skips to the easy interval. A failed review card is a lapse and enters relearning steps, or, if those are blank, receives a minimum one day interval. Repeated lapses can mark a card as a leech, which can be suspended or tagged (https://docs.ankiweb.net/deck-options.html, accessed 2026-09-29). Sibling cards from one note are buried until the next day (https://docs.ankiweb.net/studying.html#siblings-and-burying, accessed 2026-09-29).

Quantum Country differs. The essay contains 112 cards inline. Readers are tested in the text, then at intervals of 5 days, 2 weeks, 1 month and 4 months, with a failure dropping the interval one level (https://numinous.productions/ttft/, accessed 2026-09-29). The authors report about 95 minutes of review to reach roughly 54 days of retention per question after six reviews.

## How it introduces a concept [single-source]

Anki does not introduce concepts. The learner creates cards after meeting material elsewhere. Matuschak's prompt guide asks for prompts that are focused, precise, consistent, tractable and effortful, and suggests conceptual knowledge be probed through attributes, similarities, parts, causes and significance (https://andymatuschak.org/prompts, accessed 2026-09-29). The mnemonic medium moves authorship to the essay writer, who places the prompts after the prose that supports them. Orbit generalizes this to any web page through embedded web components, with a first email prompt after a few days and later reviews at two weeks, one month and two months (https://github.com/andymatuschak/orbit, accessed 2026-09-29; https://myhub.ai/items/orbit-andy-matuschaks-new-spaced-repetition-tool, accessed 2026-09-29, secondary).

SuperMemo adds incremental reading. Imported text is read in pieces, key fragments are extracted, and fragments are later turned into questions, all under scheduling (https://en.wikipedia.org/wiki/Incremental_reading, accessed 2026-09-29). SuperMemo's minimum information principle says simple questions produce better recall than complex ones (https://super-memory.com/articles/20rules.htm, accessed 2026-09-29, seen through a search summary).

## Worked examples and practice [single-source]

Practice items are cards. For mathematics, Nielsen describes a two phase process on a single proof. First he extracts atomic questions, restatements, geometric readings and one sentence synthesis prompts. Then he adds variations, such as what happens when an assumption is weakened. He estimates dozens of cards per theorem and a few hours of work (https://cognitivemedium.com/srs-mathematics, accessed 2026-09-29). Matuschak advises that procedural prompts target keywords, verbs and the transition points between steps, not each obvious action.

## Response to a wrong answer [single-source]

Immediately, the learner sees the back of the card and presses Again. The card returns after the first learning or relearning step, often within minutes. Later, its interval shrinks and it may become a leech. Under FSRS, a lapse uses a separate stability formula and post-lapse stability cannot exceed the pre-lapse value (https://expertium.github.io/Algorithm.html, accessed 2026-09-29). Anki's FSRS notes warn against pressing Hard when the answer was actually forgotten, because FSRS assumes recall succeeded (https://docs.ankiweb.net/deck-options.html, accessed 2026-09-29).

## Adaptation and sequencing [verified]

FSRS models each card with difficulty, stability and retrievability. Stability is the days for retrievability to fall from 100 to 90 percent, and retrievability is the modelled recall probability (https://github.com/open-spaced-repetition/awesome-fsrs/wiki/ABC-of-FSRS, accessed 2026-09-29; https://expertium.github.io/Algorithm.html, accessed 2026-09-29). Both pages agree. After a successful review stability is multiplied by a factor that is smaller for harder cards, smaller at high stability, and larger when retrievability was lower at review. Difficulty is described by the FSRS author community as a crude 1 to 10 heuristic. The desired retention setting, 90 percent by default in Anki, sets how likely recall should be at the scheduled review, and "Higher retention leads to shorter intervals and more reviews per day" (https://docs.ankiweb.net/deck-options.html, accessed 2026-09-29). The ABC page gives a usable range of 70 to 97 percent.

Version history is partly uncertain. FSRS first shipped in Anki as an opt-in in October 2023 and FSRS-5 in Anki 24.11 (search summaries only). Anki 25.07 release notes credit FSRS-6 (https://github.com/ankitects/anki/releases/tag/25.07, accessed 2026-09-29). FSRS-6 has 21 parameters, a trainable forgetting curve decay, and uses all reviews including same day ones (https://github.com/open-spaced-repetition/awesome-fsrs/wiki/The-Algorithm, accessed 2026-09-29). A third party site says FSRS-7 adds fractional day intervals, dual forgetting curves and about 35 parameters but is unreleased in Anki (https://yazu.app/fsrs/fsrs-7/, accessed 2026-09-29). The benchmark README already lists FSRS-7 (https://github.com/open-spaced-repetition/srs-benchmark, accessed 2026-09-29). Whether Anki ships FSRS as default is unknown. The 25.07 notes do not say, and the manual calls FSRS "an alternative" to SM-2. Prerequisites are not modelled. There is no prerequisite graph. Ordering is by due date, with optional load balancing and easy days.

## What it measures [verified]

FSRS predicts the probability that a card is recalled at a given elapsed time, trained by log loss on binary recall outcomes. The benchmark uses 9,999 to 10,000 collections and about 350 million reviews after filtering, scores by log loss, RMSE(bins) and AUC, and splits data chronologically (https://github.com/open-spaced-repetition/srs-benchmark, accessed 2026-09-29; https://expertium.github.io/Benchmark.html, accessed 2026-09-29). FSRS-6 with recency beats Anki SM-2 on log loss for 99.6 percent of users, though the benchmark's own text says no fully fair comparison exists because SM-2 does not predict probabilities. FSRS measures memory of a card, not skill or understanding.

## Interaction patterns and visual design [single-source]

Interaction is show answer, then four grade buttons with keyboard shortcuts 1 to 4 (https://docs.ankiweb.net/studying.html, accessed 2026-09-29). Cards are text, images and cloze deletions. Quantum Country places cards inline while reading, then delivers reviews by a separate session and email prompts. Orbit reviews run on desktop, mobile and web.

## Engineering signals [uncertain]

FSRS is open source in Rust and other languages, and the benchmark is public. The forgetting curve is a power function, chosen because a mix of exponentials is better approximated by a power curve (https://expertium.github.io/Algorithm.html, accessed 2026-09-29). Optimization is gradient descent on log loss, with initial stability parameters fit separately. RemNote states version 6 in beta, and says 17 parameters, which conflicts with 21 elsewhere (https://help.remnote.com/en/articles/9124137-the-fsrs-spaced-repetition-algorithm, accessed 2026-09-29). The FSRS lineage rests on MaiMemo work, a DSR variant and a stochastic shortest path formulation, reported as cutting 64 percent of recall prediction error and 17 percent of cost against baselines (https://ieeexplore.ieee.org/document/10059206/, accessed 2026-09-29, via search summary). Orbit's scheduling algorithm is not documented in its README.

## What it does badly [single-source]

Nielsen states that Anki builds recall of facts and does not by itself build practical skill, and that his math process does not reach the internalized state of extended problem solving (https://augmentingcognition.com/ltm.html, https://cognitivemedium.com/srs-mathematics, accessed 2026-09-29). He also calls some generated cards "exhaust" and finds shared decks largely illegible. The Quantum Country authors say they do not know whether learners can retrieve answers outside the test context or apply knowledge to real problems (https://numinous.productions/ttft/, accessed 2026-09-29).

Card scheduling has a specific mismatch with procedural mathematics. A card's answer is fixed, so a learner can remember the worked answer of a particular problem, not the method, and FSRS then models memory of that instance. Matuschak's consistency and tractability requirements push authors toward short, single answer prompts, which suits facts and step transitions more than multi step derivations. Grading is self reported and coarse. A card cannot tell a correct method with an arithmetic slip from an unknown method. There is no prerequisite model and no interleaving control across topics. Spacing itself is supported for mathematics procedures. In Rohrer and Taylor's two experiments with 216 college students, splitting 10 practice problems across two sessions roughly doubled four week test performance, but 3 versus 9 problems in one session had no effect (https://eric.ed.gov/?id=ED505642, accessed 2026-09-29). That result concerns spaced problem sets, not card recall. Whether card based review transfers to AP free response performance is unknown, and I found no study.

## Sources [verified]

- https://docs.ankiweb.net/deck-options.html, accessed 2026-09-29. Learning steps, lapses, leeches, desired retention.
- https://docs.ankiweb.net/studying.html, accessed 2026-09-29. Card states, answer buttons, siblings.
- https://github.com/open-spaced-repetition/awesome-fsrs/wiki/ABC-of-FSRS, accessed 2026-09-29. DSR definitions, retention range, FSRS-6 note.
- https://github.com/open-spaced-repetition/awesome-fsrs/wiki/The-Algorithm, accessed 2026-09-29. FSRS-6 forgetting curve and parameter count.
- https://expertium.github.io/Algorithm.html, accessed 2026-09-29. Stability update factors, loss function, limitations.
- https://expertium.github.io/Benchmark.html, accessed 2026-09-29. Benchmark method and SM-2 caveat.
- https://github.com/open-spaced-repetition/srs-benchmark, accessed 2026-09-29. Dataset size, metrics, FSRS versions.
- https://github.com/ankitects/anki/releases/tag/25.07, accessed 2026-09-29. FSRS-6 in Anki 25.07.
- https://yazu.app/fsrs/fsrs-7/, accessed 2026-09-29. FSRS-7 status, third party.
- https://numinous.productions/ttft/, accessed 2026-09-29. Mnemonic medium, Quantum Country schedule and limits.
- https://andymatuschak.org/prompts, accessed 2026-09-29. Prompt properties, knowledge types.
- https://augmentingcognition.com/ltm.html, accessed 2026-09-29. Nielsen on Anki, caveats.
- https://cognitivemedium.com/srs-mathematics, accessed 2026-09-29. Nielsen on mathematics cards.
- https://github.com/andymatuschak/orbit, accessed 2026-09-29. Orbit description and licensing.
- https://myhub.ai/items/orbit-andy-matuschaks-new-spaced-repetition-tool, accessed 2026-09-29. Orbit review intervals, secondary.
- https://help.remnote.com/en/articles/9124137-the-fsrs-spaced-repetition-algorithm, accessed 2026-09-29. RemNote FSRS implementation.
- https://en.wikipedia.org/wiki/Incremental_reading, accessed 2026-09-29. SuperMemo incremental reading.
- https://eric.ed.gov/?id=ED505642, accessed 2026-09-29. Rohrer and Taylor distributed practice in mathematics.
- https://ieeexplore.ieee.org/document/10059206/, accessed 2026-09-29. MaiMemo scheduling paper, via search summary.
