import pytest
from unittest.mock import MagicMock
from unittest.mock import patch
from api.lobby.request_join import unirse_lobby


def test_unirse_lobby_lobby_lleno():
    # Mock del método get_lobby() para devolver un lobby lleno.
    lobby = MagicMock()
    lobby.lobby_pcount = 10
    with patch("request_join.get_lobby", return_value=lobby):
        # Ejecuta la función unirse_lobby() con un lobby lleno.
        response = unirse_lobby(1, 2)

        # Verifica que la respuesta sea un error indicando que el lobby está lleno.
        assert response.status_code == 406
        assert response.content == "El lobby está lleno"




def test_unirse_lobby_lobby_ya_unido():
    # Mock del método get_lobby() para devolver un lobby al que el jugador ya está unido.
    lobby = MagicMock()
    lobby.lobby_pcount = 1
    with patch("request_join.get_lobby", return_value=lobby):
        # Ejecuta la función unirse_lobby() con un lobby al que el jugador ya está unido.
        response = unirse_lobby(1, 2)

        # Verifica que la respuesta sea un error indicando que el jugador ya está unido al lobby.
        assert response.status_code == 409
        assert response.content == "El jugador ya está unido al lobby"


def test_unirse_lobby_lobby_espectador():
    # Mock del método get_lobby() para devolver un lobby al que el jugador puede unirse como espectador.
    lobby = MagicMock()
    lobby.lobby_pcount = 1
    with patch("request_join.get_lobby", return_value=lobby):
        # Ejecuta la función unirse_lobby() con un lobby al que el jugador puede unirse como espectador.
        response = unirse_lobby(1, 2, espectador=True)

        # Verifica que la respuesta sea correcta.
        assert response.status_code == 200
        assert response.content == "jugador 2 estas en la partida 1 como espectador"


def test_unirse_lobby_lobby_en_juego():
    # Mock del método get_lobby() para devolver un lobby que está en juego.
    lobby = MagicMock()
    lobby.lobby_match = 1
    with patch("request_join.get_lobby", return_value=lobby):
        # Ejecuta la función unirse_lobby() con un lobby que está en juego.
        response = unirse_lobby(1, 2)

        # Verifica que la respuesta sea un error indicando que el lobby está en juego.
        assert response.status_code == 409
        assert response.content == "El lobby está en juego"
