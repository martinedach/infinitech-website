from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.data.suburb import suburbs

# Initialize Router
router = APIRouter()

# Set up Jinja2 Templates
templates = Jinja2Templates(directory="app/templates")


@router.get("/computer-repair/{suburb}", response_class=HTMLResponse)
async def computer_repair_suburb(request: Request, suburb: str):
    return templates.TemplateResponse(
        "computer_repair.html",
        {"request": request, "suburb": suburb, "suburbs": suburbs}
    )

@router.get("/laptop-repair/{suburb}", response_class=HTMLResponse)
async def laptop_repair_suburb(request: Request, suburb: str):
    return templates.TemplateResponse(
        "laptop_repair.html",
        {"request": request, "suburb": suburb, "suburbs": suburbs}
    )

@router.get("/wifi-repair/{suburb}", response_class=HTMLResponse)
async def wifi_repair_suburb(request: Request, suburb: str):
    return templates.TemplateResponse(
        "wifi_repair.html",
        {"request": request, "suburb": suburb, "suburbs": suburbs}
    )
    
@router.get("/apple-repair/{suburb}", response_class=HTMLResponse)
async def apple_repair_suburb(request: Request, suburb: str):
    return templates.TemplateResponse(
        "apple_repair.html",
        {"request": request, "suburb": suburb, "suburbs": suburbs}
    )
    

@router.get("/printer-repair/{suburb}", response_class=HTMLResponse)
async def printer_repair_suburb(request: Request, suburb: str):
    return templates.TemplateResponse(
        "printer_repair.html",
        {"request": request, "suburb": suburb, "suburbs": suburbs}
    )


# Hardware Solutions Route
@router.get("/services/hardware-solutions", response_class=HTMLResponse)
async def hardware_solutions(request: Request):
    return templates.TemplateResponse("hardware_solutions.html", {"request": request, "suburbs": suburbs})

# Software Development Route
@router.get("/services/software-development", response_class=HTMLResponse)
async def software_development(request: Request):
    return templates.TemplateResponse("software_development.html", {"request": request, "suburbs": suburbs})

# Network Services Route
@router.get("/services/network-services", response_class=HTMLResponse)
async def network_services(request: Request):
    return templates.TemplateResponse("network_services.html", {"request": request, "suburbs": suburbs})


# Cloud Deployment Route
@router.get("/services/cloud-deployment", response_class=HTMLResponse)
async def cloud_deployment(request: Request):
    return templates.TemplateResponse("cloud_deployment.html", {"request": request, "suburbs": suburbs})



# Microsoft 365 Setup, Maintenance, and Fix Route
@router.get("/services/microsoft-365-support", response_class=HTMLResponse)
async def microsoft_365_support(request: Request):
    return templates.TemplateResponse("microsoft_365_support.html", {"request": request, "suburbs": suburbs})



# Business IT Support Route
@router.get("/services/business-it-support", response_class=HTMLResponse)
async def business_it_support(request: Request):
    return templates.TemplateResponse("business_it_support.html", {"request": request, "suburbs": suburbs})


# Custom-Built PC Route
@router.get("/services/custom-built-pc", response_class=HTMLResponse)
async def custom_built_pc(request: Request):
    return templates.TemplateResponse("custom_built_pc.html", {"request": request, "suburbs": suburbs})

# Remote IT Support Route
@router.get("/services/remote-it-support", response_class=HTMLResponse)
async def remote_it_support(request: Request):
    return templates.TemplateResponse("remote_it_support.html", {"request": request, "suburbs": suburbs})
