import pytest
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from api.lobby.leave_lobby import abandonar_lobby
from main import app
import json


lobby_mock = MagicMock()
lobby_mock.lobby_id = 1  # Simula que el lobby tiene id 1

player_mock = MagicMock()
player_mock.player_id = 2  # Simula que el jugador tiene id 2.
player_mock.player_isHost = True  # Simula que el jugador es el host.
player_mock.player_lobby = 1  # Simula que el jugador está en el lobby 1.

# Test cuando el host está solo y abandona el lobby
#@patch.object(abandonar_lobby, 'get_player', return_value=player_mock)
@patch.object(abandonar_lobby, 'get_player', MagicMock(return_value=player_mock))
def test_leave_lobby_host_no_players(player_mock):
    # Configurar un mock de Lobby para un lobby con el host como único jugador
    # lobby_mock = MagicMock()
    # lobby_mock.lobby_id = 1  # Simula que el lobby tiene id 1
    # lobby_mock.lobby_pcount = 1  # Un solo jugador en el lobby

    # Configurar un mock de Player para un jugador que es el host y no hay otros jugadores

    # Configurar un mock de get_lobby y get_player para devolver los mocks de Lobby y Player
    with patch("api.lobby.leave_lobby.get_lobby", return_value=lobby_mock):
        client = TestClient(app)
        response = client.post("/lobbys/1/2")

        # Verificar que la respuesta sea exitosa y que el lobby y el match se hayan eliminado
        assert response.status_code == 404
        assert json.loads(response.content) == "Jugador 2 ha abandonado el lobby y se ha eliminado el lobby"

#------------------------------------------------------------------------------------------------------------------#

'''
# Test cuando un jugador que no es host abandona el lobby
def test_leave_lobby_non_host():
    # Configurar un mock de Lobby para un lobby válido
    # lobby_mock = MagicMock()
    # lobby_mock.lobby_id = 1  # Simula que el lobby tiene id 1

    # Configurar un mock de Player para un jugador que no es el host
    player_mock = MagicMock()
    player_mock.player_id = 2  # Simula que el jugador tiene id 2.
    player_mock.player_isHost = False  # Simula que el jugador no es el host.
    player_mock.player_lobby = 1  # Simula que el jugador está en el lobby 1.

    # Configurar un mock de get_lobby y get_player para devolver los mocks de Lobby y Player
    with patch("api.lobby.leave_lobby.get_lobby", return_value=lobby_mock), \
         patch("api.lobby.leave_lobby.get_player", return_value=player_mock):
        client = TestClient(app)
        response = client.post("/lobbys/1/2")

        # Verificar que la respuesta sea exitosa y que el jugador haya abandonado el lobby
        assert response.status_code == 200
        assert json.loads(response.content) == "Jugador 2 ha abandonado el lobby"

#------------------------------------------------------------------------------------------------------------------#

# Test cuando el host abandona y le tiene que pasar el host a otro jugador
def test_leave_lobby_host_with_players():
    # Configurar un mock de Lobby para un lobby con el host y otro jugador
    # lobby_mock = MagicMock()
    # lobby_mock.lobby_id = 1  # Simula que el lobby tiene id 1
    # lobby_mock.lobby_pcount = 2  # Dos jugadores en el lobby

    # Configurar un mock de Player para un jugador que es el host
    host_mock = MagicMock()
    host_mock.player_id = 2  # Simula que el jugador es el host.
    host_mock.player_isHost = True
    host_mock.player_lobby = 1  # Simula que el jugador está en el lobby 1.

    # Configurar un mock de Player para un jugador que no es el host
    player_mock = MagicMock()
    player_mock.player_id = 3  # Simula otro jugador que no es el host.
    player_mock.player_isHost = False
    player_mock.player_lobby = 1  # Simula que el jugador está en el lobby 1.

    # Configurar un mock de get_lobby, get_host, y get_new_host_players_id
    # para devolver los mocks de Lobby y jugadores relevantes
    with patch("api.lobby.leave_lobby.get_lobby", return_value=lobby_mock), \
         patch("api.lobby.leave_lobby.get_host", return_value=host_mock), \
         patch("api.lobby.leave_lobby.get_new_host_players_id", return_value=3):
        client = TestClient(app)
        response = client.post("/lobbys/1/2") #lobby_id/player_id

        #ver que la respuesta sea correcta y que el jugador se haya convertido en el nuevo host
        assert response.status_code == 200
        assert json.loads(response.content) == "El jugador host 2 ha abandonado el lobby y el nuevo host es 3"
'''

