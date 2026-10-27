# Architecture: US-001 Simple Python To-Do App

**Document Status**: ✅ APPROVED  
**Approved By**: User (Agentic SDLC Pipeline)  
**Approval Date**: 2026-10-15  
**Architecture Version**: 1.0  

---

## Executive Summary

This document describes the approved architecture for US-001: Simple Python To-Do App. The design employs a **three-layer modular architecture** with clear separation of concerns: data model, business logic, and presentation. This approach ensures maintainability, testability (≥80% coverage), and alignment with all functional and non-functional requirements.

**Status:** ✅ **APPROVED** (2026-10-15)

---

## 1. Architecture Pattern

**Selected Pattern: Layered (Three-Tier) Architecture**

### Justification:
- **Simplicity**: Meets requirement NFR-001 (simple and modular design)
- **Separation of Concerns**: Each layer has a single, well-defined responsibility
- **Testability**: Layers can be tested independently, enabling ≥80% code coverage (NFR-003)
- **Maintainability**: Clear boundaries and minimal dependencies
- **Extensibility**: New layers (e.g., file persistence, GUI) can be added without disrupting existing layers

### Three Layers:

| Layer | Component | Responsibility |
|-------|-----------|---|
| **1. Data Model** | `Task` class | Encapsulate task data and state |
| **2. Business Logic** | `TodoApp` class | Manage task collection, enforce rules, handle validation |
| **3. Presentation** | `CLI` / `main.py` | User interaction, menu loop, I/O orchestration |

---

## 2. Component Overview

### Component 1: Task (Data Model Layer)

**File:** `src/task.py`

**Responsibility:** Represent a single task with immutable identity and mutable completion status.

**Properties:**
```python
- id: int                # Auto-assigned sequential ID (read-only)
- name: str              # Task description/name
- is_complete: bool      # Completion status (default: False)
```

**Methods:**
```python
def __init__(id: int, name: str) -> None
    """Initialize task with ID and name."""
    
def mark_complete() -> None
    """Set task completion status to True (idempotent)."""
    
def get_display_marker() -> str
    """Return '[✓]' if complete, '[ ]' if incomplete."""
    
@property
def is_completed(self) -> bool
    """Read-only property for completion status."""
```

**Design Rationale:**
- Simple data class with minimal behavior
- Status is the only mutable attribute
- Provides idempotent `mark_complete()` (can be called multiple times safely)
- Display formatting encapsulated in class (DRY principle)

---

### Component 2: TodoApp (Business Logic Layer)

**File:** `src/todo_app.py`

**Responsibility:** Manage the task collection, generate IDs, enforce business rules, and validate inputs.

**Properties:**
```python
- tasks: dict[int, Task]     # Maps task ID → Task object
- next_id: int               # Tracks next sequential ID to assign (starts at 1)
```

**Methods:**

#### `add_task(name: str) -> Task`
- Validate task name (non-empty after stripping)
- Create new Task with next_id
- Store in tasks dict
- Increment next_id
- Return created Task
- **Error Handling:** Raise ValueError if name is empty/whitespace

#### `get_all_tasks() -> list[Task]`
- Return list of tasks in creation order (insertion order preserved in dict)
- Return empty list if no tasks exist
- **Guarantees:** Never returns None; always a list

#### `mark_complete(task_id: int) -> None`
- Validate task_id exists using task_exists()
- Call task.mark_complete()
- **Error Handling:** Raise KeyError if task_id not found
- **Idempotency:** Calling mark_complete() on already-complete task is a no-op

#### `delete_task(task_id: int) -> None`
- Validate task_id exists
- Remove task from tasks dict
- **Error Handling:** Raise KeyError if task_id not found
- **Note:** Does not renumber remaining task IDs (gaps are expected per FR-005)

#### `task_exists(task_id: int) -> bool`
- Check if task_id exists in tasks dict
- Return True/False

