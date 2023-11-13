from api.lobby.show_lobbys import show_matches
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
from main import app 
import pytest
import time 
import os 
import subprocess

client = TestClient(app)

def set_env():
    database = "db/lacosa.sqlite"
    create_database_command = "python3 db/database.py"
    get_into_database = "sqlite3 db/lacosa.sqlite"
    file_entrys = "db/test_show_entrys.txt"
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


matches = [
  {
    "lobby_id": 1,
    "match_id": 1,
    "lobby_name": 'l1',
    "number_of_players": 1,
    "host_name": 'nacho',
    "max_players": 6,
    "min_players": 5,
    "is_private" : True
  },
  {
    "lobby_id": 2,
    "match_id": 2,
    "lobby_name": 'l1',
    "number_of_players": 1,
    "host_name": 'descarte',
    "max_players": 6,
    "min_players": 5,
    "is_private" : True
  },
  {
    "lobby_id": 5,
    "match_id": 7,
    "lobby_name": 'l1',
    "number_of_players": 1,
    "host_name": 'tomas',
    "max_players": 6,
    "min_players": 5,
    "is_private" : True
  }
]

def test_discard_card():
  set_env()
  time.sleep(1)
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