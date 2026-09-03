"""Standalone test for ActionPlanningAgent."""

import os
import sys
from pathlib import Path

from dotenv import load_dotenv

PHASE_1_DIR = Path(__file__).resolve().parents[1]
if str(PHASE_1_DIR) not in sys.path:
    sys.path.insert(0, str(PHASE_1_DIR))

from workflow_agents.base_agents import ActionPlanningAgent


REPO_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(REPO_ROOT / ".env")
openai_api_key = os.getenv("OPENAI_API_KEY")

if not openai_api_key:
    raise ValueError("OPENAI_API_KEY was not found in the repository-level .env file.")

knowledge = """
# Fried Egg
1. Heat pan with oil or butter
2. Crack egg into pan
3. Cook until white is set (2-3 minutes)
4. Season with salt and pepper
5. Serve

# Scrambled Eggs
1. Crack eggs into a bowl
2. Beat eggs with a fork until mixed
3. Heat pan with butter or oil over medium heat
4. Pour egg mixture into pan
5. Stir gently as eggs cook
6. Remove from heat when eggs are just set but still moist
7. Season with salt and pepper
8. Serve immediately

# Boiled Eggs
1. Place eggs in a pot
2. Cover with cold water (about 1 inch above eggs)
3. Bring water to a boil
4. Remove from heat and cover pot
5. Let sit: 4-6 minutes for soft-boiled or 10-12 minutes for hard-boiled
6. Transfer eggs to ice water to stop cooking
7. Peel and serve
"""

action_planning_agent = ActionPlanningAgent(
    openai_api_key=openai_api_key,
    knowledge=knowledge,
)

prompt = "One morning I wanted to have scrambled eggs"
steps = action_planning_agent.extract_steps_from_prompt(prompt)

print("=== ActionPlanningAgent Test ===")
print(f"Prompt: {prompt}")
print("Extracted steps:")
for index, step in enumerate(steps, start=1):
    print(f"{index}. {step}")
