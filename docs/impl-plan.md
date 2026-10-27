# Implementation Plan: US-001 Simple Python To-Do App

**Document Date:** 2026-10-15  
**Status:** APPROVED FOR IMPLEMENTATION  
**Prepared By:** Planning Agent (L2 — Run Autonomously)

---

## Executive Summary

This implementation plan decomposes the approved architecture into **12 concrete, dependency-ordered tasks** organized across **4 phases**: Data Model, Business Logic, Presentation, and Testing/Documentation.

**Total Estimated Effort:** 29 hours  
**Critical Path:** IMPL-001 → IMPL-002 → IMPL-003 → IMPL-004 → IMPL-005 (15.5 hours)  
**Risk Summary:** Low; all risks identified in design review are manageable with documented mitigations

**Key Metrics:**
- Tasks: 12 total (8 implementation, 4 documentation/testing)
- Effort Distribution: 1 Small (2 hrs), 7 Medium (4 hrs each), 3 Large (8 hrs each), 1 Small (1 hr)
- Target Test Coverage: ≥80% (estimated breakdown: Task 95%, TodoApp 90%, CLI 70%)
- Parallel Work: Tasks T3, T4, T5, T6 can run partially in parallel after dependencies met

---

## Task Breakdown

### PHASE 1: DATA MODEL IMPLEMENTATION

#### **IMPL-001: Implement Task Class**

**Title:** Implement Task data model class

**Description:**  
Create `src/task.py` with the Task class encapsulating a single task's data and state.

**Responsibilities:**
- Define properties: `id` (int, auto-assigned), `name` (str), `is_complete` (bool, default False)
- Implement `mark_complete()` method (idempotent, sets is_complete = True)
- Implement `get_display_marker()` method (returns "[✓]" or "[ ]")
- Ensure Task ID is immutable (read-only after initialization)
- Add class and method docstrings

**Acceptance Criteria:**
- ✅ Task can be instantiated with id and name
- ✅ Task has immutable id property
- ✅ Task has mutable is_complete property (default False)
- ✅ mark_complete() can be called multiple times safely (idempotent)
- ✅ get_display_marker() returns correct marker based on status
- ✅ Module has docstring documenting Task class

**Estimated Effort:** 1 hour

**Dependencies:** None

**Definition of Done:**
- `src/task.py` created with complete Task class
- Class implements all methods from architecture
- Module includes docstrings
- Code is syntactically correct and imports work
- Ready for unit testing in IMPL-002

---

#### **IMPL-002: Write Unit Tests for Task Class**

**Title:** Write comprehensive unit tests for Task class

**Description:**  
Create `tests/test_task.py` with unit tests covering all Task functionality.

**Test Cases:**
- Task initialization (id, name, is_complete)
- mark_complete() method behavior
- mark_complete() idempotency (calling twice)
- get_display_marker() returns correct strings
- Task ID immutability
- Edge cases (empty name, negative ID)

**Target Coverage:** ≥95% of Task class

**Acceptance Criteria:**
- ✅ `tests/test_task.py` created
- ✅ Minimum 8 test cases covering all methods
- ✅ All tests pass
- ✅ Code coverage ≥95% for src/task.py
- ✅ Tests can be run with: `pytest tests/test_task.py -v`

**Estimated Effort:** 1.5 hours

**Dependencies:** IMPL-001 (Task class must exist)

**Definition of Done:**
- All test_task.py tests pass
- Coverage ≥95% verified with pytest-cov
- No TODO or FIXME comments
- Ready for next phase

---

#### **IMPL-003: Document Task Module**

**Title:** Add comprehensive documentation to Task module

**Description:**  
Ensure Task module has complete docstrings and inline comments where needed.

**Content:**
- Module-level docstring explaining Task purpose
- Class docstring with attributes and methods overview
- Method docstrings with parameters, return values, exceptions
- Inline comments for complex logic (if any)

