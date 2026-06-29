"""
Controlador para gestionar historias de usuario en MySQL con SQLAlchemy
"""
from __future__ import annotations

from typing import Any
from sqlalchemy.orm import Session
from app.models.user_story import UserStory
from app.logger import logger


class UserStoryController:
    """Gestor de historias de usuario con persistencia en MySQL"""

    def __init__(self, db: Session) -> None:
        self.db = db

    def create_user_story(self, user_story_data: dict[str, Any]) -> UserStory:
        """Crear una nueva historia de usuario"""
        try:
            user_story = UserStory.from_dict(user_story_data)
            self.db.add(user_story)
            self.db.commit()
            self.db.refresh(user_story)
            logger.info(f"Created user story with id {user_story.id}: {user_story.goal}")
            return user_story
        except Exception as exc:
            self.db.rollback()
            logger.error(f"Error creating user story: {exc}")
            raise

    def get_user_story_by_id(self, user_story_id: int) -> UserStory | None:
        """Obtener historia de usuario por ID"""
        user_story = self.db.query(UserStory).filter(UserStory.id == user_story_id).first()
        if user_story:
            logger.info(f"Retrieved user story with id {user_story_id}")
        else:
            logger.warning(f"User story with id {user_story_id} not found")
        return user_story

    def get_all_user_stories(self) -> list[UserStory]:
        """Obtener todas las historias de usuario"""
        user_stories = self.db.query(UserStory).all()
        logger.info(f"Retrieved {len(user_stories)} user stories")
        return user_stories

    def get_user_stories_by_project(self, project: str) -> list[UserStory]:
        """Obtener historias de un proyecto"""
        user_stories = self.db.query(UserStory).filter(UserStory.project == project).all()
        logger.info(f"Retrieved {len(user_stories)} user stories for project {project}")
        return user_stories

    def update_user_story(self, user_story_id: int, user_story_data: dict[str, Any]) -> UserStory:
        """Actualizar una historia de usuario"""
        try:
            user_story = self.db.query(UserStory).filter(UserStory.id == user_story_id).first()
            if not user_story:
                logger.error(f"User story with id {user_story_id} not found")
                raise ValueError(f"User story with id {user_story_id} not found")

            # Actualizar campos
            for key, value in user_story_data.items():
                if hasattr(user_story, key) and key not in ["id", "created_at"]:
                    setattr(user_story, key, value)

            self.db.commit()
            self.db.refresh(user_story)
            logger.info(f"Updated user story with id {user_story_id}")
            return user_story
        except Exception as exc:
            self.db.rollback()
            logger.error(f"Error updating user story: {exc}")
            raise

    def delete_user_story(self, user_story_id: int) -> None:
        """Eliminar una historia de usuario"""
        try:
            user_story = self.db.query(UserStory).filter(UserStory.id == user_story_id).first()
            if not user_story:
                logger.error(f"User story with id {user_story_id} not found")
                raise ValueError(f"User story with id {user_story_id} not found")

            self.db.delete(user_story)
            self.db.commit()
            logger.info(f"Deleted user story with id {user_story_id}")
        except Exception as exc:
            self.db.rollback()
            logger.error(f"Error deleting user story: {exc}")
            raise
