# Software Quality Engineering — Automated Unit Testing

### Flask To-Do List Application | Group Project

This project focuses on the design, implementation, execution, and documentation of automated unit tests for a Python Flask-based To-Do List Application.

The project demonstrates important Software Quality Engineering (SQE) techniques, including **Equivalence Class Partitioning (ECP), Boundary Value Analysis (BVA), State Transition Testing, Data-Driven Testing, Parallel Test Execution, and Ordered Test Suites**.

The automated testing framework is implemented using **Python, pytest, pytest-cov, pytest-xdist, and SQLite**.

## Project Information

| Detail | Information |
|---|---|
| Course | Software Quality Engineering (SQE) |
| Project | Automated Unit Testing of Flask To-Do Application |
| Section | BSE-5A |
| Programming Language | Python |
| Testing Framework | pytest |
| Database | SQLite |
| Application Framework | Flask |
| Submission | October 2026 |

**Original Open-Source Project:** https://github.com/YugG03/todo-flask-app

## Group Members

| Name | Student ID | Section | Unit Test Cases |
|---|---|---|---|
| Laiba Kashif | 24F-3069 | BSE-5A | 75 |
| Hamna Maryam | 24F-3063 | BSE-5A | 75 |
| **Total** | | | **150** |

Both members maintained separate test suites and submitted their work through GitHub branches and Pull Requests.

An additional 19 external CSV-driven test cases were implemented as part of the project.

## Project Objectives

The main objectives of this project are:

- Develop automated unit tests for selected Python modules.
- Apply Equivalence Class Partitioning (ECP).
- Apply Boundary Value Analysis (BVA).
- Verify valid and invalid inputs and boundary conditions.
- Test database operations and task-management functionality.
- Implement external CSV-based data-driven testing.
- Execute automated tests sequentially and in parallel.
- Configure and execute test suites in a predefined order.
- Measure source-code coverage using pytest-cov.
- Document test cases, expected results, actual results, and execution outcomes.
- Demonstrate collaborative software development using Git and GitHub.

## Modules Selected for Testing

Three Python source-code modules were selected for unit testing.

### 1. Task Validation — `task_validation.py`

Responsible for validating task-related inputs.

Functions tested:

- `validate_title()`
- `validate_due_date()`
- `validate_status()`

**Total Functions: 3**

### 2. Task Service — `task_service.py`

Responsible for managing task operations and business logic.

Functions tested:

- `add_task()`
- `list_tasks()`
- `find_task()`
- `change_status()`
- `remove_task()`

**Total Functions: 5**

### 3. Database Operations — `db.py`

Responsible for SQLite database connectivity and task storage.

Functions tested:

- `init_db()`
- `create_task()`
- `get_all_tasks()`
- `get_task_by_id()`
- `update_task()`
- `delete_task()`
- `get_connection()`

**Total Functions: 7**

### Test Allocation

| Module | Functions | Laiba's Cases | Hamna's Cases |
|---|---:|---:|---:|
| Task Validation | 3 | 15 | 15 |
| Task Service | 5 | 25 | 25 |
| Database Operations | 7 | 35 | 35 |
| **Total** | **15** | **75** | **75** |

Each member's suite includes five parameterized test cases per selected function.

## Project Structure

```text
SQE-Unit-Testing-Group-Project/
│
├── app.py
├── db.py
├── task_service.py
├── task_validation.py
├── schema.sql
│
├── templates/
│
├── data/
│   └── validation_unit_cases.csv
│
├── tests/
│   ├── conftest.py
│   ├── test_strict_member_a.py
│   ├── test_strict_member_b.py
│   └── test_validation_csv_unit.py
│
├── scripts/
│   └── run_ordered_suites.py
│
├── docs/
│   ├── Laiba_75_Test_Cases.xlsx
│   ├── Hamna_75_Test_Cases.xlsx
│   ├── CSV_Unit_Test_Cases.xlsx
│   ├── SQE_ECP_BVA_Design_Notes.docx
│   ├── SQE_Final_Summary_Report.docx
│   ├── Ordered_Test_Results.txt
│   ├── TASK3_CSV_TESTING.md
│   └── README_TASK4.md
│
├── pytest.ini
├── requirements.txt
├── requirements-test.txt
└── README.md
```

## Technologies and Tools

