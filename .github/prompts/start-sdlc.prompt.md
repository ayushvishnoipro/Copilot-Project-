---
name: start-sdlc
description: >
  Starts a new Agentic SDLC workflow from a user story or requirements summary.
  Coordinates specialist agents through requirements, architecture, planning,
  implementation, documentation, review, verification, and GitHub PR creation.
---

# Start Agentic SDLC Workflow

## Purpose
Initiate a new end-to-end Automated Documentation Sync SDLC workflow from a user story or requirements summary, coordinated by the Orchestrator Agent.

## Usage
Invoke this prompt to start a new workflow cycle.

Provide either:
- A path to a user story file, such as `user-stories/user-story-1.md`.
- A clear requirements summary when no story file exists.

Example:
`Start the SDLC workflow using user-stories/user-story-1.md`

## Instructions

1. **Validate input**
   - Confirm that a readable user story file or meaningful requirements summary is available.
   - If neither is provided, ask the user to supply one.
   - Do not reuse previous workflow artifacts as if they belong to a new workflow.

2. **Initialize the workflow**
   - Invoke the Orchestrator Agent.
   - Identify the user story, repository context, and existing project structure.
   - Check for conflicting or incomplete artifacts from previous runs.

3. **Execute the pipeline**
   - Delegate each stage to its designated specialist agent.
   - Follow the configured pipeline sequence and validate each stage's output.
   - Ask the user for clarification or approval at the required checkpoints.

4. **Incorporate feedback**
   - Route requested revisions to the responsible agent.
   - Revalidate affected artifacts after revisions.
   - Rerun downstream stages whenever upstream changes invalidate their results.

5. **Enforce quality gates**
   - Require approved requirements and architecture.
   - Resolve blocking design-review findings before implementation.
   - Require an approved implementation plan.
   - Require code review approval with no unresolved Critical or Major findings.
   - Require successful verification, including passing tests and at least 80% coverage.
   - Never bypass a failed gate because the user wants to continue.

6. **Create the pull request**
   - Prepare a PR title and description based on actual implementation changes and verification results.
   - Display the complete PR draft to the user.
   - Create the PR using the configured GitHub MCP tools only after explicit user confirmation.
   - Verify the resulting PR URL and status before reporting success.

7. **Track progress**
   - Preserve completed artifacts and append changelog entries after successful stages.
   - Report completed stages, failures, pending approvals, and blockers.
   - Do not claim success without evidence.

## Workflow Stages

1. Requirements clarification and approval — `requirements`
2. Architecture design and approval — `architecture`
3. Architecture risk assessment — `design-review`
4. Dependency-ordered implementation planning — `implementation-planner`
5. Source code and test implementation — `implementation`
6. Documentation synchronization — `documentation-sync`
7. Code quality and security review — `code-review`
8. Test execution and quality verification — `verification`
9. GitHub pull request preparation and creation — `pr`

## Expected Outcome

A verified GitHub pull request backed by approved requirements and architecture, an implementation plan, tested source code, synchronized documentation, an approved code review, and passing verification.

The workflow may pause if clarification, approval, or remediation is required. A pull request is not guaranteed if any required gate fails.

## Error Handling

- **Missing input:** Ask for the user story or requirements summary.
- **Missing artifacts:** Identify the expected file and responsible stage.
- **Review failure:** Return actionable findings to the appropriate agent.
- **Verification failure:** Stop PR creation until the required checks pass.
- **Agent or MCP failure:** Report the actual error and required corrective action.
- **User declines approval:** Pause without proceeding past the approval checkpoint.

## Final Report

At completion or pause, provide:

- **User story:** [Path or summary]
- **Requirements:** [Approved / Pending]
- **Architecture:** [Approved / Pending]
- **Implementation:** [Completed / Blocked]
- **Documentation sync:** [Completed / Blocked]
- **Code review:** [APPROVE / REQUEST CHANGES / BLOCKED]
- **Verification:** [PASS / FAIL / Not run]
- **Pull request:** [Verified URL / Not created]
- **Outstanding blockers:** [List or None]
- **Next action:** [Required approval or remediation]
