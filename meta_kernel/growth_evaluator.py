"""Evaluate growth metrics and recommend next SaaS direction."""
# pylint: disable=no-member

import openai


def evaluate_performance(portfolio: str) -> str:
    """Analyze SaaS portfolio metrics and suggest next sector."""
    prompt = (
        f"""
        Analyze current SaaS portfolio revenue, churn, growth.
        Existing portfolio info: {portfolio}
        Recommend next SaaS target sector to launch.
        """
    )
    response = openai.ChatCompletion.create(  # type: ignore[attr-defined]
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content
