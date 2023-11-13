from api.lobby.start_lobby import start_match 
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
from main import app 
import pytest
import os
import time
import subprocess

def set_env():
    database = "db/lacosa.sqlite"
    create_database_command = "python3 db/database.py"
    get_into_database = "sqlite3 db/lacosa.sqlite"
    file_entrys = "db/test_start_match.txt"
    if os.path.exists(database):
        os.remove(database)
        time.sleep(0.1)

    subprocess.run(create_database_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    time.sleep(0.1)

    with open(file_entrys, 'r') as file:
        for line in file:
            command = get_into_database + " " + line.strip() 
            print(command)
            subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            time.sleep(0.1)

client = TestClient(app)
@patch('api.lobby.start_lobby.start_match')
def test_start_match(mock_start_match):
    set_env()
    time.sleep(1)

    awnser = { 
        "message" : "Partida 2 iniciada",
        "status_code" : 200
    }
    
    mock_function = MagicMock()
    mock_function.start_match.return_value = awnser
    mock_start_match.return_value = mock_function

    response = client.put("partida/iniciar/1")
    assert response.status_code == awnser['status_code']
    
'''
como correr test:
    1.borrar lacosa.sqlite
    2.ejecutar python3 database.py en db/
    3.ingresar las entrys de test_start_match.txt a la base de datos lacosa.sqlite
    4.mover este archivo en la misma linea de main.app
    5.ejecutar pytest test_start_match.py
'''