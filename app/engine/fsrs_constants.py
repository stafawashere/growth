"""FSRS-7 default parameters, copied verbatim from the reference implementation (R28).

Source: https://github.com/open-spaced-repetition/fsrs-rs, src/inference_v7.rs, at the commit
recorded below. Shipped FSRS-7 takes 34 parameters (model_v7.rs PARAM_LEN = 34). The srs-benchmark
README at commit bd9110f791e5b37282c55a9aa8db35f68f0c4aa2 still prints a 35-value block under
"Default Parameters" that belongs to a superseded March 2026 draft of the model, so the README is
not the source here; the plan's sentence naming it is corrected in BUILD-LEDGER.md. The pinned
source file is committed as tests/fixtures/fsrs_rs_inference_v7_c137ee6.rs and
test_retrievability_monotone parses the vector out of it and checks its digest.
"""

SOURCE_REPO = "https://github.com/open-spaced-repetition/fsrs-rs"
SOURCE_FILE = "src/inference_v7.rs"
SOURCE_COMMIT = "c137ee6e096f9217632397a8fb2bdb6f6e1b92ae"
SOURCE_COMMIT_DATE = "2026-09-18"
SOURCE_FIXTURE = "tests/fixtures/fsrs_rs_inference_v7_c137ee6.rs"
SOURCE_SHA256 = "006d75f82b1fb629b5a939e8f74819ced71a5fc63361f8ff0cfd11e8fcce0af5"

MODEL_SOURCE_FILE = "src/model_v7.rs"
MODEL_SOURCE_FIXTURE = "tests/fixtures/fsrs_rs_model_v7_c137ee6.rs"
MODEL_SOURCE_SHA256 = "f6c7b70a798d777c267d4ca5def80b1e1a380b7bfbf27f03e32d3b23a8b5ab26"

FSRS7_DEFAULT_PARAMETERS = (
   0.1104, 2.2395, 3.9221, 11.7841,
   6.1686, 0.6457, 3.6807,
   1.9795, 0.0, 1.3826, 0.7024, 0.5999, 0.8146, 0.6398, 1.0,
   1.3207, 0.6707, 3.8668, 0.4416, 0.0934, 1.8631, 0.6162, 1.0869,
   0.1567, 0.0801, 0.2421, 0.9464, 0.1433, 0.7145, 0.0, 0.5667, 0.3734, 0.5333, 0.3048,
)

PARAMETER_COUNT = len(FSRS7_DEFAULT_PARAMETERS)
