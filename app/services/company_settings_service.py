from sqlalchemy.orm import Session
from app.models.company_settings import CompanySettings
from app.schemas.company_settings import CompanySettingsUpdate

def get_company_settings(db: Session):
    resultado = db.query(CompanySettings).first()
    if not resultado:
        resultado = CompanySettings(business_name = "LGi Motors")
        db.add(resultado)
        db.commit()
        db.refresh(resultado)
    return resultado

def update_company_settings(db:Session, datos: CompanySettingsUpdate):
    resultado = get_company_settings(db)
    datos_dict = datos.model_dump(exclude_unset=True)
    for campo, valor in datos_dict.items():
        setattr(resultado, campo, valor)
    db.commit()
    db.refresh(resultado)
    return resultado
    