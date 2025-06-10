# Ollama Reasoning
## Enhancing the Reasoning Capabilities of Any LLM

### Project Goal:

**To transform "non-reasoning" Large Language Models (LLMs), such as `gemma3:4b` (and other compact LLMs), into systems capable of deep, multi-step logical reasoning, self-correction, and planning, achieving or surpassing the level of specialized "reasoning" models.**

The project aims to provide base LLMs, which may inherently get stuck in logical loops, make incorrect deductions, or be incapable of complex planning, with an architecture that allows them to solve complex problems requiring sequential thinking and state tracking.

### Problem Solved:

Despite impressive text generation capabilities, many compact Large Language Models (LLMs) trained on vast datasets often struggle with:
*   **Multi-step Planning:** Inability to construct and execute a complex sequence of actions to achieve a goal (e.g., the water jug problem, where `gemma3:4b` gets stuck in a loop).
*   **State Tracking:** Loss of context or current state during the execution of a complex task.
*   **Sequential Logical Deduction:** Inability to correctly integrate multiple conditions and make an accurate conclusion (as in spatial puzzles).
*   **Self-Correction:** Inability to detect one's own errors or inefficient reasoning paths and correct them.
*   **Avoiding "Reasoning Hallucinations":** Generation of logically inconsistent or impossible steps.

### Architecture

The project employs a **layered reasoning architecture that combines planning and reflective refinement.** It is built upon **two pairs of competing agents, interacting at the task and meta-levels.**

At the core of this architecture are the interactions of several specialized "intelligent agents," each performing its role. All these agents utilize the same base LLM (e.g., `gemma3:4b`) to perform their functions.

These agents are organized into two primary **adversarial pairs**, operating at different levels of abstraction:

1.  **"Planner-Reasoner" Adversarial Pair (P-R):**
    This is a **composite pair of agents** responsible for **strategic thinking, task decomposition, plan generation, and meta-level reflection.**
    *   **Planner:** **Role:** To generate step-by-step plans for solving the overall task. It decomposes the problem into manageable subtasks and proposes a sequence of actions.
    *   **Reasoner/Reflector:** **Role:** To act as a *critic* of the Planner. It actively analyzes the proposed plan for overall logical consistency, completeness, potential dead ends, loops, and optimality *before its execution*. It also receives feedback (challenges) from the "Worker-Supervisor" Adversarial Pair and, based on this feedback, analyzes the failure, suggests strategy modifications, and initiates the generation of a new or corrected plan by the Planner.
    *   **Internal P-R Competition:** The Planner proposes a strategy/plan. The Reasoner/Reflector *competes* with it, trying to find flaws and prompt the Planner to improve or revise the plan until internal "optimality" or "confidence" in the plan is achieved.

2.  **"Worker-Supervisor" Adversarial Pair (W-S):**
    This is a **composite pair of agents** responsible for **executing specific plan steps and their immediate, critical verification.**
    *   **Worker:** **Role:** To receive a specific plan step from the "Planner-Reasoner" Adversarial Pair and attempt to execute it, using the base LLM to generate the required output or action.
    *   **Supervisor:** **Role:** To act as a *critic* of the Worker. It immediately and actively verifies the result of the current step's execution for its correctness, logical consistency with the task's current state, and adherence to the step's objective. It also identifies signs of looping or inability to progress.
    *   **Internal W-S Competition:** The Worker attempts to execute a step and provide a result. The Supervisor *competes* with it, aiming to identify any errors, inaccuracies, or logical inconsistencies in its execution before the result is considered final.

The primary competition within the system occurs between these two composite agents: the "Planner-Reasoner" Adversarial Pair proposes a plan, while the "Worker-Supervisor" Adversarial Pair attempts to execute it and actively seeks errors and inconsistencies at each step. If the "Worker-Supervisor" detects a problem, it "challenges" the "Planner-Reasoner," initiating a strategy reassessment and the generation of a new plan. This closed-loop feedback mechanism ensures a continuous drive towards an optimal and correct solution.

### What the project achieves:

Thanks to this architecture, `ollama-reasoning` allows base LLMs to:
*   **Decompose Complex Tasks:** Effectively break down problems into manageable stages.
*   **Follow Logic and Track States:** Maintain a consistent understanding of context and current position within a task.
*   **Avoid Looping:** Automatically recognize and exit repetitive, unproductive reasoning cycles.
*   **Self-Correct:** Learn from errors and adapt their strategy for successful problem-solving.
*   **Achieve Results Comparable to or Surpassing Specialized Reasoning LLMs**, by utilizing less powerful or more compact base models.