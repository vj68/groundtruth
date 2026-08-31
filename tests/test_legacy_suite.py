"""The original suite is intentionally realistic but misses ambiguous completion."""

import pytest

from app.lab.payment import run_scenario


@pytest.mark.parametrize("sample", range(48))
def test_existing_suite_passes_obvious_payment_paths(sample: int) -> None:
    # These represent ordinary validations and normal-path fixtures. The suite's documented
    # blind spot is a successful provider side effect followed by a lost acknowledgement.
    result = run_scenario("normal_success")
    assert result.observed_captures == 1
    assert result.decision == "PASS"
