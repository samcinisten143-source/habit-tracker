# service/auth_dependency.py

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
from service.verify_token_service import verify_access_token
from database.db_session import SessionLocal
from model.user import User

oauth2_scheme = HTTPBearer()

def get_current_user(token=Depends(oauth2_scheme)):
    """
    Extracts and validates the JWT token.
    Then finds the user in the database and returns user details including ID.
    """

    token_str = token.credentials

    # Decode token → returns payload (ex: {"sub": email, "exp": ...})
    payload = verify_access_token(token_str)

    email = payload.get("sub")
    if not email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload"
        )

    # Fetch user from DB by email
    db = SessionLocal()
    user = db.query(User).filter(User.email == email).first()
    db.close()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    # Debug print (safe)
    print("USER PAYLOAD:", {"id": user.id, "email": user.email})

    # Return user data as dictionary → routers expect user["id"]
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email
    }
