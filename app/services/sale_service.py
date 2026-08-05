from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.sale import Sale
from app.schemas.sale import SaleCreate, SaleResponse, SaleUpdate

def create_sale(db: Session, sale_data: SaleCreate):
    new_sale = Sale(**sale_data.model_dump())
    db.add(new_sale)
    db.commit()
    db.refresh(new_sale)
    return new_sale

def get_sales(db: Session):
    resultado = db.query(Sale).all()
    return resultado

def get_sales_by_id(db: Session, sale_id: int):
    resultado = db.query(Sale).filter(Sale.id == sale_id).first()
    if not resultado:
        raise HTTPException(status_code=404, detail="Resultado no encontrado")
    return resultado

def update_sale(db:Session, sale_data: SaleUpdate, sale_id: int):
    resultado = db.query(Sale).filter(Sale.id == sale_id).first()
    if not resultado:
        raise HTTPException(status_code=404, detail="Resultado no encontrado")
    datos = sale_data.model_dump(exclude_unset=True)
    for campo, valor in datos:
        setattr(resultado, campo, valor)
    db.commit()
    db.refresh(resultado)
    return resultado

def delete_sale(db: Session, sale_id:int):
    resultado = db.query(Sale).filter(Sale.id == sale_id).first()
    if not resultado:
        raise HTTPException(status_code=404, detail="Venta no encontrada")
    db.delete(resultado)
    db.commit
    return