import ollama

# settings
PLANNER_MODEL = 'gemma3'
REASONER_MODEL = 'gemma3'
WORKER_MODEL = 'gemma3'
SUPERVISOR_MODEL = 'gemma3'

# system prompts
PLANNER_SYSTEM_PROMPT = '''
You are a **planner**, an AI model assistant (Large Language Language Model). Your purpose is to **formulate a deliberation strategy** for solving a problem, and **prepare the necessary knowledge and reasoning approach** for another AI model. You DO NOT solve the problem yourself.

### Model Limitations (of the AI model you assist):
*   It can **only generate text** based on its pre-trained knowledge.

### Your Responsibilities:
1.  Understand the user's request and identify the **problem to be solved**.
2.  Formulate a **precise task description**.
3.  Identify what **knowledge and concepts** the AI model must use to solve the task.
4.  Construct a **deliberation plan**: a high-level outline of **how** the AI model should reason about the problem — not a solution. This plan describes **internal processing stages** or **conceptual steps** for the AI model to arrive at the necessary information or structure for its output.

### You MUST NOT:
*   **Solve the problem yourself.**
*   Provide a step-by-step solution or example of the solution.
*   Give specific actions or steps that would directly solve the task (e.g., "Fill the 5-liter bucket").
*   Simulate how the AI model should execute the plan.
*   Format or structure the AI model’s output for the user (only your own output format).
*   Include any output resembling the final answer or solution.
*   **Use verbs in `Deliberation Plan` steps that imply direct external interaction, data retrieval, or text generation.**
    *   **Forbidden verbs:** "access", "retrieve", "query", "search", "fetch", "extract", "look up", "browse", "explain", "describe", "tell", "state", "present", "summarize", "conclude".
    *   **Instead, use verbs that reflect internal processing or conceptual preparation:** "Identify", "Analyze", "Derive", "Formulate conceptual understanding", "Structure logical flow", "Determine", "Assess", "Synthesize knowledge", "Process conceptual input", "Compile relevant facts", "Evaluate information components".
*   Output any text or tags before or after your `Output Format` section.

### Output Format:
**Task**: [One-sentence statement of the problem.]
**Description**: [Short elaboration of the task goal.]
**Knowledge**:
*   [Bullet points of what the AI model must understand.]
**Deliberation Plan**:
1.  [Abstract reasoning step 1.]
2.  [Abstract reasoning step 2.]
    ...

### Output Style:
-   Clear and concise.
-   No unnecessary elaboration or explanations.
-   No conversational text or greetings.
-   No direct solutions or examples.
'''

REASONER_SYSTEM_PROMPT = '''

'''

WORKER_SYSTEM_PROMPT = '''
You are the **Worker** agent. Your role is to **execute the entire Deliberation Plan** provided by the Planner and determine the final answer to the user's **Task**.
You must apply the provided Knowledge and follow the logical flow of the Deliberation Plan to arrive at the solution.

To ensure correct and reliable execution, you will first generate your **internal reasoning process** (a 'scratchpad' or 'thought process') that explicitly tracks the state of the problem and the logical progression. This internal process will directly follow the Deliberation Plan.
Once you have determined the solution within your internal reasoning process, you will then output the final answer.

### Your Responsibilities:
1.  Understand the **Task**, **Description**, and **Knowledge** provided.
2.  **First, generate your internal reasoning process (scratchpad)**, meticulously following each step of the **Deliberation Plan**. For problems involving state changes (like the water jug problem), explicitly list the state of the system after each operation within your scratchpad. **Crucially, for each step you perform, explicitly state your reasoning, decision-making process, or the purpose behind that particular action.**
3.  **Second, based on your completed internal reasoning process, synthesize the final answer.**

### You MUST NOT:
*   Re-state the task or the overall Deliberation Plan.

### Phase 1: Internal Reasoning Process (Scratchpad)
*   You **MUST** begin your output with the `/think` tag on a new line.
*   **Generate a detailed internal reasoning process.** This is your 'scratchpad' or 'thought process'.
*   **Meticulously follow each step of the provided Deliberation Plan.** For problems involving state changes, you **MUST explicitly list the state of the system** after each operation you derive. **Also, explain *why* you are taking each action or what you expect the outcome of that action to be.**
*   This internal process should logically lead to the discovery of the solution.
*   You **MUST** end this phase with the `/think` tag on a new line.

### Phase 2: Final Answer Formulation
*   Immediately after the closing `/think` tag, **synthesize the final answer based ONLY on your completed internal reasoning process (Phase 1).**
*   This final answer should be the complete solution ready for the user, presented clearly, concisely, and in a well-structured manner. If it's a multi-step solution, describe each step using natural language and appropriate formatting (e.g., numbered lists, bullet points, or distinct paragraphs for each step with clear headings/bolding).

### Input from Planner:
{plan}

### Output Format:
/think
[Your detailed internal step-by-step reasoning here, including your thoughts and decisions for each action.]
/think
[Your final answer]
'''

SUPERVISOR_SYSTEM_PROMPT = '''

'''


if __name__ == '__main__':
    # main
    # prompt = 'Обьясни почему небо голубое для детей'
    # prompt = 'Сколько будет 2 + 2?'

    test_prompts = [
        'Какой дистрибутив linux посоветуешь?'
        # 'Сколько будет 2 + 2?',
        'Обьясни почему небо голубое для детей',
        # 'Пожалуйста, проверь, какая сегодня погода в Москве',
        # 'Найди мне три самые свежие новости о космосе.',
        # 'У тебя есть два ведра: одно вмещает 5 литров, другое — 3 литра. Как получить ровно 4 литра воды, используя только эти ведра и неограниченный источник воды?'
    ]

    for prompt in test_prompts:
        print(f'prompt: {prompt}')
        print('answer:')

        # think
        plan_think = ollama.generate(
            model = PLANNER_MODEL,
            prompt = prompt,
            system=PLANNER_SYSTEM_PROMPT,
            stream=True
        )
        plan = ''

        print('/plan')
        for msg in plan_think:
            plan += msg.response
            print(msg.response, end='', flush=True)
        print('/plan\n')

        # answer
        answer = ollama.generate(
            model = WORKER_MODEL,
            prompt = prompt,
            system=WORKER_SYSTEM_PROMPT.format(plan=plan),
            stream=True
        )

        for msg in answer:
            print(msg.response, end='', flush=True)

        print('\n')
