from api.lobby.start_lobby import start_match 
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
from main import app 
import pytest

client = TestClient(app)
@patch('api.start_match.start_match')
def test_start_match(mock_start_match):
    
    awnser = { 
        "message" : "Partida 2 iniciada",
        "status_code" : 200
    }
    
    mock_function = MagicMock()
    mock_function.start_match.return_value = awnser
    mock_start_match.return_value = mock_function

    response = client.put("partida/iniciar/2")
    assert response.status_code == awnser['status_code']
    
'''
como correr test:
    1.borrar lacosa.sqlite
    2.ejecutar python3 database.py en db/
    3.ingresar las entrys de test_start_match.txt a la base de datos lacosa.sqlite
    4.mover este archivo en la misma linea de main.app
    5.ejecutar pytest test_start_match.py
'''