from fastapi.testclient import TestClient

import api.ai_tasks as ai_tasks_module
from app.main import app

client = TestClient(app)


base_payload = {
    "id": 1,
    "title": "Crear login JWT",
    "description": "",
    "priority": "high",
    "effort_hours": 0.0,
    "status": "pending",
    "assigned_to": "juan",
}


def test_describe_task(monkeypatch):
    def fake_ask_llm(prompt: str) -> str:
        assert "Crear login JWT" in prompt
        return "Implementar autenticación JWT con renovación de token."

    monkeypatch.setattr(ai_tasks_module, "ask_llm", fake_ask_llm)

    response = client.post("/ai/tasks/describe", json=base_payload)

    assert response.status_code == 200
    assert response.json()["description"] == "Implementar autenticación JWT con renovación de token."


def test_categorize_task(monkeypatch):
    def fake_ask_llm(prompt: str) -> str:
        assert "Crear login JWT" in prompt
        return "Backend"

    monkeypatch.setattr(ai_tasks_module, "ask_llm", fake_ask_llm)

    response = client.post("/ai/tasks/categorize", json=base_payload)

    assert response.status_code == 200
    assert response.json()["category"] == "Backend"


def test_estimate_task(monkeypatch):
    def fake_ask_llm(prompt: str) -> str:
        assert "Crear login JWT" in prompt
        return "12"

    monkeypatch.setattr(ai_tasks_module, "ask_llm", fake_ask_llm)

    response = client.post("/ai/tasks/estimate", json=base_payload)

    assert response.status_code == 200
    assert response.json()["effort_hours"] == 12.0


def test_estimate_invalid_response(monkeypatch):
    monkeypatch.setattr(ai_tasks_module, "ask_llm", lambda prompt: "invalid")

    response = client.post("/ai/tasks/estimate", json=base_payload)

    assert response.status_code == 400
    assert response.json()["detail"] == "LLM devolvió valor inválido"


def test_audit_task(monkeypatch):
    calls = []

    def fake_ask_llm(prompt: str) -> str:
        calls.append(prompt)
        if "Analiza riesgos potenciales" in prompt:
            return "Riesgo de exposición de credenciales."
        return "Usar rotación de claves y pruebas de seguridad."

    monkeypatch.setattr(ai_tasks_module, "ask_llm", fake_ask_llm)

    response = client.post("/ai/tasks/audit", json=base_payload)

    assert response.status_code == 200
    assert response.json()["risk_analysis"] == "Riesgo de exposición de credenciales."
    assert response.json()["risk_mitigation"] == "Usar rotación de claves y pruebas de seguridad."
    assert len(calls) == 2
