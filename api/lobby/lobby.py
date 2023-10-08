from pydantic import *
from typing import Optional
from api.player.player import get_jugador
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pony.orm import db_session, commit ,ObjectNotFound
from definitions import match_status
from db.database import Lobby as db_lobby
from db.database import Match as db_match
from db.database import Player as db_player
from definitions import match_status
import json 

router = APIRouter()

class CreateLobby(BaseModel):
    player_id : int
    lobby_name : str
    lobby_max : int
    lobby_min : int
    lobby_password : Optional[str] = None

@router.post("/lobbys")
async def Crear_Lobby(new_lobby: CreateLobby):
    if len(new_lobby.lobby_name)>20:
        message = "Nombre demasiado largo"
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
            lobby_new = db_lobby(lobby_name = new_lobby.lobby_name, lobby_max = new_lobby.lobby_max, lobby_min = new_lobby.lobby_min,
                                lobby_password = password, lobby_pcount = 1, lobby_match = new_match.match_id)
            commit()
            player = db_player.get(lambda player : player.player_id == new_lobby.player_id)
            player.player_ingame = True
            player.player_dead = False
            player.player_isHost = True
            player.player_lobby = lobby_new
            player.player_current_match_id = new_match
            commit()

        content = {"lobby_id" : lobby_new.lobby_id}
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
            
#para que sea consistene faltaria borrar match
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
