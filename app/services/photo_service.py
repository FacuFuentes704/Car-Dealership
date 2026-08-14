import cloudinary.uploader
from fastapi import UploadFile, HTTPException
from sqlalchemy.orm import Session
from app.models.photo import Photo
from app.models.vehicle import Vehicle
from app import cloudinary_config

def upload_photo(db: Session, vehicle_id: int, is_main: bool, photo: UploadFile):
    query = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
    if not query:
        raise HTTPException(status_code=404, detail="Vehiculo no encontrado")
    contenido = photo.file.read()
    resultado = cloudinary.uploader.upload(contenido)
    url = resultado["secure_url"]
    new_photo = Photo(url=url, vehicle_id=vehicle_id, is_main=is_main)
    db.add(new_photo)
    db.commit()
    db.refresh(new_photo)
    return new_photo

def update_photo(db: Session, photo_id: int, vehicle_id: int):
    resultado = db.query(Photo).filter(Photo.vehicle_id == vehicle_id).all()
    if not resultado:
        raise HTTPException(status_code=404, detail="Vehiculo no encontrado")
    foto_principal = None

    for foto in resultado:
        foto.is_main = False
        if foto.id == photo_id:
            foto_principal = foto
    if not foto_principal:
        raise HTTPException(status_code=404, detail="Foto no encontrada")

    foto_principal.is_main = True
    db.commit()
    db.refresh(foto_principal)
    return foto_principal