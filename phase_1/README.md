# Phase 1 — Building the Agent Library

Phase 1 builds a reusable Python package containing the agent classes used by the Phase 2 project-management workflow.

## Required Agents

`workflow_agents/base_agents.py` must contain:

1. `DirectPromptAgent`
2. `AugmentedPromptAgent`
3. `KnowledgeAugmentedPromptAgent`
4. `RAGKnowledgePromptAgent` *(provided by Udacity)*
5. `EvaluationAgent`
6. `RoutingAgent`
7. `ActionPlanningAgent`

## Required Tests

Create a standalone test for every agent and capture successful terminal output for all seven tests.

Suggested test locations:

```text
tests/
├── direct_prompt_agent.py
├── augmented_prompt_agent.py
├── knowledge_augmented_prompt_agent.py
├── rag_knowledge_prompt_agent.py
├── evaluation_agent.py
├── routing_agent.py
└── action_planning_agent.py
```

## Key Rubric Requirements

- Direct prompt: user message only, no system message.
- Augmented prompt: persona + forget-prior-context instruction.
- Knowledge augmented: persona + provided knowledge + use-only-that-knowledge instruction.
- Evaluation: iterative worker/evaluator loop with `temperature=0` for evaluation/correction calls.
- Routing: `text-embedding-3-large` + cosine similarity.
- Action planning: `gpt-3.5-turbo` + clean actionable-step list.
- API keys must not be hardcoded.

See [`../docs/rubric_checklist.md`](../docs/rubric_checklist.md) for the full checklist.
