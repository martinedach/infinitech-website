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


@router.get("/computer-repair/{suburb}", response_class=HTMLResponse)
async def computer_repair_suburb(request: Request, suburb: str, db: Session = Depends(get_db)):
    suburbs = get_suburbs_from_db(db)
    
     
    # Check if the requested suburb is in the database
    if not any(s.name == suburb for s in suburbs):
        # Suburb not found, raise 404 error
        raise HTTPException(status_code=404, detail="Suburb not found")
    
    return templates.TemplateResponse(
        "computer_repair.html",
        {"request": request, "suburb": suburb, "suburbs": suburbs}
    )


@router.get("/laptop-repair/{suburb}", response_class=HTMLResponse)
async def laptop_repair_suburb(request: Request, suburb: str, db: Session = Depends(get_db)):
    suburbs = get_suburbs_from_db(db)
    
    
    # Check if the requested suburb is in the database
    if not any(s.name == suburb for s in suburbs):
        # Suburb not found, raise 404 error
        raise HTTPException(status_code=404, detail="Suburb not found")
    
    
    return templates.TemplateResponse(
        "laptop_repair.html",
        {"request": request, "suburb": suburb, "suburbs": suburbs}
    )


@router.get("/wifi-repair/{suburb}", response_class=HTMLResponse)
async def wifi_repair_suburb(request: Request, suburb: str, db: Session = Depends(get_db)):
    suburbs = get_suburbs_from_db(db)
    
    # Check if the requested suburb is in the database
    if not any(s.name == suburb for s in suburbs):
        # Suburb not found, raise 404 error
        raise HTTPException(status_code=404, detail="Suburb not found")
    
    
    return templates.TemplateResponse(
        "wifi_repair.html",
        {"request": request, "suburb": suburb, "suburbs": suburbs}
    )


@router.get("/apple-repair/{suburb}", response_class=HTMLResponse)
async def apple_repair_suburb(request: Request, suburb: str, db: Session = Depends(get_db)):
    suburbs = get_suburbs_from_db(db)
    
    # Check if the requested suburb is in the database
    if not any(s.name == suburb for s in suburbs):
        # Suburb not found, raise 404 error
        raise HTTPException(status_code=404, detail="Suburb not found")
    
    
    return templates.TemplateResponse(
        "apple_repair.html",
        {"request": request, "suburb": suburb, "suburbs": suburbs}
    )


@router.get("/printer-repair/{suburb}", response_class=HTMLResponse)
async def printer_repair_suburb(request: Request, suburb: str, db: Session = Depends(get_db)):
    suburbs = get_suburbs_from_db(db)
    
    # Check if the requested suburb is in the database
    if not any(s.name == suburb for s in suburbs):
        # Suburb not found, raise 404 error
        raise HTTPException(status_code=404, detail="Suburb not found")
    
    
    return templates.TemplateResponse(
        "printer_repair.html",
        {"request": request, "suburb": suburb, "suburbs": suburbs}
    )


# Hardware Solutions Route
@router.get("/services/hardware-solutions", response_class=HTMLResponse)
async def hardware_solutions(request: Request, db: Session = Depends(get_db)):
    suburbs = get_suburbs_from_db(db)
    return templates.TemplateResponse("hardware_solutions.html", {"request": request, "suburbs": suburbs})


# Software Development Route
@router.get("/services/software-development", response_class=HTMLResponse)
async def software_development(request: Request, db: Session = Depends(get_db)):
    suburbs = get_suburbs_from_db(db)
    return templates.TemplateResponse("software_development.html", {"request": request, "suburbs": suburbs})


# Network Services Route
@router.get("/services/network-services", response_class=HTMLResponse)
async def network_services(request: Request, db: Session = Depends(get_db)):
    suburbs = get_suburbs_from_db(db)
    return templates.TemplateResponse("network_services.html", {"request": request, "suburbs": suburbs})


# Cloud Deployment Route
@router.get("/services/cloud-deployment", response_class=HTMLResponse)
async def cloud_deployment(request: Request, db: Session = Depends(get_db)):
    suburbs = get_suburbs_from_db(db)
    return templates.TemplateResponse("cloud_deployment.html", {"request": request, "suburbs": suburbs})


# Microsoft 365 Setup, Maintenance, and Fix Route
@router.get("/services/microsoft-365-support", response_class=HTMLResponse)
async def microsoft_365_support(request: Request, db: Session = Depends(get_db)):
    suburbs = get_suburbs_from_db(db)
    return templates.TemplateResponse("microsoft_365_support.html", {"request": request, "suburbs": suburbs})


# Business IT Support Route
@router.get("/services/business-it-support", response_class=HTMLResponse)
async def business_it_support(request: Request, db: Session = Depends(get_db)):
    suburbs = get_suburbs_from_db(db)
    return templates.TemplateResponse("business_it_support.html", {"request": request, "suburbs": suburbs})


# Custom-Built PC Route
@router.get("/services/custom-built-pc", response_class=HTMLResponse)
async def custom_built_pc(request: Request, db: Session = Depends(get_db)):
    suburbs = get_suburbs_from_db(db)
    return templates.TemplateResponse("custom_built_pc.html", {"request": request, "suburbs": suburbs})


# Remote IT Support Route
@router.get("/services/remote-it-support", response_class=HTMLResponse)
async def remote_it_support(request: Request, db: Session = Depends(get_db)):
    suburbs = get_suburbs_from_db(db)
    return templates.TemplateResponse("remote_it_support.html", {"request": request, "suburbs": suburbs})


# Managed IT Services Route
@router.get("/services/managed-it-services", response_class=HTMLResponse)
async def managed_it_services(request: Request, db: Session = Depends(get_db)):
    suburbs = get_suburbs_from_db(db)
    return templates.TemplateResponse("managed_it_services.html", {"request": request, "suburbs": suburbs})


# Remote Work Support Package Route
@router.get("/services/remote-work-support", response_class=HTMLResponse)
async def remote_work_support(request: Request, db: Session = Depends(get_db)):
    suburbs = get_suburbs_from_db(db)
    return templates.TemplateResponse("remote_work_support.html", {"request": request, "suburbs": suburbs})
