"""Reusable agent classes for the AI-Powered Agentic Workflow project.

The six student-authored agents implement the behavior required by the Udacity
Phase 1 rubric. RAGKnowledgePromptAgent follows the implementation supplied in
the Udacity starter project, with small robustness improvements for file paths
and parsing.
"""

from __future__ import annotations

import ast
import csv
import math
import os
import re
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from openai import OpenAI


DEFAULT_OPENAI_BASE_URL = "https://openai.vocareum.com/v1"


def _create_openai_client(openai_api_key: str) -> OpenAI:
    """Create an OpenAI client for the Udacity/Vocareum-compatible endpoint."""
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
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
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
            f"Assume this persona: {self.persona}\n"
            "Forget all previous conversational context. Respond according to "
            "the persona for the current prompt only."
        )
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
            temperature=0,
        )
        return (response.choices[0].message.content or "").strip()


class KnowledgeAugmentedPromptAgent:
    """Respond using a persona and explicitly supplied knowledge only."""

    def __init__(self, openai_api_key: str, persona: str, knowledge: str):
        self.openai_api_key = openai_api_key
        self.persona = persona
        self.knowledge = knowledge
        self.client = _create_openai_client(self.openai_api_key)

    def respond(self, prompt: str) -> str:
        """Return an answer grounded only in the provided knowledge."""
        system_prompt = (
            f"You are {self.persona} knowledge-based assistant. Forget all previous context.\n"
            "Use only the following knowledge to answer, do not use your own knowledge: "
            f"{self.knowledge}\n"
            "Answer the prompt based on this knowledge, not your own."
        )
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
            temperature=0,
        )
        return (response.choices[0].message.content or "").strip()


class RAGKnowledgePromptAgent:
    """Retrieval-augmented agent based on the Udacity-provided implementation."""

    def __init__(
        self,
        openai_api_key: str,
        persona: str,
        chunk_size: int = 2000,
        chunk_overlap: int = 100,
        storage_dir: str | Path | None = None,
    ):
        if chunk_size <= 0:
            raise ValueError("chunk_size must be greater than zero.")
        if chunk_overlap < 0 or chunk_overlap >= chunk_size:
            raise ValueError("chunk_overlap must be non-negative and smaller than chunk_size.")

        self.persona = persona
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.openai_api_key = openai_api_key
        self.client = _create_openai_client(self.openai_api_key)
        self.storage_dir = Path(storage_dir) if storage_dir else Path.cwd()
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.unique_filename = (
            f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}.csv"
        )

    @property
    def chunks_path(self) -> Path:
        return self.storage_dir / f"chunks-{self.unique_filename}"

    @property
    def embeddings_path(self) -> Path:
        return self.storage_dir / f"embeddings-{self.unique_filename}"

    def get_embedding(self, text: str) -> list[float]:
        """Fetch an embedding using text-embedding-3-large."""
        response = self.client.embeddings.create(
            model="text-embedding-3-large",
            input=text,
            encoding_format="float",
        )
        return response.data[0].embedding

    @staticmethod
    def calculate_similarity(vector_one: list[float], vector_two: list[float]) -> float:
        """Return cosine similarity between two vectors."""
        vec1 = np.asarray(vector_one, dtype=float)
        vec2 = np.asarray(vector_two, dtype=float)
        denominator = np.linalg.norm(vec1) * np.linalg.norm(vec2)
        if denominator == 0:
            return 0.0
        return float(np.dot(vec1, vec2) / denominator)

    def chunk_text(self, text: str) -> list[dict[str, Any]]:
        """Split knowledge into overlapping chunks and persist them to CSV."""
        normalized = re.sub(r"[ \t]+", " ", text).strip()
        chunks: list[dict[str, Any]] = []
        start = 0
        chunk_id = 0

        while start < len(normalized):
            end = min(start + self.chunk_size, len(normalized))

            # Prefer a nearby sentence/paragraph boundary when possible.
            if end < len(normalized):
                window = normalized[start:end]
                boundary = max(window.rfind("\n"), window.rfind(". "))
                if boundary > self.chunk_size // 2:
                    end = start + boundary + (1 if window[boundary] == "\n" else 2)

            chunk_text = normalized[start:end].strip()
            if chunk_text:
                chunks.append(
                    {
                        "chunk_id": chunk_id,
                        "text": chunk_text,
                        "chunk_size": len(chunk_text),
                        "start_char": start,
                        "end_char": end,
                    }
                )
                chunk_id += 1

            if end >= len(normalized):
                break
            start = max(end - self.chunk_overlap, start + 1)

        with self.chunks_path.open("w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=["text", "chunk_size"])
            writer.writeheader()
            for chunk in chunks:
                writer.writerow(
                    {"text": chunk["text"], "chunk_size": chunk["chunk_size"]}
                )

        return chunks

    def calculate_embeddings(self) -> pd.DataFrame:
        """Calculate and persist embeddings for every previously created chunk."""
        if not self.chunks_path.exists():
            raise FileNotFoundError(
                "No chunk file was found. Call chunk_text(knowledge_text) first."
            )

        df = pd.read_csv(self.chunks_path, encoding="utf-8")
        df["embeddings"] = df["text"].apply(self.get_embedding)
        df.to_csv(self.embeddings_path, encoding="utf-8", index=False)
        return df

    def find_prompt_in_knowledge(self, prompt: str) -> str:
        """Retrieve the most similar knowledge chunk and answer from that chunk only."""
        if not self.embeddings_path.exists():
            raise FileNotFoundError(
                "No embeddings file was found. Call calculate_embeddings() first."
            )

        prompt_embedding = self.get_embedding(prompt)
        df = pd.read_csv(self.embeddings_path, encoding="utf-8")
        df["embeddings"] = df["embeddings"].apply(
            lambda value: np.asarray(ast.literal_eval(value), dtype=float)
        )
        df["similarity"] = df["embeddings"].apply(
            lambda embedding: self.calculate_similarity(prompt_embedding, embedding)
        )

        best_chunk = str(df.loc[df["similarity"].idxmax(), "text"])
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": (
                        f"You are {self.persona}, a knowledge-based assistant. "
                        "Forget previous context."
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        "Answer based only on this retrieved information:\n"
                        f"{best_chunk}\n\nPrompt: {prompt}"
                    ),
                },
            ],
            temperature=0,
        )
        return (response.choices[0].message.content or "").strip()


