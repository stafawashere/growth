# Provider cassettes

Cassettes for `app/providers/replay.ReplayProvider`, in the result shape
`app/providers/anthropic.py` produces: `text`, `finish_reason`, `usage` with its token fields,
`provider` and `model`.

`tutor_elaborated_v1.json` is hand written, not recorded. No Anthropic key existed when gate 23
of `docs/plan/11-phased-delivery.md` was built, so the file stands in for a recording of the tutor
role against `prompts/feedback/elaborated_v1.md`. It carries `"synthetic": true` inside the file,
and its token counts are placeholders rather than measurements.

What that means for the other gates:

- Gate 22, the prompt cache prefix length, reads a real recording against a real key. This
  cassette is not evidence for it and its usage numbers must not be quoted as token counts.
- Gate 23 needs a tutor that answers without a network call, which is all this file supplies.

Replace the file with a real recording once a key exists, keeping the same path, and drop the
`synthetic` keys at the same time.
