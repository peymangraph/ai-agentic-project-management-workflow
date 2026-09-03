"""General-purpose technical project-management agentic workflow.

Pilot input: Product-Spec-Email-Router.txt

This implementation follows the Udacity Phase 2 rubric while keeping the
workflow reusable for future product specifications.
"""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

from workflow_agents.base_agents import (
    ActionPlanningAgent,
    EvaluationAgent,
    KnowledgeAugmentedPromptAgent,
    RoutingAgent,
)


# === Setup ===
CURRENT_DIR = Path(__file__).resolve().parent
REPO_ROOT = CURRENT_DIR.parent
load_dotenv(REPO_ROOT / ".env")
openai_api_key = os.getenv("OPENAI_API_KEY")

if not openai_api_key:
    raise ValueError("OPENAI_API_KEY was not found in the repository-level .env file.")

product_spec_path = CURRENT_DIR / "Product-Spec-Email-Router.txt"
product_spec = product_spec_path.read_text(encoding="utf-8")


# === Action Planning Agent ===
# A complete development plan has three top-level artifact stages. Keeping these
# stages explicit prevents the planner from expanding the rubric exercise into
# unrelated project-administration activities such as staffing or scheduling.
knowledge_action_planning = (
    "Stories are defined from a product spec by identifying a persona, an action, "
    "and a desired outcome for each story. Each story represents a specific "
    "functionality of the product described in the specification.\n"
    "Features are defined by grouping related validated user stories.\n"
    "Tasks are defined from the validated user stories and product features and "
    "represent the engineering work required to develop the product.\n\n"
    "A complete development plan contains exactly these three ordered top-level stages:\n"
    "1. Define user stories for the product.\n"
    "2. Organize the validated user stories into product features.\n"
    "3. Create detailed engineering tasks for the validated user stories and product features.\n\n"
    "Do not decompose these three stages into smaller substeps. Do not add staffing, "
    "scheduling, prioritization, monitoring, testing, or retrospective activities."
)

action_planning_agent = ActionPlanningAgent(
    openai_api_key=openai_api_key,
    knowledge=knowledge_action_planning,
)


# === Product Manager Team ===
persona_product_manager = (
    "You are a Product Manager, you are responsible for defining the user stories for a product."
)
knowledge_product_manager = (
    "Stories are defined by writing sentences with a persona, an action, and a desired outcome. "
    "The sentences always start with: As a "
    "Write several stories for the product spec below, where the personas are the different users of the product. "
    "\n\nPRODUCT SPECIFICATION:\n"
    + product_spec
)

product_manager_knowledge_agent = KnowledgeAugmentedPromptAgent(
    openai_api_key=openai_api_key,
    persona=persona_product_manager,
    knowledge=knowledge_product_manager,
)

persona_product_manager_eval = (
    "You are an evaluation agent that checks the answers of other worker agents"
)
evaluation_criteria_product_manager = (
    "The answer should be stories that follow the following structure: "
    "As a [type of user], I want [an action or feature] so that [benefit/value]."
)

product_manager_evaluation_agent = EvaluationAgent(
    openai_api_key=openai_api_key,
    persona=persona_product_manager_eval,
    evaluation_criteria=evaluation_criteria_product_manager,
    agent_to_evaluate=product_manager_knowledge_agent,
    max_interactions=5,
)


# === Program Manager Team ===
persona_program_manager = (
    "You are a Program Manager, you are responsible for defining the features for a product."
)
knowledge_program_manager = (
    "Features of a product are defined by organizing similar user stories into cohesive groups."
)

program_manager_knowledge_agent = KnowledgeAugmentedPromptAgent(
    openai_api_key=openai_api_key,
    persona=persona_program_manager,
    knowledge=knowledge_program_manager,
)

