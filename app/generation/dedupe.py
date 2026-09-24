"""Two-stage duplicate and copyright gate for generated items.

docs/plan/04-item-generation.md, "Duplicate and copyright gate", and rejection rules 10 to 12.
The gate runs against two corpora: the official text cache under cache/text (every page variant,
.txt, .raw.txt and .ocr.txt, of every document the manifest marks ok) and the rest of the item
bank, never the item itself.

Stage one is word 5-gram shingling at an exact Jaccard threshold of 0.8. Against the bank it uses
a 256-hash MinHash signature with LSH banding (32 bands of 8 rows, so a pair at Jaccard 0.8 lands
in a shared bucket with probability 1 - (1 - 0.8 ** 8) ** 32, about 0.997) and confirms every
candidate with the exact Jaccard of the shingle sets. Against the official corpus the unit is a
question-sized span, so the gate slides a window as long as the item across every page that
shares enough shingles with it. Candidate pages come from a shingle inverted index instead of
LSH: a window reaches Jaccard t only if it shares at least t times the item's shingle count, so
the filter is exact and loses nothing, where MinHash signatures over every sliding window of a
million-token cache would cost minutes and still miss some pairs.

Stage two is a lexical TF-IDF vector standing in for the embedding. The plan names an embedding
cosine at 0.85, but no embedding model may be used here: the project allows no non-Anthropic
provider and no model downloads, and Anthropic offers no embeddings endpoint. The vector is TF-IDF
over word unigrams and bigrams of the normalised tokens, with idf fitted on the official passages
and the bank together. It sees reordered clauses and swapped words that break 5-gram shingles, but
it has no notion of meaning, so a paraphrase in different words passes it where an embedding might
not.

Stage two's operating points were set on the labelled samples in docs/operator/duplicate-gate/,
as 04 requires, and differ by corpus. Against official text the cosine threshold is 0.70, tighter
than the published 0.85: every lightly edited official passage in the samples scored 0.759 or more,
and the 786 signed-off items, written without sight of official text, peak at 0.628, so 0.70 blocks
every light edit and none of the known-original items. The zero-miss point for heavy paraphrase,
0.385, would have blocked 488 of those 786 items, which is calculus vocabulary and not copying.
Within the bank a word vector cannot tell a reworded copy of an item from a sibling of the same
template with other numbers (siblings reached cosine 0.958), so the bank half of stage two compares
the problem itself, the stem and the figure without the options: two items are near duplicates when
the multiset of ordered token pairs inside their math segments, plus the numbers and signs of each
prose sentence, matches at Jaccard 0.80 or more and their numbers match at 0.95 or more. Every
reworded copy in the samples scored 1.0 on both and no sibling passed both; on the real bank the
first form of this check, over the whole record text at 0.80, held 191 of 2,365 candidates, most of
them siblings whose statement options or long stems share boilerplate, and the numbers condition is
what removed them.

Rule 12 is the copyright span check: the longest run of consecutive words an item shares with any
official page, blocked above the 25-word anchor-quote cap.
"""
import hashlib
import json
import math
import random
import re
from array import array
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CACHE_TEXT_DIR = ROOT / "cache" / "text"
MANIFEST_PATH = ROOT / "cache" / "manifest.json"
CONTENT_DIR = ROOT / "content"

JACCARD_THRESHOLD = 0.8
COSINE_THRESHOLD = 0.85
OFFICIAL_COSINE_THRESHOLD = 0.70
BANK_MATH_THRESHOLD = 0.80
BANK_NUMBER_THRESHOLD = 0.95
NUMBER = re.compile(r"-?\d+(?:\.\d+)?")
MATH_SEGMENT = re.compile(r"\\\((.*?)\\\)", re.S)
SENTENCE_END = re.compile(r"(?<=[.?!])\s+")
PROSE_MATH_TOKEN = re.compile(r"^(\d+(\.\d+)?|[-+=<>^/])$")
NUM_HASHES = 256
SHINGLE_SIZE = 5
LSH_BANDS = 32
LSH_ROWS = 8
PASSAGE_SIZE = 80
PASSAGE_STRIDE = 40
ANCHOR_QUOTE_CAP = 25
COSINE_RECALL_FLOOR = 0.5
COSINE_TAIL_NORM_LIMIT = 0.3
MINHASH_SEED = 20260924
MERSENNE_PRIME = (1 << 61) - 1

