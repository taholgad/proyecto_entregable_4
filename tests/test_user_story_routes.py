def build_story_payload(**overrides):
    payload = {
        "project": "Portal Clientes",
        "role": "usuario",
        "goal": "consultar pedidos",
        "reason": "mejorar visibilidad",
        "description": "Listado con filtros",
        "priority": "medium",
        "story_points": 3,
        "effort_hours": 5,
    }
    payload.update(overrides)
    return payload


class TestUserStoryRoutes:
    def test_list_user_stories_empty(self, client):
        response = client.get("/api/user-stories/")
        assert response.status_code == 200
        assert response.json() == []

    def test_create_user_story(self, client):
        response = client.post("/api/user-stories/", json=build_story_payload())
        assert response.status_code == 201
        data = response.json()
        assert data["id"] is not None
        assert data["goal"] == "consultar pedidos"

    def test_get_user_story(self, client):
        created = client.post("/api/user-stories/", json=build_story_payload()).json()
        response = client.get(f"/api/user-stories/{created['id']}")
        assert response.status_code == 200
        assert response.json()["id"] == created["id"]

    def test_update_user_story(self, client):
        created = client.post("/api/user-stories/", json=build_story_payload()).json()
        response = client.put(
            f"/api/user-stories/{created['id']}",
            json=build_story_payload(priority="high"),
        )
        assert response.status_code == 200
        assert response.json()["priority"] == "high"

    def test_delete_user_story(self, client):
        created = client.post("/api/user-stories/", json=build_story_payload()).json()
        response = client.delete(f"/api/user-stories/{created['id']}")
        assert response.status_code == 200

        get_response = client.get(f"/api/user-stories/{created['id']}")
        assert get_response.status_code == 404

    def test_generate_user_story_with_mock(self, client, monkeypatch):
        mocked_story = {
            "project": "Portal Clientes",
            "role": "usuario",
            "goal": "seguir envios",
            "reason": "reducir consultas al soporte",
            "description": "Pantalla de tracking con timeline",
            "priority": "high",
            "story_points": 5,
            "effort_hours": 8,
        }

        monkeypatch.setattr(
            "app.routes.user_story_routes.generate_user_story",
            lambda prompt: mocked_story,
        )

        response = client.post(
            "/api/user-stories/generate",
            json={"prompt": "Quiero seguir estado de envios"},
        )

        assert response.status_code == 201
        data = response.json()
        assert data["goal"] == "seguir envios"
        assert data["priority"] == "high"