persona_program_manager_eval = (
    "You are an evaluation agent that checks the answers of other worker agents."
)
evaluation_criteria_program_manager = (
    "The answer should be product features that follow the following structure: "
    "Feature Name: A clear, concise title that identifies the capability\n"
    "Description: A brief explanation of what the feature does and its purpose\n"
    "Key Functionality: The specific capabilities or actions the feature provides\n"
    "User Benefit: How this feature creates value for the user"
)

program_manager_evaluation_agent = EvaluationAgent(
    openai_api_key=openai_api_key,
    persona=persona_program_manager_eval,
    evaluation_criteria=evaluation_criteria_program_manager,
    agent_to_evaluate=program_manager_knowledge_agent,
    max_interactions=5,
)


# === Development Engineer Team ===
persona_dev_engineer = (
    "You are a Development Engineer, you are responsible for defining the development tasks for a product."
)
knowledge_dev_engineer = (
    "Development tasks are defined by identifying what needs to be built to implement each user story."
)

development_engineer_knowledge_agent = KnowledgeAugmentedPromptAgent(
    openai_api_key=openai_api_key,
    persona=persona_dev_engineer,
    knowledge=knowledge_dev_engineer,
)

persona_dev_engineer_eval = (
    "You are an evaluation agent that checks the answers of other worker agents."
)
evaluation_criteria_dev_engineer = (
    "The answer should be tasks following this exact structure: "
    "Task ID: A unique identifier for tracking purposes\n"
    "Task Title: Brief description of the specific development work\n"
    "Related User Story: Reference to the parent user story\n"
    "Description: Detailed explanation of the technical work required\n"
    "Acceptance Criteria: Specific requirements that must be met for completion\n"
    "Estimated Effort: Time or complexity estimation\n"
    "Dependencies: Any tasks that must be completed first"
)

development_engineer_evaluation_agent = EvaluationAgent(
    openai_api_key=openai_api_key,
    persona=persona_dev_engineer_eval,
    evaluation_criteria=evaluation_criteria_dev_engineer,
    agent_to_evaluate=development_engineer_knowledge_agent,
    max_interactions=5,
)


# This lightweight context allows downstream specialist agents to receive
# artifacts generated by earlier routed steps while preserving the requested
# RoutingAgent-based orchestration pattern.
workflow_context = {
    "user_stories": "",
    "features": "",
}


# === Job-function support functions ===
def product_manager_support_function(query: str) -> str:
    """Generate and evaluate Product Manager user stories."""
    response_from_knowledge_agent = product_manager_knowledge_agent.respond(query)
    evaluation_result = product_manager_evaluation_agent.evaluate(
        query,
        initial_response=response_from_knowledge_agent,
    )
    final_response = evaluation_result["final_response"]
    workflow_context["user_stories"] = final_response
    return final_response


def program_manager_support_function(query: str) -> str:
    """Generate and evaluate product features using prior user stories."""
    contextual_query = (
        f"{query}\n\n"
        "Use the following validated user stories as the items to organize into product features:\n"
        f"{workflow_context['user_stories']}\n\n"
        "Return one or more features using the required Feature Name, Description, "
        "Key Functionality, and User Benefit fields."
    )
    response_from_knowledge_agent = program_manager_knowledge_agent.respond(contextual_query)
    evaluation_result = program_manager_evaluation_agent.evaluate(
        contextual_query,
        initial_response=response_from_knowledge_agent,
    )
    final_response = evaluation_result["final_response"]
    workflow_context["features"] = final_response
    return final_response


def development_engineer_support_function(query: str) -> str:
    """Generate and evaluate engineering tasks using prior workflow artifacts."""
    contextual_query = (
        f"{query}\n\n"
        "Create detailed engineering tasks for the validated user stories and product features below.\n\n"
        "VALIDATED USER STORIES:\n"
        f"{workflow_context['user_stories']}\n\n"
        "VALIDATED PRODUCT FEATURES:\n"
        f"{workflow_context['features']}\n\n"
        "Each task must include Task ID, Task Title, Related User Story, Description, "
        "Acceptance Criteria, Estimated Effort, and Dependencies."
    )
    response_from_knowledge_agent = development_engineer_knowledge_agent.respond(contextual_query)
    evaluation_result = development_engineer_evaluation_agent.evaluate(
        contextual_query,
        initial_response=response_from_knowledge_agent,
    )
    return evaluation_result["final_response"]