POSITIVE_LABELS = ("duplicate", "near_duplicate")
ALL_LABELS = ("duplicate", "near_duplicate", "distinct")

LATEX_COMMAND = re.compile(r"\\([a-z]+)")
WORD_TOKEN = re.compile(r"[a-z]+|\d+(?:\.\d+)?|[-+=<>^/]")
PAGE_FILE = re.compile(r"^page-(\d+)(\.raw|\.ocr)?\.txt$")


def normalise(text):
   """Lowercase, turn LaTeX commands into their bare names, and split into word tokens.

   Punctuation, braces and math delimiters drop out, so \\( \\frac{75}{2} \\) becomes
   frac, 75, 2. Numbers keep their decimal point, and the operator signs stay as tokens, because
   e^{x} and e^{-x} are two different items.
   """
   lowered = (text or "").lower()
   commands_as_words = LATEX_COMMAND.sub(r" \1 ", lowered)
   return WORD_TOKEN.findall(commands_as_words)


def shingle_hash(words):
   digest = hashlib.blake2b(" ".join(words).encode(), digest_size=8).digest()
   return int.from_bytes(digest, "big")


def shingle_sequence(tokens, size=SHINGLE_SIZE):
   """Hashes of every word n-gram in order. A text shorter than n is one shingle."""
   if not tokens:
      return []

   if len(tokens) < size:
      return [shingle_hash(tokens)]

   return [shingle_hash(tokens[start:start + size]) for start in range(len(tokens) - size + 1)]


def shingles(tokens, size=SHINGLE_SIZE):
   return set(shingle_sequence(tokens, size))


def exact_jaccard(shingles_a, shingles_b):
   union_size = len(shingles_a | shingles_b)

   if union_size == 0:
      return 0.0

   return len(shingles_a & shingles_b) / union_size


def minhash_coefficients(num_hashes=NUM_HASHES, seed=MINHASH_SEED):
   generator = random.Random(seed)
   return [(generator.randrange(1, MERSENNE_PRIME), generator.randrange(0, MERSENNE_PRIME)) for _ in range(num_hashes)]


MINHASH_COEFFICIENTS = minhash_coefficients()


def minhash_signature(shingle_set, coefficients=MINHASH_COEFFICIENTS):
   """One minimum per hash of the universal family (a * x + b) mod (2 ** 61 - 1)."""
   if not shingle_set:
      return [MERSENNE_PRIME] * len(coefficients)

   values = list(shingle_set)
   return [min((multiplier * value + offset) % MERSENNE_PRIME for value in values) for multiplier, offset in coefficients]


def estimated_jaccard(signature_a, signature_b):
   agreeing = sum(1 for value_a, value_b in zip(signature_a, signature_b) if value_a == value_b)
   return agreeing / len(signature_a)


def lsh_band_keys(signature, bands=LSH_BANDS, rows=LSH_ROWS):
   return [(band, tuple(signature[band * rows:(band + 1) * rows])) for band in range(bands)]


def lsh_candidate_probability(jaccard, bands=LSH_BANDS, rows=LSH_ROWS):
   return 1 - (1 - jaccard ** rows) ** bands


def longest_common_span(tokens_a, tokens_b):
   """Longest run of consecutive words shared by two token lists, as (length, start_a, start_b)."""
   best = (0, 0, 0)
   previous_row = [0] * (len(tokens_b) + 1)

   for index_a, word_a in enumerate(tokens_a):
      current_row = [0] * (len(tokens_b) + 1)

      for index_b, word_b in enumerate(tokens_b):
         if word_a != word_b:
            continue

         run_length = previous_row[index_b] + 1
         current_row[index_b + 1] = run_length

         if run_length > best[0]:
            best = (run_length, index_a - run_length + 1, index_b - run_length + 1)

      previous_row = current_row

   return best


@dataclass
class OfficialPage:
   doc_id: str
   page_number: int
   variant: str
   tokens: list

   @property
   def page_id(self):
      return f"{self.doc_id}/page-{self.page_number:03d}{self.variant}"


@dataclass
class Passage:
   passage_id: str
   tokens: list
   page_index: int = None


