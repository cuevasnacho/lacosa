from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from main import app
import json 

# from api.lobby import request_join
#from db.database import Lobby, Player, Match #cómo sería esto?

#test un jugador se quiere unir a un lobby que ya está lleno
def test_unirse_lobby_lobby_lleno():
    # Configurar un mock de Player para un jugador que no está en juego
    player_mock = MagicMock()
    player_mock.player_id = 2  # Simula que el jugador tiene id 2.
    player_mock.player_ingame = False  # Simula que el jugador no está en juego.

    # Configurar un mock de Lobby para un lobby lleno
    lobby_mock = MagicMock()
    lobby_mock.lobby_id = 1  # Simula que el lobby tiene id 1
    lobby_mock.lobby_max = 4  # El máximo permitido en el lobby es 4.
    lobby_mock.lobby_pcount = 4  # Simula que el lobby ya tiene 4 jugadores.

    # Configurar un mock de get_lobby para devolver el mock de Lobby
    with patch("api.lobby.request_join.get_lobby", return_value = lobby_mock):
        client = TestClient(app)  # Creamos el objeto TestClient
        response = client.put("/lobbys/1/2")

        # Verificar que la respuesta sea un error indicando que el lobby está lleno
        assert response.status_code == 406
        assert json.loads(response.content) == "El lobby esta lleno"

def test_unirse_lobby_inexistente():
    # Configurar un mock de Player para un jugador que no está en juego
    player_mock = MagicMock()
    player_mock.player_id = 2  # Simula que el jugador tiene id 2.
    player_mock.player_ingame = False  # Simula que el jugador no está en juego.

    # Configurar un mock de Lobby para un lobby lleno
    lobby_mock = MagicMock()
    lobby_mock.lobby_id = 1  # Simula que el lobby tiene id 1
    lobby_mock.lobby_max = 4  # El máximo permitido en el lobby es 4.
    lobby_mock.lobby_pcount = 6 # es un lobby que tiene espacio pero en realidad no existe
    # Configurar un mock de get_lobby para devolver el mock de Lobby  
    with patch("api.lobby.request_join.player_update"),\
        patch("api.lobby.request_join.lobby_update"):
        client = TestClient(app)  # Creamos el objeto TestClient
        response = client.put("/lobbys/1/2")

        # Verificar que la respuesta sea un error indicando que el lobby está lleno
        assert response.status_code == 404
        assert json.loads(response.content) == "El objeto no existe"
