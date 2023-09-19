# api/home.py

from fastapi import APIRouter,Request,Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

router = APIRouter()

def get_templates():
    return Jinja2Templates(directory="templates")

@router.get("/home", response_class=HTMLResponse)
async def home(request: Request, templates: Jinja2Templates = Depends(get_templates)):
    return templates.TemplateResponse("home.html", {"request": request})
