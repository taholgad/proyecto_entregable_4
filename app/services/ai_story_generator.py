"""
Servicio de IA para generar historias de usuario
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


def generate_user_story(prompt: str) -> dict:
    """
    Generar una historia de usuario a partir de un prompt
    Retorna un diccionario con los campos de la historia
    """
    try:
        client = get_ai_client()

        system_prompt = """Eres un experto en desarrollo de software y gestión de proyectos.
Tu tarea es convertir descripciones de usuario en historias de usuario estructuradas siguiendo el formato Agile.

Responde SOLO con un JSON válido (sin markdown, sin comillas escapadas) con la siguiente estructura:
{
    "project": "nombre del proyecto",
    "role": "el rol del usuario (ej: usuario, admin, cliente)",
    "goal": "lo que el usuario quiere lograr",
    "reason": "por qué lo quiere lograr",
    "description": "descripción detallada de la funcionalidad",
    "priority": "low|medium|high|critical",
    "story_points": número entre 1 y 8,
    "effort_hours": horas estimadas
}

Prioridades:
- low: tareas simples, 1-2 puntos, 1-4 horas
- medium: tareas normales, 3-5 puntos, 5-20 horas
- high: tareas complejas, 5-8 puntos, 20-40 horas
- critical: tareas críticas, 8 puntos, 40+ horas
"""

        message_content = f"""Genera una historia de usuario basada en: {prompt}

Responde SOLO con un JSON válido, sin explicaciones adicionales."""

        response = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4"),
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message_content},
            ],
            temperature=0.7,
            max_tokens=500,
        )

        response_text = response.choices[0].message.content.strip()

        # Limpiar respuesta de posibles markdown
        if response_text.startswith("```"):
            response_text = re.sub(r"```json\n?", "", response_text)
            response_text = re.sub(r"```\n?", "", response_text)
            response_text = response_text.strip()

        # Parsear JSON
        user_story_data = json.loads(response_text)

        logger.info(f"Generated user story: {user_story_data.get('goal')}")
        return user_story_data

    except json.JSONDecodeError as exc:
        logger.error(f"Error parsing AI response as JSON: {exc}")
        raise ValueError("Error parsing AI response") from exc
    except Exception as exc:
        logger.error(f"Error generating user story: {exc}")
        raise ValueError(f"Error generating user story: {str(exc)}") from exc
