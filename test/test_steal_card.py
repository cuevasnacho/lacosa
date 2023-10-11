import pytest
from unittest.mock import MagicMock
from unittest.mock import patch
from api.lobby.request_join import unirse_lobby
from fastapi.testclient import TestClient
from main import app 
import json 
import os 
import subprocess
import time 


fileEntrys = ["db/steal_cards_entrys_cardsInDesck.txt"]

def set_env(to_load):
    database = "db/lacosa.sqlite"
    create_database_command = "python3 db/database.py"
    get_into_database = "sqlite3 db/lacosa.sqlite"
    file_entrys = to_load
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

def test_steal_card_playerDontExist():
    set_env(fileEntrys[0])
    with patch("api.player.steal_card.steal_card"):
        response = client.post("/card/8")
        
    assert json.loads(response.content) == "El jugador no existe"
    assert response.status_code == 404



def test_steal_card_playerNotInGame():
    set_env(fileEntrys[0])
    with patch("api.player.steal_card.steal_card"):
        response = client.post("/card/9")
        
    assert json.loads(response.content) == "El jugador no esta en una partida"
    assert response.status_code == 406

#como correr test
#1.mover al directorio lacosa/
#2.ejecutar pytest test_steal_card.py -vv