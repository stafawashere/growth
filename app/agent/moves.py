"""The app chooses the tutoring move and the model writes the sentence (docs/agent/architecture.md,
The context composer, "The move"; docs/agent/research/math-tutoring.md, Conversational moves
during practice and Moves after submission).

Practice escalates by turn, never by the model's judgement. The first turn on an item asks what the
student tried (M3), or restates the task (M1) when the opening message already said what was tried.
While the student keeps answering the tutor's questions the next turn offers a question the student
can ask themselves (M4). Only after a turn in which the student did not answer does the tutor name
the governing rule (M5), and after a second such turn it points to a lesson section (M6). The
per-item ceiling of 3 turns is counted and enforced by the route, not here.

After submission the moves run in the order of plan 03's three-part contract and then its two
question types: discuss the violated step (P3), name the point (P1 and P2), ask the
self-explanation question (P4), and ask the discriminating probe (P5) only when the diagnostician
wrote one; without a probe the fourth turn repeats the self-explanation question. A turn past the
fourth stays at the violated step.

On a screen with no item the move is explain on a lesson and navigate everywhere else.
"""
PRACTICE = "practice"
AFTER_SUBMISSION = "after_submission"
BROWSING = "browsing"
MODES = (PRACTICE, AFTER_SUBMISSION, BROWSING)

RESTATE = "restate"
NAME_REPRESENTATION = "name_representation"
ASK_WHAT_TRIED = "ask_what_tried"
NEXT_SELF_QUESTION = "next_self_question"
NAME_RULE = "name_rule"
POINT_TO_SECTION = "point_to_section"
PRACTICE_MOVES = (RESTATE, NAME_REPRESENTATION, ASK_WHAT_TRIED, NEXT_SELF_QUESTION, NAME_RULE, POINT_TO_SECTION)

DISCUSS_STEP = "discuss_step"
NAME_POINT = "name_point"
SELF_EXPLANATION_QUESTION = "self_explanation_question"
PROBE = "probe"
AFTER_SUBMISSION_MOVES = (DISCUSS_STEP, NAME_POINT, SELF_EXPLANATION_QUESTION, PROBE)

EXPLAIN = "explain"
NAVIGATE = "navigate"
BROWSING_MOVES = (EXPLAIN, NAVIGATE)

MOVES = PRACTICE_MOVES + AFTER_SUBMISSION_MOVES + BROWSING_MOVES

LESSON_SCREEN_KINDS = ("lesson", "session_lesson")


def practice_move(turn_index_on_item, student_answered_question):
   is_first_turn = turn_index_on_item <= 0

   if is_first_turn:
      return RESTATE if student_answered_question else ASK_WHAT_TRIED

   if student_answered_question:
      return NEXT_SELF_QUESTION

   is_second_turn = turn_index_on_item == 1

   return NAME_RULE if is_second_turn else POINT_TO_SECTION


def after_submission_move(turn_index_on_item, has_probe):
   is_past_the_sequence = turn_index_on_item >= len(AFTER_SUBMISSION_MOVES)

   if is_past_the_sequence:
      return DISCUSS_STEP

   move = AFTER_SUBMISSION_MOVES[max(turn_index_on_item, 0)]
   is_probe_without_one = move == PROBE and not has_probe

   if is_probe_without_one:
      return SELF_EXPLANATION_QUESTION

   return move


def choose_move(mode, turn_index_on_item, student_answered_question, has_probe=False, screen_kind=None):
   """student_answered_question says whether the student's latest message answered the question the
   tutor asked in its previous turn; on a first turn it says whether the opening message already
   described what the student tried."""
   if mode == PRACTICE:
      return practice_move(turn_index_on_item, student_answered_question)

   if mode == AFTER_SUBMISSION:
      return after_submission_move(turn_index_on_item, has_probe)

   if mode == BROWSING:
      return EXPLAIN if screen_kind in LESSON_SCREEN_KINDS else NAVIGATE

   raise ValueError(f"unknown mode {mode!r}")
