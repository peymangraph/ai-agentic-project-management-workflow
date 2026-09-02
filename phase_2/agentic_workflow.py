"""General-purpose technical project-management agentic workflow.

Pilot input: Product-Spec-Email-Router.txt

Follow the Udacity Phase 2 TODO sequence and rubric checklist when completing
this file. Keep the workflow reusable for future product specifications.
"""

import os

from dotenv import load_dotenv

# TODO 1: Import ActionPlanningAgent, KnowledgeAugmentedPromptAgent,
# EvaluationAgent, and RoutingAgent from workflow_agents.base_agents.


# TODO 2: Load the OpenAI API key into `openai_api_key`.
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")


# TODO 3: Load Product-Spec-Email-Router.txt into `product_spec`.
product_spec = ""


# The starter course file provides the knowledge/persona strings used below.
# Preserve those supplied strings when transferring the official starter code.
knowledge_action_planning = ""
persona_product_manager = ""
knowledge_product_manager = ""
persona_program_manager = ""
knowledge_program_manager = ""
persona_program_manager_eval = ""
persona_dev_engineer = ""
knowledge_dev_engineer = ""
persona_dev_engineer_eval = ""
workflow_prompt = ""


# TODO 4: Instantiate ActionPlanningAgent with knowledge_action_planning.
action_planning_agent = None


# TODO 5: Append product_spec to knowledge_product_manager.


# TODO 6: Instantiate the Product Manager KnowledgeAugmentedPromptAgent.
product_manager_knowledge_agent = None


# TODO 7: Instantiate Product Manager EvaluationAgent with exact criteria:
# "The answer should be stories that follow the following structure: As a
# [type of user], I want [an action or feature] so that [benefit/value]."
product_manager_evaluation_agent = None


# TODO 8: Instantiate Program Manager knowledge and evaluation agents.
# Required feature structure:
# Feature Name:
# Description:
# Key Functionality:
# User Benefit:
program_manager_knowledge_agent = None
program_manager_evaluation_agent = None


# TODO 9: Instantiate Development Engineer knowledge and evaluation agents.
# Required task structure:
# Task ID:
# Task Title:
# Related User Story:
# Description:
# Acceptance Criteria:
# Estimated Effort:
# Dependencies:
development_engineer_knowledge_agent = None
development_engineer_evaluation_agent = None


# TODO 10: Instantiate RoutingAgent and assign `.agents` to route dictionaries
# for Product Manager, Program Manager, and Development Engineer.
routing_agent = None


# TODO 11: Implement support functions.
def product_manager_support_function(query: str):
    """Generate and evaluate Product Manager output for a routed step."""
    raise NotImplementedError


def program_manager_support_function(query: str):
    """Generate and evaluate Program Manager output for a routed step."""
    raise NotImplementedError


def development_engineer_support_function(query: str):
    """Generate and evaluate Development Engineer output for a routed step."""
    raise NotImplementedError


# TODO 12: Implement the main workflow.
def run_workflow():
    """Plan, route, evaluate, and collect project-management workflow steps."""
    # Expected high-level orchestration:
    # workflow_steps = action_planning_agent.extract_steps_from_prompt(workflow_prompt)
    # completed_steps = []
    # for step in workflow_steps:
    #     print(step)
    #     result = routing_agent.route(step)
    #     completed_steps.append(result)
    #     print(result)
    # print final workflow output
    raise NotImplementedError


if __name__ == "__main__":
    run_workflow()
