"""Reusable agent classes for the AI-Powered Agentic Workflow project.

This module implements the six student-authored agents required by the
Udacity Phase 1 rubric. The RAGKnowledgePromptAgent remains a placeholder
until the course-provided implementation is inserted unchanged.
"""

import math
import os
import re
from typing import Any, Callable

from openai import OpenAI


DEFAULT_OPENAI_BASE_URL = "https://openai.vocareum.com/v1"


def _create_openai_client(openai_api_key: str) -> OpenAI:
    """Create an OpenAI client compatible with the Udacity/Vocareum endpoint.

    The API key is always supplied by the caller. The base URL can be
    overridden with OPENAI_BASE_URL when running against another compatible
    endpoint.
    """
    if not openai_api_key:
        raise ValueError("An OpenAI API key must be provided when creating an agent.")

    return OpenAI(
        api_key=openai_api_key,
        base_url=os.getenv("OPENAI_BASE_URL", DEFAULT_OPENAI_BASE_URL),
    )


class DirectPromptAgent:
    """Send a user prompt directly to an LLM without a system prompt."""

    def __init__(self, openai_api_key: str):
        self.openai_api_key = openai_api_key
        self.client = _create_openai_client(self.openai_api_key)

    def respond(self, prompt: str) -> str:
        """Return only the model's textual response."""
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt},
            ],
        )
        return (response.choices[0].message.content or "").strip()


class AugmentedPromptAgent:
    """Respond using a predefined persona supplied through a system prompt."""

    def __init__(self, openai_api_key: str, persona: str):
        self.openai_api_key = openai_api_key
        self.persona = persona
        self.client = _create_openai_client(self.openai_api_key)

    def respond(self, prompt: str) -> str:
        """Return only the model's textual response."""
        system_prompt = (
            f"{self.persona}\n"
            "Forget all previous conversational context and respond only "
            "according to this persona."
        )

        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
        )
        return (response.choices[0].message.content or "").strip()


class KnowledgeAugmentedPromptAgent:
    """Respond using a persona and explicitly supplied knowledge only."""

    def __init__(self, openai_api_key: str, persona: str, knowledge: str):
        self.openai_api_key = openai_api_key
        self.persona = persona
        self.knowledge = knowledge
        self.client = _create_openai_client(self.openai_api_key)

        # These values make EvaluationAgent compatible with both Phase 1 and
        # Phase 2 usage patterns without changing the public respond() method.
        self._last_prompt: str | None = None
        self._last_response: str | None = None

    def respond(self, prompt: str) -> str:
        """Return an answer grounded only in the provided knowledge."""
        system_prompt = (
            f"{self.persona}\n"
            "You are a knowledge-based assistant. Forget all previous context.\n"
            "Use only the following knowledge to answer, do not use your own "
            f"knowledge:\n{self.knowledge}\n"
            "Answer the prompt based on this knowledge, not your own."
        )

        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
        )
        result = (response.choices[0].message.content or "").strip()
        self._last_prompt = prompt
        self._last_response = result
        return result


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
        if max_interactions < 1:
            raise ValueError("max_interactions must be at least 1.")

        self.openai_api_key = openai_api_key
        self.persona = persona
        self.evaluation_criteria = evaluation_criteria
        self.agent_to_evaluate = agent_to_evaluate
        self.max_interactions = max_interactions
        self.client = _create_openai_client(self.openai_api_key)

    def _evaluate_response(self, original_prompt: str, response_text: str) -> str:
        """Evaluate one worker response against the configured criteria."""
        evaluation_prompt = f"""
Original request:
{original_prompt}

Response to evaluate:
{response_text}

Evaluation criteria:
{self.evaluation_criteria}

Determine whether the response satisfies every criterion.
If it does, begin your answer with exactly: PASS
If it does not, begin your answer with exactly: FAIL
After PASS or FAIL, briefly explain the evaluation.
""".strip()

        evaluation_response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": self.persona},
                {"role": "user", "content": evaluation_prompt},
            ],
            temperature=0,
        )
        return (evaluation_response.choices[0].message.content or "").strip()

    def _create_correction_instructions(
        self,
        original_prompt: str,
        response_text: str,
        evaluation_result: str,
    ) -> str:
        """Generate actionable instructions for correcting a failed response."""
        correction_prompt = f"""
The following response did not satisfy the required evaluation criteria.

Original request:
{original_prompt}

Current response:
{response_text}

Evaluation result:
{evaluation_result}

Required criteria:
{self.evaluation_criteria}

Write clear correction instructions for the worker agent. Include the original
request and tell the worker exactly what must be changed so the next response
satisfies every criterion. Return only the correction instructions.
""".strip()

        correction_response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": self.persona},
                {"role": "user", "content": correction_prompt},
            ],
            temperature=0,
        )
        return (correction_response.choices[0].message.content or "").strip()

    def evaluate(self, prompt_or_response: str) -> dict:
        """Return final response, evaluation result, and iteration count.

        Phase 1 can call evaluate() with an original prompt. Phase 2 can first
        call the worker's respond() method and then pass that generated response
        to evaluate(). The latter is detected using the worker's most recent
        response when available.
        """
        worker_last_response = getattr(self.agent_to_evaluate, "_last_response", None)
        worker_last_prompt = getattr(self.agent_to_evaluate, "_last_prompt", None)

        if worker_last_response is not None and prompt_or_response == worker_last_response:
            original_prompt = worker_last_prompt or ""
            current_response = prompt_or_response
        else:
            original_prompt = prompt_or_response
            current_response = self.agent_to_evaluate.respond(original_prompt)

        evaluation_result = ""

        for interaction in range(1, self.max_interactions + 1):
            evaluation_result = self._evaluate_response(
                original_prompt,
                current_response,
            )

            if evaluation_result.upper().startswith("PASS"):
                return {
                    "final_response": current_response,
                    "evaluation": evaluation_result,
                    "iterations": interaction,
                }

            if interaction == self.max_interactions:
                break

            correction_instructions = self._create_correction_instructions(
                original_prompt,
                current_response,
                evaluation_result,
            )
            current_response = self.agent_to_evaluate.respond(correction_instructions)

        return {
            "final_response": current_response,
            "evaluation": evaluation_result,
            "iterations": self.max_interactions,
        }