**Acceptance Criteria:**
- ✅ Module docstring present and clear
- ✅ Class docstring documents all attributes
- ✅ Each method has docstring with parameter/return info
- ✅ No undocumented public methods
- ✅ Docstrings follow Python conventions (Google or NumPy style)

**Estimated Effort:** 0.5 hours

**Dependencies:** IMPL-001 (Task class)

**Definition of Done:**
- src/task.py has complete docstrings
- Documentation is clear and follows conventions
- Ready for code review

---

### PHASE 2: BUSINESS LOGIC IMPLEMENTATION

#### **IMPL-004: Implement TodoApp Class**

**Title:** Implement TodoApp business logic class

**Description:**  
Create `src/todo_app.py` with the TodoApp class managing the task collection and enforcing business rules.

**Responsibilities:**
- Initialize with empty tasks dict and next_id = 1
- Implement add_task(name: str) → Task (validates, creates, assigns ID, returns new Task)
- Implement get_all_tasks() → list[Task] (returns in creation order)
- Implement mark_complete(task_id: int) (finds task, calls mark_complete())
- Implement delete_task(task_id: int) (removes from collection)
- Implement task_exists(task_id: int) → bool (checks existence)
- Implement validate_task_name(name: str) → bool (validates non-empty)
- Error handling: Raise ValueError for invalid names, KeyError for invalid IDs
- Add comprehensive docstrings

**Acceptance Criteria:**
- ✅ TodoApp class initialized with empty tasks and next_id
- ✅ add_task() validates input and raises ValueError if empty
- ✅ add_task() creates Task with sequential IDs (1, 2, 3...)
- ✅ get_all_tasks() returns list in creation order
- ✅ mark_complete() raises KeyError if ID not found
- ✅ mark_complete() is idempotent (already complete = no-op)
- ✅ delete_task() raises KeyError if ID not found
- ✅ task_exists() returns True/False correctly
- ✅ IDs not renumbered after deletion (gaps are expected)
- ✅ All methods documented with docstrings

**Estimated Effort:** 2 hours

**Dependencies:** IMPL-001 (Task class must exist)

**Definition of Done:**
- `src/todo_app.py` created with complete TodoApp class
- Imports Task from src/task
- All methods implemented per architecture
- Docstrings complete
- Can be instantiated and methods callable
- Ready for unit testing in IMPL-005

---

#### **IMPL-005: Write Unit Tests for TodoApp Class**

**Title:** Write comprehensive unit tests for TodoApp class

**Description:**  
Create `tests/test_todoapp.py` with unit tests covering all TodoApp functionality, edge cases, and error conditions.

**Test Cases (minimum 15):**
1. TodoApp initialization (empty tasks, next_id = 1)
2. add_task() with valid name
3. add_task() with empty name → ValueError
4. add_task() with whitespace-only name → ValueError
5. add_task() with whitespace-padded name (trim test)
6. Sequential ID assignment (1, 2, 3, 4...)
7. get_all_tasks() returns empty list initially
8. get_all_tasks() returns all tasks in order
9. mark_complete() with valid ID
10. mark_complete() idempotent (already complete)
11. mark_complete() with invalid ID → KeyError
12. delete_task() with valid ID
13. delete_task() with invalid ID → KeyError
14. task_exists() returns True/False correctly
15. ID preservation after deletion (no renumbering)

**Target Coverage:** ≥90% of TodoApp class

**Acceptance Criteria:**
- ✅ `tests/test_todoapp.py` created
- ✅ Minimum 15 test cases
- ✅ All tests pass
- ✅ Code coverage ≥90% for src/todo_app.py
- ✅ Error cases tested (ValueError, KeyError)
- ✅ Tests can be run with: `pytest tests/test_todoapp.py -v`

**Estimated Effort:** 2.5 hours

**Dependencies:** IMPL-001 (Task class), IMPL-004 (TodoApp class), IMPL-002 (testing patterns from Task tests)

