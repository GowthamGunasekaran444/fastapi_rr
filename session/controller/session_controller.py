# app/session/controller/session_controller.py

from fastapi import HTTPException, status
from typing import List, Dict
from sqlalchemy.orm import Session
from session.model.session_model import Session, SessionCreate, SessionRename
from session.repository.session_repo import SessionRepository
from user.repository.user_repo import UserRepository # To verify user_id existence

class SessionController:
    """
    Controller class for Session operations.
    Handles business logic and interacts with the SessionRepository.
    """

    def __init__(self, session_repo: SessionRepository, user_repo: UserRepository):
        self.session_repo = session_repo
        self.user_repo = user_repo

    def create_session(self, db: Session, session_create: SessionCreate) -> Session:
        """
        Creates a new session.
        Verifies if the user_id exists before creating the session.
        """
        # Verify if user_id exists
        user_exists = self.user_repo.get_user_by_id(db, session_create.user_id)
        if not user_exists:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with user_id '{session_create.user_id}' does not exist. Cannot create session."
            )

        # Check if session_id already exists (optional, but good practice for unique IDs)
        existing_session = self.session_repo.get_session_by_id(db, session_create.session_id)
        if existing_session:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Session with session_id '{session_create.session_id}' already exists."
            )

        # Insert session
        created_session = self.session_repo.create_session(db, session_create)
        return Session.from_orm(created_session)

    def delete_session(self, db: Session, session_id: str) -> Dict[str, str]:
        """
        Deletes a session by ID.
        """
        if not self.session_repo.delete_session(db, session_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Session with session_id '{session_id}' not found."
            )
        return {"message": f"Session '{session_id}' deleted successfully."}

    def get_sessions_by_user(self, db: Session, user_id: str) -> List[Session]:
        """
        Fetches all sessions created by a specific user.
        """
        # Optionally, verify if the user exists first
        user_exists = self.user_repo.get_user_by_id(db, user_id)
        if not user_exists:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with user_id '{user_id}' not found."
            )

        sessions = self.session_repo.get_sessions_by_user_id(db, user_id)
        return [Session.from_orm(s) for s in sessions]

    def rename_session(self, db: Session, session_id: str, new_session_name: str) -> Session:
        """
        Updates the session name for the given ID.
        """
        updated_session = self.session_repo.update_session_name(db, session_id, new_session_name)
        if not updated_session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Session with session_id '{session_id}' not found."
            )
        return Session.from_orm(updated_session)