class RoutingAgent:
    """Route a prompt to the most semantically relevant configured agent."""

    def __init__(self, openai_api_key: str):
        self.openai_api_key = openai_api_key
        self.agents: list[dict[str, Any]] = []
        self.client = _create_openai_client(self.openai_api_key)

    def get_embedding(self, text: str) -> list[float]:
        """Return a text embedding using text-embedding-3-large."""
        response = self.client.embeddings.create(
            model="text-embedding-3-large",
            input=text,
        )
        return response.data[0].embedding

    @staticmethod
    def _cosine_similarity(vector_a: list[float], vector_b: list[float]) -> float:
        """Compute cosine similarity between two vectors."""
        if len(vector_a) != len(vector_b):
            raise ValueError("Embedding vectors must have the same length.")

        dot_product = sum(a * b for a, b in zip(vector_a, vector_b))
        norm_a = math.sqrt(sum(a * a for a in vector_a))
        norm_b = math.sqrt(sum(b * b for b in vector_b))

        if norm_a == 0 or norm_b == 0:
            return 0.0

        return dot_product / (norm_a * norm_b)

    def route(self, prompt: str) -> Any:
        """Select the highest-similarity route and invoke its callable."""
        if not self.agents:
            raise ValueError("RoutingAgent has no configured agents.")

        prompt_embedding = self.get_embedding(prompt)
        best_agent: dict[str, Any] | None = None
        best_similarity = float("-inf")

        for agent in self.agents:
            description = agent.get("description", "")
            func: Callable[[str], Any] | None = agent.get("func")

            if not description:
                raise ValueError("Every routing entry must include a description.")
            if not callable(func):
                raise ValueError("Every routing entry must include a callable func.")

            description_embedding = self.get_embedding(description)
            similarity = self._cosine_similarity(
                prompt_embedding,
                description_embedding,
            )

            if similarity > best_similarity:
                best_similarity = similarity
                best_agent = agent

        if best_agent is None:
            raise RuntimeError("Unable to select a route for the supplied prompt.")

        selected_func = best_agent["func"]
        return selected_func(prompt)


class ActionPlanningAgent:
    """Extract a clean ordered list of actionable steps from a user prompt."""

    def __init__(self, openai_api_key: str, knowledge: str):
        self.openai_api_key = openai_api_key
        self.knowledge = knowledge
        self.client = _create_openai_client(self.openai_api_key)

    def extract_steps_from_prompt(self, prompt: str) -> list[str]:
        """Return a clean list of actionable workflow steps."""
        system_prompt = f"""
You are an Action Planning Agent. Your role is to analyze a user's task and
extract the ordered, actionable steps needed to complete it.

Use the following knowledge when creating the action plan:
{self.knowledge}

Return only the action steps, one step per line. Do not include introductory
or concluding commentary.
""".strip()

        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
        )

        response_text = (response.choices[0].message.content or "").strip()
        steps: list[str] = []

        for line in response_text.splitlines():
            cleaned_line = line.strip()
            if not cleaned_line:
                continue

            # Remove common numbering/bullet prefixes while preserving the
            # actual action text returned by the planning model.
            cleaned_line = re.sub(
                r"^(?:step\s+\d+\s*[:.)-]?|\d+\s*[.)-]|[-*•])\s*",
                "",
                cleaned_line,
                flags=re.IGNORECASE,
            ).strip()

            if cleaned_line:
                steps.append(cleaned_line)

        return steps
