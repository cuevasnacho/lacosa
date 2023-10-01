from pydantic import *
from enum import Enum
from typing import Optional, List, Any
from api.models.user import PlayerIn , get_jugador
from fastapi import FastAPI, HTTPException, APIRouter, Query, status
from fastapi.responses import JSONResponse
from pony.orm import db_session, commit , ObjectNotFound
from pony.orm import Set, select
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
    player_id : int
    lobby_name : str
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




@router.post("/lobbys/", status_code=status.HTTP_201_CREATED)
async def Crear_Lobby(new_lobby: CreateLobby) -> CreateLobbyOut:
    if len(new_lobby.lobby_name)>20:
        message = "Nombe demasiado largo"
        status_code = 406 # no acceptable
        return JSONResponse(content=message, status_code=status_code)
    if new_lobby.lobby_max>12:
        message = "Maximo de players no permitido"
        status_code = 406 # no acceptable
        return JSONResponse(content=message, status_code=status_code)
    if new_lobby.lobby_min<5: #DECISION DE DISEÑO
        message = "Minimo de players no permitido"
        status_code = 406 # no acceptable
        return JSONResponse(content=message, status_code=status_code)
    if new_lobby.lobby_min > new_lobby.lobby_max:
        message = "Minimo y maximo de players no permitido"
        status_code = 406 # no acceptable
        return JSONResponse(content=message, status_code=status_code)

    with db_session:
        host = get_jugador(new_lobby.player_id)
        new_lobby = db_lobby(lobby_name = new_lobby.lobby_name, lobby_max = new_lobby.lobby_max,lobby_min = new_lobby.lobby_min,
        lobby_password= new_lobby.lobby_password, lobby_pcount = 1)
        new_lobby.lobby_player.add(host)
    return CreateLobbyOut(lobby_id=new_lobby.lobby_id)


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