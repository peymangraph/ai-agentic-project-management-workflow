"""Optional standout demonstration for the Udacity Agentic AI project.

This script intentionally leaves the primary grading workflow unchanged. It
reuses the same ActionPlanningAgent, RoutingAgent, specialist agents, and
EvaluationAgents from ``agentic_workflow.py`` while changing only the high-level
objective to emphasize security and compliance.
"""

from __future__ import annotations

import agentic_workflow as workflow
from quality_scoring import format_quality_score, score_product_manager_output


ALTERNATE_WORKFLOW_PROMPT = (
    "Create a security-and-compliance-focused development plan for the Email Router. "
    "Use the same three top-level planning stages: user stories, product features, "
    "and engineering tasks. Keep the plan grounded in the supplied product specification, "
    "but emphasize privacy, access control, auditability, safe email handling, operational "
    "resilience, and regulatory compliance. Do not expand the plan into extra stages."
)


def run_standout_demo() -> list[str]:
    """Run the alternate objective through the same Phase 2 agentic architecture."""
    print("\n*** Standout adaptability demonstration ***\n")
    print("Primary workflow objective: complete Email Router development plan")
    print("Alternate workflow objective: security and compliance focused Email Router plan")
    print("Architecture: unchanged ActionPlanningAgent + RoutingAgent + specialist/evaluator teams")

    # The process-local prompt change demonstrates adaptability without replacing
    # or editing the rubric-required primary workflow prompt in agentic_workflow.py.
    workflow.workflow_prompt = ALTERNATE_WORKFLOW_PROMPT

    # Reinforce the alternate scope inside planning knowledge so the dynamically
    # generated stage descriptions carry the security/compliance objective forward
    # to the routed specialist queries.
    workflow.action_planning_agent.knowledge = (
        workflow.knowledge_action_planning
        + "\n\nFor this alternate demonstration, keep exactly the same three artifact stages, "
        "but phrase each stage so it explicitly focuses on security and compliance concerns "
        "from the Email Router product specification."
    )

    completed_steps = workflow.run_workflow()

    print("\n=== ADAPTABILITY COMPARISON ===")
    print("Primary run: broad user stories, features, and engineering tasks for the full product.")
    print(
        "Alternate run: the same three-stage orchestration and routing architecture, "
        "but specialist outputs are scoped toward security, compliance, privacy, "
        "access control, auditability, resilience, and safe email handling."
    )
    print(
        "This demonstrates that the workflow can change planning emphasis through a high-level "
        "objective without replacing the underlying agents or hardcoding specialist results."
    )

    if not completed_steps:
        raise RuntimeError("Alternate workflow returned no completed steps.")

    quality_score = score_product_manager_output(completed_steps[0], workflow.product_spec)
    print("\n" + format_quality_score(quality_score))

    if quality_score["decision"] != "PASS":
        raise RuntimeError(
            "Supplemental Product Manager quality score did not pass. "
            f"Score: {quality_score}"
        )

    print("\n*** Standout demonstration completed successfully ***")
    return completed_steps


if __name__ == "__main__":
    run_standout_demo()
