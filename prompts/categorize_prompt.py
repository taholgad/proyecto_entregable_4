def build_prompt(task) -> str:
    return f"""
Clasifica la tarea.

Categorías válidas:
Frontend
Backend
Testing
Infra
DevOps
Database

Título:
{task.title}

Descripción:
{task.description}

Devuelve SOLO una categoría.
"""
