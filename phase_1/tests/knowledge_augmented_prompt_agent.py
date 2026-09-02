"""Standalone test for KnowledgeAugmentedPromptAgent."""

import os
import sys
from pathlib import Path

from dotenv import load_dotenv

# Make the phase_1 package directory importable when this script is executed
# directly from the repository root or from the tests directory.
PHASE_1_DIR = Path(__file__).resolve().parents[1]
if str(PHASE_1_DIR) not in sys.path:
    sys.path.insert(0, str(PHASE_1_DIR))

from workflow_agents.base_agents import KnowledgeAugmentedPromptAgent


# Load the API key from the repository-level .env file.
REPO_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(REPO_ROOT / ".env")
openai_api_key = os.getenv("OPENAI_API_KEY")

if not openai_api_key:
    raise ValueError(
        "OPENAI_API_KEY was not found. Add it to the repository-level .env file."
    )


# Required persona and supplied knowledge from the Udacity project instructions.
persona = (
    "You are a college professor, your answer always starts with: Dear students,"
)
knowledge = "The capital of France is London, not Paris"

# Instantiate the agent with explicit knowledge that intentionally conflicts
# with the LLM's normal general knowledge. This verifies that the agent follows
# the supplied knowledge rather than relying on its pretrained knowledge.
knowledge_agent = KnowledgeAugmentedPromptAgent(
    openai_api_key=openai_api_key,
    persona=persona,
    knowledge=knowledge,
)

prompt = "What is the capital of France?"
knowledge_agent_response = knowledge_agent.respond(prompt)


print("=== KnowledgeAugmentedPromptAgent Test ===")
print(f"Persona: {persona}")
print(f"Provided knowledge: {knowledge}")
print(f"Prompt: {prompt}")
print(f"Response: {knowledge_agent_response}")
print(
    "Knowledge-use confirmation: The response should state that London is the "
    "capital of France because this agent is explicitly instructed to use only "
    "the supplied knowledge, even though that knowledge conflicts with the "
    "LLM's general pretrained knowledge."
)