def official_doc_ids(manifest_path=MANIFEST_PATH):
   manifest = json.loads(Path(manifest_path).read_text())
   return sorted(doc_id for doc_id, entry in manifest.items() if entry.get("status") == "ok")


def load_official_pages(cache_text_dir=CACHE_TEXT_DIR, manifest_path=MANIFEST_PATH):
   """Every cached page variant of every official document, tokenised."""
   pages = []

   for doc_id in official_doc_ids(manifest_path):
      doc_dir = Path(cache_text_dir) / doc_id

      if not doc_dir.is_dir():
         continue

      for page_path in sorted(doc_dir.iterdir()):
         name_match = PAGE_FILE.match(page_path.name)

         if not name_match:
            continue

         page_number = int(name_match.group(1))
         variant = name_match.group(2) or ""
         tokens = normalise(page_path.read_text(errors="ignore"))
         pages.append(OfficialPage(doc_id, page_number, variant, tokens))

   return pages


def segment_passages(pages, size=PASSAGE_SIZE, stride=PASSAGE_STRIDE):
   """Overlapping question-sized windows over each page, named doc/page-NNN[.variant]#offset."""
   passages = []

   for page_index, page in enumerate(pages):
      if not page.tokens:
         continue

      last_start = max(len(page.tokens) - size, 0)
      starts = list(range(0, last_start + 1, stride))

      if starts[-1] != last_start:
         starts.append(last_start)

      for start in starts:
         passages.append(Passage(f"{page.page_id}#{start}", page.tokens[start:start + size], page_index))

   return passages


def option_texts(record):
   texts = []

   for option in record.get("options") or []:
      option_text = option.get("label") or option.get("text")

      if isinstance(option_text, str):
         texts.append(option_text)

   return texts


def figure_text(record):
   """What a figure shows in words: its description and a table's cells, so two items whose
   stems match but whose figures differ are told apart."""
   figure = record.get("figure") or {}
   parts = [figure.get("alt") or ""]
   parts.extend(str(column) for column in figure.get("columns") or [])

   for row in figure.get("rows") or []:
      parts.extend(str(cell) for cell in row)

   return " ".join(part for part in parts if part)


def record_text(record):
   """The text the duplicate stages compare: the stem, the figure's content and any text option
   labels."""
   stem_text = (record.get("stem") or {}).get("text") or ""
   return " ".join(part for part in [stem_text, figure_text(record)] + option_texts(record) if part)


def served_texts(record):
   """Every piece of text the app shows for a record, as (field, text) pairs."""
   fields = [("stem", (record.get("stem") or {}).get("text") or "")]

   for option in record.get("options") or []:
      option_text = option.get("label") or option.get("text")

      if isinstance(option_text, str):
         fields.append((f"option {option.get('id')}", option_text))

   figure = record.get("figure") or {}
   figure_words = figure_text(record)

   if figure_words:
      fields.append(("figure", figure_words))

   for label in figure.get("labels") or []:
      if isinstance(label.get("text"), str):
         fields.append(("figure label", label["text"]))

   for step in record.get("worked_solution") or []:
      step_text = step.get("text")

      if isinstance(step_text, str):
         fields.append((f"worked_solution step {step.get('step')}", step_text))

   return fields


def load_bank_records(content_dir=CONTENT_DIR):
   records = []

   for record_path in sorted(Path(content_dir).glob("items_*/*.json")):
      records.append(json.loads(record_path.read_text()))

   return records


def math_pairs(text):
   """The item's mathematics as a multiset of ordered token pairs: every pair inside each math
   segment, and the numbers and signs of each prose sentence in order. A rewording keeps them all,
even with its sentences reordered; another
   draw of the same template changes the pairs its numbers sit in."""
   pairs = Counter()

   for segment in MATH_SEGMENT.findall(text or ""):
      tokens = normalise(segment)
      pairs.update(zip(tokens, tokens[1:]) if len(tokens) > 1 else [tuple(tokens)])

   prose_text = MATH_SEGMENT.sub(" ", text or "")

   for sentence in SENTENCE_END.split(prose_text):
      prose = [token for token in normalise(sentence) if PROSE_MATH_TOKEN.match(token)]
      pairs.update(zip(prose, prose[1:]))

   return pairs


