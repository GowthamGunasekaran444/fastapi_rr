
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session # Import Session
from user.model.user_model import User, UserCreate
from user.controller.user_controller import UserController
from user.repository.user_repo import UserRepository
from core.db import get_db # Import get_db

# Dependency to get a User Controller instance
def get_user_controller():
    """Provides a User Controller instance with its dependencies."""
    user_repo = UserRepository()
    return UserController(user_repo)

router = APIRouter(
    prefix="/user",
    tags=["User APIs"],
    responses={404: {"description": "Not found"}},
)

@router.post("/create", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user_api(
    user_data: UserCreate,
    user_controller: UserController = Depends(get_user_controller),
    db: Session = Depends(get_db) # Inject database session
):
    """
    **User API: Create User**

    Input: `user_id`, `username`, `email`, `created_time`

    Logic:
    - Check if user exists (by user_id).
    - If exists → return conflict (409).
    - If not → insert record.

    Output: Created user record.
    """
    return user_controller.create_user(db, user_data)

@router.get("/{user_id}", response_model=User)
async def get_user_api(
    user_id: str,
    user_controller: UserController = Depends(get_user_controller),
    db: Session = Depends(get_db) # Inject database session
):
    """
    **User API: Get User by ID**

    Input: `user_id` in path

    Logic: Fetch and return user if exists.

    Output: User record.
    """
    return user_controller.get_user(db, user_id)

