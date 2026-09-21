from jose import JWTError, jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
from fastapi import HTTPException

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError("FALTA LA VARIABLE SECRET KEY")
ALGORITHM = os.getenv("ALGORITHM")
if not ALGORITHM:
    raise RuntimeError("FALTA LA VARIABLE ALGORITHM")
try:
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
except(TypeError, ValueError):
    raise RuntimeError("FALTA LA VARIABLE ACCESS_TOKEN_EXPIRE_MINUTES o no es un numero valido")

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm = ALGORITHM)

def verify_token(token: str) -> int:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms= [ALGORITHM])
        user_id = payload.get("user_id")
        return user_id
    except JWTError:
        raise HTTPException (status_code = 401, detail="Token invalido")