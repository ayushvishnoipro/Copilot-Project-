---
name: code-review
description: >
  Reviews Python source code and tests against docs/requirements.md across
  eight quality areas, producing severity-rated findings and a final verdict.
---

# Code Review Skill

## Role
Act as a senior reviewer. Report genuine defects against requirements, not personal preferences.

## Required Inputs
- `docs/requirements.md`
- All Python files in `src/` and `tests/`

Read every available file. If inputs are missing or inaccessible, report the limitation and do not claim a complete review.

## Review Process
1. Read `docs/requirements.md` and identify acceptance criteria and requirement IDs.
2. Inspect every Python source and test file.
3. Review all eight areas listed below.
4. Report evidence-based findings with file paths, line numbers, severity, and actionable fixes.
5. Reference `FR-n` or `NFR-n` for applicable requirement deviations; never invent IDs.
6. Write the report to `output/reports/code-review.md`.
7. Verify all eight areas and the final verdict are present.
8. Do not modify source code, tests, or configuration files.

## Review Areas

| Area | Check |
|---|---|
| Correctness | Behavior matches approved requirements. |
| Security | Secrets, input validation, data exposure, and security boundaries. |
| Error Handling | API failures, missing files, invalid inputs, and exceptions. |
| Test Coverage | Happy paths, edge cases, invalid inputs, and failures. |
| Code Clarity | Meaningful names, readable logic, maintainability. |
| DRY Principle | Harmful duplication of logic. |
| Dependency Safety | Dependency declarations, version constraints, known vulnerabilities supported by evidence. |
| Python Conventions | PEP 8, type hints, specific exceptions, no mutable defaults. |

## Severity
- **Critical:** Severe security exposure, major functional failure, or critical requirement violation.
- **Major:** Significant defect, security weakness, or requirement gap.
- **Minor:** Low-impact maintainability, clarity, or convention issue.

Do not report hypothetical issues as confirmed defects. Never expose secret values; identify only the affected file and line.

## Output Format
Write `output/reports/code-review.md`:

```markdown
# Code Review

## Summary
[Overall assessment and key risks]

## Findings

### Correctness
[Findings or "No findings"]

### Security
[Findings or "No findings"]

### Error Handling
[Findings or "No findings"]

### Test Coverage
[Findings or "No findings"]

### Code Clarity
[Findings or "No findings"]

### DRY Principle
[Findings or "No findings"]

### Dependency Safety
[Findings or "No findings"]

### Python Conventions
[Findings or "No findings"]

Each finding: Severity | File | Line | Requirement ID | Description | Suggestion

## Review Statistics
- Source files reviewed: [Count]
- Test files reviewed: [Count]
- Critical: [Count]
- Major: [Count]
- Minor: [Count]
- Review completeness: [Complete / Incomplete]

## Overall Recommendation
[APPROVE / REQUEST CHANGES / BLOCKED]
```

## Verdict Rules
- **APPROVE:** Review complete; no unresolved Critical or Major findings.
- **REQUEST CHANGES:** At least one Critical or Major finding remains.
- **BLOCKED:** Required inputs are missing or review cannot be completed reliably.

The Orchestrator must treat `BLOCKED` as a failed gate. Minor findings may remain under `APPROVE`.

## Quality Checklist
- All eight areas are included.
- Findings are evidence-based, actionable, and correctly classified.
- Requirement IDs and statistics are accurate.
- Secret values are excluded.
- Incomplete inspections are disclosed.
- No source, test, or configuration files are modified.
- The report is written and validated before claiming completion.
