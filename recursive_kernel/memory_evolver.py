import openai


def evolve_from_memory(mem_log: str) -> str:
    """Suggest strategy evolution from past memory logs using GPT-4o."""
    prompt = f"""
    Review my past 100 deployments and failures:
    {mem_log}
    Suggest evolution in strategy, architecture, and learning goals.
    """
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    return response.choices[0].message["content"]
