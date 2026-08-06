from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal, get_db
from app.schemas.user import UserUpdate, UserCreate, UserLogin, UserResponse, TokenResponse
from app.services.user_service import register_user, login_user, update_user, delete_user
from app.models.user import User
from app.auth.auth import get_current_user

users_router = APIRouter(prefix="/users",
                         tags=["users"])

auth_router = APIRouter(prefix="/auth",
                        tags=["auth"])

@users_router.post("/register", response_model=UserResponse)
def register(user_data:UserCreate, db: Session = Depends(get_db)):
    return register_user(user_data, db)

@auth_router.post("/login", response_model=TokenResponse)
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    return login_user(db, user_data)

@users_router.patch("/update", response_model=UserResponse)
def update(user_data:UserUpdate, db:Session = Depends(get_db), user_id: int = Depends(get_current_user)):
    return update_user(db, user_data, user_id)

@users_router.delete("/delete", response_model=UserResponse)
def delete(user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    return delete_user(db, user_id)

@users_router.get("/", response_model=UserResponse)
def get(user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    return get_current_user(db, user_id)