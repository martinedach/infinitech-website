from sqlalchemy import ARRAY, Boolean, Column, Integer, String, Text, Float, TIMESTAMP, Enum, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base import Base
import enum


class LeadStatus(enum.Enum):
    NEW = "new"
    CONTACTED = "contacted"
    QUALIFIED = "qualified"
    IN_NEGOTIATION = "in_negotiation"
    CLOSED_WON = "closed_won"
    CLOSED_LOST = "closed_lost"


class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    service = Column(String, nullable=False)
    message = Column(Text, nullable=False)

    # New fields based on suggestions
    status = Column(Enum(LeadStatus, name="lead_status"), nullable=False, server_default="new")
    assigned_to = Column(Integer, ForeignKey("users.id"), nullable=True)
    assigned_user = relationship("User", back_populates="leads")


    lead_score = Column(Integer, nullable=True)
    priority_level = Column(String, nullable=True)

    last_contacted_at = Column(TIMESTAMP, nullable=True)
    next_follow_up_at = Column(TIMESTAMP, nullable=True)
    contact_method_preferred = Column(String, nullable=True)

    converted_at = Column(TIMESTAMP, nullable=True)
    lost_at = Column(TIMESTAMP, nullable=True)
    lost_reason = Column(Text, nullable=True)

    tags = Column(ARRAY(String), nullable=True)
    notes = Column(Text, nullable=True)

    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

class Suburb(Base):
    __tablename__ = "suburbs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    city = Column(String(100), nullable=False)
    postcode = Column(String(20), nullable=False)
    region = Column(String(100), nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    
    
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    
    leads = relationship("Lead", back_populates="assigned_user")
