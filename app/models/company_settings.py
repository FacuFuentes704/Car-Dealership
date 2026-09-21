from app.database import Base
from sqlalchemy import Integer, String, Column

class CompanySettings(Base):
    __tablename__ = "company_settings"

    id = Column(Integer, primary_key=True, index=True)
    business_name = Column(String(200), nullable=False)
    address = Column(String(200), nullable=True)
    locality = Column(String(100), nullable=True)
    document_number = Column(String(50), nullable=True)
    phone = Column(String(50), nullable=True)