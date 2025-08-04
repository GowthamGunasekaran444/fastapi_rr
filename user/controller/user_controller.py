# app/user/controller/user_controller.py

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from user.model.user_model import User, UserCreate
from user.repository.user_repo import UserRepository

class UserController:
    """
    Controller class for User operations.
    Handles business logic and interacts with the UserRepository.
    """

    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def create_user(self, db: Session, user_create: UserCreate) -> User:
        """
        Creates a new user.
        Checks if the user already exists by user_id before creation.
        """
        # Check if user exists (by user_id)
        existing_user = self.user_repo.get_user_by_id(db, user_create.user_id)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"User with user_id '{user_create.user_id}' already exists."
            )

        # If not, insert record
        created_user = self.user_repo.create_user(db, user_create)
        return User.from_orm(created_user) # Convert ORM model to Pydantic model

    def get_user(self, db: Session, user_id: str) -> User:
        """
        Fetches and returns a user if exists.
        """
        user = self.user_repo.get_user_by_id(db, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with user_id '{user_id}' not found."
            )
        return User.from_orm(user) # Convert ORM model to Pydantic model

