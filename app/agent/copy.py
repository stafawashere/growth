"""The words the tutor panel shows when a turn cannot be answered (docs/agent/design.md, "The empty
state and the degraded states").

Every string that table gives is held here verbatim, and the turn route sends the one for its
error kind as the event's copy, so the client never composes a degraded state of its own. The
usage-limit line takes the reset time when the subscription reported one and the "when the limit
resets" wording when it did not. The withheld-reply decline is versioned beside the templates in
prompts/agent/decline_v1.md instead and released by the output screen.

Two kinds have no row in design.md's table, the conversation ceiling and a refused turn, so their
lines below are written in the same register until the design names its own.
"""
USAGE_LIMIT = "usage_limit"
DAILY_CAP = "daily_cap"
MINUTE_CAP = "minute_cap"
SIGN_IN = "sign_in"
UNAVAILABLE = "unavailable"
TIMED = "timed"
CEILING = "ceiling"
REFUSED = "refused"
ERROR_KINDS = (USAGE_LIMIT, DAILY_CAP, MINUTE_CAP, SIGN_IN, UNAVAILABLE, TIMED, CEILING, REFUSED)

USAGE_LIMIT_WITH_TIME = (
   "The tutor cannot answer right now because the account's Claude usage limit has been reached. "
   "It will answer again after {time}. Practice is not affected."
)
USAGE_LIMIT_WITHOUT_TIME = (
   "The tutor cannot answer right now because the account's Claude usage limit has been reached. "
   "It will answer again when the limit resets. Practice is not affected."
)
ITEM_CEILING = (
   "That is the third question on this item. Check your answer when you are ready, and we can go "
   "through it after."
)
CONVERSATION_CEILING = (
   "This conversation has reached 20 questions. Close it and open a new one to keep asking."
)

FIXED_COPY = {
   DAILY_CAP: "The tutor has used today's allowance and is unavailable for the rest of today. Practice is not affected.",
   MINUTE_CAP: "The tutor is answering too many questions at once. Wait a moment and send again.",
   SIGN_IN: (
      "The tutor cannot answer because the Claude sign-in on this computer has expired. Practice is "
      "not affected."
   ),
   UNAVAILABLE: "No connection to the tutor right now. What you typed is kept here.",
   TIMED: "Not available during a timed part.",
   REFUSED: "The tutor could not use what this screen sent. Reload the page and send again.",
}


def usage_limit_copy(reset_time=None):
   has_reset_time = reset_time is not None

   if has_reset_time:
      return USAGE_LIMIT_WITH_TIME.format(time=reset_time)

   return USAGE_LIMIT_WITHOUT_TIME


def copy_for(kind, reset_time=None, conversation_ceiling=False):
   if kind == USAGE_LIMIT:
      return usage_limit_copy(reset_time)

   if kind == CEILING:
      return CONVERSATION_CEILING if conversation_ceiling else ITEM_CEILING

   return FIXED_COPY[kind]
