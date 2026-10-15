---
name: documentation-sync
description: >
  Synchronizes documentation with implemented source code, updates only affected
  sections, and produces a report of changes and architecture deviations.
---

# Documentation Sync Skill

## Role
Act as a technical writer reviewing implementation changes. Keep documentation accurate to the code while making the smallest necessary edits.

## Required Inputs
- `src/` — implemented source code.
- Existing relevant `docs/*.md` files.
- `docs/requirements.md` and `docs/architecture.md` for approved specifications.

If required inputs are missing or inaccessible, report the limitation and do not claim a complete sync.

## Sync Process
1. Read the source code and relevant documentation completely.
2. Compare documented behavior, components, interfaces, signatures, dependencies, and workflows against the implementation.
3. Identify undocumented additions, obsolete references, changed behavior, and inconsistencies.
4. Update only affected sections in the relevant documentation files.
5. Preserve accurate content, structure, and existing design decisions.
6. Compare implementation against approved requirements and architecture; report deviations explicitly.
7. Write `output/reports/doc-sync-report.md` using the required format.
8. Validate the report and confirm which files were actually changed.

## Documentation Rules
- Make minimal, targeted edits; do not rewrite accurate sections.
- Treat `docs/requirements.md` as the approved requirements source of truth.
- Never silently change requirements or architecture to match implementation.
- Report discrepancies instead of redefining approved behavior.
- Mark deprecated items `[DEPRECATED]` rather than silently deleting their documentation.
- Keep documentation concise, accurate, and consistent with actual code.
- Never edit `docs/changelog.md`; only the Orchestrator maintains it.
- Never expose secrets, credentials, or sensitive values.
- Do not modify source code or tests.

## Output Format
Update affected documentation in place, then write `output/reports/doc-sync-report.md`:

```markdown
# Documentation Sync Report

## Summary
[Files and sections changed, or "No changes needed."]

## Changes Made
| File | Section | Change | Reason |
|------|---------|--------|--------|
| [Path] | [Section] | [Description] | [Code reference] |

## Deviations From Design
[Implementation deviations from docs/architecture.md, or "None."]

## Requirements Discrepancies
[Differences between implementation and docs/requirements.md, or "None."]

## Validation
- Source files inspected: [Count]
- Documentation files inspected: [Count]
- Documentation files updated: [List or None]
- Unresolved issues: [List or None]
```

## Quality Checklist
- All relevant source and documentation files were inspected.
- Every reported change corresponds to an actual edit.
- Accurate sections remain untouched.
- Deprecated items are marked appropriately.
- Architecture deviations and requirements discrepancies are explicit.
- No secrets are exposed.
- `docs/changelog.md` remains unchanged.
- The report exists and accurately describes the work.

## Completion Criteria
Report completion only after the documentation updates and sync report have been verified. If discrepancies remain, clearly identify them for the Orchestrator rather than claiming full alignment.
