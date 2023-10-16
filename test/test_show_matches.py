from api.lobby.show_lobbys import show_matches
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
from main import app 
import pytest

client = TestClient(app)

matches = [
  {
    "lobby_id": 1,
    "match_id": 1,
    "lobby_name": "l1",
    "number_of_players": 1,
    "host_name": "nacho",
    "max_players": 6,
    "min_players": 5
  },
  {
    "lobby_id": 2,
    "match_id": 2,
    "lobby_name": "l1",
    "number_of_players": 1,
    "host_name": "descarte",
    "max_players": 6,
    "min_players": 5
  },
  {
    "lobby_id": 5,
    "match_id": 7,
    "lobby_name": "l1",
    "number_of_players": 1,
    "host_name": "tomas",
    "max_players": 6,
    "min_players": 5
  }
]

@patch('api.show_matches.show_matches')
def test_discard_card(mock_show_matches):
    

    mock_function = MagicMock()
    mock_function.get_not_initialized_matches.return_value = matches
    mock_show_matches.return_value = mock_function

    response = client.get("/partidas/listar")
    assert response.status_code == 200
    assert response.json() == matches


'''
como correr test:
    1.borrar lacosa.sqlite
    2.ejecutar python3 database.py en db/
    3.ingresar las entrys de test_show_entrys.txt a la base de datos lacosa.sqlite
    4.mover este archivo en la misma linea de main.app
    5.ejecutar pytest test_show_matches.py
'''