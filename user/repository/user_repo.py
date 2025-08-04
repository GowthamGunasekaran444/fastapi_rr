# app/user/repository/user_repo.py

from typing import Optional
from sqlalchemy.orm import Session
from user.model.user_model import User, UserCreate, UserORM

class UserRepository:
    """
    Repository class for User operations.
    Interacts directly with the SQLAlchemy database session.
    """

    def get_user_by_id(self, db: Session, user_id: str) -> Optional[UserORM]:
        """
        Fetches a user record by user_id from the database.
        """
        return db.query(UserORM).filter(UserORM.user_id == user_id).first()

    def create_user(self, db: Session, user: UserCreate) -> UserORM:
        """
        Inserts a new user record into the database.
        """
        db_user = UserORM(
            user_id=user.user_id,
            username=user.username,
            email=user.email,
            created_time=user.created_time,
            is_active=1 # Default to active
        )
        db.add(db_user)
        db.commit() # Commit the transaction
        db.refresh(db_user) # Refresh the instance to load any new data from the database
        return db_user

