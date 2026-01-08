from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from model.user import User
from schemas.user_schema import UserLogin

from service.verify_password_service import verify_password
from service.create_token_service import create_access_token


def login_user(db: Session, user: UserLogin):

    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    access_token = create_access_token({"sub": db_user.email})

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
