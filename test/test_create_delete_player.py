from api.player.player import Crear_Jugador, delete_player
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
from main import app 
from pony.orm import db_session, ObjectNotFound
from db.database import Player as db_player
import pytest

client = TestClient(app)
@patch('api.player.player')
def test_create_delete_player(mock_create_player):
    
    response = client.post(
    "/players",
    headers={"X-Token": "coneofsilence"},
    json={"player_name" : "leo messsssssssssssssssssssssssssssssssssssssssssssssssi"},
    )
    assert response.status_code == 406
    assert response.json() == "Nombre demasiado largo"


    
    response = client.post(
    "/players",
    headers={"X-Token": "coneofsilence"},
    json={"player_name" : "leo messi"},
    )
    assert response.status_code == 200
    assert response.json() == {
        "player_id" : 1, #esta id debe ser la proxima id que se autogenere, o se debe borrar la DB y poner 1
        "player_name": "leo messi"
    }

    with db_session:
        assert db_player.get(player_id = 1 ).player_name == "leo messi"
        assert db_player.get(player_id = 0) == None


    response = client.delete(
    "/players/0",
    headers={"X-Token": "coneofsilence"})
    assert response.status_code == 404
    assert response.json() == "El jugador no existe"

    response = client.delete(
    "/players/1", #mismo id que messi
    headers={"X-Token": "coneofsilence"})
    assert response.status_code == 200
    assert response.json() == "Jugador borrado!"

    with db_session:
        assert db_player.get(player_id = 1) == None

# para correr:
#1 borrar lacosa.sqlite
#2 compilar python3 database.py
#3 mover este archivo a lacosa/
#4 correr pytest-3 test_create_delete_player.py

    
