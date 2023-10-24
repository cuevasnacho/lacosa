from api.match.next_turn import next_player
from fastapi.testclient import TestClient
from main import app 
from pony.orm import db_session, commit
from db.database import Match as db_match
from db.database import Lobby as db_lobby
from db.database import Player as db_player
from definitions import match_status
import pytest


client = TestClient(app)
@db_session
def test_next_turn_ex1():
    the_match = db_match.get(lambda m: m.match_id == 1)

    response = client.get(
    "/partida/1/next",
    headers={"X-Token": "coneofsilence"},
    )

    assert response.status_code == 200
    assert response.json() == {"next_player" : 5} #hay 2 muertos al lado de el O_o

@db_session
def test_next_turn_ex2():
    the_match = db_match.get(lambda m: m.match_id == 1)
    the_match.match_currentP = 6
    commit()
    
    response = client.get(
    "/partida/1/next",
    headers={"X-Token": "coneofsilence"},
    )

    assert response.status_code == 200
    assert response.json() == {"next_player" : 1}

@db_session
def test_next_turn_ex3():
    the_match = db_match.get(lambda m: m.match_id == 1)
    the_match.match_direction = False
    the_match.match_currentP = 2
    commit()
    

    response = client.get(
    "/partida/1/next",
    headers={"X-Token": "coneofsilence"},
    )

    assert response.status_code == 200
    assert response.json() == {"next_player" : 1}

@db_session
def test_next_turn_ex4():
    the_match = db_match.get(lambda m: m.match_id == 1)
    the_match.match_currentP = 1
    commit()
    
    response = client.get(
    "/partida/1/next",
    headers={"X-Token": "coneofsilence"},
    )

    assert response.status_code == 200
    assert response.json() == {"next_player" : 6}
    


# para correr:
#1 borrar lacosa.sqlite
#2 compilar python3 database.py
#3 mover este archivo a lacosa/ y load match_env.py tambien
#4 correr python3 load_match_env.py
#4 correr pytest-3 test_create_delete_lobby.py
