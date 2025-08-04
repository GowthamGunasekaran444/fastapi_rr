
from fastapi import APIRouter, Depends, status
from typing import List, Dict
from sqlalchemy.orm import Session # Import Session
from session.model.session_model import Session, SessionCreate, SessionRename
from session.controller.session_controller import SessionController
from session.repository.session_repo import SessionRepository
from user.repository.user_repo import UserRepository # Needed for user verification
from core.db import get_db # Import get_db

# Dependency to get a Session Controller instance
def get_session_controller():
    """Provides a Session Controller instance with its dependencies."""
    session_repo = SessionRepository()
    user_repo = UserRepository() # Inject UserRepo for user_id verification
    return SessionController(session_repo, user_repo)

router = APIRouter(
    prefix="/session",
    tags=["Session APIs"],
    responses={404: {"description": "Not found"}},
)

@router.post("/create", response_model=Session, status_code=status.HTTP_201_CREATED)
async def create_session_api(
    session_data: SessionCreate,
    session_controller: SessionController = Depends(get_session_controller),
    db: Session = Depends(get_db) # Inject database session
):
    """
    **Session API: Create Session**

    Input: `session_id`, `session_name`, `user_id`, `created_time` (maps to login_time)

    Logic:
    - Verify if `user_id` exists.
    - If exists → insert session.
    - Else → return error (404 if user not found, 409 if session_id already exists).

    Output: Created session record.
    """
    return session_controller.create_session(db, session_data)

@router.delete("/{session_id}", status_code=status.HTTP_200_OK)
async def delete_session_api(
    session_id: str,
    session_controller: SessionController = Depends(get_session_controller),
    db: Session = Depends(get_db) # Inject database session
) -> Dict[str, str]:
    """
    **Session API: Delete Session**

    Input: `session_id` in path

    Logic: Delete session by ID.

    Output: Success/failure message.
    """
    return session_controller.delete_session(db, session_id)

@router.get("/by-user/{user_id}", response_model=List[Session])
async def get_sessions_by_user_api(
    user_id: str,
    session_controller: SessionController = Depends(get_session_controller),
    db: Session = Depends(get_db) # Inject database session
):
    """
    **Session API: Get Sessions by User**

    Input: `user_id` in path

    Logic: Fetch all sessions created by this user.

    Output: List of sessions.
    """
    return session_controller.get_sessions_by_user(db, user_id)

@router.put("/{session_id}/rename", response_model=Session)
async def rename_session_api(
    session_id: str,
    rename_data: SessionRename,
    session_controller: SessionController = Depends(get_session_controller),
    db: Session = Depends(get_db) # Inject database session
):
    """
    **Session API: Rename Session**

    Input: `session_id` in path, `new_session_name` in body.

    Logic: Update session name for the given ID.

    Output: Updated session record.
    """
    return session_controller.rename_session(db, session_id, rename_data.new_session_name)

