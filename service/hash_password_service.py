from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    # bcrypt supports only 72 bytes
    password = password[:72]
    return pwd_context.hash(password)
