from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pony.orm import db_session
from db.database import Player
from api.websocket import ConnectionManager
from definitions import player_roles

router = APIRouter()

manager = ConnectionManager()

@db_session
def get_players(match_id):
    return Player.select(lambda player : player.player_current_match_id.match_id == match_id)

@db_session
def get_lacosa(match_id):
    return Player.select(lambda player : player.player_current_match_id.match_id == match_id 
                           and player.player_role == player_roles.THE_THING.value).first()
    
@db_session
def get_number_players(match_id):
    players =  Player.select(lambda player : player.player_current_match_id.match_id == match_id)
    count = 0 
    for i in players:
        count += 1
    return count 

@router.get("/partida/resultado/{match_id}")
@db_session
def match_result(match_id : int):
    players = get_players(match_id)
    lacosa = get_lacosa(match_id)
    number_players = get_number_players(match_id)
    winners = []
    
    (winners.append(lacosa.player_name)) if not lacosa.player_dead else winners
   
    for player in players:
        if lacosa.player_dead:
            #si la cosa esta muerta -> ganan los humanos y devuevlo a los vivos
            if player.player_role == player_roles.HUMAN.value and not player.player_dead:
                winners.append(player.player_name)
                winner_team = "Humanos"
        else:
            #si la cosa esta viva -> gana la cosa y los infectados
            if player.player_role == player_roles.INFECTED.value and not player.player_dead:
                winners.append(player.player_name)
                winner_team = "La cosa e infectados"
    
    #caso en el que la cosa contagia a todos y gana sola
    if len(winners) == number_players:
        winners = [lacosa.player_name]
        winner_team = "La cosa"
        
    winner_team = "Humanos" if lacosa.player_dead else ("La cosa" if len(winners) == 1 else "La cosa e infectados")
    response = {'jugadores' : winners, 'ganadores' : winner_team}
    
    return JSONResponse(content = response, status_code = 200)