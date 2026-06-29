import pytest

from app.models.task import Task, VALID_PRIORITIES, VALID_STATUSES


class TestTask:
    def test_task_creation(self):
        task = Task(
            title="Test Task",
            description="A test task",
            priority="low",
            effort_hours=2.5,
            status="pending",
            assigned_to="john",
        )
        assert task.title == "Test Task"
        assert task.effort_hours == 2.5

    def test_task_to_dict(self):
        task = Task(
            title="Test Task",
            description="A test task",
            priority="low",
            effort_hours=2.5,
            status="pending",
            assigned_to="john",
        )
        task_dict = task.to_dict()
        assert task_dict["id"] is None
        assert task_dict["title"] == "Test Task"
        assert task_dict["priority"] == "low"

    def test_task_from_dict(self):
        data = {
            "title": "Test Task",
            "description": "A test task",
            "priority": "low",
            "effort_hours": 2.5,
            "status": "pending",
            "assigned_to": "john",
        }
        task = Task.from_dict(data)
        assert task.title == "Test Task"
        assert task.effort_hours == 2.5

    def test_task_with_ai_fields(self):
        task = Task(
            title="Test Task",
            description="A test task",
            priority="low",
            effort_hours=2.5,
            status="pending",
            assigned_to="john",
            category="Backend",
            risk_analysis="Riesgo de rendimiento",
            risk_mitigation="Agregar cache",
        )

        payload = task.to_dict()

        assert payload["category"] == "Backend"
        assert payload["risk_analysis"] == "Riesgo de rendimiento"
        assert payload["risk_mitigation"] == "Agregar cache"

        loaded = Task.from_dict(payload)
        assert loaded.category == "Backend"
        assert loaded.risk_analysis == "Riesgo de rendimiento"
        assert loaded.risk_mitigation == "Agregar cache"

    def test_invalid_status_raises_error(self):
        with pytest.raises(ValueError, match="status must be one of"):
            Task(
                title="Test",
                description="Test",
                priority="low",
                effort_hours=1.0,
                status="invalid_status",
                assigned_to="john",
            )

    def test_invalid_priority_raises_error(self):
        with pytest.raises(ValueError, match="priority must be one of"):
            Task(
                title="Test",
                description="Test",
                priority="invalid_priority",
                effort_hours=1.0,
                status="pending",
                assigned_to="john",
            )

    def test_negative_effort_hours_raises_error(self):
        with pytest.raises(ValueError, match="effort_hours must be a non-negative number"):
            Task(
                title="Test",
                description="Test",
                priority="low",
                effort_hours=-1.0,
                status="pending",
                assigned_to="john",
            )

    def test_valid_statuses(self):
        for status in VALID_STATUSES:
            task = Task(
                title="Test",
                description="Test",
                priority="low",
                effort_hours=1.0,
                status=status,
                assigned_to="john",
            )
            assert task.status == status

    def test_valid_priorities(self):
        for priority in VALID_PRIORITIES:
            task = Task(
                title="Test",
                description="Test",
                priority=priority,
                effort_hours=1.0,
                status="pending",
                assigned_to="john",
            )
            assert task.priority == priority
