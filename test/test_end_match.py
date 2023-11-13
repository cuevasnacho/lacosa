from api.match.end_match import match_result 
from unittest.mock import patch
from fastapi.testclient import TestClient
from main import app 
import os 
import subprocess
import time 
import json
client = TestClient(app)

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

#gano la cosa y un jugador
response1 = {'jugadores' : ["nacho","luca"], 'ganadores' : "La cosa e infectados"}
def test_end_match_case1():
        set_env("db/test_end_match_case1.txt")
        with patch('api.match.end_match.match_result'):     
            response = client.get("/partida/resultado/1")
            assert response.status_code == 200
            assert json.loads(response.content) == response1

#gano la cosa sola
response2 = {'jugadores' : ["nacho"], 'ganadores' : "La cosa"}
def test_end_match_case2():
        set_env("db/test_end_match_case2.txt")
        with patch('api.match.end_match.match_result'):     
            response = client.get("/partida/resultado/1")
            assert response.status_code == 200
            assert json.loads(response.content) == response2

#gano los humanos
response3 = {'jugadores' : ["luca"], 'ganadores' : "Los humanos"}
def test_end_match_case3():
        set_env("db/test_end_match_case3.txt")
        with patch('api.match.end_match.match_result'):     
            response = client.get("/partida/resultado/1")
            assert response.status_code == 200
            assert json.loads(response.content) == response3
