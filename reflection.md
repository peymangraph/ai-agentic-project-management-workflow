# Reflection

## Strengths

This project demonstrates how several agentic workflow patterns can be combined into one reusable technical project-management system. The Action Planning Agent decomposes a high-level request into smaller steps, the Routing Agent selects the most appropriate specialist for each step using embeddings and cosine similarity, and each specialist team pairs a knowledge-augmented worker with an Evaluation Agent. This separation of responsibilities makes the workflow easier to understand, test, and extend than a single monolithic prompt.

A second strength is output quality control. Product Manager, Program Manager, and Development Engineer outputs are evaluated against explicit structures before they are accepted. This creates a feedback loop rather than assuming the first LLM response is good enough. The workflow also carries validated artifacts forward so that later roles can build on user stories and features produced earlier in the run.

The agent classes are reusable beyond the Email Router pilot. Their public interfaces are generic: prompt agents return text, the Evaluation Agent returns a structured dictionary, the Routing Agent accepts route dictionaries, and the Action Planning Agent returns a list of steps. A different product specification can therefore reuse the same workflow architecture with limited changes to personas, knowledge, routes, and the high-level workflow prompt.

## Limitations

The workflow still depends on LLM consistency. Even with evaluation criteria, a model can occasionally produce formatting variations, incomplete artifacts, or an action plan whose steps are phrased differently than expected. Routing is based on semantic similarity between a step and route descriptions, so ambiguous steps may be routed to the wrong specialist. The current Evaluation Agent also relies on an LLM to judge another LLM, which can introduce evaluator variability despite using temperature 0.

The current workflow executes routed steps sequentially. That is appropriate because features benefit from previously generated user stories and engineering tasks benefit from both stories and features, but independent tasks within a stage could be parallelized in a larger production system. The project also uses in-memory workflow context rather than a persistent workflow-state store, so interrupted runs do not automatically resume from the last successful step.

## One Concrete Improvement

A strong next improvement would be to introduce explicit structured state and schema validation. Each specialist could return machine-readable JSON that is validated with a schema before being accepted. The workflow state could then store validated `user_stories`, `features`, and `engineering_tasks` as typed objects rather than free-form strings. This would make routing, evaluation, downstream reuse, persistence, and automated testing more deterministic while preserving the agentic planning and refinement behavior demonstrated in this project.
