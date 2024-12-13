from sqlalchemy import Column, Integer, String, Text
from app.db.database import Base

class Lead(Base):
    __tablename__ = "leads"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    service = Column(String, nullable=False)
    message = Column(Text, nullable=False)