def problem_text(record):
   """The problem a student is set: the stem and the figure, without the options, which repeat
   the same reasoning across draws of a statement template."""
   stem_text = (record.get("stem") or {}).get("text") or ""

   return " ".join(part for part in (stem_text, figure_text(record)) if part)


def numbers(text):
   return Counter(NUMBER.findall((text or "").replace(" ", "")))


def number_agreement(numbers_a, numbers_b):
   """Jaccard of two number multisets, and full agreement when neither text has a number."""
   neither_has_numbers = not numbers_a and not numbers_b

   if neither_has_numbers:
      return 1.0

   return multiset_jaccard(numbers_a, numbers_b)


def multiset_jaccard(counts_a, counts_b):
   union = sum((counts_a | counts_b).values())

   if union == 0:
      return 0.0

   return sum((counts_a & counts_b).values()) / union


def tfidf_terms(tokens):
   bigrams = [f"{first} {second}" for first, second in zip(tokens, tokens[1:])]
   return tokens + bigrams


class TfidfModel:
   """Lexical TF-IDF over word unigrams and bigrams, the local stand-in for an embedding."""

   def __init__(self, token_lists):
      document_frequency = Counter()

      for tokens in token_lists:
         document_frequency.update(set(tfidf_terms(tokens)))

      self.document_count = len(token_lists)
      self.term_ids = {}
      self.idf = array("d")

      for term, frequency in document_frequency.items():
         self.term_ids[term] = len(self.idf)
         self.idf.append(math.log((1 + self.document_count) / (1 + frequency)) + 1)

      self.unseen_idf = math.log(1 + self.document_count) + 1

   def vector(self, tokens):
      """A unit-length sparse vector as {term id: weight}. Unseen terms count toward the norm only."""
      term_counts = Counter(tfidf_terms(tokens))
      weights = {}
      unseen_square_sum = 0.0

      for term, count in term_counts.items():
         term_id = self.term_ids.get(term)

         if term_id is None:
            unseen_square_sum += (count * self.unseen_idf) ** 2
            continue

         weights[term_id] = count * self.idf[term_id]

      norm = math.sqrt(sum(weight * weight for weight in weights.values()) + unseen_square_sum)

      if norm == 0:
         return {}

      return {term_id: weight / norm for term_id, weight in weights.items()}


def cosine(vector_a, vector_b):
   if len(vector_a) > len(vector_b):
      vector_a, vector_b = vector_b, vector_a

   return sum(weight * vector_b.get(term_id, 0.0) for term_id, weight in vector_a.items())


@dataclass
class StageResult:
   hit: bool
   score: float
   neighbour: str
   corpus: str


@dataclass
class SpanResult:
   hit: bool
   length: int
   neighbour: str


@dataclass
class GateVerdict:
   item_id: str
   stage_one: StageResult
   stage_two: StageResult
   official_span: SpanResult

   @property
   def blocked(self):
      return self.stage_one.hit or self.stage_two.hit or self.official_span.hit

   @property
   def rejection_rules(self):
      rules = []

      if self.stage_one.hit:
         rules.append(10)

      if self.stage_two.hit:
         rules.append(11)

      if self.official_span.hit:
         rules.append(12)

      return rules


def better_stage_result(current, candidate):
   if current is None or candidate.score > current.score:
      return candidate

   return current


