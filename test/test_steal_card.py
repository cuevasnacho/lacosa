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
    id = 8
    with patch("api.player.steal_card.steal_card"):
        response = client.post(f"/card/{id}")
        
    assert json.loads(response.content) == "El jugador no existe"
    assert response.status_code == 404


def test_steal_card_playerNotInGame():
    set_env(fileEntrys[0])
    id = 9
    with patch("api.player.steal_card.steal_card"):
        response = client.post(f"/card/{id}")
        
    assert json.loads(response.content) == "El jugador no esta en una partida"
    assert response.status_code == 406

""""
def test_steal_card_MatchNotExist():
    set_env(fileEntrys[0])
    id = 10
    with patch("api.player.steal_card.steal_card"):
        response = client.post(f"/card/{id}")
        
    assert json.loads(response.content) == "La partida asociada al jugador no existe"
    assert response.status_code == 404
"""

def test_steal_card_MatchFinalized():
    set_env(fileEntrys[0])
    id = 11
    with patch("api.player.steal_card.steal_card"):
        response = client.post(f"/card/{id}")
        
    assert json.loads(response.content) == "La partida no esta inicializada o ya finalizo"
    assert response.status_code == 406

def test_steal_card_PlayerNotInTurn():
    set_env(fileEntrys[0])
    id = 99
    with patch("api.player.steal_card.steal_card"):
        response = client.post(f"/card/{id}")
        
    assert json.loads(response.content) == "No es el turno del jugador"
    assert response.status_code == 406

#mock the output
def test_steal_card_validOperation():
    set_env(fileEntrys[0])
    id = 5
    with db_session:
        print("Before operation:", Card.select().show())


    with patch("api.player.steal_card.steal_card"):
        response = client.post(f"/card/{id}")
    
    data = response.json()

    assert response.status_code == 200
    assert "cartaNombre" in data
    assert "id" in data
    assert "tipo" in data

    print(f"id = {data.get('id')}, cartaNombre = {data.get('cartaNombre')} tipo = {data.get('tipo')}")
    id = data.get('id')
    """ chequear test con la database
    with db_session:
        print("After operation:", Card.select().show())

        in_hand_card = Card.get(card_id= id)
        print(f"Card in hand: {in_hand_card}")
        assert (in_hand_card is not None)
        assert in_hand_card.card_location == card_position.PLAYER.value
        assert in_hand_card.card_player == id   
    """
    

def test_steal_card_NotCardsInDeck():
    set_env(fileEntrys[2])
    id = 5

    with patch("api.player.steal_card.steal_card"):
        response = client.post(f"/card/{id}")
        
    assert response.status_code == 200
    data = response.json()
    assert "cartaNombre" in data
    assert "id" in data
    assert "tipo" in data
    
def test_steal_card_NotCardsMatch():
    set_env(fileEntrys[1])
    id = 5
    
    with patch("api.player.steal_card.steal_card"):
        response = client.post(f"/card/{id}")
        
    assert json.loads(response.content) == "No hay cartas asociadas a la partida"
    assert response.status_code == 404

#como correr test
#1.mover al directorio lacosa/
#2.ejecutar pytest test_steal_card.py -vv