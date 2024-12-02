from fastapi import APIRouter, Form, HTTPException
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from sqlalchemy import Column, Integer, String, Text, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database setup
Base = declarative_base()
DATABASE_URL = "sqlite:///./leads.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Lead(Base):
    __tablename__ = "leads"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    service = Column(String, nullable=False)
    message = Column(Text, nullable=False)

Base.metadata.create_all(bind=engine)

# Email Configuration
SMTP_SERVER = "smtp.example.com"
SMTP_PORT = 587
SMTP_USER = "your-email@example.com"
SMTP_PASS = "your-email-password"

# Create the router
router = APIRouter()

@router.post("/quote")
async def handle_quote(
    name: str = Form(...),
    email: str = Form(...),
    service: str = Form(...),
    message: str = Form(...)
):
    # Save lead to database
    db = SessionLocal()
    lead = Lead(name=name, email=email, service=service, message=message)
    db.add(lead)
    db.commit()
    db.close()

    # Send email notification
    try:
        msg = MIMEMultipart()
        msg["From"] = SMTP_USER
        msg["To"] = "admin@example.com"
        msg["Subject"] = "New Quote Request"
        body = f"Name: {name}\nEmail: {email}\nService: {service}\nMessage: {message}"
        msg.attach(MIMEText(body, "plain"))

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.sendmail(SMTP_USER, "admin@example.com", msg.as_string())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send email: {e}")

    return {"message": "Thank you for your request. We will get back to you shortly."}
