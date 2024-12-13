import logging
from fastapi import APIRouter, Form, HTTPException
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from sqlalchemy import Column, Integer, String, Text, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database setup
Base = declarative_base()
DATABASE_URL = "postgresql://user:password@db:5432/fastapi_db"
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
SMTP_SERVER = "smtp.office365.com"
SMTP_PORT = 587
SMTP_USER = "martin@infinitech.co.nz"
SMTP_PASS = "mfrpmcmsgvzdmqtc"

# Logger Configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("submissions.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Create the router
router = APIRouter()

@router.post("/quote")
async def handle_quote(
    name: str = Form(...),
    email: str = Form(...),
    message: str = Form(...)
):
    # Save lead to database
    db = SessionLocal()
    try:
        lead = Lead(name=name, email=email, service='null', message=message)
        db.add(lead)
        db.commit()
        logger.info(f"New submission: Name={name}, Email={email}, Service=null, Message={message}")
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to save submission: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to save lead to database: {e}")
    finally:
        db.close()

    # Send email notification
    try:
        msg = MIMEMultipart()
        msg["From"] = "info@infinitech.co.nz"
        msg["To"] = email
        msg["Subject"] = "New Quote Request"
        body = f"Name: {name}\nEmail: {email}\nService:  null\nMessage: {message}"
        msg.attach(MIMEText(body, "plain"))

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.sendmail(SMTP_USER, "info@infinitech.co.nz", msg.as_string())
            logger.info(f"Email sent to: {email}")
    except Exception as e:
        logger.error(f"Failed to send email: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to send email: {e}")

    return {"message": "Thank you for your request. We will get back to you shortly."}
