"""Compose SaaS business models automatically."""
# pylint: disable=no-member

import openai


def design_biz_model(solution: str) -> str:
    """Design monetization strategy for the SaaS solution."""
    prompt = (
        f"""
        Build monetization strategy for SaaS: {solution}.
        Include pricing tiers, freemium structure, potential MRR range.
        """
    )
    response = openai.ChatCompletion.create(  # type: ignore[attr-defined]
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content