class OfficialShingleIndex:
   """Every official page's shingle sequence and token ids, with shingle to position postings."""

   def __init__(self, pages):
      self.pages = [page for page in pages if page.tokens]
      self.vocabulary = {}
      self.corpus_tokens = array("i")
      self.position_page = array("i")
      self.page_starts = []
      self.page_shingles = []
      self.postings = {}

      for page_index, page in enumerate(self.pages):
         page_start = len(self.corpus_tokens)
         self.page_starts.append(page_start)

         for word in page.tokens:
            self.corpus_tokens.append(self.vocabulary.setdefault(word, len(self.vocabulary)))
            self.position_page.append(page_index)

         self.corpus_tokens.append(-1)
         self.position_page.append(page_index)

         sequence = shingle_sequence(page.tokens)
         self.page_shingles.append(sequence)

         for offset, shingle in enumerate(sequence):
            self.postings.setdefault(shingle, array("q")).append(page_start + offset)

   def token_ids(self, tokens):
      return [self.vocabulary.get(word, -2) for word in tokens]

   def shared_shingle_counts(self, item_shingles):
      counts = Counter()

      for shingle in item_shingles:
         positions = self.postings.get(shingle)

         if positions is None:
            continue

         counts.update({self.position_page[position] for position in positions})

      return counts

   def best_window(self, item_shingles, page_index, window_lengths):
      """Highest exact Jaccard between the item and any window of the page, with its start."""
      sequence = self.page_shingles[page_index]
      item_size = len(item_shingles)
      best_score = 0.0
      best_start = 0

      for window_length in window_lengths:
         window_length = max(1, min(window_length, len(sequence)))
         window_counts = {}
         shared = 0

         for position, shingle in enumerate(sequence):
            previous_count = window_counts.get(shingle, 0)
            window_counts[shingle] = previous_count + 1
            entering_new_shared = previous_count == 0 and shingle in item_shingles

            if entering_new_shared:
               shared += 1

            if position >= window_length:
               leaving = sequence[position - window_length]
               remaining = window_counts[leaving] - 1

               if remaining == 0:
                  del window_counts[leaving]

                  if leaving in item_shingles:
                     shared -= 1
               else:
                  window_counts[leaving] = remaining

            if position < window_length - 1:
               continue

            union_size = item_size + len(window_counts) - shared
            score = shared / union_size

            if score > best_score:
               best_score = score
               best_start = position - window_length + 1

         if window_length == len(sequence):
            break

      return best_score, best_start

   def best_match(self, item_shingles, threshold=JACCARD_THRESHOLD):
      """Best question-sized window over the corpus. Every page that could reach the threshold is scanned."""
      item_size = len(item_shingles)

      if item_size == 0:
         return StageResult(False, 0.0, None, "official")

      shared_counts = self.shared_shingle_counts(item_shingles)

      if not shared_counts:
         return StageResult(False, 0.0, None, "official")

      required_shared = math.ceil(threshold * item_size)
      qualifying_pages = [page_index for page_index, count in shared_counts.items() if count >= required_shared]
      shortest_window = max(1, math.ceil(threshold * item_size))
      longest_window = max(shortest_window, math.floor(item_size / threshold))
      window_lengths = range(shortest_window, longest_window + 1)

      if not qualifying_pages:
         qualifying_pages = [shared_counts.most_common(1)[0][0]]
         window_lengths = [item_size]

      best = None

      for page_index in qualifying_pages:
         score, start = self.best_window(item_shingles, page_index, window_lengths)
         neighbour = f"{self.pages[page_index].page_id}#{start}"
         best = better_stage_result(best, StageResult(score >= threshold, score, neighbour, "official"))

      return best

   def longest_run(self, tokens):
      """Longest run of consecutive words the tokens share with one official page, as (length, where).

      Runs are found from shared 5-word shingles, so a run shorter than SHINGLE_SIZE reports 0.
      """
      item_ids = self.token_ids(tokens)
      item_shingles = shingle_sequence(tokens)
      best_length = 0
      best_where = None
      is_long_enough = len(tokens) >= SHINGLE_SIZE

      if not is_long_enough:
         return best_length, best_where

      for item_start, shingle in enumerate(item_shingles):
         remaining_length = len(item_ids) - item_start

         if remaining_length <= best_length:
            break

         positions = self.postings.get(shingle)

         if positions is None:
            continue

         for corpus_start in positions:
            extends_leftward = item_start > 0 and self.corpus_tokens[corpus_start - 1] == item_ids[item_start - 1]

            if extends_leftward:
               continue

            run_length = SHINGLE_SIZE

            while run_length < remaining_length:
               next_words_agree = self.corpus_tokens[corpus_start + run_length] == item_ids[item_start + run_length]

               if not next_words_agree:
                  break

               run_length += 1

            if run_length > best_length:
               page_index = self.position_page[corpus_start]
               offset = corpus_start - self.page_starts[page_index]
               best_length = run_length
               best_where = f"{self.pages[page_index].page_id}#{offset}"

      return best_length, best_where


