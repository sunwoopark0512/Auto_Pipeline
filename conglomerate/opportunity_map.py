import openai


def map_opportunities():
    prompt = """
    For 30 global countries, list SaaS sectors with highest growth CAGR for 2024-2028.
    Output as: country, sector, CAGR%
    """
    response = openai.ChatCompletion.create(model="gpt-4o", messages=[{"role": "user", "content": prompt}])
    return response.choices[0].message.content
