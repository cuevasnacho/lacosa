from api.match.next_turn import next_player
from fastapi.testclient import TestClient
from main import app 
from pony.orm import db_session, commit
from db.database import Match as db_match
from db.database import Lobby as db_lobby
from db.database import Player as db_player
from definitions import match_status
import pytest
from load_match_env import load_match_enviroment


client = TestClient(app)
load_match_enviroment()

def set_env():
    database = "db/lacosa.sqlite"
    create_database_command = "python3 db/database.py"
    get_into_database = "sqlite3 db/lacosa.sqlite"
    file_entrys = "db/test_check_defense.txt"
    if os.path.exists(database):
        os.remove(database)
        time.sleep(0.1)

    subprocess.run(create_database_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    time.sleep(0.1)

@db_session
def test_next_turn_ex1():
    set_env()
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
