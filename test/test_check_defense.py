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

client = TestClient(app)

def set_env():
    database = "db/lacosa.sqlite"
    create_database_command = "python3 db/database.py"
    get_into_database = "sqlite3 db/lacosa.sqlite"
    file_entrys = "db/test_check_defense.txt"

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

output = [
  {
    "player_id": 1,
    "player_ingame": 1,
    "player_position": 0,
    "player_exchangeR": 0,
    "player_exchangeL": 0,
    "player_role": 0,
    "player_dead": False,
    "player_defense": False
  },
  {
    "player_id": 2,
    "player_ingame": 1,
    "player_position": 0,
    "player_exchangeR": 0,
    "player_exchangeL": 0,
    "player_role": 0,
    "player_dead": True,
    "player_defense": True
  }
]

output_cant_defense = [
  {
    "player_id": 1,
    "player_ingame": 1,
    "player_position": 0,
    "player_exchangeR": 0,
    "player_exchangeL": 0,
    "player_role": 0,
    "player_dead": False,
    "player_defense": False
  },
  {
    "player_id": 3,
    "player_ingame": 1,
    "player_position": 0,
    "player_exchangeR": 0,
    "player_exchangeL": 0,
    "player_role": 0,
    "player_dead": True,
    "player_defense": False
  }
]

#jugador puede defenderse
def test_check_defense_ok():
    set_env()
    with patch("api.player.play_card.play_card"):
        response = client.put("/carta/jugar/1/2/2")
        assert json.loads(response.content) == output
        assert response.status_code == 200

def test_check_cant_defense():
    set_env()
    with patch("api.player.play_card.play_card"):
        response = client.put("/carta/jugar/1/2/3")
        assert json.loads(response.content) == output_cant_defense
        assert response.status_code == 200

#TEST ADICIONALES PARA CHEQUEAR FUNCIONALIDAD DE play_card.py

#no existe el oponente al cual se le aplica la carta
def test_check_defense_error_oponent():
    set_env()
    with patch("api.player.play_card.play_card"):
        response = client.put("/carta/jugar/1/2/99")
        assert json.loads(response.content) == "Error aplicando efecto"
        assert response.status_code == 404

#no es el turno del jugador
def test_check_defense_error_player_turn():
    set_env()
    with patch("api.player.play_card.play_card"):
        response = client.put("/carta/jugar/2/1/1")
        assert json.loads(response.content) == "No se cumplen las precondiciones"
        assert response.status_code == 401

#el jugador no tiene la carta 
def test_check_defense_error_no_card():
    set_env()
    with patch("api.player.play_card.play_card"):
        response = client.put("/carta/jugar/1/1/2")
        assert json.loads(response.content) == "No se cumplen las precondiciones"
        assert response.status_code == 401

#como correr test
#1.mover al directorio lacosa/
#2.ejecutar pytest test_check_defense.py