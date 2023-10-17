from pydantic import *
from fastapi import  APIRouter
from fastapi.responses import JSONResponse
from pony.orm import db_session, ObjectNotFound, commit
from db.database import Lobby, Player, Match

router = APIRouter()

@db_session()
def get_lobby(lobby_id):
    return Lobby[lobby_id]

@db_session
def player_update(player_id,lobby_id,match_id):
    player_get = Player[player_id]
    player_get.player_ingame = True
    player_get.player_isHost = False
    player_get.player_lobby = lobby_id
    player_get.player_current_match_id = match_id

@db_session
def lobby_update(lobby_id,match_id):
    lobby_get = Lobby[lobby_id]
    lobby_get.lobby_pcount = lobby_get.lobby_pcount + 1
    lobby_get.lobby_match = match_id

@db_session
def get_match_id(lobby_id):
    lobby = get_lobby(lobby_id)
    match = Match.select(lambda match: match.match_id == lobby.lobby_match.match_id).first()
    return match

@router.put("/lobbys/{lobby_id}/{player_id}")
async def unirse_lobby(lobby_id : int, player_id : int):
    try:
        lobby = get_lobby(lobby_id)
    except ObjectNotFound:
        message = "El objeto no existe"
        status_code = 404 # not found
        return JSONResponse(content = message, status_code = status_code)

    if lobby.lobby_pcount + 1 > lobby.lobby_max:
        message = "El lobby esta lleno"
        status_code = 406
        return JSONResponse(content=message, status_code=status_code)
    
    with db_session:
        #cambiar esto del jugador
        match_id = get_match_id(lobby_id)
        player_update(player_id,lobby_id,match_id)

        #cambiar estado lobby
        lobby_update(lobby_id, match_id)
        commit()
    return JSONResponse(content=f"jugador {player_id} estas en la partida {lobby_id}", status_code=200)
#en db_session, vez de hacer un db_player, tomo el id del jugador y modifico los campos que quiero
