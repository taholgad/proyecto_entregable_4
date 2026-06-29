"""
Rutas para gestión de historias de usuario
"""
from __future__ import annotations

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.controllers.user_story_controller import UserStoryController
from app.schemas.task_schema import UserStoryCreateSchema, UserStoryResponseSchema, GeneratePromptSchema
from app.database.connection import get_db
from app.services.ai_story_generator import generate_user_story

router = APIRouter(prefix="/api/user-stories", tags=["user-stories"])


@router.get("/", response_model=list[UserStoryResponseSchema])
def list_user_stories(db: Session = Depends(get_db)) -> list[UserStoryResponseSchema]:
    """Obtener todas las historias de usuario"""
    controller = UserStoryController(db)
    user_stories = controller.get_all_user_stories()
    return [UserStoryResponseSchema.model_validate(us.to_dict()) for us in user_stories]


@router.get("/{user_story_id}", response_model=UserStoryResponseSchema)
def get_user_story(user_story_id: int, db: Session = Depends(get_db)) -> UserStoryResponseSchema:
    """Obtener una historia de usuario por ID"""
    controller = UserStoryController(db)
    user_story = controller.get_user_story_by_id(user_story_id)
    if user_story is None:
        raise HTTPException(status_code=404, detail="User story not found")
    return UserStoryResponseSchema.model_validate(user_story.to_dict())


@router.post("/", response_model=UserStoryResponseSchema, status_code=201)
def create_user_story(
    user_story_data: UserStoryCreateSchema, db: Session = Depends(get_db)
) -> UserStoryResponseSchema:
    """Crear una nueva historia de usuario"""
    controller = UserStoryController(db)
    try:
        user_story = controller.create_user_story(user_story_data.model_dump())
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    return UserStoryResponseSchema.model_validate(user_story.to_dict())


@router.put("/{user_story_id}", response_model=UserStoryResponseSchema)
def update_user_story(
    user_story_id: int, user_story_data: UserStoryCreateSchema, db: Session = Depends(get_db)
) -> UserStoryResponseSchema:
    """Actualizar una historia de usuario"""
    controller = UserStoryController(db)
    try:
        user_story = controller.update_user_story(user_story_id, user_story_data.model_dump())
    except ValueError as exc:
        raise HTTPException(
            status_code=404 if "not found" in str(exc) else 400, detail=str(exc)
        )
    return UserStoryResponseSchema.model_validate(user_story.to_dict())


@router.delete("/{user_story_id}", response_model=dict)
def delete_user_story(user_story_id: int, db: Session = Depends(get_db)) -> dict:
    """Eliminar una historia de usuario"""
    controller = UserStoryController(db)
    try:
        controller.delete_user_story(user_story_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    return {"detail": "User story deleted"}


@router.post("/generate", response_model=UserStoryResponseSchema, status_code=201)
def generate_user_story_endpoint(
    request: GeneratePromptSchema, db: Session = Depends(get_db)
) -> UserStoryResponseSchema:
    """Generar una historia de usuario usando IA a partir de un prompt"""
    try:
        # Generar con IA
        user_story_data = generate_user_story(request.prompt)

        # Guardar en BD
        controller = UserStoryController(db)
        user_story = controller.create_user_story(user_story_data)

        return UserStoryResponseSchema.model_validate(user_story.to_dict())
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