class DuplicateGate:
   """Both duplicate stages and the copyright span check over the official cache and the bank.

   Built once from the official pages and the bank records; check(record) scores one record
   against every official page and every bank record other than itself.
   """

   def __init__(self, official_pages, bank_records, passage_size=PASSAGE_SIZE, passage_stride=PASSAGE_STRIDE):
      self.official_index = OfficialShingleIndex(official_pages)
      self.passages = segment_passages(self.official_index.pages, passage_size, passage_stride)
      self.bank_ids = []
      self.bank_shingles = []
      self.bank_signatures = []
      self.bank_math = []
      self.bank_numbers = []
      self.math_postings = {}
      self.lsh_buckets = {}
      bank_tokens = []

      for record in bank_records:
         tokens = normalise(record_text(record))
         shingle_set = shingles(tokens)
         signature = minhash_signature(shingle_set)
         bank_index = len(self.bank_ids)
         self.bank_ids.append(record["id"])
         self.bank_shingles.append(shingle_set)
         self.bank_signatures.append(signature)
         bank_tokens.append(tokens)
         problem = problem_text(record)
         math_counts = math_pairs(problem)
         self.bank_math.append(math_counts)
         self.bank_numbers.append(numbers(problem))

         for math_pair in math_counts:
            self.math_postings.setdefault(math_pair, []).append(bank_index)

         for band_key in lsh_band_keys(signature):
            self.lsh_buckets.setdefault(band_key, []).append(bank_index)

      passage_tokens = [passage.tokens for passage in self.passages]
      self.tfidf = TfidfModel(passage_tokens + bank_tokens)
      self.vector_names = [passage.passage_id for passage in self.passages] + self.bank_ids
      self.vector_corpora = ["official"] * len(self.passages) + ["bank"] * len(self.bank_ids)
      self.vectors = []
      self.term_postings = {}

      for tokens in passage_tokens + bank_tokens:
         vector = self.tfidf.vector(tokens)
         vector_index = len(self.vectors)
         self.vectors.append(vector)

         for term_id, weight in vector.items():
            posting = self.term_postings.get(term_id)

            if posting is None:
               posting = (array("i"), array("d"))
               self.term_postings[term_id] = posting

            posting[0].append(vector_index)
            posting[1].append(weight)

   @classmethod
   def from_cache(cls, content_dir=CONTENT_DIR, cache_text_dir=CACHE_TEXT_DIR, manifest_path=MANIFEST_PATH):
      return cls(load_official_pages(cache_text_dir, manifest_path), load_bank_records(content_dir))

   def stage_one_bank(self, item_id, item_shingles, signature):
      candidates = set()

      for band_key in lsh_band_keys(signature):
         candidates.update(self.lsh_buckets.get(band_key, ()))

      best = StageResult(False, 0.0, None, "bank")

      for bank_index in candidates:
         if self.bank_ids[bank_index] == item_id:
            continue

         score = exact_jaccard(item_shingles, self.bank_shingles[bank_index])
         candidate = StageResult(score >= JACCARD_THRESHOLD, score, self.bank_ids[bank_index], "bank")
         best = better_stage_result(best, candidate)

      return best

   def page_window_cosine(self, query, page_index, window_length):
      """Highest cosine between the query and any window of the page as long as the item, with its start.

      The window's term counts, its squared norm and its dot product with the query are updated
      one token at a time, so a whole page costs a few operations per position.
      """
      page_tokens = self.official_index.pages[page_index].tokens
      window_length = max(1, min(window_length, len(page_tokens)))
      idf = self.tfidf.idf
      term_ids = self.tfidf.term_ids
      term_counts = {}
      state = {"square_sum": 0.0, "dot": 0.0}

      def adjust(term, change):
         term_id = term_ids.get(term)

         if term_id is None:
            return

         weight = idf[term_id]
         count = term_counts.get(term_id, 0)
         new_count = count + change
         term_counts[term_id] = new_count
         state["square_sum"] += (new_count * new_count - count * count) * weight * weight
         state["dot"] += change * weight * query.get(term_id, 0.0)

      def window_score():
         if state["square_sum"] <= 0:
            return 0.0

         return state["dot"] / math.sqrt(state["square_sum"])

      for position in range(window_length):
         adjust(page_tokens[position], 1)

         if position > 0:
            adjust(f"{page_tokens[position - 1]} {page_tokens[position]}", 1)

      best_score = window_score()
      best_start = 0

      for start in range(1, len(page_tokens) - window_length + 1):
         adjust(page_tokens[start - 1], -1)
         adjust(f"{page_tokens[start - 1]} {page_tokens[start]}", -1)
         end = start + window_length - 1
         adjust(page_tokens[end], 1)
         adjust(f"{page_tokens[end - 1]} {page_tokens[end]}", 1)
         score = window_score()

         if score > best_score:
            best_score = score
            best_start = start

      return best_score, best_start

   def stage_two(self, item_id, tokens):
      """Best cosine over official spans and bank records. Every neighbour at or above COSINE_RECALL_FLOOR is found.

      Query terms are taken heaviest first until the rest of the query has norm below
      COSINE_TAIL_NORM_LIMIT, and their postings give each vector a partial dot product. The rest
      can add at most its own norm, so a vector whose partial plus that norm is under the floor is
      skipped, and only the survivors get a full cosine.

      A fixed passage grid would let a span that straddles two passages score low, so every page
      holding a passage at or above the floor, and the page of the best passage, is then scanned
      with a window exactly as long as the item.
      """
      query = self.tfidf.vector(tokens)
      ordered_terms = sorted(query, key=query.get, reverse=True)
      tail_square_sum = sum(weight * weight for weight in query.values())
      partial_dots = {}

      for term_id in ordered_terms:
         if tail_square_sum < COSINE_TAIL_NORM_LIMIT ** 2:
            break

         query_weight = query[term_id]
         tail_square_sum -= query_weight * query_weight
         posting = self.term_postings.get(term_id)

         if posting is None:
            continue

         for vector_index, vector_weight in zip(*posting):
            partial_dots[vector_index] = partial_dots.get(vector_index, 0.0) + query_weight * vector_weight

      tail_norm = math.sqrt(max(tail_square_sum, 0.0))
      survivor_floor = COSINE_RECALL_FLOOR - tail_norm
      best = StageResult(False, 0.0, None, None)
      pages_to_scan = set()
      best_passage_score = 0.0
      best_passage_page = None

      for vector_index, partial_dot in partial_dots.items():
         cannot_reach_floor = partial_dot < survivor_floor
         is_bank_vector = vector_index >= len(self.passages)

         if cannot_reach_floor or is_bank_vector:
            continue

         score = cosine(query, self.vectors[vector_index])
         candidate = StageResult(score >= OFFICIAL_COSINE_THRESHOLD, score, self.vector_names[vector_index], "official")
         best = better_stage_result(best, candidate)
         is_passage = vector_index < len(self.passages)

         if not is_passage:
            continue

         page_index = self.passages[vector_index].page_index
         reaches_floor = score >= COSINE_RECALL_FLOOR
         beats_best_page = score > best_passage_score

         if reaches_floor:
            pages_to_scan.add(page_index)

         if beats_best_page:
            best_passage_score = score
            best_passage_page = page_index

      if best_passage_page is not None:
         pages_to_scan.add(best_passage_page)

      for page_index in pages_to_scan:
         score, start = self.page_window_cosine(query, page_index, len(tokens))
         neighbour = f"{self.official_index.pages[page_index].page_id}#{start}"
         best = better_stage_result(best, StageResult(score >= OFFICIAL_COSINE_THRESHOLD, score, neighbour, "official"))

      return best

   def stage_two_bank(self, item_id, problem, record_text_for_vector=""):
      """The bank half of stage two: the same mathematics and the same numbers, however worded.
      Two items with no mathematics at all, plain-text stems, fall back to the word cosine at the
      published 0.85."""
      item_math = math_pairs(problem)
      item_numbers = numbers(problem)
      item_vector = self.tfidf.vector(normalise(record_text_for_vector))
      candidates = set()

      for math_pair in item_math:
         candidates.update(self.math_postings.get(math_pair, ()))

      if not item_math:
         candidates.update(index for index, counts in enumerate(self.bank_math) if not counts)

      best = StageResult(False, 0.0, None, "bank")

      for bank_index in candidates:
         if self.bank_ids[bank_index] == item_id:
            continue

         math_score = multiset_jaccard(item_math, self.bank_math[bank_index])
         neither_has_mathematics = not item_math and not self.bank_math[bank_index]

         if neither_has_mathematics:
            math_score = cosine(item_vector, self.vectors[len(self.passages) + bank_index])
            math_score = 1.0 if math_score >= COSINE_THRESHOLD else math_score
         number_score = number_agreement(item_numbers, self.bank_numbers[bank_index])
         same_mathematics = math_score >= BANK_MATH_THRESHOLD
         same_numbers = number_score >= BANK_NUMBER_THRESHOLD
         is_near_duplicate = same_mathematics and same_numbers
         candidate = StageResult(is_near_duplicate, math_score, self.bank_ids[bank_index], "bank")
         finds_first_hit = is_near_duplicate and not best.hit
         outscores_its_kind = is_near_duplicate == best.hit and math_score > best.score

         if finds_first_hit or outscores_its_kind:
            best = candidate

      return best

   def check(self, record):
      item_id = record.get("id")
      tokens = normalise(record_text(record))
      item_shingles = shingles(tokens)
      signature = minhash_signature(item_shingles)

      official_result = self.official_index.best_match(item_shingles)
      bank_result = self.stage_one_bank(item_id, item_shingles, signature)
      stage_one = better_stage_result(official_result, bank_result)

      official_two = self.stage_two(item_id, tokens)
      bank_two = self.stage_two_bank(item_id, problem_text(record), record_text(record))
      stage_two = official_two if official_two.hit or not bank_two.hit else bank_two

      run_length, run_where = self.official_index.longest_run(tokens)
      official_span = SpanResult(run_length > ANCHOR_QUOTE_CAP, run_length, run_where)

      return GateVerdict(item_id, stage_one, stage_two, official_span)


