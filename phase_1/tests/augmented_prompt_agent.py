"""Standalone test for AugmentedPromptAgent."""

import os
import sys
from pathlib import Path

from dotenv import load_dotenv

# Make the phase_1 package directory importable when this script is executed
# directly from the repository root or from the tests directory.
PHASE_1_DIR = Path(__file__).resolve().parents[1]
if str(PHASE_1_DIR) not in sys.path:
    sys.path.insert(0, str(PHASE_1_DIR))

from workflow_agents.base_agents import AugmentedPromptAgent


# Load the API key from the repository-level .env file.
REPO_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(REPO_ROOT / ".env")
openai_api_key = os.getenv("OPENAI_API_KEY")

if not openai_api_key:
    raise ValueError(
        "OPENAI_API_KEY was not found. Add it to the repository-level .env file."
    )


# Define a persona so the same underlying LLM responds from a specific role
# and with a recognizable communication style.
persona = (
    "You are an enthusiastic travel guide. "
    "Explain destinations vividly, clearly, and concisely."
)

# Instantiate the AugmentedPromptAgent with the persona and securely loaded key.
augmented_agent = AugmentedPromptAgent(
    openai_api_key=openai_api_key,
    persona=persona,
)

# The model still relies primarily on its general pretrained knowledge because
# this agent does not receive an explicit external knowledge source. The persona
# changes how that knowledge is framed, including tone, emphasis, and style.
prompt = "Tell me about Paris in two sentences."
augmented_agent_response = augmented_agent.respond(prompt)


print("=== AugmentedPromptAgent Test ===")
print(f"Persona: {persona}")
print(f"Prompt: {prompt}")
print(f"Response: {augmented_agent_response}")
print(
    "Knowledge source: The AugmentedPromptAgent primarily uses the LLM's "
    "general pretrained knowledge because no explicit external knowledge was supplied."
)
print(
    "Persona impact: The travel-guide persona influences the tone, wording, "
    "focus, and presentation of the response while the underlying factual "
    "knowledge still comes from the model."
)
