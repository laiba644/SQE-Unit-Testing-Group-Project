# Task 3 — External CSV Data-Driven Unit Testing (No API)

**Scope:** `task_validation.py` (`validate_title`, `validate_due_date`, `validate_status`).
The external data file `data/validation_unit_cases.csv` supplies 19 cases.
The test function uses `csv.DictReader` and `pytest.mark.parametrize`.
It does not make any HTTP requests and does not call Flask.

- ECP: accepted and rejected titles, dates, and statuses.
- BVA: 1, 100, 101 title characters; leap/non-leap February 29.
- Missing/wrong-type scenarios are represented using `input_type=none`.

**Run in VS Code, in the project root:**

```powershell
.\.venv\Scripts\python.exe -m pytest tests/test_validation_csv_unit.py -v
```

**Run in parallel:**

```powershell
.\.venv\Scripts\python.exe -m pytest tests/test_validation_csv_unit.py -n 2 -v
```

**Evidence:** Save your Windows command output and record actual pass/fail for your
submission. The Excel attachment lists case IDs, test inputs, expectations and
design techniques. This independent Task 3 suite is additional to the 150
individually allocated tests; it should not be used to claim extra personal
contributions without genuine work by the relevant person.
