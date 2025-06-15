import openai


def design_legal(country: str) -> str:
    prompt = f"""
    Suggest ideal legal entity type, VAT %, SaaS data compliance law for {country}.
    """
    response = openai.ChatCompletion.create(model="gpt-4o", messages=[{"role": "user", "content": prompt}])
    return response.choices[0].message.content
