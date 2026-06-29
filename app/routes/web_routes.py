"""
Rutas HTML para la interfaz de usuario (Jinja2 Templates)
"""
from __future__ import annotations

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.controllers.task_manager import TaskManager
from app.controllers.user_story_controller import UserStoryController
from app.database.connection import SessionLocal

router = APIRouter(tags=["web"])
templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
async def dashboard(request: Request) -> str:
    """Dashboard principal"""
    db = SessionLocal()
    try:
        task_manager = TaskManager(db)
        user_story_controller = UserStoryController(db)

        tasks = task_manager.get_all_tasks()
        stories = user_story_controller.get_all_user_stories()

        total_tasks = len(tasks)
        pending_count = len([t for t in tasks if t.status == "pending"])
        in_progress_count = len([t for t in tasks if t.status == "in_progress"])
        done_count = len([t for t in tasks if t.status == "done"])

        return templates.TemplateResponse(
            "base.html",
            {
                "request": request,
                "total_tasks": total_tasks,
                "stories_count": len(stories),
                "pending_count": pending_count,
                "in_progress_count": in_progress_count,
                "done_count": done_count,
            },
        )
    finally:
        db.close()


@router.get("/user-stories", response_class=HTMLResponse)
async def user_stories_page(request: Request) -> str:
    """Página de historias de usuario"""
    db = SessionLocal()
    try:
        controller = UserStoryController(db)
        stories = controller.get_all_user_stories()

        stories_data = [story.to_dict() for story in stories]

        return templates.TemplateResponse(
            "user_stories.html",
            {"request": request, "stories": stories_data},
        )
    finally:
        db.close()


@router.get("/tasks", response_class=HTMLResponse)
async def tasks_page(request: Request) -> str:
    """Página de tareas"""
    db = SessionLocal()
    try:
        manager = TaskManager(db)
        tasks = manager.get_all_tasks()

        tasks_data = [task.to_dict() for task in tasks]
        total_tasks = len(tasks_data)
        pending_count = len([t for t in tasks_data if t.get("status") == "pending"])
        in_progress_count = len(
            [t for t in tasks_data if t.get("status") == "in_progress"]
        )
        done_count = len([t for t in tasks_data if t.get("status") == "done"])

        return templates.TemplateResponse(
            "tasks.html",
            {
                "request": request,
                "tasks": tasks_data,
                "total_tasks": total_tasks,
                "pending_count": pending_count,
                "in_progress_count": in_progress_count,
                "done_count": done_count,
            },
        )
    finally:
        db.close()
