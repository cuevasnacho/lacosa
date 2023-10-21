#levantar el servidor
#uvicorn main:app --reload

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from db.database import Player as db_player
from pony.orm import db_session
from fastapi.middleware.cors import CORSMiddleware

from api.player.discard_card import router as discard_router
from api.lobby.show_lobbys import router as show_matches_router
from api.player.player import router as user_router
from api.lobby.lobby import router as lobby_router
from api.lobby.request_join import router as request_join_router
from api.lobby.start_lobby import router as start_match_router
from api.match.next_turn import router as next_turn_router
from fastapi.middleware.cors import CORSMiddleware
from api.card.load_templates import load_templates
from api.player.play_card import router as play_card_router
from api.player.steal_card import router as steal_card_router
from api.player.get_hand import router as get_hand_router
from api.player.get_status import router as get_status_router
from api.match.match_websocket import router as match_websocket
from api.match.end_match import router as end_math_router
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

app.include_router(discard_router)
app.include_router(show_matches_router)
app.include_router(user_router)
app.include_router(lobby_router)
app.include_router(request_join_router)
app.include_router(start_match_router)
app.include_router(play_card_router)
app.include_router(next_turn_router)
app.include_router(steal_card_router)
app.include_router(get_hand_router)
app.include_router(get_status_router)
app.include_router(match_websocket)
app.include_router(end_math_router)