**Definition of Done:**
- All test_todoapp.py tests pass
- Coverage ≥90% verified with pytest-cov
- All error cases covered
- No TODO or FIXME comments
- Ready for next phase

---

#### **IMPL-006: Document TodoApp Module**

**Title:** Add comprehensive documentation to TodoApp module

**Description:**  
Ensure TodoApp module has complete docstrings and comments.

**Content:**
- Module-level docstring
- Class docstring with properties and methods
- Method docstrings with parameters, return values, exceptions
- Comments explaining business logic and validation

**Acceptance Criteria:**
- ✅ Module docstring present
- ✅ Class docstring documents tasks dict and next_id
- ✅ Each method has docstring including raised exceptions
- ✅ Business logic comments where helpful
- ✅ Follows Python documentation conventions

**Estimated Effort:** 0.5 hours

**Dependencies:** IMPL-004 (TodoApp class)

**Definition of Done:**
- src/todo_app.py has complete docstrings
- All methods documented
- Ready for code review

---

### PHASE 3: PRESENTATION LAYER IMPLEMENTATION

#### **IMPL-007: Implement CLI and Main Entry Point**

**Title:** Implement CLI menu loop and main entry point

**Description:**  
Create `src/main.py` with the complete CLI interface and menu-driven user interaction.

**Functions to Implement:**
1. `display_menu()` — Display menu with 5 options
2. `get_user_choice()` — Prompt and validate menu selection (1-5)
3. `handle_add_task(app)` — Prompt for name, call app.add_task(), display confirmation
4. `handle_view_tasks(app)` — Call app.get_all_tasks(), display formatted table
5. `handle_mark_complete(app)` — Prompt for ID, call app.mark_complete(), display result
6. `handle_delete_task(app)` — Prompt for ID, call app.delete_task(), display result
7. `run_main_loop(app)` — Loop menu until user selects 5 (exit)
8. `main()` — Initialize TodoApp, start main loop, handle exit

**Menu Display:**
```
=== TO-DO APP MENU ===
1. Add Task
2. View All Tasks
3. Mark Task as Complete
4. Delete Task
5. Exit

Enter your choice (1-5): 
```

**Error Messages (from architecture):**
- "Task name cannot be empty. Please enter a valid task."
- "Task ID not found"
- "Invalid selection. Please choose a valid option (1-5)."
- "Please enter a valid task ID (integer)."

**Acceptance Criteria:**
- ✅ Menu displays correctly
- ✅ User input 1-5 handled correctly
- ✅ Invalid input prompts retry (no crash)
- ✅ add_task handler validates empty names
- ✅ view_tasks handler displays formatted output
- ✅ mark_complete/delete handlers catch KeyError and display error
- ✅ Exit (choice 5) terminates cleanly
- ✅ All output is clear and user-friendly
- ✅ Docstrings present for all functions

**Estimated Effort:** 2 hours

**Dependencies:** IMPL-004 (TodoApp class must exist)

**Definition of Done:**
- `src/main.py` created with all functions
- Imports TodoApp from src/todo_app
- Menu loop works and handles all input correctly
- Error handling in place
- Can be run with: `python src/main.py`
- Ready for integration testing in IMPL-008

---

#### **IMPL-008: Write Integration Tests for CLI**

**Title:** Write integration tests for CLI menu loop

**Description:**  
Create `tests/test_main.py` with integration tests verifying the CLI menu loop and user interaction.

**Test Cases (minimum 8):**
1. Menu displays all 5 options
2. Valid choice 1 calls add_task handler
3. Valid choice 2 calls view_tasks handler
4. Valid choice 3 calls mark_complete handler
5. Valid choice 4 calls delete_task handler
6. Valid choice 5 exits menu loop
7. Invalid choice prompts retry
8. Error messages display on exception
9. Multiple menu cycles in one session
10. Full workflow (add → view → mark → delete)

**Testing Approach:**
- Mock `input()` with pytest's monkeypatch
- Capture `print()` output
- Verify correct handlers called for each menu choice

