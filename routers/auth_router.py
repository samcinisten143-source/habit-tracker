from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.db_session import get_db
from schemas.user_schema import UserCreate, UserLogin, UserResponse
from service.register_service import register_user
from service.login_service import login_user
from service.auth_dependency import get_current_user
from model.user import User
from schemas.user_schema import RegisterResponse


router = APIRouter(prefix="/auth", tags=["Authentication"])


# -------------------------------
# Register New User
# -------------------------------
@router.post("/register", response_model=RegisterResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    return register_user(db, user)


# -------------------------------
# Login
# -------------------------------
@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    """
    Authenticate a user and return an access token.
    """
    return login_user(db, user)


# -------------------------------
# Get Logged-In User
# -------------------------------
@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    """
    Return details of the currently authenticated user.
    """
    return current_user
