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

fileEntrys = ["db/steal_card_entrys/steal_cards_entrys_cardsInDesck.txt",
              "db/steal_card_entrys/No_CardsInMatch.txt",
              "db/steal_card_entrys/CardsIndiscard.txt"]

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

def test_steal_card_playerDontExist():
    set_env("db/steal_card_entrys/steal_cards_entrys_cardsInDesck.txt")
    time.sleep(1)

    id = 8
    with patch("api.player.steal_card.steal_card"):
        response = client.post(f"/card/{id}")
        
    assert json.loads(response.content) == "El jugador no existe"
    assert response.status_code == 404


def test_steal_card_playerNotInGame():
    set_env("db/steal_card_entrys/steal_cards_entrys_cardsInDesck.txt")
    time.sleep(1)

    id = 9
    with patch("api.player.steal_card.steal_card"):
        response = client.post(f"/card/{id}")
        
    assert json.loads(response.content) == "El jugador no esta en una partida"
    assert response.status_code == 406


def test_steal_card_MatchFinalized():
    set_env("db/steal_card_entrys/steal_cards_entrys_cardsInDesck.txt")
    time.sleep(1)

    id = 11
    with patch("api.player.steal_card.steal_card"):
        response = client.post(f"/card/{id}")
        
    assert json.loads(response.content) == "La partida no esta inicializada o ya finalizo"
    assert response.status_code == 406

def test_steal_card_PlayerNotInTurn():
    set_env("db/steal_card_entrys/steal_cards_entrys_cardsInDesck.txt")
    time.sleep(1)
    id = 99
    with patch("api.player.steal_card.steal_card"):
        response = client.post(f"/card/{id}")
        
    assert json.loads(response.content) == "No es el turno del jugador"
    assert response.status_code == 406


#como correr test
#1.mover al directorio lacosa/
#2.ejecutar pytest test_steal_card.py -vv