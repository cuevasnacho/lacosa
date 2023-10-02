from api.play_card import play_card 
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
from main import app 
import pytest

client = TestClient(app)
@patch('api.play_card.play_card')
def test_play_card(mock_play_card):
    
    awnser = { 
        "message" : "El jugador 1 aplico efecto sobre 2",
        "status_code" : 200
    }
    
    mock_function = MagicMock()
    mock_function.play_card.return_value = awnser
    mock_play_card.return_value = mock_function

    response = client.put("carta/jugar/1/1/2")
    assert response.status_code == awnser['status_code']
    
'''
como correr test:
    1.borrar lacosa.sqlite
    2.ejecutar python3 database.py en db/
    3.ingresar las entrys de test_play_card.txt a la base de datos lacosa.sqlite
    4.mover este archivo en la misma linea de main.app
    5.ejecutar pytest test_play_card.py
'''