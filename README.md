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

## Flexible Architecture: Choosing a Reasoning Mode

The `Ollama Reasoning` project is designed with flexibility in mind, allowing users to select between two levels of complexity and performance: the **Standard Mode** and the **Full Reasoning Mode** architecture. This enables optimization of resource utilization based on the complexity of the task and the required level of reliability.

### 1. Standard Mode: `Planner` + `Worker`

This mode activates the basic agent pair, which already significantly enhances the LLM's capabilities for structured reasoning and transparency.

*   **How It Works:**
    *   **Planner:** Receives the user's task and generates a step-by-step `Deliberation Plan`.
    *   **Worker:** Receives this plan and proceeds to execute it. It maintains a detailed internal monologue, following the plan step by step, and formulates the final answer.
*   **Advantages:**
    *   **Efficiency:** Significantly faster and more economical compared to the full architecture, as it requires fewer iterations and LLM calls.
    *   **Transparency:** Provides a detailed `/think` block, allowing the user to trace the model's thought process.
    *   **Sufficiency for Many Tasks:** Effectively handles most standard queries, including explanations, recommendations, simple calculations, and multi-step logical problems with predictable solutions.
    *   **Reliable Formatting:** Ensures clean, structured output.
*   **Ideal for:**
    *   General question-answering.
    *   Tasks where the solution follows a relatively linear path.
    *   Applications requiring quick responses and resource efficiency.

### 2. Full Reasoning Mode: `Planner-Reasoner` + `Worker-Supervisor`

This mode activates all four specialized agents and their adversarial interactions, designed to tackle the most complex and critical problems where a high degree of self-correction and error resilience is required.

*   **How It Works:**
    1.  The **Planner** generates an initial plan.
    2.  The **Reasoner/Reflector** (the Planner's critic) actively analyzes the proposed plan for logical consistency, completeness, potential dead ends, loops, and optimality *before its execution*. If the plan is deemed suboptimal or contains flaws, the Reasoner/Reflector prompts the Planner to revise it.
    3.  The **Worker** attempts to execute *each step* of the approved plan.
    4.  The **Supervisor** (the Worker's critic) immediately and actively verifies the result of the current step's execution for correctness, logical consistency with the task's current state, and adherence to the step's objective.
    5.  If the Supervisor detects an error, looping behavior, or an inability to progress, it "challenges" the Reasoner/Reflector, initiating a reassessment of the strategy and the generation of a new plan.
    6.  This closed-loop feedback mechanism continues until an optimal and correct solution is achieved.
*   **Advantages:**
    *   **Maximum Reliability:** Significantly enhances the accuracy and correctness of solutions for complex problems, minimizing logical errors and "hallucinations."
    *   **Active Self-Correction:** The system can detect and correct its own errors at various levels, not just at the final output stage.
    *   **Ability to Solve Difficult Problems:** Effectively overcomes challenges related to multi-step planning, state tracking, dead ends, and loops (e.g., the classic "water jug problem").
    *   **Resilience for "Non-Reasoning" LLMs:** Allows less powerful or compact base LLMs to approach the performance of specialized "reasoning" models.
*   **Disadvantages:**
    *   **Higher Computational Cost:** Involves significantly more LLM calls, leading to increased token usage and longer response times.
    *   **Increased Latency:** Due to numerous iterations of review and reflection.
*   **Ideal for:**
    *   Complex, multi-step logical problems and puzzles.
    *   Tasks requiring precise state tracking.
    *   Applications where absolute solution accuracy is critical, and the tolerance for error is very low.
    *   Use with less powerful or compact base LLMs that frequently err without such a structured approach.