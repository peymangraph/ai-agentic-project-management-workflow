"""Standalone test for DirectPromptAgent."""

import os
import sys
from pathlib import Path

from dotenv import load_dotenv

# Make the phase_1 package directory importable when this script is executed
# directly from the repository root or from the tests directory.
PHASE_1_DIR = Path(__file__).resolve().parents[1]
if str(PHASE_1_DIR) not in sys.path:
    sys.path.insert(0, str(PHASE_1_DIR))

from workflow_agents.base_agents import DirectPromptAgent


# Load the API key from the repository-level .env file.
REPO_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(REPO_ROOT / ".env")
openai_api_key = os.getenv("OPENAI_API_KEY")

if not openai_api_key:
    raise ValueError(
        "OPENAI_API_KEY was not found. Add it to the repository-level .env file."
    )


# Instantiate the DirectPromptAgent using the securely loaded API key.
direct_agent = DirectPromptAgent(openai_api_key=openai_api_key)

# The DirectPromptAgent sends this user prompt directly to the LLM without a
# system prompt, additional knowledge, memory, or tools.
prompt = "What is the Capital of France?"
direct_agent_response = direct_agent.respond(prompt)


print("=== DirectPromptAgent Test ===")
print(f"Prompt: {prompt}")
print(f"Response: {direct_agent_response}")
print(
    "Knowledge source: The DirectPromptAgent relies on the selected LLM's "
    "general pretrained knowledge because no additional context or external "
    "knowledge is supplied to the agent."
)
