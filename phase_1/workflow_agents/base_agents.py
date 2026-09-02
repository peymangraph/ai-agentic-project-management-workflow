"""Reusable agent classes for the AI-Powered Agentic Workflow project.

This file is intentionally scaffolded around the Udacity Phase 1 rubric.
Implement and validate each TODO with the corresponding standalone test.
"""

from typing import Any, Callable

from openai import OpenAI


class DirectPromptAgent:
    """Send a user prompt directly to an LLM without a system prompt."""

    def __init__(self, openai_api_key: str):
        self.openai_api_key = openai_api_key
        # TODO: Initialize the OpenAI client.

    def respond(self, prompt: str) -> str:
        """Return only the model's textual response."""
        # TODO: Use gpt-3.5-turbo and send only a user message.
        raise NotImplementedError


class AugmentedPromptAgent:
    """Respond using a predefined persona supplied through a system prompt."""

    def __init__(self, openai_api_key: str, persona: str):
        self.openai_api_key = openai_api_key
        self.persona = persona
        # TODO: Initialize the OpenAI client.

    def respond(self, prompt: str) -> str:
        """Return only the model's textual response."""
        # TODO: Set persona, instruct the model to forget previous context,
        # and use gpt-3.5-turbo.
        raise NotImplementedError


class KnowledgeAugmentedPromptAgent:
    """Respond using a persona and explicitly supplied knowledge only."""

    def __init__(self, openai_api_key: str, persona: str, knowledge: str):
        self.openai_api_key = openai_api_key
        self.persona = persona
        self.knowledge = knowledge
        # TODO: Initialize the OpenAI client.

    def respond(self, prompt: str) -> str:
        """Return an answer grounded only in the provided knowledge."""
        # TODO: Build the required knowledge-only system message and call
        # gpt-3.5-turbo.
        raise NotImplementedError


class RAGKnowledgePromptAgent:
    """Retrieval-augmented knowledge agent.

    Udacity provides this implementation. Replace this placeholder with the
    supplied course implementation rather than inventing an incompatible one.
    """

    pass


class EvaluationAgent:
    """Evaluate and iteratively refine another agent's response."""

    def __init__(
        self,
        openai_api_key: str,
        persona: str,
        evaluation_criteria: str,
        agent_to_evaluate: Any,
        max_interactions: int = 5,
    ):
        self.openai_api_key = openai_api_key
        self.persona = persona
        self.evaluation_criteria = evaluation_criteria
        self.agent_to_evaluate = agent_to_evaluate
        self.max_interactions = max_interactions
        # TODO: Initialize the OpenAI client.

    def evaluate(self, prompt_or_response: str) -> dict:
        """Return final response, evaluation result, and iteration count."""
        # TODO: Implement the bounded evaluation/refinement loop.
        # Evaluation and correction-instruction calls must use temperature=0.
        raise NotImplementedError


class RoutingAgent:
    """Route a prompt to the most semantically relevant configured agent."""

    def __init__(self, openai_api_key: str):
        self.openai_api_key = openai_api_key
        self.agents: list[dict[str, Any]] = []
        # TODO: Initialize the OpenAI client.

    def get_embedding(self, text: str) -> list[float]:
        """Return a text embedding using text-embedding-3-large."""
        # TODO: Call the embeddings API.
        raise NotImplementedError

    def route(self, prompt: str) -> Any:
        """Select the highest-similarity route and invoke its callable."""
        # TODO: Embed prompt and route descriptions, compute cosine similarity,
        # choose the highest scoring route, call its `func`, and return output.
        raise NotImplementedError


class ActionPlanningAgent:
    """Extract a clean ordered list of actionable steps from a user prompt."""

    def __init__(self, openai_api_key: str, knowledge: str):
        self.openai_api_key = openai_api_key
        self.knowledge = knowledge
        # TODO: Initialize the OpenAI client.

    def extract_steps_from_prompt(self, prompt: str) -> list[str]:
        """Return a clean list of actionable workflow steps."""
        # TODO: Use an Action Planning Agent system prompt, supplied knowledge,
        # gpt-3.5-turbo, and clean the model output into a list.
        raise NotImplementedError
