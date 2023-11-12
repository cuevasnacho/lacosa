from fastapi.testclient import TestClient
from fastapi.responses import JSONResponse
from main import app
import os
import subprocess
import time
from api.card.load_templates import load_templates
from pony.orm import db_session, commit
from db.database import Card, Player
import json
#debo importar el player
from db.database import Player as db_player
from db.database import Match as db_match
from db.database import Lobby as db_lobby
from definitions import match_status
from pony.orm import Database, PrimaryKey, Required, Set, Optional
from pony import *

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

def test_leave_lobby_non_host():
    # set_env("db/test_leave_lobby_non_host.txt", True)
    time.sleep(2)
    response = client.post("/lobbys/1/1")
    time.sleep(2)

    with db_session:
        player = Player.get(player_id = 1)
        assert player.player_ingame == False
        assert player.player_isHost == False
        assert player.player_current_match_id == None
        assert player.player_lobby == None

        assert response.json() == "Jugador 1 salio del lobby"
        assert response.status_code == 404