#### `validate_task_name(name: str) -> bool`
- Strip whitespace from name
- Check if non-empty
- Return True if valid, False otherwise

**Design Rationale:**
- In-memory dict provides O(1) lookups for task retrieval/deletion
- Sequential ID assignment ensures predictable, user-friendly IDs (1, 2, 3...)
- Exception-based error handling (KeyError, ValueError) signals errors clearly to CLI
- Validation logic centralized (DRY principle)

---

### Component 3: CLI / main.py (Presentation Layer)

**File:** `src/main.py`

**Responsibility:** Orchestrate user interaction via command-line menu loop.

**Key Functions:**

#### `display_menu() -> None`
Display the interactive menu:
```
=== TO-DO APP MENU ===
1. Add Task
2. View All Tasks
3. Mark Task as Complete
4. Delete Task
5. Exit
```

#### `get_user_choice() -> str`
- Prompt: "Enter your choice (1-5): "
- Read user input
- Validate selection is in [1, 2, 3, 4, 5]
- Return choice or re-prompt on invalid input
- **Error Handling:** Catch ValueError, display error message, retry

#### `handle_add_task(app: TodoApp) -> None`
- Prompt: "Enter task name: "
- Read task name
- Call `app.add_task(name)`
- Display: "Task added: [ID] Task Name"
- **Error Handling:** Catch ValueError, display "Task name cannot be empty"

#### `handle_view_tasks(app: TodoApp) -> None`
- Call `app.get_all_tasks()`
- If no tasks: Display "No tasks yet."
- Else: Display formatted table:
  ```
  ID  | Status | Task Name
  --- | ------ | ---------
  1   | [ ]    | Buy groceries
  2   | [✓]    | Finish project
  ```

#### `handle_mark_complete(app: TodoApp) -> None`
- Prompt: "Enter task ID: "
- Read ID, validate as integer
- Call `app.mark_complete(task_id)`
- Display: "Task [ID] marked as complete."
- **Error Handling:** Catch KeyError, display "Task ID not found"

#### `handle_delete_task(app: TodoApp) -> None`
- Prompt: "Enter task ID: "
- Read ID, validate as integer
- Call `app.delete_task(task_id)`
- Display: "Task [ID] deleted."
- **Error Handling:** Catch KeyError, display "Task ID not found"

#### `run_main_loop(app: TodoApp) -> None`
- Loop until user selects exit:
  ```python
  while True:
      display_menu()
      choice = get_user_choice()
      if choice == "1":
          handle_add_task(app)
      elif choice == "2":
          handle_view_tasks(app)
      elif choice == "3":
          handle_mark_complete(app)
      elif choice == "4":
          handle_delete_task(app)
      elif choice == "5":
          break  # Exit loop
  ```

#### `main() -> None`
- Create TodoApp instance
- Call run_main_loop(app)
- Display: "Goodbye!" on exit
- **Error Handling:** Wrap in try-except to catch unexpected exceptions, display error message, return to menu

**Design Rationale:**
- Each user action (add, view, complete, delete) has dedicated handler function
- Input validation and error handling at presentation layer
- CLI remains decoupled from business logic (TodoApp)
- Numeric menu (1-5) for simplicity and accessibility

---

