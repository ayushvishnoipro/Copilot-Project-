---
name: resume-sdlc
description: >
  Resumes a paused or interrupted Agentic SDLC workflow from a specified stage.
  Recovers workflow progress, validates existing artifacts, incorporates revisions
  and approvals, and continues without unnecessarily repeating completed work.
---

# Resume Agentic SDLC Workflow

## Purpose
Resume an in-progress Automated Documentation Sync SDLC workflow after interruption, clarification, revision, failed review, failed verification, or an approval checkpoint.

## Usage
Invoke this prompt when an existing workflow needs to continue from a previous stage.

Provide:
- The stage to resume from, if known.
- Any updated requirements, architecture decisions, review findings, or test fixes.
- The required approval or action to take next.

Example:
`Resume the SDLC workflow from code review. Fix the Major findings, rerun the review, and continue after approval.`

## Instructions

1. **Recover workflow state**
   - Ask the Orchestrator to inspect the existing repository, changelog, reports, and available workflow-state artifacts.
   - Identify the user story and the last successfully completed stage.
   - Use the requested resume stage when valid; otherwise, determine the earliest incomplete or failed stage.

2. **Validate existing artifacts**
   - Confirm that required files exist, are non-empty, and contain valid results.
   - Check approval statuses and review/verification verdicts.
   - Do not treat file existence alone as proof of completion.
   - Identify stale artifacts that may no longer match the current requirements or code.

3. **Apply updates**
   - Incorporate new user instructions, approved decisions, and revisions.
   - Route changes to the responsible specialist agent.
   - Re-run downstream stages when an upstream change invalidates their results.

4. **Resume from the correct stage**
   - Requirements: revise and approve requirements.
   - Architecture: revise and approve the architecture.
   - Design Review: resolve blocking design findings and repeat the review.
   - Implementation Planning: update tasks and dependencies.
   - Implementation: fix code or tests according to approved requirements and the plan.
   - Documentation Sync: regenerate or reconcile documentation without silently changing approved requirements.
   - Code Review: address findings and repeat the review.
   - Verification: rerun failed checks and confirm all quality gates pass.
   - PR Creation: prepare or resume the PR draft; create the PR only after explicit user confirmation.

5. **Preserve completed work**
   - Skip stages only when their artifacts and approval status are verified and remain valid.
   - Do not overwrite unrelated user changes.
   - Preserve existing changelog entries and append new entries only after successful stages.

6. **Enforce pipeline gates**
   - Do not bypass requirements or architecture approval.
   - Do not proceed with unresolved Critical or Major code review findings.
   - Do not proceed to PR creation when verification fails.
   - Never interpret silence as approval or create a PR without explicit confirmation.

7. **Report progress**
   - State the recovered workflow status and the stage being resumed.
   - Identify invalid or missing artifacts and unresolved blockers.
   - Continue through the Orchestrator and its configured specialist agents.
   - Stop at the next required user approval checkpoint.

## Resumption Points

- After requirements clarification or revision.
- After architecture feedback or revision.
- After design review findings.
- After implementation planning approval.
- After implementation failure or code changes.
- After documentation synchronization.
- After code review findings or approval.
- After verification failure or success.
- Before or after PR draft preparation, subject to explicit approval for creation.

## Expected Outcome

The workflow resumes from the earliest necessary stage, incorporates the requested updates, preserves valid completed work, reruns affected downstream stages, and respects all approval and quality gates.

## Failure Handling

- If the requested stage cannot be identified, ask the user which stage to resume.
- If required inputs or artifacts are missing, report the exact files needed.
- If previous results are stale or inconsistent, rerun the affected stage.
- If an agent fails, report the error and stop at the appropriate boundary.
- If verification fails, return to implementation and repeat code review and verification.
- If GitHub MCP or repository access is unavailable, report the blocker without claiming PR creation.

## Final Report

When the resumed workflow pauses or completes, report:

- **User story:** [Path]
- **Resumed stage:** [Stage]
- **Completed stages:** [Verified stages]
- **Stages rerun:** [Affected stages]
- **Current status:** [In progress / Paused / Blocked / Complete]
- **Outstanding blockers:** [List or None]
- **Next action:** [Required approval or next stage]
- **Pull request:** [Verified URL or Not created]
