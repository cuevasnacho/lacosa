
from fastapi.testclient import TestClient
from main import app 
import pytest

client = TestClient(app)

def test_create_player():
  response = client.post(
    "/players",
    headers={"X-Token": "coneofsilence"},
    json={"player_name": "foobar"},
  )
  assert response.status_code == 201
  assert response.json() == {
    "player_id": 10,              #fijate de poner el id siguiente en la db
    "player_name": "foobar",
  }
