"""docs/agent/drawing-design.md, The splitter: prose passes through with its step markers taken out,
the first figure block is buffered to its closing fence, a fence or a marker split anywhere across
deltas is read the same as whole, nothing inside a math span is a marker or a fence, and an
unclosed, oversized or second block is refused. StepMarkers sends each marked step before its
sentence and the rest at the end.
"""
import pytest

from app.agent.drawing.stream import FigureSplitter, StepMarkers

REPLY = (
   "Here is the idea. [[step:curve]] The curve comes first \\( [[step:no]] \\) today.\n"
   "```figure\n"
   '{"kind": "graph", "steps": []}\n'
   "```\n"
   "Then the secant. [[step:secant]] It joins two points.\n"
   "```figure\n"
   "a second block\n"
   "```\n"
   "The end."
)

EXPECTED = [
   ("text", "Here is the idea. "),
   ("marker", "curve"),
   ("text", " The curve comes first \\( [[step:no]] \\) today.\n"),
   ("fence", None),
   ("block", '{"kind": "graph", "steps": []}'),
   ("text", "Then the secant. "),
   ("marker", "secant"),
   ("text", " It joins two points.\n"),
   ("refused", "extra"),
   ("text", "The end."),
]


def _merged(pieces):
   merged = []

   for kind, value in pieces:
      continues_text = kind == "text" and len(merged) > 0 and merged[-1][0] == "text"

      if continues_text:
         merged[-1] = ("text", merged[-1][1] + value)
      else:
         merged.append((kind, value))

   return merged


def _split(deltas):
   splitter = FigureSplitter()
   pieces = []

   for delta in deltas:
      pieces.extend(splitter.feed(delta))

   pieces.extend(splitter.finish())

   return _merged(pieces)


def test_the_whole_reply_splits_into_prose_markers_and_one_block():
   assert _split([REPLY]) == EXPECTED


@pytest.mark.parametrize("cut", range(1, len(REPLY)))
def test_every_split_position_reads_the_same_as_the_whole_reply(cut):
   assert _split([REPLY[:cut], REPLY[cut:]]) == EXPECTED


@pytest.mark.parametrize("size", range(1, 17))
def test_every_chunk_size_reads_the_same_as_the_whole_reply(size):
   assert _split([REPLY[start:start + size] for start in range(0, len(REPLY), size)]) == EXPECTED


@pytest.mark.parametrize(
   "text",
   [
      "Inside \\( [[step:a]] \\) and \\[ [[step:b]] \\] stay.",
      "A display \\[\n```figure\n\\] is no fence.",
      "Mid-line ```figure\n is no fence.",
      "```figures\nis another word.",
      "A marker [[step:this_id_is_too_long]] stays.",
      "Half [[step: a marker.",
   ],
)
def test_math_spans_mid_line_fences_and_broken_markers_stay_prose(text):
   for size in (1, 3, len(text)):
      assert _split([text[start:start + size] for start in range(0, len(text), size)]) == [("text", text)]


def test_an_unclosed_block_is_refused_unclosed_and_its_text_dropped():
   pieces = _split(["Before.\n```figure\n{\"kind\": ", "\"graph\"}\n"])

   assert pieces == [("text", "Before.\n"), ("fence", None), ("refused", "unclosed")]


def test_a_block_past_2000_characters_is_refused_oversized_and_the_prose_after_it_goes_on():
   block = "x" * 2001
   pieces = _split(["Before.\n```figure\n", block[:1000], block[1000:], "\n```\nAfter."])

   assert pieces == [("text", "Before.\n"), ("fence", None), ("refused", "oversized"), ("text", "After.")]


def test_a_block_of_2000_characters_is_read():
   block = "x" * 2000
   pieces = _split(["```figure\n", block, "\n```\n"])

   assert pieces == [("fence", None), ("block", block)]


def test_a_closing_fence_at_the_end_of_the_stream_closes_the_block():
   assert _split(["```figure\n{}\n```"]) == [("fence", None), ("block", "{}")]


def test_a_marked_step_goes_out_before_its_sentence_with_every_earlier_step_first():
   steps = StepMarkers(["curve", "secant", "tangent"])
   steps.mark("secant", 30)
   steps.mark("nowhere", 31)
   steps.mark("secant", 32)

   assert steps.due_before(20) == []
   assert steps.due_before(40) == ["curve", "secant"]

   steps.mark("curve", 45)

   assert steps.due_before(60) == []
   assert steps.remaining() == ["tangent"]
   assert steps.revealed == ["curve", "secant", "tangent"]
