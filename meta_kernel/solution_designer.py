"""Design SaaS solution architecture for discovered problems."""
# pylint: disable=no-member

import openai


def design_solution(problem_statement: str) -> str:
    """Propose a SaaS solution for the given problem."""
    prompt = (
        f"""
        Given problem: "{problem_statement}", propose SaaS solution architecture.
        Include modules, data flows, key AI components.
        """
    )
    response = openai.ChatCompletion.create(  # type: ignore[attr-defined]
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content
