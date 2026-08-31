import pytest

from app.lab.payment import held_out_matrix, run_scenario


@pytest.mark.parametrize(
    "case_id,observed,decision",
    [
        ("normal_success", 1, "PASS"),
        ("known_bad", 2, "BLOCK"),
        ("corrected", 1, "PASS"),
        ("exact_recurrence", 2, "BLOCK"),
        ("held_out_variant", 2, "BLOCK"),
        ("safe_change", 1, "PASS"),
    ],
)
def test_scenario_truth(case_id: str, observed: int, decision: str) -> None:
    result = run_scenario(case_id)
    assert result.observed_captures == observed
    assert result.decision == decision
    assert result.passed


def test_held_out_evaluation_proves_sensitivity_and_specificity() -> None:
    results = {result.case_id: result for result in held_out_matrix()}
    assert results["exact_recurrence"].decision == "BLOCK"
    assert results["held_out_variant"].decision == "BLOCK"
    assert results["safe_change"].decision == "PASS"

