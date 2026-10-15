# Agentic SDLC - Automated Documentation Sync

## Overview

This repository demonstrates an **Agentic SDLC (Software Development Lifecycle)** workflow using GitHub Copilot. A central **Orchestrator Agent** coordinates multiple specialized agents to manage the complete software development lifecycle while delivering an **Automated Documentation Sync** application.

## Project Structure

```
├── .github/
│   ├── copilot-instructions.md      # Shared Copilot configuration
│   ├── agents/                       # Specialized agent definitions
│   │   ├── orchestrator.agent.md     # Workflow orchestrator
│   │   ├── requirements.agent.md     # Requirements gathering
│   │   ├── architecture.agent.md     # Architecture design
│   │   ├── design-review.agent.md    # Design validation
│   │   ├── planning.agent.md         # Implementation planning
│   │   ├── implementation.agent.md   # Code implementation
│   │   ├── code-review.agent.md      # Code review
│   │   ├── verification.agent.md     # Testing & verification
│   │   └── pr.agent.md               # PR creation
│   ├── prompts/                      # Workflow entry points
│   │   ├── start-sdlc.prompt.md      # Start new workflow
│   │   └── resume-sdlc.prompt.md     # Resume workflow
│   ├── skills/                       # Reusable procedures
│   │   ├── requirements-analysis/    # Requirements gathering
│   │   ├── documentation-sync/       # Doc sync implementation
│   │   ├── code-review/              # Code review procedures
│   │   └── verification/             # Testing procedures
│   └── hooks/                        # Lifecycle automation (TBD)
├── docs/                             # Generated documentation
│   ├── requirements.md               # Approved requirements
│   ├── architecture.md               # System architecture
│   ├── design-review.md              # Design review findings
│   ├── impl-plan.md                  # Implementation plan
│   └── verification-report.md        # Test results
└── README.md                         # This file
```

## Workflow Stages

The Orchestrator Agent manages the following workflow stages:

1. **INPUT_RECEIVED** - User story provided
2. **REQUIREMENTS_CLARIFICATION** - Requirements Agent gathers details
3. **REQUIREMENTS_APPROVAL** - Approval gate
4. **ARCHITECTURE_DESIGN** - Architecture Agent designs system
5. **DESIGN_REVIEW** - Design Review Agent validates design
6. **DESIGN_REVISION** - Handle design changes (if needed)
7. **IMPLEMENTATION_PLANNING** - Planning Agent creates task list
8. **IMPLEMENTATION** - Implementation Agent builds application
9. **CODE_REVIEW** - Code Review Agent reviews changes
10. **IMPLEMENTATION_REVISION** - Handle code review findings (if needed)
11. **VERIFICATION** - Verification Agent runs tests
12. **VERIFICATION_RETRY** - Handle test failures (if needed)
13. **PR_PREPARATION** - PR Agent prepares pull request
14. **PR_CREATED** - Pull request successfully created
15. **BLOCKED** - Workflow blocked on unresolvable issue

## Getting Started

### Starting a New Workflow

Use the `start-sdlc.prompt.md` entry point:

```
Start an Agentic SDLC workflow with the following user story:
[Your user story here]
```

The Orchestrator will guide you through requirements clarification, design, implementation, and PR creation.

### Resuming a Workflow

Use the `resume-sdlc.prompt.md` entry point to resume an interrupted workflow.

## Agents

### Orchestrator Agent
Central coordinator managing workflow state and delegating to specialized agents.

### Specialized Agents
- **Requirements Agent**: Gathers and documents requirements
- **Architecture Agent**: Designs system architecture
- **Design Review Agent**: Validates architecture against requirements
- **Planning Agent**: Creates prioritized implementation plan
- **Implementation Agent**: Builds the application
- **Code Review Agent**: Reviews implementation quality
- **Verification Agent**: Tests and validates completeness
- **PR Agent**: Creates pull request with documentation

## Skills

Reusable procedures for common tasks:

- **Requirements Analysis**: Gathering and structuring requirements
- **Documentation Sync**: Core application functionality
- **Code Review**: Quality assessment and validation
- **Verification**: Testing and validation procedures

## Technology Stack

- GitHub Copilot for AI-powered agent coordination
- GitHub CLI for repository operations
- Git for version control
- Markdown for documentation
- (Application technology stack TBD)

## Documentation

- `docs/requirements.md` - Approved system requirements
- `docs/architecture.md` - Complete system architecture design
- `docs/design-review.md` - Design review findings and recommendations
- `docs/impl-plan.md` - Detailed implementation plan
- `docs/verification-report.md` - Test execution results

## Status

🚀 **Initial structure created** - Ready for workflow initiation

## Next Steps

1. Review the agent and skill definitions in `.github/agents/` and `.github/skills/`
2. Initiate a workflow by providing a user story
3. Follow the Orchestrator through each workflow stage
4. Approve or revise artifacts as needed
5. Review and merge the final pull request

---

**Last Updated**: 2026-10-14