import pytest
from unittest.mock import MagicMock
from unittest.mock import patch
from fastapi.testclient import TestClient
from main import app 
from pony.orm import db_session
from definitions import card_position
import json 
import os 
import subprocess
import time 
from db.database import Player, Card

def set_env():
    database = "db/lacosa.sqlite"
    create_database_command = "python3 db/database.py"
    get_into_database = "sqlite3 db/lacosa.sqlite"
    file_entrys = "db/steal_card_entrys/No_CardsInMatch.txt"
    if os.path.exists(database):
        os.remove(database)
        time.sleep(0.1)

    subprocess.run(create_database_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    time.sleep(0.1)

    with open(file_entrys, 'r') as file:
    # Itera sobre cada línea del archivo
        for line in file:
            # Procesa la línea, por ejemplo, imprimiéndola en la consola
            command = get_into_database + " " + line.strip() 
            print(command)
            subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            time.sleep(0.1)

client = TestClient(app)


def test_steal_card_NotCardsMatch():
    set_env()
    time.sleep(1)
    id = 5
    
    with patch("api.player.steal_card.steal_card"):
        response = client.post(f"/card/{id}")
        
    assert json.loads(response.content) == "No hay cartas asociadas a la partida"
    assert response.status_code == 404
