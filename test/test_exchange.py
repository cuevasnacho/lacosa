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

def set_env(data):
    database = "db/lacosa.sqlite"
    create_database_command = "python3 db/database.py"
    get_into_database = "sqlite3 db/lacosa.sqlite"
    file_entrys = data
    if os.path.exists(database):
        os.remove(database)
        time.sleep(0.1)
    
    subprocess.run(create_database_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    time.sleep(0.1)
    with open(file_entrys, 'r') as file:
        for line in file:
            command = get_into_database + " " + line.strip() 
            subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            time.sleep(0.1)
'''
#intercambio de cartas
def test_swap_cards():
    set_env("db/test_swap_cards.txt")
    #intercambio
    time.sleep(1)
    response = client.put("/intercambio/cartas/1/1/2/2/''") #jugador 1 tiene carta 1 y jugador 2 tiene carta 2
    time.sleep(2)
    with db_session:
        #jugador 1 tiene carta 2
        player1_card = Card.select(lambda card : card.card_id == 1).first()
        assert player1_card.card_player.player_id == 2
        #jugador 2 tiene carta 1
        player2_card = Card.select(lambda card : card.card_id == 2).first()
        assert player2_card.card_player.player_id == 1
        assert json.loads(response.content) == "Cambio realizado"
'''