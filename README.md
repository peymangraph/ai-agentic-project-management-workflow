# AI-Powered Agentic Workflow for Project Management

A reusable agentic AI workflow for technical project management that transforms product ideas and specifications into structured **user stories**, **product features**, and **detailed engineering tasks** using planning, routing, knowledge-augmented generation, and evaluation agents.

> **Pilot use case:** InnovateNext Solutions' Email Router product specification. The architecture is intentionally general-purpose so it can be reused for future product-development workflows.

## Project Goals

Technical project managers often spend significant time converting product ideas into consistent development plans. This project demonstrates how an agentic workflow can reduce that bottleneck by combining specialized AI agents that plan work, route tasks, generate domain-specific artifacts, and evaluate outputs against explicit quality criteria.

## Architecture

```text
High-Level TPM Prompt + Product Specification
                    |
                    v
           ActionPlanningAgent
                    |
                    v
              Workflow Steps
                    |
                    v
              RoutingAgent
          /           |            \
         v            v             v
Product Manager   Program Manager   Development Engineer
Knowledge Agent   Knowledge Agent   Knowledge Agent
      |                 |                 |
      v                 v                 v
Evaluation Agent   Evaluation Agent   Evaluation Agent
          \             |             /
                    v
          Structured Project Plan
```

## Agentic Patterns Used

- **Action Planning** — decomposes a high-level project-management goal into actionable steps.
- **Routing** — semantically matches each step to the appropriate specialized role.
- **Knowledge-Augmented Prompting** — grounds role-specific generation in supplied project knowledge.
- **Evaluation / Optimization** — checks generated artifacts against explicit quality criteria and supports iterative refinement.
- **RAG** — included in the reusable Phase 1 toolkit as a provided agent implementation.

## Repository Structure

```text
ai-agentic-project-management-workflow/
├── phase_1/
│   ├── workflow_agents/
│   │   ├── __init__.py
│   │   └── base_agents.py
│   ├── tests/
│   │   ├── direct_prompt_agent.py
│   │   ├── augmented_prompt_agent.py
│   │   ├── knowledge_augmented_prompt_agent.py
│   │   ├── rag_knowledge_prompt_agent.py
│   │   ├── evaluation_agent.py
│   │   ├── routing_agent.py
│   │   └── action_planning_agent.py
│   └── README.md
├── phase_2/
│   ├── agentic_workflow.py
│   └── README.md
├── docs/
│   ├── project_overview.md
│   └── rubric_checklist.md
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Phase 1 — Reusable Agent Toolkit

Phase 1 implements and tests seven reusable agent classes:

1. `DirectPromptAgent`
2. `AugmentedPromptAgent`
3. `KnowledgeAugmentedPromptAgent`
4. `RAGKnowledgePromptAgent` *(provided by Udacity)*
5. `EvaluationAgent`
6. `RoutingAgent`
7. `ActionPlanningAgent`

Six agents are student-implemented. The RAG agent is provided, but successful execution evidence is still required. Each agent has its own standalone test script.

## Phase 2 — Project Management Workflow

Phase 2 combines selected Phase 1 agents into a reusable project-management workflow:

- `ActionPlanningAgent` decomposes the TPM request.
- `RoutingAgent` assigns each action to the correct specialist.
- Product Manager agents generate and validate user stories.
- Program Manager agents generate and validate product features.
- Development Engineer agents generate and validate engineering tasks.

### Required Output Formats

**User stories**

```text
As a [type of user], I want [an action or feature] so that [benefit/value].
```

**Product features**

```text
Feature Name:
Description:
Key Functionality:
User Benefit:
```

**Engineering tasks**

```text
Task ID:
Task Title:
Related User Story:
Description:
Acceptance Criteria:
Estimated Effort:
Dependencies:
```

## Environment Setup

The Udacity workspace already includes the required libraries. For local development:

```bash
python -m venv .venv
source .venv/bin/activate     # Linux/macOS
# .venv\Scripts\activate      # Windows
pip install -r requirements.txt
```

Copy the environment template:

```bash
cp .env.example .env
```

Then set:

```text
OPENAI_API_KEY=your_key_here
```

Never commit `.env` or API keys.

## Dependencies

- `openai==1.78.1`
- `python-dotenv==1.1.0`
- `pandas==2.2.3`

## Testing and Submission Evidence

The Udacity submission requires:

- completed `phase_1/workflow_agents/base_agents.py`;
- standalone tests for all six student-implemented agents;
- successful execution evidence for all seven agents, including RAG;
- completed `phase_2/agentic_workflow.py`;
- terminal output or screenshots from the complete Phase 2 workflow.

See [`docs/rubric_checklist.md`](docs/rubric_checklist.md) before submission.

## Security

- Keep API keys in `.env` only.
- Do not commit secrets, credentials, or sensitive project data.
- Treat any accidentally exposed key as compromised and rotate it immediately.

## Status

🚧 **In development** — repository scaffold initialized; Phase 1 agent implementation is next.

## Educational Context

This repository implements the Udacity **AI-Powered Agentic Workflow for Project Management** project. It is intended as a learning project demonstrating reusable agent design and agentic workflow orchestration.