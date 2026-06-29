import pytest

from app.controllers.task_manager import TaskManager


@pytest.fixture
def manager(db_session):
    return TaskManager(db_session)


@pytest.fixture
def task_data():
    return {
        "title": "Test Task",
        "description": "A test task",
        "priority": "low",
        "effort_hours": 2.5,
        "status": "pending",
        "assigned_to": "john",
    }


class TestTaskManager:
    def test_create_task(self, manager, task_data):
        task = manager.create_task(task_data)
        assert task.id is not None
        assert task.title == "Test Task"

    def test_get_task_by_id(self, manager, task_data):
        created_task = manager.create_task(task_data)
        retrieved_task = manager.get_task_by_id(created_task.id)
        assert retrieved_task is not None
        assert retrieved_task.id == created_task.id

    def test_get_nonexistent_task_returns_none(self, manager):
        assert manager.get_task_by_id(9999) is None

    def test_update_task(self, manager, task_data):
        created_task = manager.create_task(task_data)
        updated_task = manager.update_task(created_task.id, {"status": "in_progress"})
        assert updated_task.status == "in_progress"

    def test_update_nonexistent_task_raises_error(self, manager):
        with pytest.raises(ValueError, match="not found"):
            manager.update_task(9999, {"status": "done"})

    def test_delete_task(self, manager, task_data):
        created_task = manager.create_task(task_data)
        manager.delete_task(created_task.id)
        assert manager.get_task_by_id(created_task.id) is None

    def test_delete_nonexistent_task_raises_error(self, manager):
        with pytest.raises(ValueError, match="not found"):
            manager.delete_task(9999)
