"""Task 3: data-driven pure unit tests using external CSV (no Flask / API)."""
import csv
from pathlib import Path

import pytest
import task_validation

pytestmark = [pytest.mark.unit, pytest.mark.csv]
CSV_FILE = Path(__file__).resolve().parents[1] / "data" / "validation_unit_cases.csv"
ALLOWED_FUNCTIONS = {"validate_title", "validate_due_date", "validate_status"}
EXCEPTIONS = {"ValueError": ValueError, "TypeError": TypeError}


def read_cases():
    with CSV_FILE.open("r", newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


@pytest.mark.parametrize("case", read_cases(), ids=lambda item: item["case_id"])
def test_validation_using_external_csv(case):
    function_name = case["function"]
    assert function_name in ALLOWED_FUNCTIONS
    function = getattr(task_validation, function_name)
    value = None if case["input_type"] == "none" else case["input_value"]
    exception_name = case["expected_exception"]
    if exception_name:
        with pytest.raises(EXCEPTIONS[exception_name]):
            function(value)
    else:
        assert function(value) == case["expected_value"]
