"""
Servicio de IA para generar tareas a partir de historias de usuario
"""
from __future__ import annotations

import json
import os
import re
from openai import AzureOpenAI
from dotenv import load_dotenv
from app.logger import logger

load_dotenv()


def get_ai_client() -> AzureOpenAI:
    """Obtener cliente de Azure OpenAI"""
    return AzureOpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        api_version=os.getenv("OPENAI_API_VERSION"),
        azure_endpoint=os.getenv("OPENAI_BASE_URL"),
    )


def generate_tasks_for_story(user_story_description: str, story_id: int) -> list[dict]:
    """
    Generar tareas a partir de una historia de usuario
    Retorna una lista de diccionarios con los campos de cada tarea
    """
    try:
        client = get_ai_client()

        system_prompt = """Eres un experto en gestión de proyectos y desarrollo de software.
Tu tarea es descomponer historias de usuario en tareas concretas y realizables.

Responde ONLY con un JSON array válido (sin markdown) con estructura:
[
    {
        "title": "nombre de la tarea",
        "description": "descripción detallada",
        "priority": "low|medium|high|blocking",
        "effort_hours": horas estimadas (número),
        "status": "pending",
        "assigned_to": "sin asignar",
        "category": "categoría",
        "risk_analysis": "posibles riesgos",
        "risk_mitigation": "cómo mitigarlos"
    }
]

Directrices:
- Genera 3-5 tareas por historia
- Desglosa en tareas pequeñas y manejables (máximo 16 horas)
- La suma de effort_hours debe ser coherente con la historia
- Usa prioridades coherentes
"""

        message_content = f"""Desglosa esta historia de usuario en tareas concretas:
{user_story_description}

Responde SOLO con un JSON array válido, sin explicaciones."""

        response = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4"),
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message_content},
            ],
            temperature=0.7,
            max_tokens=1500,
        )

        response_text = response.choices[0].message.content.strip()

        # Limpiar respuesta de posibles markdown
        if response_text.startswith("```"):
            response_text = re.sub(r"```json\n?", "", response_text)
            response_text = re.sub(r"```\n?", "", response_text)
            response_text = response_text.strip()

        # Parsear JSON array
        tasks_data = json.loads(response_text)

        # Agregar user_story_id a cada tarea
        for task in tasks_data:
            task["user_story_id"] = story_id

        logger.info(f"Generated {len(tasks_data)} tasks for story {story_id}")
        return tasks_data

    except json.JSONDecodeError as exc:
        logger.error(f"Error parsing AI response as JSON: {exc}")
        raise ValueError("Error parsing AI response") from exc
    except Exception as exc:
        logger.error(f"Error generating tasks: {exc}")
        raise ValueError(f"Error generating tasks: {str(exc)}") from exc