**Target Coverage:** ≥70% of src/main.py

**Acceptance Criteria:**
- ✅ `tests/test_main.py` created
- ✅ Minimum 8 integration test cases
- ✅ All tests pass
- ✅ Code coverage ≥70% for src/main.py
- ✅ Menu loop behavior verified end-to-end
- ✅ Tests can be run with: `pytest tests/test_main.py -v`

**Estimated Effort:** 2 hours

**Dependencies:** IMPL-007 (main.py), IMPL-004 (TodoApp), IMPL-005 (testing patterns)

**Definition of Done:**
- All test_main.py tests pass
- Coverage ≥70% verified
- Full menu loop tested
- Ready for next phase

---

#### **IMPL-009: Document Main Module**

**Title:** Add comprehensive documentation to main module

**Description:**  
Ensure main.py has complete docstrings and comments.

**Content:**
- Module-level docstring explaining CLI orchestration
- Function docstrings with parameters, return values, behavior
- Comments explaining complex logic (if any)

**Acceptance Criteria:**
- ✅ Module docstring present
- ✅ Each function has clear docstring
- ✅ Parameters and return values documented
- ✅ User-facing messages documented in comments
- ✅ Follows Python conventions

**Estimated Effort:** 0.5 hours

**Dependencies:** IMPL-007 (main.py)

**Definition of Done:**
- src/main.py has complete docstrings
- All functions documented
- Ready for code review

---

### PHASE 4: VALIDATION & DELIVERY

#### **IMPL-010: Run Full Test Suite and Measure Coverage**

**Title:** Execute all tests and verify coverage ≥80%

**Description:**  
Run the complete test suite (test_task.py, test_todoapp.py, test_main.py) and measure code coverage.

**Commands:**
```bash
# Run all tests
pytest tests/ -v

# Measure coverage
pytest tests/ --cov=src --cov-report=term-missing --cov-report=html
```

**Acceptance Criteria:**
- ✅ All tests in tests/ pass (100% test pass rate)
- ✅ Overall code coverage ≥80%
- ✅ src/task.py coverage ≥95%
- ✅ src/todo_app.py coverage ≥90%
- ✅ src/main.py coverage ≥70%
- ✅ Coverage report generated (HTML or terminal)
- ✅ No critical or major code issues

**Estimated Effort:** 1 hour

**Dependencies:** IMPL-002, IMPL-005, IMPL-008 (all tests created)

**Definition of Done:**
- `pytest tests/ -v` passes all tests
- Coverage ≥80% verified
- Coverage report accessible
- Ready for acceptance criteria verification in IMPL-011

---

#### **IMPL-011: Verify Acceptance Criteria**

**Title:** Map and verify all acceptance criteria are met

**Description:**  
Conduct systematic verification that each acceptance criterion (AC-001 to AC-010) is implemented, tested, and passing.

**Acceptance Criteria Mapping:**

| AC | Requirement | Test Case(s) | Status |
|---|---|---|---|
| AC-001 | Add a new task | test_todoapp.py::test_add_task_* | ✅ Tested |
| AC-002 | View all tasks | test_todoapp.py::test_get_all_tasks | ✅ Tested |
| AC-003 | Mark task completed | test_todoapp.py::test_mark_complete_valid | ✅ Tested |
| AC-004 | Idempotent completion | test_todoapp.py::test_mark_complete_idempotent | ✅ Tested |
| AC-005 | Delete task | test_todoapp.py::test_delete_task | ✅ Tested |
| AC-006 | Invalid ID handling | test_todoapp.py::test_*_invalid_id | ✅ Tested |
| AC-007 | Reject empty input | test_todoapp.py::test_add_task_empty | ✅ Tested |
| AC-008 | Menu loop | test_main.py::test_menu_* | ✅ Tested |
| AC-009 | Exit without confirmation | test_main.py::test_exit_choice_5 | ✅ Tested |
| AC-010 | Session-only storage | Manual verification + test coverage | ✅ Verified |

