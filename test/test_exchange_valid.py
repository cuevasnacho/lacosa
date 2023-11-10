from api.player.exchange import swap_cards,exchange_defense,exchange_valid
from fastapi.testclient import TestClient
from main import app 
import os 
import subprocess
import time 
from api.card.load_templates import load_templates
from pony.orm import db_session, commit
from db.database import Card
import json 

client = TestClient(app)

def set_env(data,delete):
    database = "db/lacosa.sqlite"
    create_database_command = "python3 db/database.py"
    get_into_database = "sqlite3 db/lacosa.sqlite"
    file_entrys = data
    if os.path.exists(database) and delete:
        os.remove(database)
        time.sleep(0.1)
    
    subprocess.run(create_database_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    time.sleep(0.1)
    with open(file_entrys, 'r') as file:
        for line in file:
            command = get_into_database + " " + line.strip() 
            subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            time.sleep(0.1)

def test_exchange_valid_not_adjacent():
    load_templates()
    set_env("db/test_exchange_valid_not_adjacent.txt",False)
    time.sleep(1)
    #caso de intercambio a un jugador no adyacente
    response = client.get("/intercambio/valido/1/3/1/''") #lanzallamas
    assert json.loads(response.content) == False
    
def test_exchange_valid_puerta_atrancada():
    load_templates()
    set_env("db/test_exchange_valid_not_adjacent.txt",False)
    #caso de intercambio a un jugador adyacente y carta valida
    response = client.get("/intercambio/valido/1/4/1/''") #lanzallamas
    assert json.loads(response.content) == False

def test_exchange_valid():
    load_templates()
    set_env("db/test_exchange_valid_not_adjacent.txt",False)
    #caso de intercambio a un jugador adyacente y carta valida
    time.sleep(1)
    response = client.get("/intercambio/valido/1/2/1/''") #lanzallamas
    assert json.loads(response.content) == False


def test_exchange_card_invalid():
    load_templates()
    set_env("db/test_exchange_valid_not_adjacent.txt",False)
    time.sleep(1)
    #caso de intercambio a un jugador adyacente y carta invalida
    response = client.get("/intercambio/valido/1/2/5/''") #lanzallamas
    assert json.loads(response.content) == False