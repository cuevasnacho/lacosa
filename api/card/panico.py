from db.database import Card, CardTemplate, Player, Match
from pony.orm import db_session
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from api.card.load_templates import Template_Diccionary
from api.card.alejate import *
from pony import orm 
from definitions import cards_subtypes
from pydantic import BaseModel
import json 
from typing import List
from definitions import player_roles
from api.match.match_websocket import manager
from api.messages import iniciar_defensa, start_exchange_seduction,fin_turno, end_or_exchange
from api.player.defend import discard_Card


router = APIRouter()

@router.put("/carta/panico/{player_id}/{card_id}/{oponent_id}")
async def play_panic(player_id : int, card_id : int):
    if check_pre_conditions(player_id, card_id):
        response = apply_card_efect(card_id,oponent_id, player_id)
        valid_play = response[0]
        card_name = response[1]
        if valid_play:
            discard_Card(card_id)
            message = "Okeey"
            status_code = 200 # no acceptable
            return JSONResponse(content=message, status_code=status_code)
        else:
            content = "Jugada invalida"
            return JSONResponse(content = content, status_code = 401)

    else:
        content = "No se cumplen las precondiciones"
        return JSONResponse(content = content, status_code = 401)