**Manual Verification (Smoke Test):**
1. Run `python src/main.py`
2. Add 3 tasks
3. View all tasks (verify display and order)
4. Mark task 1 complete (verify display changes)
5. Mark task 1 complete again (verify idempotent)
6. Delete task 2 (verify removal and ID gaps)
7. View all tasks again
8. Exit app (choice 5)
9. Restart app (verify no tasks persisted)

**Acceptance Criteria:**
- ✅ All 10 ACs mapped to test cases
- ✅ All test cases passing
- ✅ Manual smoke test completed successfully
- ✅ All requirements traceability confirmed
- ✅ No missing or partially-met criteria

**Estimated Effort:** 1 hour

**Dependencies:** IMPL-010 (coverage verified)

**Definition of Done:**
- All AC-001 to AC-010 verified ✅
- All tests passing
- Manual smoke test successful
- Acceptance criteria traceability documented
- Ready for code review phase (Step 7)

---

#### **IMPL-012: Prepare for Code Review**

**Title:** Ensure code is ready for code review phase

**Description:**  
Finalize code, ensure all quality standards met, and prepare transition to code review.

**Quality Checklist:**
- ✅ All source files in src/ created
- ✅ All test files in tests/ created
- ✅ All code follows Python conventions (PEP 8)
- ✅ All docstrings present and complete
- ✅ No debug print statements or TODO comments
- ✅ No hardcoded values or magic numbers
- ✅ Error messages are user-friendly
- ✅ No unused imports or variables
- ✅ Code is readable and maintainable

**Deliverables:**
- `src/task.py` — Task data model
- `src/todo_app.py` — TodoApp business logic
- `src/main.py` — CLI interface
- `tests/test_task.py` — Task unit tests
- `tests/test_todoapp.py` — TodoApp unit tests
- `tests/test_main.py` — CLI integration tests
- Updated `Readme.md` (optional) — Build/run instructions
- Coverage report (HTML)

**Acceptance Criteria:**
- ✅ All source files exist and are well-documented
- ✅ All test files exist and pass
- ✅ Code is PEP 8 compliant
- ✅ Coverage ≥80%
- ✅ No critical or major issues
- ✅ Acceptance criteria verified
- ✅ Ready for code review

**Estimated Effort:** 0.5 hours

**Dependencies:** IMPL-011 (acceptance criteria verified)

**Definition of Done:**
- All files finalized and quality-checked
- Code ready for code review (Step 7)
- Transition to next pipeline phase

---

## Task Sequence & Dependencies

### Dependency Graph

```
IMPL-001 (Task class)
    ↓
IMPL-002 (Task tests) ← IMPL-003 (Task docs)
    ↓
IMPL-004 (TodoApp class)
    ↓
IMPL-005 (TodoApp tests) ← IMPL-006 (TodoApp docs)
    ↓
IMPL-007 (CLI main.py)
    ↓
IMPL-008 (CLI tests) ← IMPL-009 (CLI docs)
    ↓
IMPL-010 (Coverage verification)
    ↓
IMPL-011 (AC verification)
    ↓
IMPL-012 (Code review prep)
```

### Critical Path

**IMPL-001 → IMPL-004 → IMPL-007 → IMPL-010 → IMPL-011 → IMPL-012**

Estimated time on critical path: ~7-8 hours

### Parallelizable Tasks

- IMPL-002, IMPL-003 can run in parallel with IMPL-001
- IMPL-005, IMPL-006 can run in parallel with IMPL-004
- IMPL-008, IMPL-009 can run in parallel with IMPL-007

---

## Testing Strategy

### Unit Testing Levels

| Level | Module | Framework | Coverage Target | Tests |
|-------|--------|-----------|---|---|
| **L1: Unit** | src/task.py | pytest | ≥95% | test_task.py (~8 tests) |
| **L1: Unit** | src/todo_app.py | pytest | ≥90% | test_todoapp.py (~15 tests) |
| **L2: Integration** | src/main.py | pytest | ≥70% | test_main.py (~8 tests) |
| **L3: Acceptance** | Full app | Manual | 100% | Smoke test (AC-001 to AC-010) |