class EvaluationAgent:
    """Evaluate and iteratively refine another agent's response."""

    def __init__(
        self,
        openai_api_key: str,
        persona: str,
        evaluation_criteria: str,
        agent_to_evaluate: Any | None = None,
        max_interactions: int = 5,
        worker_agent: Any | None = None,
    ):
        self.openai_api_key = openai_api_key
        self.persona = persona
        self.evaluation_criteria = evaluation_criteria
        self.agent_to_evaluate = (
            agent_to_evaluate if agent_to_evaluate is not None else worker_agent
        )
        self.worker_agent = self.agent_to_evaluate
        self.max_interactions = max_interactions
        self.client = _create_openai_client(self.openai_api_key)

        if self.agent_to_evaluate is None:
            raise ValueError("EvaluationAgent requires an agent_to_evaluate/worker_agent.")
        if self.max_interactions <= 0:
            raise ValueError("max_interactions must be greater than zero.")

    def _evaluate_response(self, worker_response: str) -> str:
        eval_prompt = (
            f"Does the following answer meet the evaluation criteria?\n\n"
            f"ANSWER:\n{worker_response}\n\n"
            f"EVALUATION CRITERIA:\n{self.evaluation_criteria}\n\n"
            "Respond Yes or No, followed by a concise reason."
        )
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": self.persona},
                {"role": "user", "content": eval_prompt},
            ],
            temperature=0,
        )
        return (response.choices[0].message.content or "").strip()

    def _correction_instructions(self, evaluation: str) -> str:
        instruction_prompt = (
            "Provide precise instructions to fix an answer based on the following "
            f"evaluation. Preserve correct content and change only what is needed:\n{evaluation}"
        )
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": self.persona},
                {"role": "user", "content": instruction_prompt},
            ],
            temperature=0,
        )
        return (response.choices[0].message.content or "").strip()

    def evaluate(
        self,
        initial_prompt: str,
        initial_response: str | None = None,
    ) -> dict[str, Any]:
        """Return final response, evaluation result, and interaction count.

        When ``initial_response`` is supplied, it is evaluated first. Otherwise
        the worker agent is asked to respond to ``initial_prompt``. Failed
        evaluations produce correction instructions and another worker attempt,
        up to ``max_interactions``.
        """
        prompt_to_evaluate = initial_prompt
        response_from_worker = initial_response or ""
        evaluation = ""

        for i in range(self.max_interactions):
            print(f"\n--- Interaction {i + 1} ---")

            if not (i == 0 and initial_response is not None):
                print("Step 1: Worker agent generates a response to the prompt")
                print(f"Prompt:\n{prompt_to_evaluate}")
                response_from_worker = self.agent_to_evaluate.respond(prompt_to_evaluate)
            else:
                print("Step 1: Using the worker response supplied for evaluation")

            print(f"Worker Agent Response:\n{response_from_worker}")
            print("Step 2: Evaluator agent judges the response")
            evaluation = self._evaluate_response(response_from_worker)
            print(f"Evaluator Agent Evaluation:\n{evaluation}")

            if evaluation.lower().startswith("yes"):
                print("Final solution accepted.")
                return {
                    "final_response": response_from_worker,
                    "evaluation": evaluation,
                    "iterations": i + 1,
                }

            print("Step 3: Generate correction instructions")
            instructions = self._correction_instructions(evaluation)
            print(f"Instructions to fix:\n{instructions}")

            prompt_to_evaluate = (
                f"The original prompt was: {initial_prompt}\n"
                f"The response to that prompt was: {response_from_worker}\n"
                "It has been evaluated as not meeting the criteria.\n"
                f"Make only these corrections, preserving valid content: {instructions}"
            )

        return {
            "final_response": response_from_worker,
            "evaluation": evaluation,
            "iterations": self.max_interactions,
        }


