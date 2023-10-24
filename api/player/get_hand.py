from db.database import Card, CardTemplate
from pony.orm import db_session, ObjectNotFound
from fastapi import APIRouter, WebSocket
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List
from pony import orm 
from api.player.player import get_jugador
from definitions import match_status
from api.player.steal_card import get_match

router = APIRouter()

class card_response(BaseModel):
    cartaNombre : str
    id : int
    tipo : bool

class hand(BaseModel):
    cartas: List[card_response]

@db_session
def get_Hand(player):
    hand = []

    cards_related = list(orm.select(
            (card)
            for card in Card
            if card.card_player.player_id == player.player_id and card.card_match == player.player_current_match_id))
    
    for card in cards_related:
        hand.append(card_response(cartaNombre = (card.card_cardT.cardT_name).lower(),
                                  id = card.card_id, 
                                  tipo = card.card_cardT.cardT_type))

    if len(hand) == 0:
        raise ObjectNotFound("El jugador no tiene ninguna carta asociada")

    return hand

@router.get("/players/{player_id}/{match_id}")
async def get_hand(player_id: int, match_id: int) -> hand:
    #try :
    player = get_jugador(player_id)

    if player.player_current_match_id == match_id :
        message = "El jugador no pertenece a la partida indicada"
        status_code = 406 # no acceptable
        return JSONResponse(content=message, status_code=status_code)
    
    match = get_match(match_id)

    if match.match_status != match_status.INITIALIZED.value:
        message = "El jugador no pertenece a una partida iniciada"
        status_code = 406 # no acceptable
        return JSONResponse(content=message, status_code=status_code)

    player_hand = get_Hand(player)

    return hand(cartas =player_hand)
    '''
    except ObjectNotFound as e: 
        content = str(e)
        return JSONResponse(content=content, status_code=404)

    except Exception as e:
        content = f"Error al acceder a los datos de {player_id}"
        return JSONResponse(content = content, status_code = 410) #comportamiento inesperado
    '''