# Project Overview

## AI-Powered Agentic Workflow for Project Management

This project implements a reusable agentic AI system for **InnovateNext Solutions**. The system is designed to help technical project managers transform high-level product ideas into consistent, actionable development plans.

The **Email Router** product specification is the pilot use case, but the workflow is intentionally designed to support future product-development initiatives as well.

## Business Problem

Technical project managers are often responsible for turning product ideas into user stories, product features, and engineering tasks. When this work is performed manually across many concurrent initiatives, common problems include:

- inconsistent planning quality;
- miscommunication between product, program, and engineering teams;
- TPM bottlenecks;
- slower project execution;
- difficulty scaling project-management practices across teams.

The project addresses this by combining reusable AI agents into a structured workflow that can plan, route, generate, evaluate, and refine project artifacts.

## Audience

The primary audience is InnovateNext Solutions' technical project-management and leadership organization, especially:

- Technical Project Managers (TPMs)
- Head of Product
- Lead Technical Program Manager
- Product Managers
- Program Managers
- Development Engineers

## Phase 1 — Agentic Toolkit

Phase 1 builds a reusable Python agent library in `workflow_agents/base_agents.py`.

Required agents:

1. `DirectPromptAgent`
2. `AugmentedPromptAgent`
3. `KnowledgeAugmentedPromptAgent`
4. `RAGKnowledgePromptAgent` *(provided implementation)*
5. `EvaluationAgent`
6. `RoutingAgent`
7. `ActionPlanningAgent`

Each agent is validated with a standalone script. The final submission requires execution evidence for all seven agents.

## Phase 2 — General-Purpose TPM Workflow

Phase 2 uses the Phase 1 library to implement `agentic_workflow.py`.

The workflow:

1. receives a high-level TPM request;
2. loads a product specification;
3. uses an `ActionPlanningAgent` to decompose the goal into logical subtasks;
4. uses a `RoutingAgent` to assign each subtask to the appropriate specialized role;
5. generates user stories through a Product Manager knowledge agent;
6. generates product features through a Program Manager knowledge agent;
7. generates detailed engineering tasks through a Development Engineer knowledge agent;
8. evaluates each artifact against explicit quality criteria;
9. prints the completed workflow output.

## Expected Artifacts

### User Stories

```text
As a [type of user], I want [an action or feature] so that [benefit/value].
```

### Product Features

```text
Feature Name:
Description:
Key Functionality:
User Benefit:
```

### Engineering Tasks

```text
Task ID:
Task Title:
Related User Story:
Description:
Acceptance Criteria:
Estimated Effort:
Dependencies:
```

## Design Principle

The Email Router is a **pilot**, not a hard-coded workflow target. Product-specific information should be supplied as knowledge/input so the agent architecture remains reusable for other product-development projects.

## Final Submission

The final project package must include:

- completed Phase 1 agent library;
- all Phase 1 test scripts;
- execution evidence for seven agent tests;
- completed Phase 2 workflow script;
- execution evidence from the full Email Router workflow.