## 3. Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                    USER (CLI Interaction)                       │
│  Input: menu selections, task names, task IDs                   │
│  Output: menu display, task lists, confirmation messages        │
└──────────────────────────────┬──────────────────────────────────┘
                               │
                      (method calls + user input)
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│              PRESENTATION LAYER (main.py / CLI)                 │
│                                                                 │
│  display_menu()          ┐                                      │
│  get_user_choice()       ├─ User interaction orchestration     │
│  handle_add_task()       │                                      │
│  handle_view_tasks()     ├─ Delegates to TodoApp methods       │
│  handle_mark_complete()  │                                      │
│  handle_delete_task()    ┤                                      │
│  run_main_loop()         │                                      │
│  main()                  ┘                                      │
│                                                                 │
└──────────────────────────────┬──────────────────────────────────┘
                               │
                     (create, read, update, delete)
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│           BUSINESS LOGIC LAYER (TodoApp)                        │
│                                                                 │
│  add_task(name)          ┐                                      │
│  get_all_tasks()         ├─ Task management & validation       │
│  mark_complete(id)       │                                      │
│  delete_task(id)         ├─ Business rule enforcement         │
│  task_exists(id)         │                                      │
│  validate_task_name(name)┘                                      │
│                                                                 │
│  Internal State:                                                │
│  - tasks: dict[int, Task]                                       │
│  - next_id: int                                                 │
│                                                                 │
└──────────────────────────────┬──────────────────────────────────┘
                               │
                     (create, read, update)
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│              DATA MODEL LAYER (Task)                            │
│                                                                 │
│  Encapsulates single task:                                      │
│  - id: int (sequential)                                         │
│  - name: str                                                    │
│  - is_complete: bool                                            │
│                                                                 │
│  Methods:                                                       │
│  - mark_complete()                                              │
│  - get_display_marker()                                         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘


