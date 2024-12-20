from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException
from contextlib import asynccontextmanager
from fastapi import Request
from pathlib import Path
from app.data.suburb import suburbs
from app.db.database import create_tables_and_populate
from app.routers.quotes import router as quotes_router
from app.routers.services_router import router as services_router
from app.routers.sitemap_router import router as sitemap_router
from app.routers.admin_router import router as admin_router
from app.routers.blog_router import router as blog_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup tasks
    create_tables_and_populate()
    yield  # The app runs here
    # Shutdown tasks (if needed)

app = FastAPI(lifespan=lifespan)



# Set up templates and static files
templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(quotes_router)
app.include_router(services_router)
app.include_router(sitemap_router)
app.include_router(admin_router)
app.include_router(blog_router)



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




# Homepage route
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "suburbs": suburbs})

# Services page route
@app.get("/services", response_class=HTMLResponse)
async def services_page(request: Request):
    return templates.TemplateResponse("services.html", {"request": request, "suburbs": suburbs})

# Contact page route
@app.get("/contact", response_class=HTMLResponse)
async def contact_page(request: Request):
    return templates.TemplateResponse("contact.html", {"request": request, "suburbs": suburbs})

# Contact form submission route
@app.post("/contact/submit")
async def submit_contact_form(
    name: str = Form(...),
    email: str = Form(...),
    message: str = Form(...)
):
    # Handle the form submission (e.g., save to database, send email)
    # For now, we'll just return a confirmation message.
    return {
        "message": "Thank you for reaching out!",
        "name": name,
        "email": email,
        "submitted_message": message,
        "suburbs": suburbs
    }
    
    
    
@app.get("/services/hardware", response_class=HTMLResponse)
async def hardware_page(request: Request):
    return templates.TemplateResponse("hardware.html", {"request": request, "suburbs": suburbs})


# Software Development Page
@app.get("/services/software", response_class=HTMLResponse)
async def software_page(request: Request):
    return templates.TemplateResponse("software.html", {"request": request, "suburbs": suburbs})


# Network Support Page
@app.get("/services/network", response_class=HTMLResponse)
async def network_page(request: Request):
    return templates.TemplateResponse("network.html", {"request": request, "suburbs": suburbs})

# Network Support Page
@app.get("/about-us", response_class=HTMLResponse)
async def aboutus_page(request: Request):
    return templates.TemplateResponse("aboutus.html", {"request": request, "suburbs": suburbs})

@app.get("/robots.txt", response_class=PlainTextResponse)
async def robots_txt():
    content = """
    User-agent: *
    Disallow: /private
    Disallow: /admin
    Disallow: /hidden
    Allow: /

    Sitemap: https://infinitech.com/sitemap.xml
    """
    return content

# Custom 404 handler
@app.exception_handler(StarletteHTTPException)
async def custom_404_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code == 404:
        return templates.TemplateResponse("404.html", {"request": request, "suburbs": suburbs}, status_code=404)
    return HTMLResponse(content=str(exc.detail), status_code=exc.status_code)


