"""Standalone test for RoutingAgent."""

import os
import sys
from pathlib import Path

from dotenv import load_dotenv

PHASE_1_DIR = Path(__file__).resolve().parents[1]
if str(PHASE_1_DIR) not in sys.path:
    sys.path.insert(0, str(PHASE_1_DIR))

from workflow_agents.base_agents import KnowledgeAugmentedPromptAgent, RoutingAgent


REPO_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(REPO_ROOT / ".env")
openai_api_key = os.getenv("OPENAI_API_KEY")

if not openai_api_key:
    raise ValueError("OPENAI_API_KEY was not found in the repository-level .env file.")

texas_agent = KnowledgeAugmentedPromptAgent(
    openai_api_key,
    "You are a college professor who answers questions about Texas.",
    "You know everything about Texas, including its cities, communities, and history.",
)

europe_agent = KnowledgeAugmentedPromptAgent(
    openai_api_key,
    "You are a college professor who answers questions about Europe.",
    "You know everything about Europe, including Italy, Rome, European places, and history.",
)

math_agent = KnowledgeAugmentedPromptAgent(
    openai_api_key,
    "You are a college math professor.",
    "You know everything about math. For prompts with numbers, extract the mathematical relationship and show the answer without explanation.",
)

routing_agent = RoutingAgent(openai_api_key)
routing_agent.agents = [
    {
        "name": "texas agent",
        "description": "Answer a question about Texas, Texas cities, or Texas history.",
        "func": lambda query: texas_agent.respond(query),
    },
    {
        "name": "europe agent",
        "description": "Answer a question about Europe, Italy, Rome Italy, or European history.",
        "func": lambda query: europe_agent.respond(query),
    },
    {
        "name": "math agent",
        "description": "When a prompt contains numbers or asks for a calculation, respond with a math formula and answer.",
        "func": lambda query: math_agent.respond(query),
    },
]

test_prompts = [
    "Tell me about the history of Rome, Texas",
    "Tell me about the history of Rome, Italy",
    "One story takes 2 days, and there are 20 stories",
]

print("=== RoutingAgent Test ===")
for prompt in test_prompts:
    print(f"\nPrompt: {prompt}")
    print("Response:")
    print(routing_agent.route(prompt))
