"""Constants of the lesson layer, docs/plan/15-lessons.md. Every value is [inferred] there and sits
in that document's open-questions register. The engine's own constants stay in app/engine/constants.py.
"""

LESSONS_PER_SESSION_MAX = 2  # 15, Engine and session integration, new constants
LESSON_READ_MINUTES_MAX = 6.0  # 15, band table, low band
LESSON_BRIEF_MINUTES_MAX = 3.0  # 15, band table, mid band
LESSON_SHARE_MAX = 0.30  # 15, Engine and session integration, reading share of the forecast
LESSON_FORECAST_MIN_COMPLETIONS = 5  # 15, Engine and session integration, forecast switch
REFRESHER_MINUTES_MAX = 1.5  # 15, Re-teaching
REFRESHERS_PER_SESSION_MAX = 2  # 15, Re-teaching
REFRESHER_MIN_GAP_DAYS = 3  # 15, Re-teaching
LESSON_WORDS_FULL_MAX = 900  # 15, Content model, minute cap at 150 words per minute
LESSON_WORDS_BRIEF_MAX = 450  # 15, Content model, minute cap at 150 words per minute
LESSON_COMMON_ERRORS_MAX = 4  # 15, Engine and session integration, new constants
LESSON_CHECKS_MIN = 2  # 15, Engine and session integration, new constants
LESSON_CHECKS_MAX = 3  # 15, Engine and session integration, new constants

DECISION_SET_MAX = 6  # 15, Methods, decision lessons for confusable sets
METHOD_CONFUSION_WINDOW = 6  # 15, Methods, trigger T5
METHOD_CONFUSION_FLOOR = 0.5  # 15, Methods, trigger T5
FLUENCY_MIN_ATTEMPTS = 5  # 15, Methods, fluency
STRATEGY_WORDS_MAX = 80  # 15, Content model, strategy row
CUE_WORDS_MAX = 20  # 15, Content model, worked_examples row

WORDS_PER_MINUTE = 150  # 15, Content model, assumed reading rate
ORIENTATION_WORDS_MAX = 60  # 15, Content model, orientation row
KEY_IDEA_WORDS_MAX = 120  # 15, Content model, key_ideas row
KEY_IDEAS_CORE_MAX = 2  # 15, Content model, key_ideas row
WHY_WORDS_MAX = 25  # 15, Content model, worked_examples row
BRIDGE_WORDS_MAX = 60  # 15, Content model, prerequisite_bridge row
STRATEGY_BLOCKS_MAX = 3  # 15, Content model, strategy row
WORKED_EXAMPLES_MAX = 2  # 15, Content model, worked_examples row
READER_CHECK_LINES_MAX = 6  # 15, Content model, what_a_reader_scores row
QUOTE_WORDS_MAX = 25  # 15, Sourcing, one anchor quote per block, qa/07_quotes.py cap
MID_ERRORS = 2  # 15, Content model, common_errors row, mid band shows the first 2

BANDS = ("low", "mid")
