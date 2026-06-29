"""
Rutas para gestión de tareas
"""
from __future__ import annotations

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.controllers.task_manager import TaskManager
from app.controllers.user_story_controller import UserStoryController
from app.schemas.task_schema import TaskCreateSchema, TaskResponseSchema
from app.database.connection import get_db
from app.services.ai_task_generator import generate_tasks_for_story

router = APIRouter(prefix="/api/tasks", tags=["tasks"])


@router.get("/", response_model=list[TaskResponseSchema])
def list_tasks(db: Session = Depends(get_db)) -> list[TaskResponseSchema]:
    """Obtener todas las tareas"""
    manager = TaskManager(db)
    return [TaskResponseSchema.model_validate(task.to_dict()) for task in manager.get_all_tasks()]


@router.get("/{task_id}", response_model=TaskResponseSchema)
def get_task(task_id: int, db: Session = Depends(get_db)) -> TaskResponseSchema:
    """Obtener una tarea por ID"""
    manager = TaskManager(db)
    task = manager.get_task_by_id(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return TaskResponseSchema.model_validate(task.to_dict())


@router.post("/", response_model=TaskResponseSchema, status_code=201)
def create_task(task_data: TaskCreateSchema, db: Session = Depends(get_db)) -> TaskResponseSchema:
    """Crear una nueva tarea"""
    manager = TaskManager(db)
    try:
        task = manager.create_task(task_data.model_dump())
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    return TaskResponseSchema.model_validate(task.to_dict())


@router.put("/{task_id}", response_model=TaskResponseSchema)
def update_task(
    task_id: int, task_data: TaskCreateSchema, db: Session = Depends(get_db)
) -> TaskResponseSchema:
    """Actualizar una tarea"""
    manager = TaskManager(db)
    try:
        task = manager.update_task(task_id, task_data.model_dump())
    except ValueError as exc:
        raise HTTPException(
            status_code=404 if "not found" in str(exc) else 400, detail=str(exc)
        )
    return TaskResponseSchema.model_validate(task.to_dict())


@router.delete("/{task_id}", response_model=dict)
def delete_task(task_id: int, db: Session = Depends(get_db)) -> dict:
    """Eliminar una tarea"""
    manager = TaskManager(db)
    try:
        manager.delete_task(task_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    return {"detail": "Task deleted"}


@router.post("/user-stories/{story_id}/generate-tasks", response_model=list[TaskResponseSchema], status_code=201)
def generate_tasks_endpoint(
    story_id: int, db: Session = Depends(get_db)
) -> list[TaskResponseSchema]:
    """Generar tareas automáticamente para una historia de usuario"""
    # Verificar que la historia existe
    story_controller = UserStoryController(db)
    story = story_controller.get_user_story_by_id(story_id)
    if story is None:
        raise HTTPException(status_code=404, detail="User story not found")

    try:
        # Generar tareas con IA
        story_description = f"{story.goal}. {story.description or ''}"
        tasks_data = generate_tasks_for_story(story_description, story_id)

        # Guardar tareas en BD
        manager = TaskManager(db)
        created_tasks = []
        for task_data in tasks_data:
            task = manager.create_task(task_data)
            created_tasks.append(task)

        return [TaskResponseSchema.model_validate(task.to_dict()) for task in created_tasks]
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
