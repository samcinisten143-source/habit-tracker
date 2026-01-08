from pydantic import BaseModel, EmailStr, Field


# -----------------------------
# Create User (Input)
# -----------------------------
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=72)

    model_config = {
        "from_attributes": True
    }


# -----------------------------
# Login User (Input)
# -----------------------------
class UserLogin(BaseModel):
    email: EmailStr
    password: str


# -----------------------------
# User Response (Output)
# -----------------------------
class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr

    model_config = {
        "from_attributes": True
    }


# -----------------------------
# Register Response (Output)
# -----------------------------
class RegisterResponse(BaseModel):
    message: str
    user: UserResponse
    access_token: str
    token_type: str

    model_config = {
        "from_attributes": True
    }
