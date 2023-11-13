from api.player.discard_card import discard_card  
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
from main import app 
import os 
import time 
import subprocess

def set_env():
    database = "db/lacosa.sqlite"
    create_database_command = "python3 db/database.py"
    get_into_database = "sqlite3 db/lacosa.sqlite"
    file_entrys = "db/test_discard_card.txt"
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
@patch('api.player.discard_card.discard_card')
def test_discard_card(mock_discard_card):
    set_env()
    time.sleep(1)
    awnser = { 
        "message" : "Carta descartada",
        "status_code" : 200
    }
    
    mock_function = MagicMock()
    mock_function.discard_card.return_value = awnser
    mock_discard_card.return_value = mock_function

    response = client.put("carta/descartar/2/1")
    assert response.status_code == awnser['status_code']
    
'''
como correr test:
    1.mover este archivo en la misma linea de main.app
    2.ejecutar pytest test_discard_card.py
'''