| Tool | Purpose |
|---|---|
| Python | Application and automated test development |
| Flask | Web application framework |
| SQLite | Database storage |
| pytest | Unit test automation |
| pytest-cov | Code coverage measurement |
| pytest-xdist | Parallel test execution |
| CSV | External data-driven test inputs |
| Microsoft Excel | Test case documentation |
| Visual Studio Code | Development environment |
| Git | Version control |
| GitHub | Collaboration and source-code management |

## Installation and Project Setup

The following instructions demonstrate how to set up the project on a Windows computer using PowerShell or the VS Code terminal.

### Step 1 — Clone the Repository

```powershell
git clone https://github.com/laiba644/SQE-Unit-Testing-Group-Project.git
```

### Step 2 — Open the Project Directory

```powershell
cd SQE-Unit-Testing-Group-Project
```

### Step 3 — Create a Virtual Environment

```powershell
python -m venv .venv
```

### Step 4 — Install Dependencies

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt -r requirements-test.txt
```

### Step 5 — Run the Flask Application

```powershell
.\.venv\Scripts\python.exe app.py
```

Open the application in a browser:

http://127.0.0.1:5000/

The application can be stopped by pressing `Ctrl + C` in the terminal.

**Note:** Automated unit tests do not require the Flask web server to be running.

## Automated Unit Testing

Automated unit tests are implemented using pytest and parameterized test cases.

### Run Laiba's Unit Tests

```powershell
.\.venv\Scripts\python.exe -m pytest tests/test_strict_member_a.py -v
```

**Recorded Result: 75 Passed**

### Run Hamna's Unit Tests

```powershell
.\.venv\Scripts\python.exe -m pytest tests/test_strict_member_b.py -v
```

**Recorded Result: 75 Passed**

### Run All Selected Automated Tests

```powershell
.\.venv\Scripts\python.exe -m pytest tests/test_strict_member_a.py tests/test_strict_member_b.py tests/test_validation_csv_unit.py -v
```

**Recorded Result: 169 Passed, 0 Failed**

## External CSV Data-Driven Testing

Data-driven testing was implemented using an external CSV file.

The test inputs are maintained separately from the automated Python test code.

**CSV Data File:**

`data/validation_unit_cases.csv`

**Automated CSV Test File:**

`tests/test_validation_csv_unit.py`

The CSV suite contains **19 automated test cases** covering validation scenarios.

### Run CSV Tests Sequentially

```powershell
.\.venv\Scripts\python.exe -m pytest tests/test_validation_csv_unit.py -v
```

**Recorded Result: 19 Passed**

### Run CSV Tests in Parallel

```powershell
.\.venv\Scripts\python.exe -m pytest tests/test_validation_csv_unit.py -n 2 -v
```

**Recorded Result: 19 Passed Using 2 Workers**

Parallel execution is supported by the pytest-xdist plugin. Individual test completion order is not guaranteed when parallel execution is enabled.

## Ordered Test Suite Execution

An automated test runner was implemented to execute the three test suites in a predefined sequence.

**Execution Order:**

1. Laiba's Unit Tests — 75 Cases
2. Hamna's Unit Tests — 75 Cases
3. External CSV-Driven Tests — 19 Cases

### Run Ordered Test Suites

```powershell
.\.venv\Scripts\python.exe scripts/run_ordered_suites.py
```

The runner executes each suite sequentially and stops when a suite fails.

**Recorded Result: All 3 Suites Passed**

**Total: 169 Passed**

Detailed execution evidence is available in:

`docs/Ordered_Test_Results.txt`

## Code Coverage Analysis

Code coverage was measured using pytest-cov to evaluate how much of the selected source code was exercised by automated testing.

### Run Coverage Analysis

```powershell
.\.venv\Scripts\python.exe -m pytest tests/test_strict_member_a.py tests/test_strict_member_b.py tests/test_validation_csv_unit.py --cov=task_validation --cov=task_service --cov=db --cov-report=term --cov-report=html
```

### Recorded Coverage Results

| Python Module | Statements | Missed | Coverage |
|---|---:|---:|---:|
| `db.py` | 44 | 0 | 100% |
| `task_service.py` | 29 | 0 | 100% |
| `task_validation.py` | 26 | 1 | 96% |
| **Overall** | **99** | **1** | **99%** |

**Overall Code Coverage: 99%**

The coverage percentage represents the three selected Python modules, not the entire Flask application.

The HTML coverage report is generated in the `htmlcov` directory. Open `htmlcov/index.html` to view the detailed report.

## Software Testing Techniques

### Equivalence Class Partitioning (ECP)

Inputs were divided into valid and invalid classes to evaluate expected behavior across different categories.

Examples include:

- Valid and invalid task titles.
- Valid and invalid due dates.
- Supported and unsupported task statuses.
- Existing and nonexistent database records.

### Boundary Value Analysis (BVA)

Boundary values were tested to identify issues around input limits.

Examples include:

- Empty task titles.
- Title length boundaries.
- Over-limit task titles.
- Valid and invalid leap-year dates.
- Empty and populated task lists.

### State Transition Testing

Task status changes were tested to verify correct state updates.

Examples include:

- Changing a task from pending to completed.
- Changing a task from completed to pending.
- Rejecting invalid status values.
- Verifying persisted database state.

### Data-Driven Testing

External CSV data was used to supply multiple test inputs and expected outcomes through parameterized pytest tests.

### Test Isolation

Temporary SQLite databases and pytest fixtures were used to keep test cases independent and repeatable.

## Automated Test Execution Summary

| Test Execution | Test Cases | Recorded Result |
|---|---:|---|
| Laiba's Unit Tests | 75 | Passed |
| Hamna's Unit Tests | 75 | Passed |
| External CSV-Driven Tests | 19 | Passed |
| Combined Automated Tests | 169 | Passed |
| Ordered Test Suites | 169 | Passed |
| CSV Parallel Execution | 19 | Passed |
| Selected Modules Code Coverage | — | 99% |

The recorded combined coverage run reported seven warnings. These warnings did not cause test failures; SQLite connection resource cleanup remains an area for improvement.

## Test Documentation

All relevant test cases, testing techniques, expected outcomes, execution results, and summary reports are documented.

| Document | File |
|---|---|
| Laiba's 75 Test Cases | [Laiba Test Cases](docs/Laiba_75_Test_Cases.xlsx) |
| Hamna's 75 Test Cases | [Hamna Test Cases](docs/Hamna_75_Test_Cases.xlsx) |
| CSV Test Cases | [CSV Test Cases](docs/CSV_Unit_Test_Cases.xlsx) |
| ECP/BVA Design Notes | [ECP/BVA Notes](docs/SQE_ECP_BVA_Design_Notes.docx) |
| Final Summary Report | [Summary Report](docs/SQE_Final_Summary_Report.docx) |
| Ordered Execution Results | [Execution Evidence](docs/Ordered_Test_Results.txt) |
| CSV Testing Documentation | [CSV Testing Guide](docs/TASK3_CSV_TESTING.md) |
| Ordered Suites Documentation | [Ordered Suites Guide](docs/README_TASK4.md) |

## GitHub Collaboration

Git and GitHub were used to manage the project collaboratively.

The development workflow included:

- Creating separate feature branches.
- Developing and reviewing assigned test suites.
- Recording individual changes through Git commits.
- Pushing branches to the shared repository.
- Creating Pull Requests.
- Reviewing changes before merging.
- Merging completed work into the main branch.
- Maintaining test documentation and execution evidence.

This workflow helped organize contributions and maintain the project's version history.

## Testing Results and Limitations

The locally recorded test executions achieved:

- **169 automated test cases passed.**
- **0 failed test cases in the combined run.**
- **99% coverage across the three selected modules.**
- Successful sequential and parallel CSV testing.
- Successful execution of three ordered test suites.

The automated test count refers to parameterized pytest cases rather than the number of Python test function declarations.

The reported testing results were obtained from local execution and do not represent a verified GitHub Actions CI result.

## Project Conclusion

This project demonstrates the application of automated unit testing to a Python Flask To-Do List Application.

A total of **169 automated test cases** were executed successfully across three selected modules and an external CSV-driven suite. The combined test execution achieved **99% code coverage** for the assessed modules.

The project applies multiple software testing techniques, including ECP, BVA, state-transition testing, data-driven testing, parallel execution, and ordered test execution.

The test cases and their results are supported by Excel documentation, testing reports, and recorded execution evidence.

## Acknowledgment

This educational project is based on the open-source [Flask To-Do List Application by YugG03](https://github.com/YugG03/todo-flask-app).

The SQE group project focuses on automated testing, test design, documentation, and collaborative development.

---

**Software Quality Engineering — Group Project**

**Laiba Kashif (24F-3069) | Hamna Maryam (24F-3063)**

**BSE-5A | October 2026**
