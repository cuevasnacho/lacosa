from pydantic import *
from fastapi import  APIRouter
from fastapi.responses import JSONResponse
from pony.orm import db_session, ObjectNotFound, commit
from db.database import Lobby, Player, Match
import json

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
def get_match(lobby_id):
    lobby = get_lobby(lobby_id)
    match = Match.select(lambda match: match.match_id == lobby.lobby_match.match_id).first()
    return match

#obtener los jugadores del lobby
@db_session()
def get_lobby_players(lobby_id):
    lobby = get_lobby(lobby_id)
    players = []
    for player in lobby.lobby_player:
        players.append(player)
    return players

#funcion para obtener el host del lobby
@db_session()
def get_host(lobby_id):
    for player in get_lobby_players(lobby_id):
        print(f'{player.player_id} get_host leave_lobby.py')
        if player.player_isHost:
            return player.player_id

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

@db_session()
def get_new_host_players_id(lobby_id):
    players = Player.select(lambda player: player.player_lobby.lobby_id == lobby_id)
    if not players:
        return None
    new_host_id = min(players, key=lambda player: player.player_id).player_id
    return new_host_id

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
async def abandonar_lobby(lobby_id : int, player_id : int):
    try:
        lobby = get_lobby(lobby_id)
        player = get_player(player_id)
    except ObjectNotFound:
        message = "El objeto no existe"
        status_code = 404 # not found
        return JSONResponse(content = message, status_code = status_code)
    
    if player.player_isHost:
        players_in_lobby = get_lobby_players(lobby_id)
        for player in players_in_lobby:
            player_update(player.player_id)
        delete_entry(lobby, get_match(lobby_id))
    else:
        lobby_update(lobby_id)
        player_update(player_id)
        return JSONResponse(content = f"Jugador {player_id} salio del lobby", status_code=200)
