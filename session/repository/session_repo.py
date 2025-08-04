# app/session/repository/session_repo.py

from typing import Optional, List
from datetime import datetime
from sqlalchemy.orm import Session
from session.model.session_model import Session, SessionCreate, SessionORM
from user.model.user_model import UserORM # Import UserORM for user verification

class SessionRepository:
    """
    Repository class for Session operations.
    Interacts directly with the SQLAlchemy database session.
    """

    def get_session_by_id(self, db: Session, session_id: str) -> Optional[SessionORM]:
        """
        Fetches a session record by session_id.
        """
        return db.query(SessionORM).filter(SessionORM.session_id == session_id).first()

    def create_session(self, db: Session, session: SessionCreate) -> SessionORM:
        """
        Inserts a new session record into the database.
        """
        db_session = SessionORM(
            session_id=session.session_id,
            user_id=session.user_id,
            session_name=session.session_name,
            login_time=session.login_time,
            active_status=1 # Default to active
        )
        db.add(db_session)
        db.commit()
        db.refresh(db_session)
        return db_session

    def delete_session(self, db: Session, session_id: str) -> bool:
        """
        Deletes a session record by session_id.
        Returns True if deleted, False otherwise.
        """
        session_to_delete = db.query(SessionORM).filter(SessionORM.session_id == session_id).first()
        if session_to_delete:
            db.delete(session_to_delete)
            db.commit()
            return True
        return False

    def get_sessions_by_user_id(self, db: Session, user_id: str) -> List[SessionORM]:
        """
        Fetches all sessions created by a specific user_id.
        """
        return db.query(SessionORM).filter(SessionORM.user_id == user_id).all()

    def update_session_name(self, db: Session, session_id: str, new_session_name: str) -> Optional[SessionORM]:
        """
        Updates the session name for a given session_id.
        """
        db_session = db.query(SessionORM).filter(SessionORM.session_id == session_id).first()
        if db_session:
            db_session.session_name = new_session_name
            db.commit()
            db.refresh(db_session)
            return db_session
        return None