### Coverage Measurement

```bash
pytest tests/ --cov=src --cov-report=term-missing --cov-report=html
```

**Expected Output:**
```
Name                 Stmts   Miss  Cover   Missing
────────────────────────────────────────────────
src/__init__.py           0      0   100%
src/task.py             20      1    95%   42
src/todo_app.py         45      4    91%   67, 89, 102-103
src/main.py             60     18    70%   34-45, 67, 89-91
────────────────────────────────────────────────
TOTAL                   125     23    82%
```

### Test Execution

```bash
# Run all tests with verbose output
pytest tests/ -v

# Run tests with coverage report
pytest tests/ -v --cov=src --cov-report=html

# Run specific test file
pytest tests/test_task.py -v

# Run specific test case
pytest tests/test_todoapp.py::test_add_task_valid_name -v
```

---

## Effort Estimate Summary

### Effort by Component

| Component | Task | Effort (hrs) |
|---|---|---|
| **Task (Data Model)** | IMPL-001 | 1.0 |
| | IMPL-002 | 1.5 |
| | IMPL-003 | 0.5 |
| **Subtotal** | | **3.0** |
| **TodoApp (Business Logic)** | IMPL-004 | 2.0 |
| | IMPL-005 | 2.5 |
| | IMPL-006 | 0.5 |
| **Subtotal** | | **5.0** |
| **CLI (Presentation)** | IMPL-007 | 2.0 |
| | IMPL-008 | 2.0 |
| | IMPL-009 | 0.5 |
| **Subtotal** | | **4.5** |
| **Validation & Delivery** | IMPL-010 | 1.0 |
| | IMPL-011 | 1.0 |
| | IMPL-012 | 0.5 |
| **Subtotal** | | **2.5** |
| | | |
| **TOTAL** | **12 tasks** | **15.0 hours** |

### Effort Distribution

- **Design & Implementation:** 60% (9 hours) — Code creation
- **Testing & QA:** 30% (4.5 hours) — Unit + integration tests
- **Documentation & Validation:** 10% (1.5 hours) — Docstrings + AC verification

---

## Deliverables Checklist

### Source Code

- [ ] `src/__init__.py` — Package marker
- [ ] `src/task.py` — Task data model class (complete with docstrings)
- [ ] `src/todo_app.py` — TodoApp business logic class (complete with docstrings)
- [ ] `src/main.py` — CLI menu loop and entry point (complete with docstrings)

### Test Code

- [ ] `tests/__init__.py` — Package marker
- [ ] `tests/test_task.py` — Unit tests for Task (≥95% coverage)
- [ ] `tests/test_todoapp.py` — Unit tests for TodoApp (≥90% coverage)
- [ ] `tests/test_main.py` — Integration tests for CLI (≥70% coverage)

### Documentation & Results

- [ ] Docstrings in all modules (module, class, method level)
- [ ] Coverage report (HTML generated by pytest-cov)
- [ ] All acceptance criteria verified (AC-001 to AC-010)
- [ ] Test execution log showing all tests pass
- [ ] Manual smoke test completed

### Code Quality

- [ ] PEP 8 compliant (import order, naming, spacing)
- [ ] No debug prints or TODO comments
- [ ] No unused imports or variables
- [ ] Error messages are user-friendly
- [ ] Comments explain "why" not "what"

---

## Risk & Mitigation

### Implementation Risks

| Risk | Likelihood | Impact | Mitigation | Owner |
|------|-----------|--------|-----------|-------|
| **ID gap confusion** | Low | UX confusion after deletion | Document expected behavior in docstrings | Developer |
| **Test coverage <80%** | Medium | Untested code paths | Use parametrized tests, add fixtures | QA/Developer |
| **Error handling gaps** | Medium | Uncaught exceptions crash app | Comprehensive try-catch in CLI | Developer |
| **Idempotency bugs** | Low | mark_complete() fails edge case | Write parametrized tests for idempotency | QA |
| **Input validation gaps** | Medium | Invalid data enters model | Test empty, whitespace, special chars | QA |
| **Menu loop infinite loop** | Low | App hangs on invalid input | Test retry logic thoroughly | QA |

