---
title: Anki and FSRS, how the daily set is chosen
research_date: 2026-09-29
status: draft
purpose: Record how Anki and the FSRS scheduler decide which card comes next, how a day's set is sized, ordered, capped and spread, and where the public evidence is weak, so Growth's daily practice set can borrow retrievability-driven selection and avoid the known cap and backlog failures.
---

# Anki and FSRS, the daily set

This file reads Anki as a scheduler of daily reviews, not as a lesson product. The lesson-side reading is in docs/pedagogy/products/anki-fsrs.md and is not repeated. All pages below were read on 2026-09-29, and where a search summary was the only view of a page that is said in the text.

## What decides the next problem [verified]

A card is due when its scheduled interval has elapsed. Under FSRS the interval is the solution of the forgetting curve for the desired retention r, I = S / FACTOR times (r to the power 1/DECAY minus 1), so at r = 0.9 the interval equals the stability S (https://github.com/open-spaced-repetition/awesome-fsrs/wiki/The-Algorithm, accessed 2026-09-29). Retrievability R is the modelled recall probability, stability S is the days for R to fall to 90 percent, and difficulty D runs from 1 to 10 (same page). In FSRS-6 the curve is a power function whose decay exponent w20 is fitted per user, and the model has 21 parameters (same page). Within a session Anki gathers intraday learning cards first, then interday learning cards, then review cards, then new cards (https://docs.ankiweb.net/deck-options.html, accessed 2026-09-29). Under FSRS the review sort option "Relative overdueness" is replaced by ascending retrievability, so the card the model thinks you are most likely to have forgotten is offered first (same manual). The default review sort is due date then random, which the manual recommends only when there is little backlog (same manual). D does not choose the next card, it only shapes the next stability. That reading is [inferred] from the update formulas described at https://expertium.github.io/Algorithm.html (accessed 2026-09-29).

## How a set is sized and ordered [verified]

The set is whatever is due, cut by two caps. New cards per day and maximum reviews per day both apply, and by default the review cap also blocks new cards once it is reached, unless "New Cards Ignore Review Limit" is on (https://docs.ankiweb.net/deck-options.html, accessed 2026-09-29). Interday learning cards count against the review cap (same manual). The manual says that learning 20 new cards a day steadily yields roughly 200 reviews a day, and that many users are overwhelmed after introducing hundreds in the first days (same manual). New cards are gathered by deck order, ascending position, random notes or random cards, then sorted by card type or randomly, and the new versus review order is mix, new first or new last (same manual). The default among those three is not stated in the passages read, so it is unknown here.

Desired retention is the size lever under FSRS. The manual gives 90 percent as the default and says workload rises very quickly above 90 percent and can overwhelm above 97 percent, without a published table of reviews per day at each level (same manual). Expertium's retention page adds that at 90 percent desired retention the average predicted retrievability over all cards is about 94.7 percent (https://expertium.github.io/Retention.html, accessed 2026-09-29). It gives no workload numbers.

## How difficulty is chosen and estimated [single-source]

Anki does not choose problems by difficulty. Difficulty is a per-card state variable, estimated from grade history by the optimizer, and it changes how fast stability grows after a success (https://expertium.github.io/Algorithm.html, accessed 2026-09-29). The optimizer minimizes log loss, binary cross entropy with Again as failure and Hard, Good and Easy as success, by gradient descent, and the first four parameters, the initial stabilities per first grade, are first estimated directly from first and second reviews and then refined (same page). Parameter groups in FSRS-6 are initial stabilities, difficulty initialization, same-day stability, difficulty updates, and the forgetting curve (https://github.com/open-spaced-repetition/awesome-fsrs/wiki/The-Algorithm, accessed 2026-09-29). The manual says a few hundred reviews is the floor for a fit, suggests optimizing about monthly, and advises separate presets for decks of very different difficulty (https://docs.ankiweb.net/deck-options.html, accessed 2026-09-29). Its author admits the definition of D ignores R, that adding R did not improve accuracy, and that stability predictions carry a mean absolute percentage error near 33 percent (https://expertium.github.io/Algorithm.html, accessed 2026-09-29).

## What happens after a wrong answer [single-source]

Pressing Again sends the card into relearning, and the button shows the next interval set by the deck's relearning steps and lapse settings (https://docs.ankiweb.net/studying.html, accessed 2026-09-29). The manual has a minimum interval option for how many days a lapsed card waits after relearning (https://docs.ankiweb.net/deck-options.html, accessed 2026-09-29). Under FSRS a lapse cuts stability by a fitted post-lapse factor and the loss function counts only Again as failure (https://expertium.github.io/Algorithm.html, accessed 2026-09-29). Anki assumes the learner presses Again on a forgotten answer and warns that using Hard for a forgotten card wrecks the fit (https://docs.ankiweb.net/deck-options.html, accessed 2026-09-29).

FSRS models same-day repeats poorly. A moderator wrote on 2025-02-07 that FSRS has no model for intraday memory and advised keeping learning steps (https://forums.ankiweb.net/t/fsrs-short-term-scheduling/55504, accessed 2026-09-29). An issue opened on 2024-10-14 asked for an FSRS short-term scheduler and noted that it is very unlikely to schedule under 4 hours (https://github.com/ankitects/anki/issues/3497, accessed 2026-09-29). That page was seen through a summary only and does not state the release that shipped it.

## How review is compressed or deduplicated [verified]

Four mechanisms spread or thin the load. Sibling burying hides other cards of the same note until the next day (https://docs.ankiweb.net/studying.html, accessed 2026-09-29). Fuzz moves an interval by a small random amount so that cards learned together do not stick together, for example 2 to 4 days for a 3 day interval and 86 to 94 for 90 days (https://github.com/open-spaced-repetition/fsrs4anki-helper, accessed 2026-09-29). The load balancer replaces the random pick with a weighted pick inside the same fuzz range, favouring days with fewer cards due, per preset, ignoring intervals over 90 days, and the developers said its retention effect is almost the same as fuzz (https://github.com/ankitects/anki/pull/3230, accessed 2026-09-29). Easy Days nudge an interval after calculation so that chosen weekdays get less work, is not retroactive, and gives the same total workload if all days are set alike (https://docs.ankiweb.net/deck-options.html, accessed 2026-09-29). None of these merges two different questions into one.

## What the student sees on the day screen [single-source]

The deck overview shows three counts, New, Learning and To Review, with buried cards in grey when burying is on (https://docs.ankiweb.net/studying.html, accessed 2026-09-29). Anki keeps showing cards until the day's allotment has run out. When reviews were hidden by the cap, the congratulations screen carries a message suggesting a higher limit (https://docs.ankiweb.net/deck-options.html, accessed 2026-09-29).

The count shown is the capped number, not the backlog.

## What is public about the engineering [verified]

FSRS is open source, with the Rust port fsrs-rs and the benchmark at https://github.com/open-spaced-repetition/srs-benchmark (accessed 2026-09-29). The scheduling method was published as Ye, Su and Cao, KDD 2022 pages 4381 to 4390, and extended in IEEE TKDE 35(10) 2023 pages 10085 to 10097, which frame scheduling as a stochastic shortest path problem (search results at https://dl.acm.org/doi/10.1109/TKDE.2023.3251721, accessed 2026-09-29, abstract only). The benchmark uses 9,999 collections and 349,923,850 evaluation reviews without same-day reviews, and 10,000 collections and 519,296,315 reviews with them, from about 727 million reviews in total, split by time so that training reviews precede test reviews.

Log loss without same-day reviews, lower is better, with parameter count in brackets. FSRS-7 0.3401 (34), FSRS-7 with recency weighting 0.3370 (34), FSRS-6 0.3460 (21), FSRS-5 0.3561 (19), FSRS v4 0.3726 (17), DASH 0.3682 (9), ACT-R 0.4033 (5), HLR 0.4694 (3), the constant user-average baseline 0.3945, and the moving-average baseline 0.3369 (0). A neural net with 2,762,884 parameters, RWKV-Instant, reaches 0.2773. With same-day reviews scored, FSRS-7 is 0.3206, FSRS-6 0.3842, DASH 0.3487, HLR 0.705 and moving average 0.3301 (all from the benchmark README, accessed 2026-09-29).

SM-2 has no row in the current README. Expertium's unfinished benchmark page reports that FSRS-6 with recency weighting beats Anki SM-2 on log loss for 99.6 percent of users, after a converter that turns SM-2 intervals into probabilities (https://expertium.github.io/Benchmark.html, accessed 2026-09-29). An older Anki-run benchmark on 4,632,965 reviews gave SM2 0.7317 against FSRS v4 0.3874 (https://github.com/ankitects/fsrs-benchmark, accessed 2026-09-29).

FSRS-7 splits memory into fast and slow traces and accepts fractional intervals, but a third-party tracker says it is not released in fsrs-rs mainline and expects production use no earlier than 2027 (https://yazu.app/fsrs/fsrs-7/, accessed 2026-09-29). Clanki, a fork, is reported to use FSRS-7 only (https://github.com/Expertium/Clanki/pull/40, accessed 2026-09-29, search result only).

I found no dedicated 2024 to 2026 blog post on short-term memory, only the issue, forum and README notes above, which say FSRS-5 began training on same-day reviews, FSRS-6 improved their formula, and FSRS-7 alone can predict same-day recall.

## What it does badly [single-source]

The hidden backlog is the best documented harm. A user guide argues that the default 200 review cap masks the true backlog, that random order can show years-overdue long-interval cards before short-interval cards close to forgotten, and that the masking pushes users to quit (https://controlaltbackspace.org/catch-up/, accessed 2026-09-29).

The benchmark shows a weak margin over a trivial baseline. Without same-day reviews the moving-average baseline has lower log loss than FSRS-6 and FSRS-7 (0.3369 against 0.3460 and 0.3401), while FSRS-7 wins on discrimination, AUC 0.7167 against 0.7001, and on the same-day set (benchmark README, accessed 2026-09-29). Expertium notes SM-2 was never designed to output probabilities, so its comparison is not clean (https://expertium.github.io/Benchmark.html, accessed 2026-09-29). Nielsen, in the lesson file, says card scheduling builds recall of facts and not problem-solving skill (https://augmentingcognition.com/ltm.html, accessed 2026-09-29, not re-read here). For math, a card whose answer is fixed trains memory of one instance, an [inferred] limit already recorded in the lesson file.

## Sources [verified]

- https://docs.ankiweb.net/deck-options.html, accessed 2026-09-29. Caps, orders, easy days, FSRS options, optimizer advice.
- https://docs.ankiweb.net/studying.html, accessed 2026-09-29. Overview counts, burying, Again.
- https://github.com/open-spaced-repetition/awesome-fsrs/wiki/The-Algorithm, accessed 2026-09-29. R, S, D, curve, 21 parameters, interval formula.
- https://expertium.github.io/Algorithm.html, accessed 2026-09-29. Loss, optimizer, limitations.
- https://expertium.github.io/Retention.html and https://expertium.github.io/Benchmark.html, accessed 2026-09-29. Retention terms, SM-2 caveat, 99.6 percent.
- https://github.com/open-spaced-repetition/srs-benchmark, accessed 2026-09-29. Results tables, dataset, version notes.
- https://github.com/ankitects/fsrs-benchmark, accessed 2026-09-29. Older SM2 numbers.
- https://github.com/ankitects/anki/pull/3230 and https://github.com/open-spaced-repetition/fsrs4anki-helper, accessed 2026-09-29. Load balancer, fuzz ranges.
- https://github.com/ankitects/anki/issues/3497 and https://forums.ankiweb.net/t/fsrs-short-term-scheduling/55504, accessed 2026-09-29. Short-term scheduling.
- https://yazu.app/fsrs/fsrs-7/, accessed 2026-09-29. FSRS-7 status, third party.
- https://controlaltbackspace.org/catch-up/, accessed 2026-09-29. Cap masks backlog.
- https://dl.acm.org/doi/10.1109/TKDE.2023.3251721, accessed 2026-09-29. Scheduling paper, abstract only.
