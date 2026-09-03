"""Standalone test for the Udacity-provided RAGKnowledgePromptAgent behavior."""

import os
import sys
import tempfile
from pathlib import Path

from dotenv import load_dotenv

PHASE_1_DIR = Path(__file__).resolve().parents[1]
if str(PHASE_1_DIR) not in sys.path:
    sys.path.insert(0, str(PHASE_1_DIR))

from workflow_agents.base_agents import RAGKnowledgePromptAgent


REPO_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(REPO_ROOT / ".env")
openai_api_key = os.getenv("OPENAI_API_KEY")

if not openai_api_key:
    raise ValueError("OPENAI_API_KEY was not found in the repository-level .env file.")

persona = "You are a college professor; your answer always starts with: Dear students,"
knowledge_text = """
Clara is a marine biologist and science communicator in Boston. Inspired by her
family's resilience and love of learning, she created a podcast called
Crosscurrents. The podcast explores the intersection of science, culture, and
ethics. Clara interviews researchers, engineers, artists, and activists about
subjects including marine ecology, AI ethics, endangered languages, climate
migration, neuroplasticity, prompt engineering, and retrieval-augmented
generation. She also builds Python dashboards for ocean research and contributes
to open-source projects involving semantic search and vector databases.
"""

prompt = "What is the podcast that Clara hosts about?"

print("=== RAGKnowledgePromptAgent Test ===")
print(f"Prompt: {prompt}")

# Temporary storage keeps generated chunk/embedding CSV files out of the repo.
with tempfile.TemporaryDirectory() as temp_dir:
    rag_agent = RAGKnowledgePromptAgent(
        openai_api_key=openai_api_key,
        persona=persona,
        chunk_size=260,
        chunk_overlap=50,
        storage_dir=temp_dir,
    )
    chunks = rag_agent.chunk_text(knowledge_text)
    rag_agent.calculate_embeddings()
    answer = rag_agent.find_prompt_in_knowledge(prompt)

    print(f"Chunks created: {len(chunks)}")
    print(f"Response: {answer}")
    print("Knowledge source: retrieved chunks from the explicitly supplied knowledge corpus.")
