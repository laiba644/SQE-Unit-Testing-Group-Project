# SQE Task 4 — Ordered Unit Test Suites

Copy `scripts/run_ordered_suites.py` into the `scripts` folder of the new `SQE-Unit-Testing-Group-Project` repository. Create `scripts` if absent.

## Explicit group execution order
1. Laiba: `tests/test_strict_member_a.py` (75 parameterized executions)
2. Hamna: `tests/test_strict_member_b.py` (75 parameterized executions)
3. External CSV: `tests/test_validation_csv_unit.py` (19 parameterized executions)

The script executes each test group in a separate subprocess, waits for completion, and stops on failures. Tests within each suite execute in the order defined in the source file (test function declarations and each `@pytest.mark.parametrize` list). This ordered mode is **sequential**. Parallel execution is an independently configured mode using pytest-xdist, so an ordered execution cannot also guarantee parallel case ordering.

## Commands (PowerShell, repository root)

Ordered execution and evidence saved to text file:

```powershell
.\.venv\Scripts\python.exe scripts/run_ordered_suites.py 2>&1 | Tee-Object -FilePath Ordered_Test_Results.txt
```

Parallel mode (different run):

```powershell
.\.venv\Scripts\python.exe -m pytest tests/test_strict_member_a.py tests/test_strict_member_b.py tests/test_validation_csv_unit.py -n 2 -v
```

Coverage report (different run):

```powershell
.\.venv\Scripts\python.exe -m pytest tests/test_strict_member_a.py tests/test_strict_member_b.py tests/test_validation_csv_unit.py --cov=task_validation --cov=task_service --cov=db --cov-report=html --cov-report=term
```

Record actual outputs, warnings, and any deviations before submission.
