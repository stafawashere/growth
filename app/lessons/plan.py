"""plan_lesson, the one function that decides what a lesson serves: docs/plan/15-lessons.md,
Adaptation to the student and Re-teaching.

The function is pure. It reads a lesson record (schemas/lesson.schema.json), a band, a reason and
the ids the diagnosis produced, and returns the ordered sections, the checks, the minutes, the
reason and the anchors. It reads no database and no clock, so the same inputs give the same plan
(invariant L13).
"""
import math
from dataclasses import asdict, dataclass

from app.lessons import constants

FIRST_CONTACT = "first_contact"
FEEDBACK = "feedback"
READ_AGAIN = "read_again"
REFRESHER_REASONS = ("T1", "T2", "T3", "T4", "T5")
REASONS = (FIRST_CONTACT, FEEDBACK, READ_AGAIN) + REFRESHER_REASONS

FULL = "full"
STEPS_ONLY = "steps_only"

CHECK = "check"
PREDICTION = "prediction"
ORIENTATION = "orientation"
KEY_IDEAS = "key_ideas"
STRATEGY = "strategy"
WORKED_EXAMPLE = "worked_example"
READER_SCORES = "what_a_reader_scores"
COMMON_ERROR = "common_error"
REPRESENTATIONS = "representations"
PREREQUISITE_BRIDGE = "prerequisite_bridge"

PROSE_FIELDS = {
   PREDICTION: ("stem.text", "options[].label", "resolution.text"),
   ORIENTATION: ("text",),
   KEY_IDEAS: ("text", "notation", "quote.text"),
   STRATEGY: (
      "cue",
      "method",
      "rival",
      "separating_feature",
      "contrast.this.text",
      "contrast.not_this.text",
      "contrast.not_this.why_not",
      "contrast.feature",
   ),
   WORKED_EXAMPLE: ("problem.text", "steps[].cue", "steps[].why"),
   READER_SCORES: ("lines[].text",),
   COMMON_ERROR: (
      "observed_behavior",
      "scoring_consequence",
      "wrong_step.text",
      "right_step.text",
      "possible_reason.text",
   ),
   REPRESENTATIONS: ("text",),
   PREREQUISITE_BRIDGE: ("text",),
   CHECK: ("stem.text",),
}

FIRST_CONTACT_REQUIRED_TYPES = (
   PREDICTION,
   ORIENTATION,
   PREREQUISITE_BRIDGE,
   KEY_IDEAS,
   STRATEGY,
   COMMON_ERROR,
)


@dataclass(frozen=True)
class SectionRef:
   id: str
   type: str
   form: str = FULL


@dataclass(frozen=True)
class LessonPlan:
   lesson_id: str
   version: int
   band: str
   reason: str
   sections: tuple
   checks: tuple
   minutes: float
   words: int
   anchors: tuple

   def as_dict(self):
      return asdict(self)


def prose_values(node, path):
   """The strings a dotted path with [] for list steps reaches inside a record."""
   head, _, rest = path.partition(".")
   is_list_step = head.endswith("[]")
   key = head[:-2] if is_list_step else head
   child = node.get(key) if isinstance(node, dict) else None

   if child is None:
      return []

   if is_list_step:
      children = child
   else:
      children = [child]

   values = []

   for entry in children:
      if rest:
         values.extend(prose_values(entry, rest))
      elif isinstance(entry, str):
         values.append(entry)

   return values


def section_texts(section):
   paths = PROSE_FIELDS.get(section.get("type"), ())
   texts = []

   for path in paths:
      texts.extend(prose_values(section, path))

   return texts


def section_words(section):
   return sum(len(text.split()) for text in section_texts(section))


def estimate_minutes(words):
   return math.ceil(words / constants.WORDS_PER_MINUTE * 10) / 10


def in_band(record, band):
   return band in record.get("bands", constants.BANDS)


def ordered_unique(values):
   seen = set()
   result = []

   for value in values:
      already_seen = value in seen

      if already_seen:
         continue

      seen.add(value)
      result.append(value)

   return result


class LessonView:
   """Index over one lesson record so the plan rules read as selections."""

   def __init__(self, lesson):
      self.lesson = lesson
      self.sections = list(lesson.get("sections", []))
      self.checks = list(lesson.get("checks", []))
      self.by_id = {record["id"]: record for record in self.sections + self.checks}

   def of_type(self, section_type, band=None):
      records = [section for section in self.sections if section["type"] == section_type]

      if band is None:
         return records

      return [record for record in records if in_band(record, band)]

   def ref(self, section_id, form=FULL):
      record = self.by_id[section_id]
      section_type = record.get("type", CHECK)

      return SectionRef(section_id, section_type, form)

   def scores_for(self, example_id):
      return [
         section
         for section in self.of_type(READER_SCORES)
         if section.get("example_id") == example_id
      ]

   def errors_named(self, error_ids):
      by_error = {section["error_id"]: section for section in self.of_type(COMMON_ERROR)}

      return [by_error[error_id] for error_id in ordered_unique(error_ids) if error_id in by_error]

   def core_key_ideas(self):
      return [section for section in self.of_type(KEY_IDEAS) if section.get("depth") == "core"]


