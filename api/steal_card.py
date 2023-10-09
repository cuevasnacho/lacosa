from pydantic import *
from fastapi import FastAPI, HTTPException, APIRouter, Query, status
from fastapi.responses import JSONResponse
from db.database import Match, Player, Card
from pony.orm import db_session, commit ,select, ObjectNotFound
from definitions import match_status , card_position
from api.player.player import get_jugador
from db.database import Player as db_player

router = APIRouter()

class carta_robada(BaseModel):
    card_id : int
    card_type : bool
    card_name : str 

@db_session
def get_match(id_match):
    try:
        match = Match.get(match_id = id_match)

    except ObjectNotFound:
        message = "La partida asociada al jugador no existe"
        status_code = 404 # not found
        return JSONResponse(content=message, status_code=status_code)

@db_session
def discard_to_deck(match_id):
    discard = card_posible_query = Card.select(lambda c : c.card_match.match_id == match_id and
                           c.card_location == card_position.DISCARD.value)
    match = get_match(match_id)

    for card in discard:
        card.card_location = card_position.DECK.value
        match.match_cardsCount += 1
        commit()


@db_session
def get_card_from_deck(match_id):
    try :
        card_steal = Card.select(lambda c : c.card_match.match_id == match_id and
                           c.card_location == card_position.DECK.value).random(1)[0]

        if (card_steal is None):
            discard_to_deck(match_id)
            card_steal = Card.select(lambda c : c.card_match.match_id == match_id and
                           c.card_location == card_position.DECK.value).random(1)[0]

        return card_steal

    except ObjectNotFound:
        message = "No hay cartas asociadas a la partida"
        status_code = 404 # not found
        return JSONResponse(content=message, status_code=status_code)

@router.post("/card/{player_id}")
async def steal_card(player_id : int)-> carta_robada:
    with db_session:
        try:
    
            player = Player.get(player_id = player_id)

            if not(player.player_ingame):
                content = "El jugador no esta en una partida"
                return JSONResponse(content = content, status_code = 406)
            
            match = Match.get(match_id = player.player_current_match_id.match_id)

            if (match.match_status != match_status.INITIALIZED.value):
                content = "La partida no esta inicializada o ya finalizo"
                return JSONResponse(content = content, status_code = 406)

            if (player.player_id == match.match_currentP):
                content = "No es el turno del jugador"
                return JSONResponse(content = content, status_code = 406)
            
            card = get_card_from_deck(match.match_id)

            card.card_location = card_position.PLAYER.value
            card.card_player = player
            match.match_cardsCount -= 1
            commit()

            content = carta_robada(card_id =card.card_id, card_type = card.card_cardT.cardT_type, card_name =card.card_cardT.cardT_name)
            return content
        
        except Exception as e:
            print(f"Error durante el robo de cartas: {e}")
            content = "No hay cartas en el mazo ni en la pila de descartes"
            return JSONResponse(content = content, status_code = 406)