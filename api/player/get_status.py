

from db import database
from db.database import Lobby, Match, Player, Card
from pony.orm import db_session
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from definitions import match_status, results
from pydantic import BaseModel
from pony import orm 
from player import get_jugador
import json


router = APIRouter()

class card_response(BaseModel):
    card_id : int
    card_type : bool
    card_name : str

class status_response(BaseModel):
    cards_owned : [card_response]
    actual_turn : int
    finished : bool

@database
def get_Hand(player):
    hand = []

    cards_related = orm.select(
            (card.card_id, card.card_type, card.card_name)
            for card in Card
            if card.card_player.player_id == player.player_id)

    for card in cards_related:
        hand.append(card_response(card_id = card[0], card_type = card[1], card_name = card[2]))

    return hand

@router.get("/players/{player_id}/{match_id}")
async def get_status(player_id: int, match_id: int):
    try :
        player =get_jugador(player_id)

        if player.player_current_match_id == match_id :
            message = "El jugador no pertenece a la partida"
            status_code = 406 # no acceptable
            return JSONResponse(content=message, status_code=status_code)

        hand = get_Hand(player)

    except Exception as e:
        print(f"Error al acceder a los datos: {e}")
        content = f"Error al acceder a los datos de {player_id}"
        return JSONResponse(content = content, status_code = 410) #comportamiento inesperado
