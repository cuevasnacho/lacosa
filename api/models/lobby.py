from pydantic import *
from typing import Optional, List, Any
from api.models.user import get_jugador
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pony.orm import db_session, commit , ObjectNotFound
from definitions import match_status

from db.database import Lobby as db_lobby
from db.database import Match as db_match
from db.database import Player as db_player
from definitions import match_status
import json 

router = APIRouter()

class Lobby(BaseModel):
    lobby_id : int
    lobby_name: str
    lobby_max : int
    lobby_min : int
    lobby_password : Optional[str] = None

class CreateLobbyOut(BaseModel):
    lobby_id : int

class ListedLobbys(BaseModel):
    lobby_id : int
    lobby_name : str
    lobby_max : int
    lobby_pcount : int

@db_session()
def get_lobby(lobby_id):
    try:
        lobby = db_lobby[lobby_id]
        return lobby
    except ObjectNotFound:
        message = "El lobby no existe"
        status_code = 404 # not found
        return JSONResponse(content=message, status_code=status_code)


@db_session()
def get_match(match_id):
    try:
        match= db_match[match_id]
        return match
    except ObjectNotFound:
        message = "La partida no existe"
        status_code = 404 # not found
        return JSONResponse(content=message, status_code=status_code)


class CreateLobby(BaseModel):
    player_id : int
    lobby_name : str
    lobby_max : int
    lobby_min : int
    lobby_password : Optional[str] = None

@router.post("/lobbys/")
async def Crear_Lobby(new_lobby: CreateLobby):
    if len(new_lobby.lobby_name)>20:
        message = "Nombe demasiado largo"
        status_code = 406 # no acceptable
        return JSONResponse(content=message, status_code=status_code)
    if new_lobby.lobby_max>12:
        message = "Maximo de players no permitido"
        status_code = 406 # no acceptable
        return JSONResponse(content=message, status_code=status_code)
    if new_lobby.lobby_min<4: #DECISION DE DISEÑO
        message = "Minimo de players no permitido"
        status_code = 406 # no acceptable
        return JSONResponse(content=message, status_code=status_code)
    if new_lobby.lobby_min > new_lobby.lobby_max:
        message = "Minimo y maximo de players no permitido"
        status_code = 406 # no acceptable
        return JSONResponse(content=message, status_code=status_code)
    try:
        with db_session:
            new_match = db_match(match_status = match_status.NOT_INITIALIZED.value, match_direction = True,
                                match_currentP = 0, match_cardsCount = 0)
            password = new_lobby.lobby_password if new_lobby.lobby_password else None 
            commit()
            new_lobby = db_lobby(lobby_name = new_lobby.lobby_name, lobby_max = new_lobby.lobby_max, lobby_min = new_lobby.lobby_min,
                                lobby_password = password, lobby_pcount = 1, lobby_match = new_match.match_id)
            commit()
        content = {"lobby_id" : new_lobby.lobby_id}
        return JSONResponse(content= json.loads(json.dumps(content)), status_code=200)

    except:
        content = "Error creacion del lobby"
        return JSONResponse(content= content, status_code=404)


@router.get("/lobbys/{lobby_id}/refrescar")
async def players_in_lobby(lobby_id : int):  
    players_names = []
    with db_session:
        players = db_player.select(lambda player : player.player_lobby.lobby_id == lobby_id)
        for player in players:
            players_names.append(player.player_name)
        
        if players:
            content = json.loads(json.dumps({"players" : players_names}))
            return JSONResponse(content = content, status_code = 200)            
            
        else:
            content = f"El lobby {lobby_id} no tiene jugadores / No existe"
            return JSONResponse(content = content, status_code = 404)            
            
 

@router.delete("/lobbys/{lobby_id}")
async def delete_lobby(lobby_id: int) :
    with db_session:
        try:
            fetch_lobby = get_lobby(lobby_id)
            db_lobby[lobby_id].delete()
        except ObjectNotFound:
            message = "El lobby no existe"
            status_code = 404 # not found
            return JSONResponse(content=message, status_code=status_code)
    message = "lobby borrado!"
    status_code = 200 # no acceptable
    return JSONResponse(content=message, status_code=status_code)



def Buscar_Lobby(lobby_id : int):
    lobby = get_lobby(lobby_id)
    return {
  "lobby_id": lobby.lobby_id,
  "lobby_name": lobby.lobby_name,
  "lobby_max": lobby.lobby_max,
  "lobby_pcount": lobby.lobby_pcount
}

def database_to_list_lobby(lobby: db_lobby) -> ListedLobbys:
    return ListedLobbys(
    lobby_id=db_lobby.lobby_id,
    lobby_name=db_lobby.lobby_name,
    lobby_max=db_lobby.lobby_max,
    lobby_pcount=db_lobby.lobby_pcount,
)  # por si sirve

# @router.get("/lobbys/list")
# async def lista_lobbys() -> List[ListedLobbys]:
#     listed_lobby = []
#     with db_session:
#         lobbys = list(db_lobby.select(lambda p: p.lobby_id > 0))
#         for c in lobbys:
#             lobby_info = Buscar_Lobby(c.lobby_id)
#             listed_lobby.append(lobby_info)
#         return listed_lobby
