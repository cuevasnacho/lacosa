from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from main import app
import json

def test_abandonar_lobby_except():
    #Configurar un mock de player
    player_mock = MagicMock()
    player_mock.player_id = 3

    lobby_mock = MagicMock()
    lobby_mock.lobby_id = 5

    match_mock = MagicMock()
    match_mock.match_id = 1
    match_mock.match_lobby = 2

    with patch("api.lobby.leave_lobby.get_player", return_value = player_mock):
        client = TestClient(app)
        response = client.put("/lobbys/2/2")

        assert response.status_code == 404
        assert json.loads(response.content) == "El objeto no existe"

"""
def test_abandonar_lobby_try():

    #Configurar un mock de lobby
    lobby_mock = MagicMock()
    lobby_mock.lobby_id = 2
    lobby_mock.lobby_pcount = 4
    lobby_mock.lobby_min = 4
    lobby_mock.lobby_max = 4

    #Configurar un mock de player
    player_mock1 = MagicMock()
    player_mock1.player_id = 2
    player_mock1.player_ishost = True
    player_mock1.player_lobby = 2

    player_mock2 = MagicMock()
    player_mock2.player_id = 3
    player_mock2.player_ishost = False
    player_mock2.player_lobby = 2

    player_mock3 = MagicMock()
    player_mock3.player_id = 4
    player_mock3.player_ishost = False
    player_mock3.player_lobby = 2

    player_mock4 = MagicMock()
    player_mock4.player_id = 5
    player_mock4.player_ishost = False
    player_mock4.player_lobby = 2

    match_mock = MagicMock()
    match_mock.match_id = 1
    match_mock.match_lobby = 2

    with patch("api.lobby.leave_lobby.get_player", return_value = player_mock1),\
        patch("api.lobby.leave_lobby.get_match_id", return_value = match_mock.match_id),\
        patch("api.lobby.leave_lobby.get_lobby", return_value = lobby_mock),\
        patch("api.lobby.leave_lobby.get_lobby_players", return_value = [player_mock1, player_mock2, player_mock3, player_mock4]),\
        patch("api.lobby.leave_lobby.player_update"),\
        patch("api.lobby.leave_lobby.lobby_update"):

        client = TestClient(app)

        response = client.post("/lobbys/2/2")
        #lobbys/{lobby_id}/{player_id}
        assert response.json() == "El host ha abandonado el lobby"
        assert response.status_code == 200

"""