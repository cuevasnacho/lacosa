from pydantic import *
from fastapi import  APIRouter
from fastapi.responses import JSONResponse
from pony.orm import db_session, ObjectNotFound, commit
from db.database import Lobby, Player, Match


#en este modulo debo implementar el endpoint y la logica correspondiente para que un jugador tenga la posibilidad
#de abandonar un lobby. Si el jugador es el host, y no hay otro jugador en el lobby, se elimina el lobby, y el match asociado.

router = APIRouter()

#obtener el lobby
@db_session()
def get_lobby(lobby_id):
    return Lobby[lobby_id]

@db_session()
def get_player(player_id):
    return Player[player_id]

#funcion para obtener el match del lobby
@db_session()
def get_match_id(lobby_id):
    lobby = get_lobby(lobby_id)
    match = Match.select(lambda match: match.match_id == lobby.lobby_match.match_id).first()
    return match

#funcion para obtener el host del lobby
@db_session()
def get_host(lobby_id):
    for player in Lobby.lobby_player:
        if player.player_isHost:
            return player
    return None

@db_session()
def lobby_update(lobby_id):
    lobby = get_lobby(lobby_id)
    lobby.lobby_pcount = lobby.lobby_pcount - 1
    commit()

@db_session()
def player_update(player_id):
    player = Player[player_id]
    player.player_ingame = False
    player.player_isHost = False
    player.player_lobby = None
    player.player_current_match_id = None
    commit()


#funcion para hacer una lista con el id de los jugadores del lobby
@db_session()
def get_new_host_players_id(lobby_id):
    lobby = get_lobby(lobby_id)
    players = Player.select(lambda player : player.player_lobby.lobby_id == lobby_id)
    players_id = []
    for player in players:
        players_id.append(player.player_id)
        players_id.sort()
    return players_id[0]

@db_session
def delete_entry(entry1,entry2):
    entry1.delete()
    entry2.delete()
    commit()

@db_session
def set_new_host(player_id):
    player = Player[player_id]
    player.player_isHost = True
    commit()

@router.post("/lobbys/{lobby_id}/{player_id}")
async def leave_Lobby(lobby_id : int, player_id : int):
    try:
        lobby = get_lobby(lobby_id)
        player = get_player(player_id)
    except ObjectNotFound:
        message = "El objeto no existe"
        status_code = 404 # not found
        return JSONResponse(content = message, status_code = status_code)

    if not player.player_isHost: 
        lobby_update(lobby_id)
        player_update(player_id)

    #si es host y no hay otro jugador, se elimina el lobby y el match asociado.
    elif player.player_isHost and lobby.lobby_pcount == 1:
        #actualizamos al jugador
        #player_name = Player[player_id].player_name
        player_update(player_id)
        match = get_match_id(lobby_id)
        #borramos match y lobby
        delete_entry(lobby,match)
              
    else: 
        player_update(player_id)
        new_host_id = get_new_host_players_id(lobby_id)
        print(f"newgostttttt {new_host_id}")
        set_new_host(new_host_id)