def first_contact_refs(view, band, prerequisite_ids):
   """Plan order for both bands: the prediction, orientation, bridges, key ideas, strategy,
   example 1 with its scoring lines, check 1, the error blocks, example 2 with its scoring lines,
   check 2, representations, check 3."""
   predictions = view.of_type(PREDICTION, band)
   orientation = view.of_type(ORIENTATION, band)
   wanted_bridges = set(prerequisite_ids)
   bridges = [
      section
      for section in view.of_type(PREREQUISITE_BRIDGE)
      if section.get("prerequisite_id") in wanted_bridges
   ]
   key_ideas = view.of_type(KEY_IDEAS, band)
   strategies = view.of_type(STRATEGY, band)
   examples = view.of_type(WORKED_EXAMPLE, band)
   errors = view.of_type(COMMON_ERROR, band)
   representations = view.of_type(REPRESENTATIONS, band)
   checks = [check for check in view.checks if in_band(check, band)]

   is_low = band == "low"

   if is_low:
      errors = errors[:constants.LESSON_COMMON_ERRORS_MAX]
      checks = checks[:constants.LESSON_CHECKS_MAX]
      examples = examples[:constants.WORKED_EXAMPLES_MAX]
   else:
      key_ideas = [section for section in key_ideas if section.get("depth") == "core"]
      strategies = strategies[:1]
      errors = errors[:constants.MID_ERRORS]
      checks = checks[:constants.LESSON_CHECKS_MIN]
      examples = examples[:1]

   sequence = []
   sequence.extend(predictions)
   sequence.extend(orientation)
   sequence.extend(bridges)
   sequence.extend(key_ideas)
   sequence.extend(strategies)

   first_example = examples[:1]
   second_example = examples[1:2]

   for example in first_example:
      sequence.append(example)
      sequence.extend(view.scores_for(example["id"]))

   sequence.extend(checks[:1])
   sequence.extend(errors)

   for example in second_example:
      sequence.append(example)
      sequence.extend(view.scores_for(example["id"]))

   sequence.extend(checks[1:2])
   sequence.extend(representations)
   sequence.extend(checks[2:])

   return [view.ref(record["id"]) for record in sequence]


def fit_first_contact(view, refs, words_cap):
   """Drop the last optional entries until the words fit. Entries that teach the concept stay."""
   first_example = next((r.id for r in refs if r.type == WORKED_EXAMPLE), None)
   first_scores = None
   first_check = next((r.id for r in refs if r.type == CHECK), None)

   for ref in refs:
      is_scores_of_first = ref.type == READER_SCORES and view.by_id[ref.id].get("example_id") == first_example

      if is_scores_of_first:
         first_scores = ref.id

   pinned_ids = {first_example, first_scores, first_check}
   kept = list(refs)

   while ref_words(view, kept) > words_cap:
      droppable = [
         ref
         for ref in kept
         if ref.type not in FIRST_CONTACT_REQUIRED_TYPES and ref.id not in pinned_ids
      ]
      nothing_left_to_drop = len(droppable) == 0

      if nothing_left_to_drop:
         break

      kept.remove(droppable[-1])

   return kept


def ref_words(view, refs):
   return sum(section_words(view.by_id[ref.id]) for ref in refs)


def fit_refresher(view, refs, minutes_cap):
   kept = list(refs)

   while len(kept) > 1 and estimate_minutes(ref_words(view, kept)) > minutes_cap:
      kept.pop()

   return kept


def refresher_pointer_refs(view):
   return [view.ref(pointer) for pointer in view.lesson.get("refresher", []) if pointer in view.by_id]


def t1_refs(view, error_ids):
   named = view.errors_named(error_ids)
   core = view.core_key_ideas()

   return [view.ref(record["id"]) for record in named + core]


def t2_refs(view):
   core = view.core_key_ideas()
   examples = view.of_type(WORKED_EXAMPLE)
   refs = [view.ref(record["id"]) for record in core]

   for example in examples[:1]:
      refs.append(view.ref(example["id"], STEPS_ONLY))

   return refs


