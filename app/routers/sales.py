from fastapi import Depends, APIRouter
from app.schemas.sale import SaleCreate, SaleResponse, SaleUpdate
from app.models.user import User
from app.database import get_db
from app.auth.auth import get_current_user
from sqlalchemy.orm import Session
from app.services.sale_service import get_sales, get_sales_by_id, delete_sale, update_sale, create_sale

sales_router = APIRouter(prefix="/sales",
                         tags=["sales"])

@sales_router.post("/", response_model=SaleResponse)
def create(sale_data: SaleCreate, db: Session = Depends(get_db), user_id: User = Depends(get_current_user)):
    return create_sale(db, sale_data, user_id.id)

@sales_router.get("/", response_model=list[SaleResponse])
def show_sales(db: Session = Depends(get_db), user_id: User = Depends(get_current_user)):
    return get_sales(db)

@sales_router.get("/{sale_id}", response_model=SaleResponse)
def show_by_id(sale_id: int, db: Session = Depends(get_db), user_id: User = Depends(get_current_user)):
    return get_sales_by_id(db, sale_id)

@sales_router.patch("/{sale_id}", response_model=SaleResponse)
def update(sale_id: int, sale_Data: SaleUpdate, db: Session = Depends(get_db), user_id: User = Depends(get_current_user)):
    return update_sale(db, sale_Data, sale_id)

@sales_router.delete("/{sale_id}", status_code=204)
def delete(sale_id: int, db: Session = Depends(get_db), user_id: User = Depends(get_current_user)):
    return delete_sale(db, sale_id)