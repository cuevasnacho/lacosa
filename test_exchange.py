from api.player.exchange import swap_cards,exchange_defense,exchange_valid
from fastapi.testclient import TestClient
from main import app 
import os 
import subprocess
import time 
from api.card.load_templates import load_templates

client = TestClient(app)
#ACTUALIZAR ENDPOINDS
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

'''
#intercambio de cartas
def test_swap_cards():
    set_env("db/test_swap_cards.txt",True)
    #intercambio
    time.sleep(1)
    response = client.put("/intercambio/cartas/1/1/2/2/' '") #jugador 1 tiene carta 1 y jugador 2 tiene carta 2
    time.sleep(1)
    with db_session:
        #jugador 1 tiene carta 2
        player1_card = Card.select(lambda card : card.card_id == 1).first()
        assert player1_card.card_player.player_id == 2
        #jugador 2 tiene carta 1
        player2_card = Card.select(lambda card : card.card_id == 2).first()
        assert player2_card.card_player.player_id == 1

        #assert json.loads(response.content) == "Cambio realizado"

#tengo que esperar que anadan alguna carta de  ["aterrador","no_gracias","fallaste"] y modificar el id en la carta de test_exchange_defense.txt
def test_exchange_defense():
    load_templates()
    set_env("db/test_exchange_defense.txt",False)
    time.sleep(1)

    #caso que se puede defender -> PONER ACAS
    #response = client.get("/intercambio/defensa/3") #caso en que tiene carta para defenderse -> igualar id en test
    #assert response.content.decode('utf-8') == 'true'

    #caso que no se defiende -> lanzallamas
    response = client.get("/intercambio/defensa/1")
    assert response.content.decode('utf-8') == 'false'
'''


def test_exchange_defense():
    set_env("db/test_exchange_defense.txt",False)
    time.sleep(1)

    response = client.get("/intercambio/valido/{player_id}/{oponent_id}/{player_card_id}/{motive}") #lanzallamas
    assert response.content.decode('utf-8') == 'false'
