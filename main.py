#levantar el servidor 
#uvicorn main:app --reload

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from db.database import Player as db_player
from pony.orm import db_session

from api.home import router as home_router 
from api.discard_card import router as discard_router
from api.show_matches import router as show_matches_router
from api.models.user import router as user_router
from api.models.lobby import router as lobby_router


app = FastAPI()

#configuro directorio de archivos estaticos 
app.mount("/static", StaticFiles(directory="static"), name="static")

#configuro directorio de paginas dinamicas
templates = Jinja2Templates(directory="/templates")

#agregar el router de usuarios a la aplicación
app.include_router(home_router)
app.include_router(discard_router)
app.include_router(show_matches_router)
app.include_router(user_router)
app.include_router(lobby_router)