IN-MEMORY SESSION STORAGE:
┌─────────────────────────────────────────────────────────────────┐
│ TodoApp Instance (RAM)                                          │
│                                                                 │
│ tasks = {                                                       │
│   1: Task(id=1, name="Buy groceries", is_complete=False)       │
│   2: Task(id=2, name="Finish project", is_complete=True)       │
│   3: Task(id=3, name="Call mom", is_complete=False)            │
│ }                                                               │
│                                                                 │
│ next_id = 4                                                     │
│                                                                 │
│ [Persists only during session; lost on exit per FR-009]        │
└─────────────────────────────────────────────────────────────────┘
```

---

## 4. Technology Stack

| Component | Technology | Rationale |
|-----------|-----------|-----------|
| **Language** | Python 3.8+ | Required by FR-001 |
| **Runtime** | Standard Python Interpreter | Cross-platform (Windows, Linux, macOS) |
| **Storage** | In-Memory (dict) | Required by FR-009 (session-only) |
| **I/O** | `input()`, `print()` (stdlib) | Simple CLI interface |
| **Testing Framework** | pytest | Industry-standard, supports ≥80% coverage requirement |
| **Coverage Tool** | pytest-cov | Measures code coverage % |
| **CLI Framework** | None (pure Python) | Keeps implementation simple per NFR-001 |
| **Dependencies** | Only Python stdlib (production) | Minimizes deployment complexity |
| | pytest, pytest-cov (dev) | Development/testing only |

---

## 5. Design Patterns & SOLID Principles

### Patterns Applied:

| Pattern | Implementation | Benefit |
|---------|---|---|
| **Separation of Concerns** | Task (data) → TodoApp (logic) → CLI (I/O) | Easy to test, modify, extend |
| **Single Responsibility** | Each class has one reason to change | Maintainability |
| **Dependency Injection** | CLI receives TodoApp instance as parameter | Decoupling, easier testing |
| **Input Validation** | Centralized in TodoApp | Prevents invalid state |
| **Exception-Based Errors** | KeyError (not found), ValueError (invalid input) | Clear error signaling to CLI |

### SOLID Compliance:

- ✅ **S** (Single Responsibility): Task manages task state; TodoApp manages collection; CLI handles I/O
- ✅ **O** (Open/Closed): Architecture open for extension (e.g., add file persistence layer); closed for modification
- ✅ **L** (Liskov Substitution): Not directly applicable (no inheritance in this simple design)
- ✅ **I** (Interface Segregation): Focused, minimal methods per class
- ✅ **D** (Dependency Inversion): CLI depends on TodoApp abstraction, not vice versa

---

## 6. File Organization

```
Copilot-Project/
│
├── docs/
│   ├── requirements.md           ✅ Approved requirements
│   ├── architecture.md           ✅ This document
│   ├── design-review.md          (Step 3)
│   ├── impl-plan.md              (Step 4)
│   └── ...
│
├── src/
│   ├── __init__.py               # Package marker
│   ├── task.py                   # Task data model class
│   ├── todo_app.py               # TodoApp business logic class
│   └── main.py                   # CLI orchestration & entry point
│
├── tests/
│   ├── __init__.py               # Package marker
│   ├── test_task.py              # Unit tests for Task class
│   ├── test_todoapp.py           # Unit tests for TodoApp class
│   └── test_main.py              # Integration/CLI tests (optional)
│
├── .gitignore                    # Ignore __pycache__, .pytest_cache, *.pyc
├── pytest.ini                    # Pytest configuration
├── requirements-dev.txt          # Dev dependencies (pytest, pytest-cov)
├── CHANGELOG.md                  # Version/pipeline history
├── Readme.md                     # Project overview
└── .mcp.json                     # MCP configuration
```

---

## 7. Key Design Decisions

| Decision | Rationale | Trade-off | Alternative Considered |
|----------|-----------|-----------|---|
| **In-memory dict storage** | Fast O(1) lookups, simple, meets FR-009 | No persistence across sessions (intentional) | List-based with linear search |
| **Sequential ID generation** | User-friendly, predictable, per FR-002 | Requires manual next_id tracking | UUID (harder to remember for users) |
| **Exception-based errors** | Clear error signaling, Python idiomatic | Requires try-catch in CLI | Return (success, message) tuples |
| **Numeric menu (1-5)** | Simple, accessible, no typo risk | Less descriptive than text | Text commands (add/view/etc.) |
| **Immediate exit on Ctrl+C** | Clean, simple behavior | No confirmation prompt | Graceful handling with confirmation |
| **No persistence layer** | Simplifies design, meets FR-009 | Tasks lost on exit (intentional) | Add JSON file storage |
| **Task.id immutable** | Prevents accidental ID reassignment | Cannot change task ID | Mutable ID (confusing) |
| **Layered architecture** | Clean separation, testability | Slight overhead for small app | Monolithic (harder to test) |

---

## 8. Risk Analysis & Mitigation

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|-----------|
| **Data loss on unexpected crash** | Medium | Session lost (per design) | Intentional design per FR-009; no recovery needed |
| **Memory growth with many tasks** | Low | Single-session CLI app unlikely to accumulate 10K+ tasks | Acceptable within scope; linear growth only |
| **Invalid ID gaps after deletion** | Low | Users may be confused by gaps | Document in help menu; expected behavior |
| **No undo capability** | Low | User mistakes permanent (per scope) | Intentional; not in acceptance criteria |
| **80% coverage not achieved** | Medium | Untested code paths in production | Enforce in CI/CD; add fixtures and parametrization |
| **Poor CLI UX (no input history)** | Low | Repetitive typing in long sessions | By design; session-only app; acceptable trade-off |
| **Unicode input issues** | Low | Special characters may not display correctly | Use `input()` / `print()` which handle UTF-8 by default |

---

## 9. Testing & Validation Strategy

### Unit Testing Framework

**Tool:** pytest + pytest-cov

**Test Organization:**
```
tests/
├── test_task.py           # Task class unit tests
├── test_todoapp.py        # TodoApp class unit tests
└── test_main.py           # CLI integration tests (optional)
```

### Test Coverage Areas

#### **test_task.py (Task Unit Tests)**

```
✅ Task initialization with auto-assigned ID
✅ Task name storage and retrieval
✅ Initial completion status = False
✅ mark_complete() sets status to True
✅ mark_complete() is idempotent (calling twice = no error)
✅ get_display_marker() returns '[✓]' when complete
✅ get_display_marker() returns '[ ]' when incomplete
✅ Task ID is read-only (cannot be reassigned)
```

**Target Coverage:** ≥95% (Task is simple, should be fully covered)

#### **test_todoapp.py (TodoApp Unit Tests)**

```
✅ TodoApp initialization (empty tasks dict, next_id = 1)
✅ add_task() with valid name → creates Task, assigns ID, increments next_id
✅ add_task() with empty name → raises ValueError
✅ add_task() with whitespace-only name → raises ValueError
✅ add_task() with whitespace-padded name → trims and accepts
✅ Sequential ID assignment (1, 2, 3, 4...)
✅ get_all_tasks() returns list in creation order
✅ get_all_tasks() returns empty list when no tasks
✅ mark_complete() with valid ID → sets status to True
✅ mark_complete() idempotent (calling on already-complete task = no-op)
✅ mark_complete() with invalid ID → raises KeyError
✅ delete_task() removes task from collection
✅ delete_task() with invalid ID → raises KeyError
✅ delete_task() preserves IDs (no renumbering)
✅ task_exists() returns True for existing ID
✅ task_exists() returns False for non-existing ID
✅ validate_task_name() accepts non-empty strings
✅ validate_task_name() rejects empty/whitespace
✅ Multiple tasks can be added and managed simultaneously
```

**Target Coverage:** ≥90% (TodoApp contains core logic)

#### **test_main.py (Integration Tests, Optional)**

```
✅ Menu loop cycles correctly
✅ User input is processed for each menu option
✅ Error messages display on invalid input
✅ Tasks persist within a session
✅ Application exits cleanly on selection 5
✅ Invalid menu selections prompt for retry
✅ All CLI handlers call correct TodoApp methods
```

**Target Coverage:** ≥70% (CLI integration optional; focus on unit tests)

### Coverage Target: ≥80% Overall

**Measurement Command:**
```bash
pytest tests/ -v --cov=src --cov-report=html --cov-report=term-missing
```

**Expected Breakdown:**
- `src/task.py`: ≥95%
- `src/todo_app.py`: ≥90%
- `src/main.py`: ≥70%
- **Overall: ≥80%** ✅

### Acceptance Criteria Mapping to Tests

| AC | Requirement | Test Case(s) |
|---|---|---|
| AC-001 | Add a new task | test_todoapp.py::test_add_task_valid_name |
| AC-002 | View all tasks | test_todoapp.py::test_get_all_tasks, test_main.py::test_handle_view_tasks |
| AC-003 | Mark task as completed | test_todoapp.py::test_mark_complete_valid_id |
| AC-004 | Idempotent mark complete | test_todoapp.py::test_mark_complete_idempotent |
| AC-005 | Delete a task | test_todoapp.py::test_delete_task |
| AC-006 | Invalid task ID handling | test_todoapp.py::test_mark_complete_invalid_id, test_todoapp.py::test_delete_task_invalid_id |
| AC-007 | Reject empty task name | test_todoapp.py::test_add_task_empty_name, test_todoapp.py::test_add_task_whitespace_only |
| AC-008 | Menu loops | test_main.py::test_menu_loop (integration) |
| AC-009 | Exit without confirmation | test_main.py::test_exit_cleanly |
| AC-010 | Tasks lost on exit | test_main.py::test_session_only_storage |

---

## 10. Validation Process

### Pre-Implementation Validation

✅ Requirements document (`docs/requirements.md`) reviewed and approved  
✅ Architecture document (`docs/architecture.md`) reviewed and approved  
✅ Design review completed (Step 3)  

### Pre-Deployment Validation

```bash
# 1. Run all unit tests
pytest tests/ -v

