# Submission Outputs

Udacity requires execution evidence for all seven Phase 1 agent tests and for the full Phase 2 workflow. Run the commands below from the repository root after activating the project environment.

## Phase 1

```powershell
python phase_1/tests/direct_prompt_agent.py | Tee-Object submission_outputs/01-direct-prompt.txt
python phase_1/tests/augmented_prompt_agent.py | Tee-Object submission_outputs/02-augmented-prompt.txt
python phase_1/tests/knowledge_augmented_prompt_agent.py | Tee-Object submission_outputs/03-knowledge-augmented-prompt.txt
python phase_1/tests/rag_knowledge_prompt_agent.py | Tee-Object submission_outputs/04-rag-knowledge-prompt.txt
python phase_1/tests/evaluation_agent.py | Tee-Object submission_outputs/05-evaluation-agent.txt
python phase_1/tests/routing_agent.py | Tee-Object submission_outputs/06-routing-agent.txt
python phase_1/tests/action_planning_agent.py | Tee-Object submission_outputs/07-action-planning-agent.txt
```

## Phase 2

```powershell
python phase_2/agentic_workflow.py | Tee-Object submission_outputs/08-agentic-workflow.txt
```

Review the saved output files before committing them. They should show successful execution and must not contain API keys or other secrets.

If you prefer screenshots, capture the same successful terminal runs and organize the images alongside the submission package. Text output files are easier to review and satisfy the project instructions.
