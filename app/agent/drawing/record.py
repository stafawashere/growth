"""The figure an agent turn stores in agent_turns.figure (docs/agent/drawing-design.md, Storage,
privacy and logs): the validated source figure only when it was shown, the outcome (shown,
refused:<reason> or withheld) and the number of steps sent. A withheld or refused figure keeps no
spec, so nothing the screen stopped is stored.
"""
SHOWN = "shown"
WITHHELD = "withheld"
REFUSED_PREFIX = "refused:"


def stored_figure(outcome, spec=None, revealed=0):
   kept_spec = spec if outcome == SHOWN else None

   return {"spec": kept_spec, "outcome": outcome, "revealed": revealed}


def refused_outcome(reason):
   return f"{REFUSED_PREFIX}{reason}"


def shown_spec(figure):
   """The source figure of a stored figure that was shown, or None."""
   is_record = isinstance(figure, dict)
   spec = figure.get("spec") if is_record else None
   was_shown = is_record and figure.get("outcome") == SHOWN and isinstance(spec, dict)

   return spec if was_shown else None
