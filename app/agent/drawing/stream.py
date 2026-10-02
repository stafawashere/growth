"""The figure splitter (docs/agent/drawing-design.md, The splitter).

FigureSplitter sits between the provider's text deltas and the sentence screen. feed returns the
pieces a delta completes, in order, and finish the pieces the end of the stream completes. A piece
is a pair:

- ("text", prose), the reply's prose with every [[step:ID]] marker taken out
- ("marker", step_id), where a marker stood in that prose
- ("fence", None), the opening fence of the reply's first figure block
- ("block", text), the first block's text once its closing fence is seen
- ("refused", reason): oversized when the first block grows past 2,000 characters, extra at the
  opening fence of any later block, unclosed when the stream ends inside the first block
- ("marks_fence", None), ("marks_block", text) and ("marks_refused", reason), the same for the
  reply's one marks block (docs/agent/drawing-design.md, Marks on the page), whose cap is 1,500

A fence is a line of its own: ```figure or ```marks opens a block and ``` closes it. A reply holds
one block of each kind, and a second of either kind is refused extra. Anything that could still
become a fence or a marker is held until a later delta decides it. Nothing inside \\( \\) or \\[ \\]
is read as a marker or a fence. A refused block is swallowed whole and the prose after its closing
fence goes on.

StepMarkers decides, once a figure is shown, which of its steps go out before each released
sentence. A marker is kept with its offset in the marker-free prose, and a step goes out
immediately before the sentence whose text holds that offset, together with any earlier step not
sent yet, so the steps always arrive in the figure's order. A marker for an unknown step or for a
step already sent is ignored, and so is every marker before the figure, because the markers are
only kept from the moment the figure is shown. remaining gives the steps no sentence marked.
"""
import re

MAX_BLOCK_CHARACTERS = 2000
MAX_MARKS_CHARACTERS = 1500
FENCE_SLACK = 16

TEXT = "text"
MARKER = "marker"
FENCE = "fence"
BLOCK = "block"
REFUSED = "refused"
MARKS_FENCE = "marks_fence"
MARKS_BLOCK = "marks_block"
MARKS_REFUSED = "marks_refused"
FIGURE_KIND = "figure"
MARKS_KIND = "marks"
PIECE_KINDS = {
   FIGURE_KIND: (FENCE, BLOCK, REFUSED, MAX_BLOCK_CHARACTERS),
   MARKS_KIND: (MARKS_FENCE, MARKS_BLOCK, MARKS_REFUSED, MAX_MARKS_CHARACTERS),
}

OVERSIZED = "oversized"
EXTRA = "extra"
UNCLOSED = "unclosed"

MARKER_HEAD = "[[step:"
MARKER_PATTERN = r"\[\[step:([A-Za-z0-9_]{1,16})\]\]"
MARKER_TAIL_PATTERN = r"[A-Za-z0-9_]{0,16}\]?"
FENCE_HEADS = ("```figure", "```marks")
OPENING_FENCE_PATTERN = r"```(figure|marks)[ \t]*\r?\n"
FINAL_OPENING_FENCE_PATTERN = r"```(figure|marks)[ \t]*\Z"
LINE_SPACE_PATTERN = r"[ \t\r]*"
CLOSING_MARK = "```"
MATH_OPENERS = {"\\(": "\\)", "\\[": "\\]"}


def _could_become_marker(rest):
   head = rest[: len(MARKER_HEAD)]

   if not MARKER_HEAD.startswith(head):
      return False

   if len(rest) <= len(MARKER_HEAD):
      return True

   return re.fullmatch(MARKER_TAIL_PATTERN, rest[len(MARKER_HEAD):]) is not None


def _could_become_fence(rest):
   for fence_head in FENCE_HEADS:
      head = rest[: len(fence_head)]

      if not fence_head.startswith(head):
         continue

      if len(rest) <= len(fence_head):
         return True

      if re.fullmatch(LINE_SPACE_PATTERN, rest[len(fence_head):]) is not None:
         return True

   return False


def _merged(pieces):
   merged = []

   for kind, value in pieces:
      is_empty_text = kind == TEXT and value == ""
      continues_text = kind == TEXT and len(merged) > 0 and merged[-1][0] == TEXT

      if is_empty_text:
         continue

      if continues_text:
         merged[-1] = (TEXT, merged[-1][1] + value)
      else:
         merged.append((kind, value))

   return merged


