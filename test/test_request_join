# import pytest
from unittest.mock import MagicMock, patch
from api.lobby.request_join import unirse_lobby, lobby_upadte, player_update
from fastapi.testclient import TestClient
from main import app
import json 
from pony.orm import ObjectNotFound
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
        patch("api.lobby.request_join.lobby_upadte"):
        client = TestClient(app)  # Creamos el objeto TestClient
        response = client.put("/lobbys/2/2")

        # Verificar que la respuesta sea un error indicando que el lobby está lleno
        assert response.status_code == 404
        assert json.loads(response.content) == "El objeto no existe"


'''
#test un jugador se quiere unir a un lobby pero ya está en uno
async def test_unirse_lobby_jugador_ya_unido():
    # Configurar un mock de Player para un jugador que ya está en juego
    player_mock = MagicMock()
    player_mock.player_id = 2  # Simula que el jugador tiene id 2.
    player_mock.player_ingame = True  # Simula que el jugador ya está en juego.

    # Configurar un mock de Lobby para un jugador ya unido
    lobby_mock = MagicMock()
    lobby_mock.lobby_id = 1  # Simula que el lobby tiene id 1
    lobby_mock.lobby_players = [player_mock]  # Simula que el jugador ya está unido al lobby.

    # Configurar un mock de get_lobby para devolver el mock de Lobby
    with patch("api.lobby.request_join.get_lobby", return_value = lobby_mock):
        client = TestClient(app)  # Creamos el objeto TestClient
        response = client.put("/lobbys/1/2")

        # Verificar que la respuesta sea un error indicando que el jugador ya está unido al lobby
        assert response.status_code == 409
        assert response.content == 'El jugador ya está unido al lobby'


#test unirse a un lobby que , o un lobby que ya empezó la partida
def test_unirse_lobby_lobby_en_juego():
    # Configurar un mock de Player para un jugador que no está en juego

    # Configurar un mock de Lobby para un lobby en juego
    lobby_mock = MagicMock()
    lobby_mock.lobby_match = 1  # Simula que el lobby ya está en juego.
    lobby_mock.lobby_match.match_status = 2  # Simula que el lobby ya está en juego.

    # Configurar un mock de get_lobby para devolver el mock de Lobby
    with patch("api.lobby.request_join.get_lobby", return_value = lobby_mock):
        response = unirse_lobby(1, 2)
        # Verificar que la respuesta sea un error indicando que el lobby está en juego
        assert response.status_code == 409
        assert response.content == "El lobby está en juego"

#test un jugador que es host se quiere unir a una partida
'''
