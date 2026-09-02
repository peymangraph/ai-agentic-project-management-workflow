# Phase 2 — Implementing the Agentic Workflow

Phase 2 combines the reusable agents from Phase 1 into a general-purpose technical project-management workflow.

## Required Workflow

```text
TPM Prompt + Product Specification
          |
          v
 ActionPlanningAgent
          |
          v
     Workflow Steps
          |
          v
     RoutingAgent
   /       |        \
  v        v         v
Product   Program   Development
Manager   Manager   Engineer
  |        |         |
  v        v         v
Knowledge Agents + Evaluation Agents
          |
          v
Structured Project Plan
```

## Required Phase 2 Components

- Load `OPENAI_API_KEY` from environment variables.
- Load the official `Product-Spec-Email-Router.txt` into `product_spec`.
- Instantiate `ActionPlanningAgent` using the provided `knowledge_action_planning`.
- Append `product_spec` to `knowledge_product_manager`.
- Instantiate Product Manager, Program Manager, and Development Engineer knowledge agents.
- Instantiate one EvaluationAgent per specialist role using the exact Udacity evaluation criteria.
- Configure a RoutingAgent with `name`, `description`, and `func` for all three routes.
- Implement one support function per role.
- Generate `workflow_steps`, route every step, collect results in `completed_steps`, and print the final workflow output.

## Pilot

The official pilot input is `Product-Spec-Email-Router.txt`. Do not hard-code the workflow around Email Router concepts; the same architecture should work with future product specifications.

## Before Submission

Review [`../docs/rubric_checklist.md`](../docs/rubric_checklist.md) and capture the full terminal output from the completed workflow.