def t3_refs(view, error_ids, prerequisite_ids):
   wanted = set(prerequisite_ids)
   bridges = [
      section
      for section in view.of_type(PREREQUISITE_BRIDGE)
      if section.get("prerequisite_id") in wanted
   ]
   named = view.errors_named(error_ids)
   selected = bridges + named
   has_nothing_named = len(selected) == 0

   if has_nothing_named:
      selected = view.core_key_ideas()

   return [view.ref(record["id"]) for record in selected]


def is_repeat_t4(lesson_state):
   state = lesson_state or {}
   was_t4 = state.get("refresher_reason") == "T4"
   days_since = state.get("days_since_refresher")
   is_recent = days_since is not None and days_since < constants.REFRESHER_MIN_GAP_DAYS

   return was_t4 and is_recent


def t4_refs(view, lesson_state):
   if is_repeat_t4(lesson_state):
      return refresher_pointer_refs(view)

   refs = first_contact_refs(view, "low", ())
   first_contact_only = (CHECK, PREDICTION)

   return [ref for ref in refs if ref.type not in first_contact_only]


def read_again_refs(view):
   return [view.ref(record["id"]) for record in view.of_type(STRATEGY)]


def named_anchors(view, refs, error_ids):
   named = {section["id"] for section in view.errors_named(error_ids)}

   return tuple(ref.id for ref in refs if ref.id in named)


def plan_lesson(lesson, band, reason, error_ids=(), prerequisite_ids=(), lesson_state=None):
   is_known_reason = reason in REASONS

   if not is_known_reason:
      raise ValueError(f"unknown lesson reason {reason!r}")

   view = LessonView(lesson)
   error_ids = tuple(error_ids)
   prerequisite_ids = tuple(prerequisite_ids)
   lesson_id = lesson["id"]
   version = lesson["version"]
   is_no_insertion = band == "none"
   is_first_contact = reason == FIRST_CONTACT

   if is_no_insertion:
      return LessonPlan(lesson_id, version, band, reason, (), (), 0.0, 0, ())

   if reason == FEEDBACK:
      anchors = tuple(section["id"] for section in view.errors_named(error_ids))

      return LessonPlan(lesson_id, version, band, reason, (), (), 0.0, 0, anchors)

   if is_first_contact:
      return first_contact_plan(view, lesson, band, prerequisite_ids)

   refs = refresher_refs(view, reason, error_ids, prerequisite_ids, lesson_state)
   refs = [ref for ref in refs if ref.type != PREDICTION]
   is_t4_first = reason == "T4" and not is_repeat_t4(lesson_state)

   if is_t4_first:
      minutes_cap = constants.LESSON_READ_MINUTES_MAX
   else:
      minutes_cap = constants.REFRESHER_MINUTES_MAX

   refs = fit_refresher(view, refs, minutes_cap)
   words = ref_words(view, refs)
   minutes = min(estimate_minutes(words), minutes_cap)
   refs = tuple(refs)

   return LessonPlan(
      lesson_id,
      version,
      band,
      reason,
      refs,
      (),
      minutes,
      words,
      named_anchors(view, refs, error_ids),
   )


def refresher_refs(view, reason, error_ids, prerequisite_ids, lesson_state):
   if reason == "T1":
      return t1_refs(view, error_ids)

   if reason == "T2":
      return t2_refs(view)

   if reason == "T3":
      return t3_refs(view, error_ids, prerequisite_ids)

   if reason == "T4":
      return t4_refs(view, lesson_state)

   if reason == "T5":
      return refresher_pointer_refs(view)

   return read_again_refs(view)


def first_contact_plan(view, lesson, band, prerequisite_ids):
   is_low = band == "low"
   words_cap = constants.LESSON_WORDS_FULL_MAX if is_low else constants.LESSON_WORDS_BRIEF_MAX
   minutes_cap = constants.LESSON_READ_MINUTES_MAX if is_low else constants.LESSON_BRIEF_MINUTES_MAX
   minutes_key = "full" if is_low else "brief"
   authored_minutes = lesson["read_minutes"][minutes_key]

   refs = first_contact_refs(view, band, prerequisite_ids)
   refs = fit_first_contact(view, refs, words_cap)
   check_ids = tuple(ref.id for ref in refs if ref.type == CHECK)

   return LessonPlan(
      lesson["id"],
      lesson["version"],
      band,
      FIRST_CONTACT,
      tuple(refs),
      check_ids,
      min(float(authored_minutes), minutes_cap),
      ref_words(view, refs),
      (),
   )


def band_words(lesson, band):
   """Words of the untrimmed first-contact plan for a band, which is what word_count records."""
   view = LessonView(lesson)
   refs = first_contact_refs(view, band, ())

   return ref_words(view, refs)