class FigureSplitter:
   def __init__(self):
      self._pending = ""
      self._math_closer = None
      self._at_line_start = True
      self._in_block = False
      self._block_text = ""
      self._block_kind = FIGURE_KIND
      self._blocks_opened = {FIGURE_KIND: 0, MARKS_KIND: 0}
      self._block_refused = False

   def feed(self, delta):
      self._pending += delta

      return self._drained(final=False)

   def finish(self):
      pieces = self._drained(final=True)
      opened_of_its_kind = self._blocks_opened[self._block_kind]
      is_first_block_open = self._in_block and opened_of_its_kind == 1 and not self._block_refused

      if is_first_block_open:
         pieces.append((PIECE_KINDS[self._block_kind][2], UNCLOSED))

      self._in_block = False
      self._block_text = ""

      return pieces

   def _drained(self, final):
      pieces = []
      switched = True

      while switched:
         switched = self._scan_block(pieces, final) if self._in_block else self._scan_prose(pieces, final)

      return _merged(pieces)

   def _open_block(self, pieces, block_kind):
      fence, _block, refused, _cap = PIECE_KINDS[block_kind]
      is_first = self._blocks_opened[block_kind] == 0
      self._blocks_opened[block_kind] += 1
      self._block_kind = block_kind
      self._in_block = True
      self._block_text = ""
      self._block_refused = not is_first
      pieces.append((fence, None) if is_first else (refused, EXTRA))

   def _scan_prose(self, pieces, final):
      """Prose up to the next opening fence; True when a block opened."""
      text = self._pending
      position = 0
      plain_start = 0

      while position < len(text):
         if self._math_closer is not None:
            closer_at = text.find(self._math_closer, position)

            if closer_at < 0:
               holds_half_closer = text.endswith("\\") and not final
               position = len(text) - 1 if holds_half_closer else len(text)
               break

            position = closer_at + 2
            self._math_closer = None
            self._at_line_start = False
            continue

         character = text[position]
         pair = text[position: position + 2]

         if pair in MATH_OPENERS:
            self._math_closer = MATH_OPENERS[pair]
            self._at_line_start = False
            position += 2
            continue

         is_half_opener = character == "\\" and position + 1 == len(text) and not final

         if is_half_opener:
            break

         if character == "[":
            marker = re.match(MARKER_PATTERN, text[position:])

            if marker is not None:
               pieces.append((TEXT, text[plain_start:position]))
               pieces.append((MARKER, marker.group(1)))
               position += marker.end()
               plain_start = position
               continue

            waits_for_marker = not final and _could_become_marker(text[position:])

            if waits_for_marker:
               break

         starts_fence = self._at_line_start and character == "`"

         if starts_fence:
            rest = text[position:]
            fence = re.match(OPENING_FENCE_PATTERN, rest)
            may_close_the_stream = fence is None and final

            if may_close_the_stream:
               fence = re.match(FINAL_OPENING_FENCE_PATTERN, rest)

            if fence is not None:
               pieces.append((TEXT, text[plain_start:position]))
               self._pending = rest[fence.end():]
               self._open_block(pieces, fence.group(1))

               return True

            waits_for_fence = not final and _could_become_fence(rest)

            if waits_for_fence:
               break

         self._at_line_start = character == "\n"
         position += 1

      pieces.append((TEXT, text[plain_start:position]))
      self._pending = text[position:]

      if final:
         pieces.append((TEXT, self._pending))
         self._pending = ""

      return False

   def _closing_fence(self, final):
      """(content_end, resume_at) of the closing fence line, or None while none is certain."""
      text = self._block_text
      search_from = 0

      while True:
         at = text.find(CLOSING_MARK, search_from)

         if at < 0:
            return None

         search_from = at + 1
         is_line_start = at == 0 or text[at - 1] == "\n"

         if not is_line_start:
            continue

         after = at + len(CLOSING_MARK)
         line_end = text.find("\n", after)
         runs_to_the_end = line_end < 0
         rest_of_line = text[after:] if runs_to_the_end else text[after:line_end]
         is_bare = re.fullmatch(LINE_SPACE_PATTERN, rest_of_line) is not None

         if not is_bare:
            continue

         if not runs_to_the_end:
            return at, line_end + 1

         if final:
            return at, len(text)

         return None

   def _scan_block(self, pieces, final):
      """The block up to its closing fence; True when the block closed."""
      self._block_text += self._pending
      self._pending = ""
      closing = self._closing_fence(final)

      _fence, block, _refused, cap = PIECE_KINDS[self._block_kind]

      if closing is None:
         is_past_the_cap = len(self._block_text) > cap + FENCE_SLACK

         if is_past_the_cap:
            self._refuse_oversized(pieces)

         return False

      content_end, resume_at = closing
      content = self._block_text[:content_end]
      ends_its_line = content.endswith("\n")

      if ends_its_line:
         content = content[:-1]
      is_oversized = len(content) > cap

      if is_oversized:
         self._refuse_oversized(pieces)

      if not self._block_refused:
         pieces.append((block, content))

      self._pending = self._block_text[resume_at:]
      self._block_text = ""
      self._in_block = False
      self._at_line_start = True

      return True

   def _refuse_oversized(self, pieces):
      if self._block_refused:
         return

      self._block_refused = True
      pieces.append((PIECE_KINDS[self._block_kind][2], OVERSIZED))


class StepMarkers:
   def __init__(self, step_ids):
      self.step_ids = tuple(step_ids)
      self.revealed = []
      self._marked = []

   def mark(self, step_id, offset):
      is_known = step_id in self.step_ids
      is_sent = step_id in self.revealed
      is_marked = any(step_id == marked for _offset, marked in self._marked)
      is_new = is_known and not is_sent and not is_marked

      if is_new:
         self._marked.append((offset, step_id))

   def _through(self, step_id):
      due = []

      for candidate in self.step_ids[: self.step_ids.index(step_id) + 1]:
         if candidate not in self.revealed:
            self.revealed.append(candidate)
            due.append(candidate)

      return due

   def due_before(self, end):
      """The steps to send before a sentence that ends at this offset of the prose."""
      due = []
      kept = []

      for offset, step_id in self._marked:
         if offset < end:
            due.extend(self._through(step_id))
         else:
            kept.append((offset, step_id))

      self._marked = kept

      return due

   def remaining(self):
      self._marked = []

      return self._through(self.step_ids[-1]) if self.step_ids else []
