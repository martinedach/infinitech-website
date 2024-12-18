from datetime import timedelta
from typing import Optional
from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.auth.auth import get_current_user, authenticate_user, create_access_token, get_password_hash
from app.db.database import get_db
from app.models.models import User as DBUser 
from app.models.models import Lead, Suburb
from app.models.pymodels import UserCreate, UserRead  # Adjust if necessary
import os

router = APIRouter(
    prefix="/admin",
    tags=["admin"]
)

templates = Jinja2Templates(directory="app/templates")

LOG_FILE_PATH = "submissions.log"


# Login page
@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

# Token endpoint for login
@router.post("/token")
def login_for_access_token(
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    print(f"Received username: {username}")
    user = authenticate_user(username, password, db)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    # Create access token
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=timedelta(minutes=30)
    )

    # Return token in response
    return JSONResponse(
        content={"access_token": access_token, "token_type": "bearer"},
        status_code=200
    )

@router.get("/dashboard")
def admin_dashboard(request: Request, user: dict = Depends(get_current_user)):
    return templates.TemplateResponse("dashboard.html", {"request": request, "user": user})

# Route to view all users
@router.get("/users/")
def read_users(request: Request, db: Session = Depends(get_db)):
    users = db.query(DBUser).all()  # Fetch all users
    return templates.TemplateResponse(
        "users.html", {"request": request, "users": users, "title": "Manage Users"}
    )

# Route to create a new user
@router.post("/user/", response_model=UserRead, dependencies=[Depends(get_current_user)])
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = DBUser(username=user.username, email=user.email, hashed_password=get_password_hash(user.password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user




# Function to parse log lines
def parse_logs(log_file_path):
    log_entries = []
    if os.path.exists(log_file_path):
        with open(log_file_path, "r") as file:
            for line in file:
                if " - " in line:
                    parts = line.split(" - ", maxsplit=2)
                    if len(parts) == 3:
                        timestamp, log_level, message = parts
                        log_entries.append({
                            "timestamp": timestamp.strip(),
                            "log_level": log_level.strip(),
                            "message": message.strip()
                        })
                else:
                    # Append multi-line log content under the previous message
                    if log_entries:
                        log_entries[-1]["message"] += f"\n{line.strip()}"
    return log_entries




@router.get("/logs")
def view_logs(request: Request, user: dict = Depends(get_current_user)):
    logs = parse_logs(LOG_FILE_PATH)
    return templates.TemplateResponse(
        "logs.html", {"request": request, "logs": logs, "title": "System Logs"}
    )
    
    
    
# Endpoint to view leads
@router.get("/leads")
def view_leads(request: Request, db: Session = Depends(get_db)):
    leads = db.query(Lead).all()  # Fetch all leads from the database
    return templates.TemplateResponse(
        "leads.html", {"request": request, "leads": leads, "title": "Leads Management"}
    )
    
    
    
@router.post("/suburbs/add")
def add_suburb(
    name: str = Form(...),
    city: str = Form(...),
    region: str = Form(...),
    postcode: str = Form(...),
    latitude: Optional[float] = Form(None),
    longitude: Optional[float] = Form(None),
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)  # Optional: Restrict access to authenticated users
):
    # Check if the suburb already exists
    existing_suburb = db.query(Suburb).filter(Suburb.name == name).first()
    if existing_suburb:
        raise HTTPException(status_code=400, detail="Suburb already exists.")

    # Add the new suburb
    new_suburb = Suburb(
        name=name,
        city=city,
        region=region,
        postcode=postcode,
        latitude=latitude,
        longitude=longitude,
    )
    db.add(new_suburb)
    db.commit()
    db.refresh(new_suburb)

    # Redirect back to the suburbs management page
    return RedirectResponse(url="/admin/suburbs", status_code=303)
    
    
@router.post("/suburbs/remove")
def remove_suburb(
    id: int = Form(...),
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)  # Optional: Restrict access to authenticated users
):
    # Check if the suburb exists
    suburb = db.query(Suburb).filter(Suburb.id == id).first()
    if not suburb:
        raise HTTPException(status_code=404, detail="Suburb not found.")

    # Remove the suburb
    db.delete(suburb)
    db.commit()

    # Redirect back to the suburbs management page
    return RedirectResponse(url="/admin/suburbs", status_code=303)



@router.get("/suburbs", response_class=HTMLResponse)
def view_suburbs(
    request: Request,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)  # Optional: Restrict access to authenticated users
):
    # Fetch all suburbs
    suburbs = db.query(Suburb).all()
    return templates.TemplateResponse(
        "suburbs.html", {"request": request, "suburbs": suburbs, "title": "Suburbs Management"}
    )
