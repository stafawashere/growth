"""The two-stage duplicate gate, app/generation/dedupe.py.

Official text is read from cache/text at run time and edited in memory; no official wording is
written into this file.
"""
import pytest

from app.generation import dedupe

SYNONYMS = {
   "find": "determine",
   "value": "amount",
   "function": "map",
   "graph": "plot",
   "approximate": "estimate",
   "interval": "range",
   "given": "stated",
   "shown": "displayed",
}

FOREIGN_WORDS = ["zebra", "quokka", "marmot"]

BANK_STEM = (
   "A cylindrical water tower drains through a valve at its base so that the depth of water, in "
   "meters, satisfies a differential equation in which the rate of change of depth is proportional "
   "to the square root of the depth. At noon the depth is 9 meters and it is falling at 0.6 meters "
   "per hour. Using separation of variables, determine the time at which the tower is empty and "
   "the depth two hours after noon."
)

DISTINCT_STEM = (
   "Let g be the function defined by g(x) = x^3 - 6x^2 + 9x + 2 on the closed interval from 0 to 5. "
   "At which value of x does g attain its absolute minimum on that interval?"
)


def item(item_id, text):
   return {"id": item_id, "stem": {"text": text}, "options": []}


def substitute_words(tokens, positions):
   edited = list(tokens)

   for foreign_word, position in zip(FOREIGN_WORDS, positions):
      edited[position] = foreign_word

   return edited


def reorder_and_swap(tokens, clause_length=16, swap_limit=2):
   clauses = [tokens[start:start + clause_length] for start in range(0, len(tokens), clause_length)]
   reordered = [word for clause in reversed(clauses) for word in clause]
   swaps_made = 0

   for position, word in enumerate(reordered):
      can_swap = word in SYNONYMS and swaps_made < swap_limit

      if can_swap:
         reordered[position] = SYNONYMS[word]
         swaps_made += 1

   return reordered, swaps_made


def swappable_word_count(tokens):
   return sum(1 for word in tokens if word in SYNONYMS)


@pytest.fixture(scope="module")
def official_pages():
   return dedupe.load_official_pages()


def is_long_primary_frq_page(page):
   is_free_response = page.doc_id.startswith("frq-")
   is_primary_text = page.variant == ""
   is_long_enough = len(page.tokens) >= 260

   return is_free_response and is_primary_text and is_long_enough


def long_primary_frq_pages(official_pages):
   return [page for page in official_pages if is_long_primary_frq_page(page)]


@pytest.fixture(scope="module")
def source_page(official_pages):
   candidate_pages = long_primary_frq_pages(official_pages)
   assert candidate_pages, "no cached free-response page has 260 tokens"

   return candidate_pages[0]


@pytest.fixture(scope="module")
def paraphrase_page(official_pages):
   candidate_pages = [
      page for page in long_primary_frq_pages(official_pages)
      if swappable_word_count(page.tokens[60:140]) >= 2
   ]
   assert candidate_pages, "no cached free-response page has two swappable words in tokens 60 to 140"

   return candidate_pages[0]


@pytest.fixture(scope="module")
def gate(official_pages):
   bank_records = [item("ITM-TEST-BANK-00", BANK_STEM), item("ITM-TEST-DISTINCT-00", DISTINCT_STEM)]
   return dedupe.DuplicateGate(official_pages, bank_records)


def test_minhash_estimate_tracks_exact_jaccard():
   base_tokens = [f"token{index}" for index in range(260)]

   for shift in (0, 10, 22, 50, 100, 150):
      shingles_a = dedupe.shingles(base_tokens[:204])
      shingles_b = dedupe.shingles(base_tokens[shift:204 + shift])
      exact = dedupe.exact_jaccard(shingles_a, shingles_b)
      signature_a = dedupe.minhash_signature(shingles_a)
      signature_b = dedupe.minhash_signature(shingles_b)
      estimate = dedupe.estimated_jaccard(signature_a, signature_b)

      assert len(signature_a) == dedupe.NUM_HASHES
      assert abs(estimate - exact) <= 0.1, f"shift {shift}: estimate {estimate:.3f}, exact {exact:.3f}"

      at_threshold = exact >= dedupe.JACCARD_THRESHOLD

      if at_threshold:
         shared_band_keys = set(dedupe.lsh_band_keys(signature_a)) & set(dedupe.lsh_band_keys(signature_b))
         assert shared_band_keys, f"shift {shift}: a pair at Jaccard {exact:.3f} shares no LSH bucket"


def test_duplicate_gate_blocks(gate, source_page, paraphrase_page):
   copied_span = source_page.tokens[30:230]
   light_edit = substitute_words(copied_span, [50, 100, 150])
   light_edit_jaccard = dedupe.exact_jaccard(dedupe.shingles(copied_span), dedupe.shingles(light_edit))
   light_edit_verdict = gate.check(item("ITM-TEST-EDIT-00", " ".join(light_edit)))

   assert light_edit_jaccard >= dedupe.JACCARD_THRESHOLD
   assert light_edit_verdict.stage_one.hit, light_edit_verdict
   assert light_edit_verdict.stage_one.corpus == "official"
   assert light_edit_verdict.stage_one.neighbour.startswith(source_page.page_id + "#")
   assert light_edit_verdict.blocked

   paraphrased_span = paraphrase_page.tokens[60:140]
   paraphrase, swaps_made = reorder_and_swap(paraphrased_span)
   paraphrase_jaccard = dedupe.exact_jaccard(dedupe.shingles(paraphrased_span), dedupe.shingles(paraphrase))
   paraphrase_verdict = gate.check(item("ITM-TEST-PARA-00", " ".join(paraphrase)))

   assert swaps_made == 2
   assert paraphrase_jaccard < dedupe.JACCARD_THRESHOLD
   assert paraphrase_verdict.stage_one.score < dedupe.JACCARD_THRESHOLD, paraphrase_verdict
   assert not paraphrase_verdict.stage_one.hit
   assert paraphrase_verdict.stage_two.hit, paraphrase_verdict
   assert paraphrase_verdict.stage_two.corpus == "official"
   assert paraphrase_verdict.stage_two.neighbour.startswith(paraphrase_page.page_id + "#")
   assert paraphrase_verdict.blocked

   bank_tokens = dedupe.normalise(BANK_STEM)
   bank_edit = substitute_words(bank_tokens, [40])
   bank_edit_verdict = gate.check(item("ITM-TEST-BANK-01", " ".join(bank_edit)))

   assert bank_edit_verdict.stage_one.hit, bank_edit_verdict
   assert bank_edit_verdict.stage_one.neighbour == "ITM-TEST-BANK-00"

   distinct_verdict = gate.check(item("ITM-TEST-DISTINCT-00", DISTINCT_STEM))
   bank_member_verdict = gate.check(item("ITM-TEST-BANK-00", BANK_STEM))

   assert not distinct_verdict.blocked, distinct_verdict
   assert not bank_member_verdict.blocked, bank_member_verdict
