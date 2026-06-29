def build_prompt(task) -> str:
    return f"""
Genera una descripción clara para esta tarea.

Título:
{task.title}

Prioridad:
{task.priority}

Devuelve SOLO la descripción.
"""
