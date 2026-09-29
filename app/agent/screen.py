"""The deterministic output screen between the provider stream and the student (docs/agent/
architecture.md, Streaming end to end).

SentenceScreen accumulates the reply's text deltas and releases it a sentence at a time. A sentence
ends at a full stop, a question mark or an exclamation mark followed by whitespace, or at a blank
line, and never inside a \\( \\) or \\[ \\] span, so a decimal point, a factorial or a period inside
a formula does not split one. Each sentence is run through the checks app/evals/agent_checks.py
holds, the same functions the eval scores the golden set with. A sentence that passes is released.
The first sentence that fails is never released: the screen records the verdict on `withheld`,
releases the fixed decline copy from prompts/agent/decline_v1.md in its place, and releases nothing
after it, so the route ends the turn with outcome withheld and stores the decline.
"""
from pathlib import Path

from app.evals import agent_checks

DECLINE_PATH = Path(__file__).resolve().parents[2] / "prompts" / "agent" / "decline_v1.md"
SENTENCE_ENDS = (".", "?", "!")
MATH_OPENERS = {"\\(": "\\)", "\\[": "\\]"}


def decline_text(path=DECLINE_PATH):
   """The decline copy is the file's body under its front matter, as one line."""
   text = path.read_text()
   has_front_matter = text.startswith("---\n")

   if has_front_matter:
      _opening, _front_matter, text = text.split("---\n", 2)

   return " ".join(text.split())


def sentence_end(buffer):
   """The index just past the first sentence end outside math, or None while none is certain."""
   closer = None
   position = 0
   length = len(buffer)

   while position < length:
      pair = buffer[position:position + 2]

      if closer is not None:
         if pair == closer:
            closer = None
            position += 2
            continue

         position += 1
         continue

      if pair in MATH_OPENERS:
         closer = MATH_OPENERS[pair]
         position += 2
         continue

      is_blank_line = buffer.startswith("\n\n", position)

      if is_blank_line:
         return position + 2

      character = buffer[position]
      is_terminator = character in SENTENCE_ENDS
      has_next = position + 1 < length
      is_followed_by_space = has_next and buffer[position + 1].isspace()
      ends_a_sentence = is_terminator and is_followed_by_space

      if ends_a_sentence:
         return position + 1

      position += 1

   return None


class SentenceScreen:
   def __init__(self, packet, key_forms, decline=None):
      self.facts = agent_checks.facts_from_packet(packet)
      self.key_forms = key_forms
      self.decline = decline if decline is not None else decline_text()
      self.withheld = None
      self._buffer = ""

   def _verdict_for(self, sentence):
      for verdict in agent_checks.run_checks(sentence, self.facts, self.key_forms, agent_checks.SENTENCE_CHECKS):
         if not verdict.passed:
            return verdict

      return None

   def _screened(self, sentence):
      failed = self._verdict_for(sentence)

      if failed is None:
         return [sentence]

      self.withheld = failed
      self._buffer = ""

      return [self.decline]

   def feed(self, delta):
      if self.withheld is not None:
         return []

      self._buffer += delta
      released = []

      while True:
         end = sentence_end(self._buffer)

         if end is None:
            return released

         sentence, self._buffer = self._buffer[:end], self._buffer[end:]
         released.extend(self._screened(sentence))

         if self.withheld is not None:
            return released

   def flush(self):
      if self.withheld is not None:
         return []

      remainder, self._buffer = self._buffer, ""
      is_blank = remainder.strip() == ""

      if is_blank:
         return [remainder] if remainder else []

      return self._screened(remainder)
