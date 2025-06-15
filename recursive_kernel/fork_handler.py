import openai


def fork_new_entity(purpose: str) -> str:
    """Design a sub-agent kernel optimized for the given purpose via GPT-4o."""
    prompt = f"""
    Design a sub-agent Kernel optimized for: {purpose}
    Include behavior, resource limits, API scope, training feedback loops.
    """
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    return response.choices[0].message["content"]
