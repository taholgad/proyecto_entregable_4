"""
Controlador para gestionar tareas en MySQL con SQLAlchemy
"""
from __future__ import annotations

from typing import Any
from sqlalchemy.orm import Session
from app.models.task import Task
from app.logger import logger


class TaskManager:
    """Gestor de tareas con persistencia en MySQL"""

    def __init__(self, db: Session) -> None:
        self.db = db

    def create_task(self, task_data: dict[str, Any]) -> Task:
        """Crear una nueva tarea"""
        try:
            task = Task.from_dict(task_data)
            self.db.add(task)
            self.db.commit()
            self.db.refresh(task)
            logger.info(f"Created task with id {task.id}: {task.title}")
            return task
        except Exception as exc:
            self.db.rollback()
            logger.error(f"Error creating task: {exc}")
            raise

    def get_task_by_id(self, task_id: int) -> Task | None:
        """Obtener tarea por ID"""
        task = self.db.query(Task).filter(Task.id == task_id).first()
        if task:
            logger.info(f"Retrieved task with id {task_id}")
        else:
            logger.warning(f"Task with id {task_id} not found")
        return task

    def get_all_tasks(self) -> list[Task]:
        """Obtener todas las tareas"""
        tasks = self.db.query(Task).all()
        logger.info(f"Retrieved {len(tasks)} tasks")
        return tasks

    def get_tasks_by_user_story(self, user_story_id: int) -> list[Task]:
        """Obtener tareas de una historia"""
        tasks = self.db.query(Task).filter(Task.user_story_id == user_story_id).all()
        logger.info(f"Retrieved {len(tasks)} tasks for user story {user_story_id}")
        return tasks

    def update_task(self, task_id: int, task_data: dict[str, Any]) -> Task:
        """Actualizar una tarea"""
        try:
            task = self.db.query(Task).filter(Task.id == task_id).first()
            if not task:
                logger.error(f"Task with id {task_id} not found")
                raise ValueError(f"Task with id {task_id} not found")

            # Actualizar campos
            for key, value in task_data.items():
                if hasattr(task, key) and key not in ["id", "created_at"]:
                    setattr(task, key, value)

            self.db.commit()
            self.db.refresh(task)
            logger.info(f"Updated task with id {task_id}")
            return task
        except Exception as exc:
            self.db.rollback()
            logger.error(f"Error updating task: {exc}")
            raise

    def delete_task(self, task_id: int) -> None:
        """Eliminar una tarea"""
        try:
            task = self.db.query(Task).filter(Task.id == task_id).first()
            if not task:
                logger.error(f"Task with id {task_id} not found")
                raise ValueError(f"Task with id {task_id} not found")

            self.db.delete(task)
            self.db.commit()
            logger.info(f"Deleted task with id {task_id}")
        except Exception as exc:
            self.db.rollback()
            logger.error(f"Error deleting task: {exc}")
            raise
