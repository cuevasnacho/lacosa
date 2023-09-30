from pydantic import *
from enum import Enum
from typing import Optional, List, Any
from api.models.user import Player, get_jugador
from fastapi import FastAPI, HTTPException, APIRouter, Query
from fastapi.responses import JSONResponse
from pony.orm import db_session, commit , ObjectNotFound
from pony.orm import Set
from definitions import match_status

from db.database import Lobby as db_lobby
from db.database import Match as db_Match
from db.database import Player as db_player

router = APIRouter()



class Lobby(BaseModel):
    lobby_id : int
    lobby_name: str
    lobby_max : int
    lobby_min : int
    lobby_password : Optional[str] = None


class CreateLobby(BaseModel):
    lobby_id : int



@db_session()
def get_lobby(lobby_id):
    try:
        lobby = db_lobby[lobby_id]
        return lobby
    except ObjectNotFound:
        message = "El lobby no existe"
        status_code = 404 # not found
        return JSONResponse(content=message, status_code=status_code)




@router.post("/lobby", response_model=CreateLobby)
async def Crear_Lobby(player_id: int, new_lobby: Lobby, lobby_name : str, lobby_max : int, lobby_min : int,
password : Optional[str] = None ):
    if len(lobby_name)>20:
        message = "Nombe demasiado largo"
        status_code = 406 # no acceptable
        return JSONResponse(content=message, status_code=status_code)
    if lobby_max>12:
        message = "Maximo de players no permitido"
        status_code = 406 # no acceptable
        return JSONResponse(content=message, status_code=status_code)
    if lobby_min<5: #DECISION DE DISEÑO
        message = "Minimo de players no permitido"
        status_code = 406 # no acceptable
        return JSONResponse(content=message, status_code=status_code)
    if lobby_min > lobby_max:
        message = "Minimo y maximo de players no permitido"
        status_code = 406 # no acceptable
        return JSONResponse(content=message, status_code=status_code)

    with db_session:
        host = get_jugador(player_id)
        new_lobby = db_lobby(lobby_name = lobby_name, lobby_max = lobby_max,lobby_min = lobby_min,
        lobby_password= password, lobby_pcount = 1)
        new_lobby.lobby_player.add(host)
    return new_lobby

@router.post("/lobby/{lobby_id}")
async def Buscar_Lobby(lobby_id : int):
    lobby = get_lobby(lobby_id)
    return {
  "lobby_id": lobby.lobby_id,
  "lobby_name": lobby.lobby_name,
  "lobby_max": lobby.lobby_max,
  "lobby_min": lobby.lobby_min,
  "lobby_password": lobby.lobby_password
}
    
