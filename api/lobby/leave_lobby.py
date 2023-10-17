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
def get_lobby_id(lobby_id):
    return Lobby[lobby_id]

#funcion para obtener el match del lobby
@db_session
def get_match_id(lobby_id):
    lobby = get_lobby_id(lobby_id)
    match = Match.select(lambda match: match.match_id == lobby.lobby_match.match_id).first()
    return match

#funcion para obtener el host del lobby
@db_session
def get_host(lobby_id):
    for player in Lobby.lobby_player:
        if player.player_isHost:
            return player
    return None

@db_session
def lobby_update(lobby_id):
    lobby = get_lobby_id(lobby_id)
    lobby.lobby_pcount = lobby.lobby_pcount - 1

@db_session
def player_update(player_id):
    player = Player[player_id]
    player.player_ingame = False
    player.player_isHost = False
    player.player_lobby = None
    player.player_current_match_id = None


#funcion para hacer una lista con el id de los jugadores del lobby
@db_session
def get_players_id(lobby_id):
    lobby = get_lobby_id(lobby_id)
    players_id = []
    for player in lobby.lobby_player:
        players_id.append(player.player_id)
        players_id.sort()
    return players_id

@router.post("/lobbys/{lobby_id}/{player_id}")
async def leave_Lobby(lobby_id : int, player_id : int):
    try:
        lobby = get_lobby_id(lobby_id)
    except ObjectNotFound:
        message = "El objeto no existe"
        status_code = 404 # not found
        return JSONResponse(content = message, status_code = status_code)

    #Si el jugador NO es el host, se lo elimina del lobby, y se actualiza el estado de ese lobby y de ese jugador.
    if not Player.player_isHost:
        with db_session:
            #player_name = Player[player_id].player_name
            lobby.lobby_player.remove(player_id) #remove es una función set de pony
            lobby_update(lobby_id)
            commit()
    else:
        with db_session:
            #Si el jugador es el host, (y ademas hay otro jugador en el lobby aparte del host), abandona la partida, y se le transfiere el host a otro jugador.
            if Player.player_isHost and lobby.lobby_pcount > 1:
                #removemos al host de la partida
                #player_name = Player[player_id].player_name
                lobby.lobby_player.remove(Player.player_id)
                #tengo que obtener el jugador con el id mas chico y hacerlo host (criterio de seleccion para el nuevo host, dudas con esto)
                players_id = get_players_id(lobby_id)
                new_host_id = players_id[0]
                new_host = Player.new_host_id
                new_host.player_isHost = True
                lobby_update(lobby_id)
                commit()
            #si es host y no hay otro jugador, se elimina el lobby y el match asociado.
            if Player.player_isHost and lobby.lobby_pcount == 1:
                #actualizamos al jugador
                #player_name = Player[player_id].player_name
                player_update(player_id)
                #borramos el lobby
                lobby.delete()
                #borramos el match
                match = get_match_id(lobby_id)
                match.delete()
                commit()
    return JSONResponse(content=f"jugador {player_id} abandonaste el lobby {lobby_id}", status_code=200)