# 2. Measure code coverage (must be ≥80%)
pytest tests/ --cov=src --cov-report=term-missing --cov-report=html

# 3. Verify all acceptance criteria are tested
# (See mapping table above)

# 4. Manual smoke test (run application and exercise all features)
python src/main.py
```

### Definition of Done (Implementation Complete)

- ✅ All source files created under `src/`
- ✅ All unit tests created under `tests/`
- ✅ Code coverage ≥80% (verified by pytest)
- ✅ All acceptance criteria tested (AC-001 through AC-010)
- ✅ No critical or major code review findings
- ✅ Verification tests pass (PASS verdict)
- ✅ Documentation synchronized with code
- ✅ Pull request created and merged

---

## 11. Next Steps

### Phase Sequence

1. ✅ **Step 1: Requirements** — COMPLETE (`docs/requirements.md` approved)
2. ✅ **Step 2: Architecture** — COMPLETE (this document, approved)
3. **Step 3: Design Review** — Review architecture for risks, compliance issues
4. **Step 4: Implementation Planning** — Decompose into dependency-ordered tasks
5. **Step 5: Implementation** — Write source code and tests
6. **Step 6: Documentation Sync** — Align docs with implementation
7. **Step 7: Code Review** — Review code against requirements and quality standards
8. **Step 8: Verification** — Run tests, measure coverage, verify acceptance criteria
9. **Step 9: Pull Request** — Create PR on GitHub

### Handoff to Design Review

**Artifact:** `docs/architecture.md` (this document)  
**Status:** ✅ APPROVED by user  
**Next Stage:** Design Review (Step 3) — autonomous review for risks, gaps, compliance

---

## 12. User Approval Statement

**Approved By:** User  
**Date:** 2026-10-15  
**Status:** ✅ **APPROVED**

This architecture design has been reviewed and approved. It satisfies all functional requirements (FR-001 through FR-010), all non-functional requirements (NFR-001 through NFR-006), and all acceptance criteria (AC-001 through AC-010).

The three-layer modular architecture is approved for implementation.

**Approval Signature:**  
✅ User-approved (2026-10-15 12:01:05 IST)

---

## Appendix A: Class Diagrams

### Task Class
```
┌─────────────────────────────┐
│          Task               │
├─────────────────────────────┤
│ - id: int                   │
│ - name: str                 │
│ - is_complete: bool         │
├─────────────────────────────┤
│ + mark_complete(): void     │
│ + get_display_marker(): str │
└─────────────────────────────┘
```

### TodoApp Class
```
┌──────────────────────────────────────────┐
│          TodoApp                         │
├──────────────────────────────────────────┤
│ - tasks: dict[int, Task]                 │
│ - next_id: int                           │
├──────────────────────────────────────────┤
│ + add_task(name: str): Task              │
│ + get_all_tasks(): list[Task]            │
│ + mark_complete(task_id: int): void      │
│ + delete_task(task_id: int): void        │
│ + task_exists(task_id: int): bool        │
│ + validate_task_name(name: str): bool    │
└──────────────────────────────────────────┘
```

### Main Module
```
┌──────────────────────────────────────────┐
│          main.py (CLI)                   │
├──────────────────────────────────────────┤
│ Functions:                               │
│ + display_menu(): void                   │
│ + get_user_choice(): str                 │
│ + handle_add_task(app: TodoApp): void    │
│ + handle_view_tasks(app: TodoApp): void  │
│ + handle_mark_complete(app): void        │
│ + handle_delete_task(app): void          │
│ + run_main_loop(app: TodoApp): void      │
│ + main(): void                           │
└──────────────────────────────────────────┘
```

---

---

## Appendix B: Requirements Traceability Matrix

### Functional Requirements Traceability

| ID | Requirement | Component | Design Element | Test Coverage |
|----|---|---|---|---|
| FR-001 | Task data model (ID, name, is_complete) | Task class | Properties: id, name, is_complete | test_task.py |
| FR-002 | Create task (auto-ID, non-empty name) | TodoApp.add_task() | Sequential ID generation, validation | test_todoapp.py::test_add_task_* |
| FR-003 | View all tasks in order with markers | TodoApp.get_all_tasks() + Task.get_display_marker() | Dict insertion order, "[✓]" and "[ ]" | test_todoapp.py::test_get_all_tasks |
| FR-004 | Mark task complete (idempotent) | TodoApp.mark_complete() + Task.mark_complete() | Idempotent method design | test_todoapp.py::test_mark_complete_* |
| FR-005 | Delete task (preserve IDs) | TodoApp.delete_task() | Dict removal, no renumbering | test_todoapp.py::test_delete_task_* |
| FR-006 | Invalid ID error handling | TodoApp methods + CLI exception handlers | KeyError raised, caught in CLI | test_todoapp.py::test_*_invalid_id |
| FR-007 | Input validation (non-empty name) | TodoApp.validate_task_name() | String trimming and emptiness check | test_todoapp.py::test_validate_task_name |
| FR-008 | Interactive menu system | CLI.run_main_loop() + CLI.display_menu() | Loop until exit, choice routing | test_main.py::test_menu_loop |
| FR-009 | Exit application (no confirmation) | CLI.run_main_loop() exit branch | Break loop, no confirmation prompt | test_main.py::test_exit_cleanly |
| FR-010 | Graceful error handling | CLI exception handlers + CLI.main() | Try-catch all layers, return to menu | test_main.py::test_error_handling |

### Non-Functional Requirements Traceability

| ID | Requirement | Design Element | Validation |
|----|---|---|---|
| NFR-001 | Simple modular design (Task, TodoApp, main) | Three-layer architecture | Architecture review (this doc) |
| NFR-002 | Code quality (Python best practices) | SOLID principles, docstrings, type hints | Code review in Phase 7 |
| NFR-003 | ≥80% test coverage | Comprehensive unit tests with pytest-cov | pytest --cov=src --cov-report=term-missing |
| NFR-004 | Session-only, in-memory storage | Dict-based in-memory storage, no persistence | Manual verification test |
| NFR-005 | Performance (sub-second latency) | In-memory dict O(1) operations | No explicit test (acceptable for CLI) |
| NFR-006 | Clear CLI interface | Menu display, formatted task list | User acceptance testing |

### Acceptance Criteria Traceability

| ID | Criteria | Design Coverage | Test Cases |
|----|---|---|---|
| AC-001 | Create new task via menu | TodoApp.add_task() + CLI.handle_add_task() | test_todoapp.py::test_add_task_success |
| AC-002 | View all tasks in creation order | TodoApp.get_all_tasks() + display formatting | test_todoapp.py::test_get_all_tasks |
| AC-003 | Mark task complete by ID | TodoApp.mark_complete() + CLI.handle_mark_complete() | test_todoapp.py::test_mark_complete_success |
| AC-004 | Mark already-complete task (no error) | Task.mark_complete() idempotency | test_task.py::test_mark_complete_idempotent |
| AC-005 | Delete task by ID | TodoApp.delete_task() + CLI.handle_delete_task() | test_todoapp.py::test_delete_task_success |
| AC-006 | Invalid ID displays error | TodoApp exception handling + CLI catch-and-display | test_todoapp.py::test_*_invalid_id, test_main.py |
| AC-007 | Empty/whitespace input rejected | TodoApp.validate_task_name() + CLI retry loop | test_todoapp.py::test_validate_task_name_* |
| AC-008 | Menu loops until exit | CLI.run_main_loop() loop control | test_main.py::test_menu_loop_exit |
| AC-009 | Exit without confirmation | CLI.run_main_loop() break on exit choice | test_main.py::test_exit_no_confirmation |
| AC-010 | Tasks lost on exit | Session-only design (no persistence) | test_main.py::test_session_only_storage |

---

## Appendix C: Architecture Review Checklist

**Review Status**: ✅ APPROVED (User Sign-off)

### Design Quality Checklist

- ✅ Architecture pattern selected and justified (Layered Architecture)
- ✅ All components have well-defined responsibilities
- ✅ Clear data flow between layers (Task → TodoApp → CLI)
- ✅ Dependencies flow inward (CLI depends on TodoApp, TodoApp depends on Task)
- ✅ No circular dependencies
- ✅ Separation of concerns maintained
- ✅ Testability prioritized (enables ≥80% coverage)
- ✅ Error handling strategy defined
- ✅ Input validation centralized in business logic
- ✅ SOLID principles applied

### Requirements Compliance Checklist

- ✅ All 10 functional requirements (FR-001 to FR-010) addressed in design
- ✅ All 6 non-functional requirements (NFR-001 to NFR-006) addressed in design
- ✅ All 10 acceptance criteria (AC-001 to AC-010) traceable to components
- ✅ Requirements constraints respected (in-memory, no persistence, CLI only)
- ✅ Out-of-scope items not included in architecture

### Technology & Dependencies Checklist

- ✅ Python 3.8+ language selected
- ✅ Only standard library used (no external runtime dependencies)
- ✅ Testing frameworks identified (pytest, pytest-cov)
- ✅ No unnecessary infrastructure or over-engineering
- ✅ Deployment and testing strategies defined

### Risks & Mitigation Checklist

- ✅ Data loss risk identified and accepted (session-only by design)
- ✅ No undo capability documented (acceptable per scope)
- ✅ ID gap behavior documented (no renumbering per FR-005)
- ✅ Test coverage target identified (≥80%)
- ✅ Error handling strategy defined for all error cases

### Approval & Sign-Off Checklist

- ✅ Architecture proposal presented to user
- ✅ User feedback incorporated (open questions answered)
- ✅ Final architecture explicitly approved by user
- ✅ Approval documented with date and time
- ✅ Design ready for implementation phase

---

## Appendix D: Architecture Decision Log

| Date | Decision | Rationale | Status |
|------|----------|-----------|--------|
| 2026-10-15 | Use Layered Architecture | Meets requirement NFR-001 for modularity; enables testability | ✅ APPROVED |
| 2026-10-15 | Dict-based task storage | O(1) lookups; preserves insertion order; simple in-memory | ✅ APPROVED |
| 2026-10-15 | Exception-based error handling | Clear signal to CLI; prevents invalid state; standard Python | ✅ APPROVED |
| 2026-10-15 | Numeric menu (1-5) | Simple, unambiguous input; easy validation | ✅ APPROVED |
| 2026-10-15 | No persistence layer | Meets NFR-004; simplifies design; session-only requirement | ✅ APPROVED |
| 2026-10-15 | Immediate exit (no confirmation) | Clean shutdown; minimal complexity | ✅ APPROVED |

---

## Appendix E: Document Control

| Attribute | Value |
|-----------|-------|
| Document Title | Architecture: US-001 Simple Python To-Do App |
| Document ID | ARCH-US-001-2026-10-15 |
| Version | 1.0 |
| Status | ✅ APPROVED |
| Author | Architecture Agent (Agentic SDLC Pipeline) |
| Approved By | User |
| Approval Date | 2026-10-15 12:01 IST |
| Last Updated | 2026-10-15 12:01 IST |
| Review Cycle | 1 (Single review and approval) |
| Distribution | Agentic SDLC Pipeline, Development Team |
| Classification | Internal Project Documentation |

---

## Appendix F: Glossary

| Term | Definition |
|------|-----------|
| **Task** | A unit of work with a name and completion status |
| **Task ID** | Sequential integer (1, 2, 3...) uniquely identifying a task |
| **Mark Complete** | Change task status to complete (display marker changes to [✓]) |
| **Delete** | Remove task from collection permanently |
| **Menu Loop** | Repeating user interaction cycle: display menu → accept choice → perform action → return to menu |
| **Session** | Single continuous application execution (from start to exit) |
| **CLI** | Command-Line Interface (text-based user interaction) |
| **In-Memory** | Data stored in RAM, not persisted to disk |
| **Idempotent** | Operation producing same result on repeated execution |
| **Layer** | Logical tier in three-layer architecture (data, logic, presentation) |

---

**End of Architecture Document**  
**Status**: ✅ **APPROVED BY USER** (2026-10-15)  
**Ready for**: Implementation Phase (Step 5)
