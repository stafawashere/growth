"""The provider layer (docs/plan/07-ai-provider-layer.md).

P1 wires exactly one role, tutor on claude-sonnet-5, through app/providers/anthropic.py, plus
app/providers/replay.py for cassette playback in tests. The integrator, not this package, wires
either provider into app/runtime/ or app/main.py.
"""