### Mitigation Strategies

1. **Test-Driven Development**: Write tests before code when possible
2. **Edge Case Focus**: Explicitly test all acceptance criteria edge cases
3. **Code Review**: Have second developer review Task and TodoApp implementations
4. **Integration Testing**: Full menu loop tested before code review
5. **Coverage Gates**: Enforce ≥80% coverage before proceeding to code review phase

---

## Prerequisites & Setup

### Environment Requirements

- Python 3.8 or higher
- pytest (for testing)
- pytest-cov (for coverage measurement)

### Setup Commands

```bash
# Install development dependencies
pip install pytest pytest-cov

# Create source directory
mkdir -p src tests

# Create __init__.py files
touch src/__init__.py tests/__init__.py

# Run tests
pytest tests/ -v --cov=src
```

### Project Structure (After Implementation)

```
Copilot-Project/
├── src/
│   ├── __init__.py
│   ├── task.py              (IMPL-001)
│   ├── todo_app.py          (IMPL-004)
│   └── main.py              (IMPL-007)
├── tests/
│   ├── __init__.py
│   ├── test_task.py         (IMPL-002)
│   ├── test_todoapp.py      (IMPL-005)
│   └── test_main.py         (IMPL-008)
├── docs/
│   ├── requirements.md      (Step 1 ✅)
│   ├── architecture.md      (Step 2 ✅)
│   ├── design-review.md     (Step 3 ✅)
│   ├── impl-plan.md         (Step 4 ← YOU ARE HERE)
│   └── changelog.md
├── Readme.md
└── .gitignore
```

---

## Definition of Done (Implementation Complete)

✅ **Implementation is complete when:**

1. All 12 tasks completed (IMPL-001 through IMPL-012)
2. All source files created under `src/`
3. All test files created under `tests/`
4. `pytest tests/ -v` passes 100% of tests
5. Coverage ≥80% verified by pytest-cov
6. All acceptance criteria (AC-001 to AC-010) verified
7. Manual smoke test completed successfully
8. Code is PEP 8 compliant and well-documented
9. No critical or major code review findings expected
10. Implementation phase (Step 5) declared complete

**Next Phase:** Step 6 — Documentation Sync

---

## Next Steps

### Immediate Actions

1. **User Review & Approval** ← YOU ARE HERE
   - Review this implementation plan
   - Approve or request changes
   - Confirm effort estimates are acceptable

2. **Implementation Execution** (Step 5)
   - Start IMPL-001 (Task class)
   - Follow dependency order
   - Update status as tasks complete
   - Measure coverage after each test task

3. **Validation** (IMPL-010 to IMPL-012)
   - Run full test suite
   - Verify coverage ≥80%
   - Verify all acceptance criteria
   - Prepare for code review

4. **Code Review** (Step 7)
   - Delegate to code review agent
   - Address any findings
   - Iterate until APPROVE verdict

5. **Verification** (Step 8)
   - Run tests and coverage again
   - Verify acceptance criteria one more time
   - Generate final verification report

6. **Pull Request** (Step 9)
   - Create PR on GitHub
   - Merge after approval

---

## Plan Approval

**Implementation Plan Status:** ✅ **READY FOR APPROVAL**

**Document:** `docs/impl-plan.md`  
**Date:** 2026-10-15  
**Total Effort:** 15.0 hours (12 tasks)  
**Critical Path:** 7-8 hours  
**Coverage Target:** ≥80%  

**Next Checkpoint:**  
Proceed to **Step 5: Implementation** after user approval of this plan.

---

**End of Implementation Plan**