class RoutingAgent:
    """Route a prompt to the configured agent with the highest semantic match."""

    def __init__(self, openai_api_key: str, agents: list[dict[str, Any]] | None = None):
        self.openai_api_key = openai_api_key
        self.agents = list(agents or [])
        self.client = _create_openai_client(self.openai_api_key)

    def get_embedding(self, text: str) -> list[float]:
        """Return a text embedding using text-embedding-3-large."""
        response = self.client.embeddings.create(
            model="text-embedding-3-large",
            input=text,
            encoding_format="float",
        )
        return response.data[0].embedding

    @staticmethod
    def _cosine_similarity(vector_one: list[float], vector_two: list[float]) -> float:
        dot_product = sum(a * b for a, b in zip(vector_one, vector_two))
        norm_one = math.sqrt(sum(a * a for a in vector_one))
        norm_two = math.sqrt(sum(b * b for b in vector_two))
        if norm_one == 0 or norm_two == 0:
            return 0.0
        return dot_product / (norm_one * norm_two)

    def route(self, prompt: str) -> Any:
        """Select the highest-similarity route, invoke its func, and return output."""
        if not self.agents:
            return "Sorry, no suitable agent could be selected."

        input_embedding = self.get_embedding(prompt)
        best_agent: dict[str, Any] | None = None
        best_score = -1.0

        for agent in self.agents:
            description = str(agent.get("description", "")).strip()
            func = agent.get("func")
            if not description or not callable(func):
                continue

            agent_embedding = self.get_embedding(description)
            similarity = self._cosine_similarity(input_embedding, agent_embedding)
            print(
                f"[Router] {agent.get('name', 'unnamed agent')}: "
                f"similarity={similarity:.3f}"
            )

            if similarity > best_score:
                best_score = similarity
                best_agent = agent

        if best_agent is None:
            return "Sorry, no suitable agent could be selected."

        print(f"[Router] Best agent: {best_agent['name']} (score={best_score:.3f})")
        return best_agent["func"](prompt)


class ActionPlanningAgent:
    """Extract a clean ordered list of actionable steps from a user prompt."""

    def __init__(self, openai_api_key: str, knowledge: str):
        self.openai_api_key = openai_api_key
        self.knowledge = knowledge
        self.client = _create_openai_client(self.openai_api_key)

    @staticmethod
    def _clean_steps(response_text: str) -> list[str]:
        stripped = response_text.strip()
        if not stripped:
            return []

        # Accept a Python/JSON-like list when the model returns one.
        try:
            parsed = ast.literal_eval(stripped)
            if isinstance(parsed, list):
                return [str(item).strip() for item in parsed if str(item).strip()]
        except (ValueError, SyntaxError):
            pass

        steps: list[str] = []
        for line in stripped.splitlines():
            line = line.strip()
            if not line or line.lower() in {"steps:", "action steps:"}:
                continue
            line = re.sub(r"^(?:[-*•]+\s*|\d+[.)]\s*)", "", line).strip()
            line = line.strip("'\" ,")
            if line:
                steps.append(line)
        return steps

    def extract_steps_from_prompt(self, prompt: str) -> list[str]:
        """Use supplied knowledge to return only the actionable steps requested."""
        system_prompt = (
            "You are an action planning agent. Using your knowledge, you extract "
            "from the user prompt the steps requested to complete the action the "
            "user is asking for. You return the steps as a list. Only return the "
            "steps in your knowledge. Forget any previous context. This is your "
            f"knowledge: {self.knowledge}"
        )
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
            temperature=0,
        )
        response_text = (response.choices[0].message.content or "").strip()
        return self._clean_steps(response_text)