# === Routing Agent ===
routing_agent = RoutingAgent(openai_api_key=openai_api_key)
routing_agent.agents = [
    {
        "name": "Product Manager",
        "description": (
            "Define user stories for the product. Responsible for product personas and "
            "user stories in As a user, I want, so that format. Does not define product "
            "features or engineering tasks."
        ),
        "func": lambda query: product_manager_support_function(query),
    },
    {
        "name": "Program Manager",
        "description": (
            "Organize validated user stories into product features. Defines Feature Name, "
            "Description, Key Functionality, and User Benefit. Does not create engineering tasks."
        ),
        "func": lambda query: program_manager_support_function(query),
    },
    {
        "name": "Development Engineer",
        "description": (
            "Create detailed engineering tasks for validated user stories and product features, "
            "including acceptance criteria, estimated effort, and dependencies."
        ),
        "func": lambda query: development_engineer_support_function(query),
    },
]


# The primary rubric run requests the complete plan while explicitly asking for
# top-level stages only. The ActionPlanningAgent still decides/extracts the steps;
# the workflow does not hardcode routed results.
workflow_prompt = (
    "Create a complete development plan for this product using only the three top-level "
    "stages in your planning knowledge. Do not expand those stages into substeps."
)


def _validate_primary_workflow_steps(workflow_steps: list[str]) -> None:
    """Fail clearly if the primary planner drifts away from the three rubric stages."""
    if len(workflow_steps) != 3:
        raise RuntimeError(
            "The primary workflow must contain exactly three top-level stages: "
            "user stories, product features, and engineering tasks. "
            f"Received {len(workflow_steps)} steps: {workflow_steps}"
        )

    normalized_steps = [step.lower() for step in workflow_steps]
    expected_concepts = (
        ("user stor",),
        ("feature",),
        ("task",),
    )

    for index, (step, required_terms) in enumerate(
        zip(normalized_steps, expected_concepts), start=1
    ):
        if not all(term in step for term in required_terms):
            raise RuntimeError(
                f"Workflow stage {index} is not clearly aligned with the expected "
                f"rubric artifact. Received: {workflow_steps[index - 1]!r}"
            )


def run_workflow() -> list[str]:
    """Plan, route, evaluate, and collect the complete project-management workflow."""
    print("\n*** Workflow execution started ***\n")
    print(f"Task to complete in this workflow, workflow prompt = {workflow_prompt}")
    print("\nDefining workflow steps from the workflow prompt")

    workflow_steps = action_planning_agent.extract_steps_from_prompt(workflow_prompt)
    if not workflow_steps:
        raise RuntimeError("The ActionPlanningAgent returned no workflow steps.")

    _validate_primary_workflow_steps(workflow_steps)

    print("Workflow steps:")
    for index, step in enumerate(workflow_steps, start=1):
        print(f"{index}. {step}")

    completed_steps: list[str] = []

    for index, step in enumerate(workflow_steps, start=1):
        print(f"\n=== Executing workflow step {index}/{len(workflow_steps)} ===")
        print(f"Current step: {step}")
        try:
            result = routing_agent.route(step)
        except Exception as exc:
            print(f"ERROR while processing step {index}: {exc}")
            raise

        completed_steps.append(result)
        print("\nStep result:")
        print(result)

    print("\n\n=== FINAL WORKFLOW OUTPUT ===")
    for index, (step, result) in enumerate(zip(workflow_steps, completed_steps), start=1):
        print(f"\n--- Completed Step {index}: {step} ---")
        print(result)

    return completed_steps


if __name__ == "__main__":
    run_workflow()
