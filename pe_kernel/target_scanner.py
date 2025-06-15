import openai

def scan_targets(niche: str, min_mrr: int = 10000, growth: float = 0.1):
    """Use OpenAI to find SaaS targets in a given niche."""
    prompt = f"""
    Find active SaaS companies in {niche} with MRR > ${min_mrr}, 
    growth > {growth*100}% suitable for acquisition.
    """
    client = openai.OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o", messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
