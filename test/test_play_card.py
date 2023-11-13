from api.player.play_card import play_card 
from fastapi.testclient import TestClient
from main import app 
import pytest
import os
import time
import subprocess

def set_env(file):
    database = "db/lacosa.sqlite"
    create_database_command = "python3 db/database.py"
    get_into_database = "sqlite3 db/lacosa.sqlite"
    file_entrys = file 
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
def test_play_card():
    set_env("db/test_play_card.txt")
    time.sleep(1)
    
    awnser = { 
        "message" : "El jugador 1 aplico efecto sobre 2",
        "status_code" : 200
    }
    
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