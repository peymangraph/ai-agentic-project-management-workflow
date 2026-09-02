# Udacity Submission Rubric Checklist

Use this checklist before final submission.

## Phase 1 — Agentic Toolkit

### Agent Implementation

- [ ] `DirectPromptAgent` implemented in `workflow_agents/base_agents.py`
- [ ] `AugmentedPromptAgent` implemented
- [ ] `KnowledgeAugmentedPromptAgent` implemented
- [ ] `EvaluationAgent` implemented
- [ ] `RoutingAgent` implemented
- [ ] `ActionPlanningAgent` implemented
- [ ] Provided `RAGKnowledgePromptAgent` retained and understood
- [ ] Every student-implemented agent has an `__init__` with required attributes
- [ ] Every agent exposes the required public method (`respond`, `evaluate`, `route`, or `extract_steps_from_prompt`)

### LLM Configuration

- [ ] API key is passed/configured securely and is not hardcoded in agent classes
- [ ] Direct LLM interactions use `gpt-3.5-turbo` unless instructions specify otherwise
- [ ] `RoutingAgent` uses `text-embedding-3-large`
- [ ] `EvaluationAgent` uses `temperature=0` for evaluation and correction-instruction calls

### Agent-Specific Requirements

#### DirectPromptAgent
- [ ] Sends only a user message
- [ ] Does not use a system prompt
- [ ] Returns only response text

#### AugmentedPromptAgent
- [ ] Stores persona
- [ ] System prompt establishes persona
- [ ] System prompt instructs model to forget prior context
- [ ] Returns only response text

#### KnowledgeAugmentedPromptAgent
- [ ] Stores persona and knowledge
- [ ] System prompt says to forget previous context
- [ ] System prompt says to use only provided knowledge
- [ ] Returns only response text

#### EvaluationAgent
- [ ] Loops up to `max_interactions`
- [ ] Retrieves worker response
- [ ] Evaluates response against explicit criteria
- [ ] Generates correction instructions when needed
- [ ] Returns dictionary with final response, evaluation result, and iteration count

#### RoutingAgent
- [ ] Embeds user prompt
- [ ] Embeds every route description
- [ ] Computes cosine similarity
- [ ] Selects highest-scoring route
- [ ] Invokes selected route's callable function
- [ ] Returns selected agent response

#### ActionPlanningAgent
- [ ] Uses an Action Planning Agent system role
- [ ] Uses supplied knowledge
- [ ] Uses `gpt-3.5-turbo`
- [ ] Parses LLM output into a clean list of actionable steps

## Phase 1 — Testing Evidence

- [ ] Direct Prompt Agent test script
- [ ] Augmented Prompt Agent test script
- [ ] Knowledge Augmented Prompt Agent test script
- [ ] RAG Knowledge Prompt Agent test script
- [ ] Evaluation Agent test script
- [ ] Routing Agent test script
- [ ] Action Planning Agent test script
- [ ] Seven successful terminal-output screenshots or text files collected
- [ ] Direct Prompt evidence explains general LLM knowledge source
- [ ] Augmented Prompt evidence discusses knowledge source and persona impact
- [ ] Knowledge Augmented evidence confirms provided knowledge was used

## Phase 2 — Setup

- [ ] `agentic_workflow.py` imports `ActionPlanningAgent`
- [ ] Imports `KnowledgeAugmentedPromptAgent`
- [ ] Imports `EvaluationAgent`
- [ ] Imports `RoutingAgent`
- [ ] Loads `OPENAI_API_KEY` from environment
- [ ] Loads `Product-Spec-Email-Router.txt` into `product_spec`
- [ ] Instantiates Action Planning Agent with `knowledge_action_planning`
- [ ] Appends `product_spec` to `knowledge_product_manager`

## Phase 2 — Specialized Teams

### Product Manager
- [ ] Product Manager knowledge agent instantiated with correct persona/knowledge
- [ ] Product Manager EvaluationAgent uses exact required criteria
- [ ] Output format: `As a [type of user], I want [an action or feature] so that [benefit/value].`

### Program Manager
- [ ] Program Manager knowledge agent instantiated
- [ ] Program Manager EvaluationAgent instantiated
- [ ] Output contains `Feature Name:`
- [ ] Output contains `Description:`
- [ ] Output contains `Key Functionality:`
- [ ] Output contains `User Benefit:`

### Development Engineer
- [ ] Development Engineer knowledge agent instantiated
- [ ] Development Engineer EvaluationAgent instantiated
- [ ] Output contains `Task ID:`
- [ ] Output contains `Task Title:`
- [ ] Output contains `Related User Story:`
- [ ] Output contains `Description:`
- [ ] Output contains `Acceptance Criteria:`
- [ ] Output contains `Estimated Effort:`
- [ ] Output contains `Dependencies:`

## Phase 2 — Routing

- [ ] `RoutingAgent` instantiated
- [ ] `.agents` contains route dictionaries for Product Manager, Program Manager, Development Engineer
- [ ] Every route has `name`
- [ ] Every route has `description`
- [ ] Every route has `func`
- [ ] Route descriptions clearly distinguish responsibilities

## Phase 2 — Support Functions

- [ ] `product_manager_support_function(query)` implemented
- [ ] `program_manager_support_function(query)` implemented
- [ ] `development_engineer_support_function(query)` implemented
- [ ] Each support function calls the corresponding knowledge agent's `.respond(query)`
- [ ] Each passes the result to the corresponding EvaluationAgent `.evaluate(...)`
- [ ] Each returns the validated `final_response`

## Phase 2 — Workflow Execution

- [ ] Action planner generates `workflow_steps` from `workflow_prompt`
- [ ] `completed_steps = []` initialized
- [ ] Workflow iterates through every step
- [ ] Current step is printed
- [ ] `routing_agent.route(step)` is called
- [ ] Result is appended to `completed_steps`
- [ ] Current result is printed
- [ ] Final workflow output is printed
- [ ] Final Email Router output includes user stories, features, and engineering tasks

## Code Quality

- [ ] Descriptive variable/function names
- [ ] Python naming conventions followed
- [ ] Classes/functions contain useful docstrings or comments
- [ ] `base_agents.py` is organized by agent class
- [ ] `agentic_workflow.py` is logically organized by setup, agents, support functions, and execution
- [ ] No secrets committed

## Optional Standout Improvements

- [ ] Demonstrate a modified `workflow_prompt`
- [ ] Add richer evaluation/scoring criteria
- [ ] Add basic error handling or logging
- [ ] Add `reflection.md` discussing strengths, limitations, and one concrete improvement
