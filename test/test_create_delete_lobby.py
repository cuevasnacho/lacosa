from api.lobby.lobby import Crear_Lobby, delete_lobby
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
from main import app 
from pony.orm import db_session
from db.database import Lobby as db_lobby
from db.database import Match as db_match
from db.database import Player
import pytest

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

client = TestClient(app)
@patch('api.lobby.lobby')
def test_create_delete_lobby(mock_create_lobby):
    set_env()
    response = client.post(
    "/lobbys",
    headers={"X-Token": "coneofsilence"},
    json={
  "player_id": 0, #el player no existe
  "lobby_name": "dunga",
  "lobby_max": 10,
  "lobby_min": 6,
  "lobby_password": "dunga"
},
    )
    assert response.status_code == 404
    assert response.json() == "Error creacion del lobby"


    response = client.post(
    "/lobbys",
    headers={"X-Token": "coneofsilence"},
    json={
  "player_id": 1, #el player existe
  "lobby_name": "dungaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
  "lobby_max": 10,
  "lobby_min": 6,
  "lobby_password": "dunga"
},
    )

    assert response.status_code == 406
    assert response.json() == "Nombre demasiado largo"


    response = client.post(
    "/lobbys",
    headers={"X-Token": "coneofsilence"},
    json={
  "player_id": 1, #el player existe
  "lobby_name": "dungaa",
  "lobby_max": 10,
  "lobby_min": 3,
  "lobby_password": "dunga"
},
    )

    assert response.status_code == 406
    assert response.json() == "Minimo de jugadores no permitido"

    response = client.post(
    "/lobbys",
    headers={"X-Token": "coneofsilence"},
    json={
  "player_id": 1, #el player existe
  "lobby_name": "dungaa",
  "lobby_max": 15,
  "lobby_min": 5,
  "lobby_password": "dunga"
},
    )

    assert response.status_code == 406
    assert response.json() == "Maximo de jugadores no permitido"

    response = client.post(
    "/lobbys",
    headers={"X-Token": "coneofsilence"},
    json={
  "player_id": 1, #el player existe
  "lobby_name": "dungaa",
  "lobby_max": 6,
  "lobby_min": 10,
  "lobby_password": "dunga"
},
    )

    assert response.status_code == 406
    assert response.json() == "Minimo y maximo de jugadores no permitido"

    add_player = client.post(
    "/players",
    headers={"X-Token": "coneofsilence"},
    json={"player_name" : "leo messi"},
    )

    response = client.post(
    "/lobbys",
    headers={"X-Token": "coneofsilence"},
    json={
  "player_id": 1, #el player existe en la db
  "lobby_name": "dungaa",
  "lobby_max": 11,
  "lobby_min": 6,
  "lobby_password": "dunga"
},
    )

    assert response.status_code == 200
    assert response.json() == {
        "lobby_id" : 2 #esta id siempre es par por que el primer test crea la entrada igual en la base de datos
    }
    
    with db_session:
        assert db_lobby.get(lobby_id = 2).lobby_name == "dungaa"
        assert db_lobby.get(lobby_id = 0) == None
        assert db_lobby.get(lobby_id = 2).lobby_player == {Player[1]}

    
    response = client.delete(
    "/players/1", #para borrar el player
    headers={"X-Token": "coneofsilence"})
    assert response.status_code == 200
    assert response.json() == "Jugador borrado!"

    response = client.delete(
    "/lobbys/0",
    headers={"X-Token": "coneofsilence"},
    )

    assert response.status_code == 404
    assert response.json() == "El lobby no existe"
    
    response = client.delete(
    "/lobbys/2",
    headers={"X-Token": "coneofsilence"},
    )

    assert response.status_code == 200
    assert response.json() == "lobby borrado!"


    with db_session:
      assert db_lobby.get(lobby_id = 2) == None



# para correr:
#1 borrar lacosa.sqlite
#2 compilar python3 database.py
#3 mover este archivo a lacosa/
#4 correr pytest-3 test_create_delete_lobby.py

    
