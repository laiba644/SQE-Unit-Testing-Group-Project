"""Run the three SQE test groups in an explicit, reproducible sequence.

Suite order: Laiba (75), Hamna (75), external CSV (19).
Within each group, pytest uses test-function definition order and the order of
values in each @pytest.mark.parametrize declaration. Do not use -n or
random-order plugins in this sequential, ordered run.
"""

from pathlib import Path
import subprocess
import sys
import time

PROJECT_ROOT = Path(__file__).resolve().parents[1]

SUITES = (
    ("01 — Laiba unit tests", "tests/test_strict_member_a.py"),
    ("02 — Hamna unit tests", "tests/test_strict_member_b.py"),
    ("03 — External CSV data-driven tests", "tests/test_validation_csv_unit.py"),
)


def main() -> int:
    print("SQE ORDERED UNIT TEST EXECUTION", flush=True)
    start = time.perf_counter()
    for label, relative_file in SUITES:
        test_file = PROJECT_ROOT / relative_file
        if not test_file.is_file():
            print(f"ERROR: Missing test file: {test_file}", flush=True)
            return 2
        print(f"\n{'=' * 64}\n{label}\n{'=' * 64}", flush=True)
        cmd = [sys.executable, "-m", "pytest", "-v", relative_file]
        result = subprocess.run(cmd, cwd=PROJECT_ROOT, check=False)
        if result.returncode != 0:
            print(f"STOPPED: {label} failed (exit code {result.returncode}).", flush=True)
            return result.returncode

    print(f"\nAll 3 suites passed in the configured order. Total elapsed: {time.perf_counter() - start:.2f}s", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
