"""tools/subscription_smoke.py checks_for, on recorded call shapes only. No CLI is run.

The CLI answers --json-schema through its internal StructuredOutput tool, one extra turn, so a
structured call passes no_tool_ran at two turns. Any other extra turn is a tool that ran.
"""
from tools.subscription_smoke import checks_for


def recorded_call(num_turns, structured_output=None, permission_denials=None):
   return {
      "error": None,
      "num_turns": num_turns,
      "permission_denials": permission_denials or [],
      "structured_output": structured_output,
      "total_cost_usd": 0.004519,
      "usage": {"input_tokens": 1200, "output_tokens": 150},
      "reported_input_tokens": 1200,
      "leaked_markers": [],
   }


def test_the_structured_output_turn_is_not_read_as_a_tool():
   call = recorded_call(2, structured_output={"sentence": "Rewrite first."})

   assert checks_for(call, asked_for_structured_output=True)["no_tool_ran"] is True


def test_a_second_turn_on_a_plain_call_is_a_tool_that_ran():
   call = recorded_call(2)

   assert checks_for(call)["no_tool_ran"] is False


def test_a_second_turn_without_structured_output_is_a_tool_that_ran():
   call = recorded_call(2)

   assert checks_for(call, asked_for_structured_output=True)["no_tool_ran"] is False


def test_a_third_turn_on_a_structured_call_is_a_tool_that_ran():
   call = recorded_call(3, structured_output={"sentence": "Rewrite first."})

   assert checks_for(call, asked_for_structured_output=True)["no_tool_ran"] is False


def test_a_permission_denial_fails_even_at_the_expected_turns():
   call = recorded_call(2, structured_output={"sentence": "Rewrite first."}, permission_denials=[{"tool_name": "Bash"}])

   assert checks_for(call, asked_for_structured_output=True)["no_tool_ran"] is False