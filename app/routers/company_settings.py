from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth.auth import get_current_user
from app.models.user import User
from app.schemas.company_settings import CompanySettingsResponse, CompanySettingsUpdate
from app.services.company_settings_service import get_company_settings, update_company_settings

company_settings_router = APIRouter(prefix="/company-settings", tags=["company-settings"])

@company_settings_router.get("/", response_model=CompanySettingsResponse)
def show(db: Session = Depends(get_db), user_id: User = Depends(get_current_user)):
    return get_company_settings(db)

@company_settings_router.patch("/", response_model=CompanySettingsResponse)
def update(datos: CompanySettingsUpdate, db: Session = Depends(get_db), user_id: User = Depends(get_current_user)):
    return update_company_settings(db, datos)