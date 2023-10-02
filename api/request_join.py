from pydantic import *
from api.models.user import get_jugador
from fastapi import  APIRouter
from fastapi.responses import JSONResponse
from pony.orm import db_session, ObjectNotFound, commit
from db.database import Lobby as db_lobby
from db.database import Player as db_player

# debo hacer un endpoint para ingresar a una partida
#verificar que la partida no este llena
#verificar que el estado del usuario permita unirse a la partida
#verificar que el usuario no este ya en la partida
#si todo esta ok, se agrega el usuario a la partida
#deberia usar 2 db session, una para player y una para lobby
#hacer un lobby_pcount + 1
#hacer un player_ingame = True
#obtener el id del match al que se unio
#hacer un match_currentP + 1
#primero debo verificar si la partida existe
#PONER QUE EL JUGADOR NO SEA HOST, PONER IS_HOST DE TRUE A FALSE
#para modificar una instancia de player

router = APIRouter()

def player_in_lobby(player_id : int):
    player_info = db_player[player_id]
    return {"player_name": player_info.player_name, "player_isHost": player_info.player_isHost}

#verifico si la partida existe:

@db_session()
def get_lobby(lobby_id):
    return db_lobby[lobby_id]

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
        player_get = db_player[player_id]
        lobby_get = db_lobby[lobby_id]

        player_get.player_ingame = True
        player_get.player_isHost = False
        lobby_get.lobby_pcount = lobby_get.lobby_pcount + 1
        player_get.player_lobby = lobby_id
        commit()
    return JSONResponse(content=f"jugador {player_id} estas en la partida {lobby_id}", status_code=200)
#en db_session, vez de hacer un db_player, tomo el id del jugador y modifico los campos que quiero
