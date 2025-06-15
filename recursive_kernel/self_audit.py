import openai


def audit_kernel(kernel_code: str) -> str:
    """Review kernel code and return feedback via GPT-4o."""
    prompt = f"""
    Review the following kernel architecture and suggest:
    - Redundancy
    - Bottlenecks
    - Ethical risk
    - Optimizations

    Code:
    {kernel_code[:5000]}...
    """
    response = openai.ChatCompletion.create(
        model='gpt-4o',
        messages=[{'role': 'user', 'content': prompt}],
        temperature=0
)
    return response.choices[0].message['content']
