from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.models import Suburb

# Initialize Router
router = APIRouter()

# Set up Jinja2 Templates
templates = Jinja2Templates(directory="app/templates")


# Helper function to fetch suburbs from the database
def get_suburbs_from_db(db: Session):
    return db.query(Suburb).all()



# Smart Home Setup Guide Route
@router.get("/blog/how-to-set-up-a-smart-home-system-a-beginners-guide", response_class=HTMLResponse)
async def smart_home_setup_post(request: Request, db: Session = Depends(get_db)):
    suburbs = get_suburbs_from_db(db)  # Optional: if you want to include related data like locations
    return templates.TemplateResponse("smart_home_setup_post.html", {"request": request, "suburbs": suburbs})

