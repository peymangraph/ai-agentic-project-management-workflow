"""Standalone test for EvaluationAgent."""

import os
import sys
from pathlib import Path

from dotenv import load_dotenv

PHASE_1_DIR = Path(__file__).resolve().parents[1]
if str(PHASE_1_DIR) not in sys.path:
    sys.path.insert(0, str(PHASE_1_DIR))

from workflow_agents.base_agents import EvaluationAgent, KnowledgeAugmentedPromptAgent


REPO_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(REPO_ROOT / ".env")
openai_api_key = os.getenv("OPENAI_API_KEY")

if not openai_api_key:
    raise ValueError("OPENAI_API_KEY was not found in the repository-level .env file.")

prompt = "What is the capital of France?"

worker_persona = (
    "You are a college professor, your answer always starts with: Dear students,"
)
worker_knowledge = "The capitol of France is London, not Paris"
knowledge_agent = KnowledgeAugmentedPromptAgent(
    openai_api_key=openai_api_key,
    persona=worker_persona,
    knowledge=worker_knowledge,
)

# Keep the required evaluator role while making its scope explicit: the evaluator
# must judge only the supplied criterion. It must not use outside factual knowledge
# or invent unstated requirements such as capitalization or punctuation.
evaluator_persona = (
    "You are an evaluation agent that checks the answers of other worker agents. "
    "Evaluate only the explicit evaluation criteria supplied to you. Do not fact-check "
    "the answer using outside or general knowledge unless factual correctness is itself "
    "part of the stated criteria. Do not invent additional requirements such as all-caps, "
    "special punctuation, or a particular city. If a criterion only requires that the "
    "answer be solely the name of a city, then any bare city name satisfies that format criterion."
)
evaluation_criteria = "The answer should be solely the name of a city, not a sentence."
evaluation_agent = EvaluationAgent(
    openai_api_key=openai_api_key,
    persona=evaluator_persona,
    evaluation_criteria=evaluation_criteria,
    agent_to_evaluate=knowledge_agent,
    max_interactions=10,
)

print("=== EvaluationAgent Test ===")
print(f"Prompt: {prompt}")
evaluation_result = evaluation_agent.evaluate(prompt)

# The intentionally supplied knowledge says London. The evaluator may accept a
# trailing period, but it must not accept a sentence or unrelated explanation.
normalized_final_response = evaluation_result["final_response"].strip().rstrip(".").strip()
if normalized_final_response != "London":
    raise AssertionError(
        "EvaluationAgent accepted a response that did not satisfy the city-name-only "
        f"criterion. Final response: {evaluation_result['final_response']!r}"
    )

if evaluation_result["evaluation"].splitlines()[0].strip().upper() != "PASS":
    raise AssertionError(
        "EvaluationAgent did not finish with an explicit PASS verdict. "
        f"Evaluation: {evaluation_result['evaluation']!r}"
    )

print("Evaluation result:")
print(evaluation_result)
print("Validation: PASS verdict received and final accepted answer is London only.")
