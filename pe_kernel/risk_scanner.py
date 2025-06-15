import openai

def scan_risks(domain: str, tech_stack: str, customer_base: str):
    """Analyze potential risks for a SaaS company."""
    prompt = f"""
    Analyze legal, technical, data privacy risks for SaaS company with:
    domain={domain}, stack={tech_stack}, customers={customer_base}
    """
    client = openai.OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o", messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
