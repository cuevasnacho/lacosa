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
from api.start_match import router as start_match_router
from api.models.lobby import router as lobby_router
from api.start_match import router as start_match_router
from fastapi.middleware.cors import CORSMiddleware
from api.load_templates import load_templates
from api.play_card import router as play_card_router
app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#configuro directorio de archivos estaticos
app.mount("/static", StaticFiles(directory="static"), name="static")

#configuro directorio de paginas dinamicas
templates = Jinja2Templates(directory="/templates")

#configuro estado base de la base de datos
load_templates()

#agregar el router de usuarios a la aplicación
app.include_router(home_router)
app.include_router(discard_router)
app.include_router(show_matches_router)
app.include_router(user_router)
app.include_router(start_match_router)
app.include_router(lobby_router)
app.include_router(start_match_router)
app.include_router(play_card_router)