def pair_score(text_a, text_b, stage, model=None):
   """Stage one scores exact 5-gram Jaccard; stage two scores TF-IDF cosine under the given model."""
   tokens_a = normalise(text_a)
   tokens_b = normalise(text_b)

   if stage in (1, "jaccard"):
      return exact_jaccard(shingles(tokens_a), shingles(tokens_b))

   if stage in (2, "cosine"):
      return cosine(model.vector(tokens_a), model.vector(tokens_b))

   raise ValueError(f"unknown stage {stage!r}")


def precision_recall(pairs, labels, stage, threshold, model=None):
   """Score one stage at one threshold on a labelled sample of (text_a, text_b) pairs.

   Labels are duplicate, near_duplicate or distinct, and the first two are positives the gate must
   block. The plan sets thresholds where false negatives are zero, so they are returned by index.
   For stage two with no model, idf is fitted on the sample's own texts.
   """
   if len(pairs) != len(labels):
      raise ValueError("pairs and labels differ in length")

   unknown_labels = sorted(set(labels) - set(ALL_LABELS))

   if unknown_labels:
      raise ValueError(f"unknown labels {unknown_labels}")

   needs_model = stage in (2, "cosine") and model is None

   if needs_model:
      model = TfidfModel([normalise(text) for pair in pairs for text in pair])

   counts = Counter()
   false_negatives = []
   false_positives = []
   scores = []

   for pair_index, ((text_a, text_b), label) in enumerate(zip(pairs, labels)):
      score = pair_score(text_a, text_b, stage, model)
      is_positive = label in POSITIVE_LABELS
      is_flagged = score >= threshold
      scores.append(score)

      if is_positive and is_flagged:
         counts["true_positive"] += 1
      elif is_positive:
         counts["false_negative"] += 1
         false_negatives.append(pair_index)
      elif is_flagged:
         counts["false_positive"] += 1
         false_positives.append(pair_index)
      else:
         counts["true_negative"] += 1

   flagged_count = counts["true_positive"] + counts["false_positive"]
   positive_count = counts["true_positive"] + counts["false_negative"]

   return {
      "stage": stage,
      "threshold": threshold,
      "precision": counts["true_positive"] / flagged_count if flagged_count else None,
      "recall": counts["true_positive"] / positive_count if positive_count else None,
      "true_positive": counts["true_positive"],
      "false_positive": counts["false_positive"],
      "false_negative": counts["false_negative"],
      "true_negative": counts["true_negative"],
      "false_negative_indices": false_negatives,
      "false_positive_indices": false_positives,
      "scores": scores,
   }
