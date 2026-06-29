def build_task_payload(**overrides):
    payload = {
        "title": "Test Task",
        "description": "A test task",
        "priority": "low",
        "effort_hours": 2.5,
        "status": "pending",
        "assigned_to": "john",
        "user_story_id": None,
    }
    payload.update(overrides)
    return payload


def build_story_payload(**overrides):
    payload = {
        "project": "E-commerce",
        "role": "cliente",
        "goal": "comprar online",
        "reason": "ahorrar tiempo",
        "description": "Flujo de compra web",
        "priority": "high",
        "story_points": 5,
        "effort_hours": 8,
    }
    payload.update(overrides)
    return payload


class TestTaskRoutes:
    def test_api_openapi_endpoint(self, client):
        response = client.get("/openapi.json")
        assert response.status_code == 200
        assert "openapi" in response.json()

    def test_list_tasks_empty(self, client):
        response = client.get("/api/tasks/")
        assert response.status_code == 200
        assert response.json() == []

    def test_create_task(self, client):
        response = client.post("/api/tasks/", json=build_task_payload())
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Test Task"
        assert data["id"] is not None

    def test_get_task(self, client):
        created = client.post("/api/tasks/", json=build_task_payload()).json()
        response = client.get(f"/api/tasks/{created['id']}")
        assert response.status_code == 200
        assert response.json()["id"] == created["id"]

    def test_get_nonexistent_task(self, client):
        response = client.get("/api/tasks/9999")
        assert response.status_code == 404

    def test_update_task(self, client):
        created = client.post("/api/tasks/", json=build_task_payload()).json()
        response = client.put(
            f"/api/tasks/{created['id']}",
            json=build_task_payload(status="in_progress"),
        )
        assert response.status_code == 200
        assert response.json()["status"] == "in_progress"

    def test_delete_task(self, client):
        created = client.post("/api/tasks/", json=build_task_payload()).json()
        response = client.delete(f"/api/tasks/{created['id']}")
        assert response.status_code == 200

        get_response = client.get(f"/api/tasks/{created['id']}")
        assert get_response.status_code == 404

    def test_generate_tasks_for_story(self, client, monkeypatch):
        story_response = client.post("/api/user-stories/", json=build_story_payload())
        assert story_response.status_code == 201
        story_id = story_response.json()["id"]

        def fake_generate_tasks_for_story(story_description: str, current_story_id: int):
            assert str(current_story_id) == str(story_id)
            assert story_description
            return [
                {
                    "title": "Diseñar endpoint",
                    "description": "Crear endpoint de checkout",
                    "priority": "high",
                    "effort_hours": 3,
                    "status": "pending",
                    "assigned_to": "dev1",
                    "user_story_id": current_story_id,
                }
            ]

        monkeypatch.setattr(
            "app.routes.task_routes.generate_tasks_for_story",
            fake_generate_tasks_for_story,
        )

        response = client.post(f"/api/tasks/user-stories/{story_id}/generate-tasks")

        assert response.status_code == 201
        tasks = response.json()
        assert len(tasks) == 1
        assert tasks[0]["title"] == "Diseñar endpoint"
        assert tasks[0]["user_story_id"] == story_id
