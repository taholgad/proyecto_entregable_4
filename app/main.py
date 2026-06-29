from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request
import logging

from api.ai_tasks import router as ai_router
from app.routes.task_routes import router as task_router
from app.routes.user_story_routes import router as user_story_router
from app.routes.web_routes import router as web_router
from app.database.base import Base
from app.database.connection import engine
from app.models.task import Task
from app.models.user_story import UserStory

app = FastAPI(title="Task Manager API")
logger = logging.getLogger(__name__)

# Configurar Jinja2 para templates
templates = Jinja2Templates(directory="templates")

app.include_router(task_router)
app.include_router(user_story_router)
app.include_router(ai_router)
app.include_router(web_router)


@app.on_event("startup")
def init_database() -> None:
    try:
        Base.metadata.create_all(bind=engine)
    except Exception as exc:
        logger.warning("No se pudo inicializar la base de datos en startup: %s", exc)


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Task Manager API is running"}
