"""Module for automatically discovering SaaS market problems."""
# pylint: disable=no-member

import openai


def mine_problems() -> str:
    """Scan SaaS markets and return discovered problems."""
    prompt = (
        """
        Scan global SaaS markets across B2B/B2C.
        Identify unmet needs, inefficiencies, regulatory shifts, underserved segments.
        Output: sector, problem description.
        """
    )
    response = openai.ChatCompletion.create(  # type: ignore[attr-defined]
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content
