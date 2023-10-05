from api.player.discard_card import discard_card  # Replace with the actual function to be tested
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
from main import app 
import pytest

client = TestClient(app)
@patch('api.discard_card.discard_card')
def test_discard_card(mock_discard_card):
    
    awnser = { 
        "message" : "Carta descartada",
        "status_code" : 200
    }
    
    mock_function = MagicMock()
    mock_function.discard_card.return_value = awnser
    mock_discard_card.return_value = mock_function

    response = client.put("carta/descartar/2/0")
    assert response.status_code == awnser['status_code']
    
'''
como correr test:
    1.borrar lacosa.sqlite
    2.ejecutar python3 database.py en db/
    3.ingresar las entrys de example_entrys.txt a la base de datos lacosa.sqlite
    4.mover este archivo en la misma linea de main.app
    5.ejecutar pytest test_discard_card.py
'''