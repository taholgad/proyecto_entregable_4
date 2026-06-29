def build_prompt(task) -> str:
    return f"""
Estima horas de trabajo.

Título:
{task.title}

Descripción:
{task.description}

Categoría:
{task.category}

Devuelve SOLO un número.
"""
