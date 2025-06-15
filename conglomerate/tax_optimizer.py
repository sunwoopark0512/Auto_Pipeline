import openai


def optimal_holding_structure(markets):
    prompt = f"""
    Given markets: {markets}, suggest optimal HQ location for SaaS tax minimization.
    Consider withholding tax, profit repatriation, VAT rules.
    """
    response = openai.ChatCompletion.create(model="gpt-4o", messages=[{"role": "user", "content": prompt}])
    return response.choices[0].message.content
