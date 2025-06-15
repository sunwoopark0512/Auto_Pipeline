import openai, random, os

MODELS = {
    "gpt-3.5-turbo": {"rpm": 3500, "cost": 0.001, "latency": 0.6},
    "gpt-4o": {"rpm": 500, "cost": 0.01, "latency": 1.2},
}

budget_cents = float(os.getenv("LLM_BUDGET_CENTS", "50"))
spent = 0


def choose_model(prompt_len):
    global spent
    if spent > budget_cents:
        return "gpt-3.5-turbo"
    # latency budget
    if prompt_len > 800:
        return "gpt-3.5-turbo"
    return "gpt-4o" if random.random() < 0.3 else "gpt-3.5-turbo"


def routed_completion(prompt):
    model = choose_model(len(prompt))
    resp = openai.ChatCompletion.create(
        model=model, messages=[{"role": "user", "content": prompt}]
    )
    spent += MODELS[model]["cost"] * len(prompt) / 1000
    return resp.choices[0].message.content
