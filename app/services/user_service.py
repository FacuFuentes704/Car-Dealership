from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate, UserResponse, UserLogin
from app.auth.auth import hash_password, verify_password
from app.auth.jwt import create_access_token
from fastapi import HTTPException

def register_user(db: Session, user_data: UserCreate):
    resultado = db.query(User).filter(User.email == user_data.email).first()
    if resultado:
        raise HTTPException(status_code=400, detail="Email duplicado")
    hashed_password = hash_password(user_data.password)
    new_user = User(name = user_data.name, email = user_data.email, password = hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def login_user(db: Session, user_data: UserLogin):
    resultado = db.query(User).filter(User.email == user_data.email).first()
    if not resultado:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    hashed_password = resultado.password
    verify = verify_password(user_data.password, hashed_password)
    if verify is False:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    if resultado.is_active is False:
        raise HTTPException(status_code=403, detail="Usuario inactivo")
    token = create_access_token({"user_id": resultado.id})
    return {"access_token": token, "token_type": "bearer"}

def update_user(db: Session, user_data: UserUpdate, user_id:int):
    resultado = db.query(User).filter(User.id == user_id).first()
    if not resultado:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    datos = user_data.model_dump(exclude_unset=True)
    if "password" in datos:
        datos["password"] = hash_password(datos["password"])
    for campo, valor in datos.items():
        setattr(resultado, campo, valor)
    db.commit()
    db.refresh(resultado)
    return resultado

def delete_user(db: Session, user_id:int):
    resultado = db.query(User).filter(User.id == user_id).first()
    if not resultado:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    resultado.is_active = False
    db.commit()
    return

def get_user_profile(db:Session, user_id:int):
    resultado = db.query(User).filter(User.id == user_id).first()
    if not resultado:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return resultado