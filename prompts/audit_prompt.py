def risk_prompt(task) -> str:
    return f"""
Analiza riesgos potenciales.

Task:
{task}
"""


def mitigation_prompt(task, risk) -> str:
    return f"""
Basándote en:

Task:
{task}

Riesgos:
{risk}

Genera plan mitigación.
"""
