---
title: Duplicate gate validation on labelled samples
research_date: 2026-09-24
status: complete
purpose: Records the labelled samples the duplicate and copyright gate was validated on, the precision and recall of each stage at the published and the adopted operating points, and why the operating points changed.
---

# Duplicate gate validation [verified]

docs/plan/04-item-generation.md requires both thresholds of the duplicate gate to be validated on a
labelled sample before they are trusted. Four samples of 220 pairs each are here, built by
`tools/duplicate_sample.py build` with seeds 20260924 (`sample.json`), 20261010 (`holdout.json`),
20261101 (`test.json`) and 20261201 (`final.json`), and scored by `tools/duplicate_sample.py score`
into the matching `-report.json`. A pair names items by id and official text by page and word
offset, with the transformation and its seed, so no official text is committed; the texts are
rebuilt from `cache/text` and `content/` when scored.

Each sample holds 110 positive pairs (20 reformatted copies, 20 light edits and 30 paraphrases of
bank items; 20 light edits and 20 paraphrases of official passages) and 110 negative pairs (siblings
of one archetype with other numbers, any two bank items, and a generated item against an official
passage). Labels come from the rule that built each pair and were read against the rebuilt texts by
claude-opus-5-5 on the operator's delegation of 2026-09-24. They are model labels.

## Results on the final sample [verified]

| Operating point | Precision | Recall | Missed |
| --- | --- | --- | --- |
| Published: MinHash 5-gram Jaccard 0.8 alone | 1.000 | 0.236 | 84 of 110 |
| Published: TF-IDF cosine 0.85 alone | 0.879 | 0.527 | 52 of 110 |
| Published: either stage | 0.879 | 0.527 | 52 of 110 |
| Adopted: Jaccard 0.8, then cosine 0.70 against official text and the same-problem rule within the bank | 1.000 | 0.891 | 12 of 110, all heavy paraphrases of official text |

The other three samples agree: adopted precision 1.000 on every one, recall 0.891, 0.918 and 0.891,
and every miss a heavy paraphrase of an official passage (every listed synonym swapped and the
sentences reordered). Every light edit of official text, every reformatted copy and every reworded
copy of a bank item was caught on all four samples, and no sibling was called a copy.

## What changed and why [verified]

- Stage one stays at Jaccard 0.8 with 256 hashes over word 5-grams. It never raised a false alarm
  on any sample, and it is what catches near-verbatim reuse.
- Stage two against official text tightened from cosine 0.85 to 0.70. Every light edit of official
  text scored at least 0.758, and the 786 signed-off items that were written without sight of
  official text peak at 0.628, so 0.70 blocks the edits and none of the known-original items. The
  point that would hold false negatives at zero, about 0.28 on these samples, would have blocked
  488 of those 786 items at 0.30: that is calculus vocabulary, not copying, so the zero-miss rule of
  04 was not followed for heavy paraphrase. That residual is carried by construction instead: no
  template author or solver was given official text, and `test_no_official_text_served` holds every
  served text under the 25-word anchor-quote cap (the longest shared run in the bank is 21 words, a
  generic sentence about a region revolved about the x-axis in ITM-GEN-08012-11).
- Stage two within the bank compares the problem, not the words. A word vector cannot separate a
  reworded copy from a sibling of the same template with other numbers (siblings reached cosine
  0.985). Two bank items are copies when their stem and figure, without the options, share ordered
  math-token pairs at Jaccard 0.80 or more and their numbers at 0.95 or more; two items with no
  mathematics fall back to the word cosine at 0.85. On the real candidates the first version of this
  rule, over the whole record at 0.80 without the numbers condition, held 191 of 2,365 candidates,
  most of them siblings sharing boilerplate; with the numbers condition 39 same-archetype pairs were
  flagged in the whole bank, and the ones read were true copies (the same function with only the
  units changed).
- The stage-two stand-in is a local TF-IDF vector over word unigrams and bigrams, not an embedding:
  the project allows no non-Anthropic provider and no model download, and Anthropic has no
  embeddings endpoint.

The gate is `app/generation/dedupe.py`; its tests are `tests/generation/test_dedupe.py`,
`tests/generation/test_duplicate_gate_labelled.py` (test_minhash_threshold and the labelled
evaluation) and `tests/generation/test_no_official_text.py`.
