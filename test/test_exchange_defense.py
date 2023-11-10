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

#tengo que esperar que anadan alguna carta de  ["aterrador","no_gracias","fallaste"] y modificar el id en la carta de test_exchange_defense.txt
def test_exchange_defense():
    load_templates()
    set_env("db/test_exchange_defense.txt",False)
    time.sleep(1)

    #caso que se puede defender -> aterrador 
    response = client.get("/intercambio/defensa/1/1/2") #caso en que tiene carta para defenderse -> igualar id en test
    response = json.loads(response.content.decode('utf-8'))
    assert response['data'] == True

def test_exchange_not_defense():
    load_templates()
    set_env("db/test_exchange_defense.txt",False)
    time.sleep(1)

    #caso que no se defiende -> lanzallamas
    response = client.get("/intercambio/defensa/2/1/2")
    response = json.loads(response.content.decode('utf-8'))
    if os.path.exists("db/lacosa.sqlite"):
        os.remove("db/lacosa.sqlite")
        time.sleep(0.1)
    subprocess.run("python3 db/database.py", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert response['data'] == False


