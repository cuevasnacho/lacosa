from api.player.player import Crear_Jugador, delete_player
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
from main import app 
from pony.orm import db_session, ObjectNotFound
from db.database import Player as db_player
import pytest
import os 
import subprocess
import time 

def set_env():
    database = "db/lacosa.sqlite"
    create_database_command = "python3 db/database.py"
    get_into_database = "sqlite3 db/lacosa.sqlite"
    file_entrys = "db/test_create_delete_player.txt"
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
def test_create_delete_player():
    set_env()
    time.sleep(0.1)
    
    response = client.post(
    "/players",
    headers={"X-Token": "coneofsilence"},
    json={"player_name" : "leo messsssssssssssssssssssssssssssssssssssssssssssssssi"},
    )
    assert response.status_code == 406
    assert response.json() == "Nombre demasiado largo"


    
    response = client.post(
    "/players",
    headers={"X-Token": "coneofsilence"},
    json={"player_name" : "leo messi"},
    )
    assert response.status_code == 200
    assert response.json() == {
        "player_id" : 3, #esta id debe ser la proxima id que se autogenere, o se debe borrar la DB y poner 1
        "player_name": "leo messi"
    }

    with db_session:
        assert db_player.get(player_id = 3 ).player_name == "leo messi"
        assert db_player.get(player_id = 0) == None


    response = client.delete(
    "/players/0",
    headers={"X-Token": "coneofsilence"})
    assert response.status_code == 404
    assert response.json() == "El jugador no existe"

    response = client.delete(
    "/players/2", #mismo id que messi
    headers={"X-Token": "coneofsilence"})
    assert response.status_code == 200
    assert response.json() == "Jugador borrado!"

    with db_session:
        assert db_player.get(player_id = 1) == None
# para correr:
#1 borrar lacosa.sqlite
#2 compilar python3 database.py
#3 mover este archivo a lacosa/
#4 correr pytest-3 test_create_delete_player.py

    
