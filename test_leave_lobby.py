#import pytest
from unittest.mock import MagicMock, patch
from api.lobby.leave_lobby import leave_Lobby, lobby_update, player_update
from fastapi.testclient import TestClient
from main import app
import json
from pony.orm import *
from api.lobby import leave_lobby
# from db.database import Lobby, Player, Match #cómo sería esto?

#Un jugador que no es host abandona la partida
def test_abandona_uno_que_no_es_host():
    #mock de lobby
    lobby_mock = MagicMock()
    lobby_mock.id = 1
    lobby_mock.name = "lobby1"
    lobby_mock.pcount = 2

    #mock de player que abandona
    player_mock = MagicMock()
    player_mock.id = 1
    player_mock.name = "player1"
    player_mock.host = False
    player_mock.lobby = 1
    player_mock.match = 1
    
    #mock de match
    #match_mock = MagicMock()
    #match_mock.id = 1
    #match_mock.lobby = 1
    #match_mock.status = 0

    with patch("api.lobby.leave_lobby.get_lobby_id", return_value = lobby_mock):
        client = TestClient(app)  # Creamos el objeto TestClient
        response = client.put("/lobbys/1/2")

        # Verificar que la respuesta sea un error indicando que el lobby está lleno
        assert response.status_code == 406
        assert json.loads(response.content) == "jugador {player_id} abandonaste el lobby {lobby_id}"