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
    cartaNombre : str
    id : int
    tipo : bool


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
        card_steal = Card.select(lambda c : c.card_match.match_id == match_id and
                           c.card_location == card_position.DECK.value).random(1)[0]

        if (card_steal is None):
            discard_to_deck(match_id)
            card_steal = Card.select(lambda c : c.card_match.match_id == match_id and
                           c.card_location == card_position.DECK.value).random(1)[0]

        if card_steal is None:
            raise ObjectNotFound("No hay cartas asociadas a la partida")
    
        return card_steal

@db_session
def get_match(id_match):
    match = Match.get(match_id=id_match)
    if match is None:
        raise ObjectNotFound("La partida asociada al jugador no existe")
    return match

@router.post("/card/{player_id}")
async def steal_card(player_id : int)-> carta_robada:
    with db_session:
        try:
    
            player = Player.get(player_id = player_id)

            if not(player.player_ingame):
                content = "El jugador no esta en una partida"
                return JSONResponse(content = content, status_code = 406)
            
            match = get_match(player.player_current_match_id.match_id)

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

            content = carta_robada(cartaNombre = card.card_cardT.cardT_name,
                                  id = card.card_id, 
                                  tipo = card.card_cardT.cardT_type)

            return content

        except ObjectNotFound as e:
            content = str(e)
            return JSONResponse(content=content, status_code=404)
        
        except Exception as e:
            print(f"Error durante el robo de cartas: {e}")
            content = str(f"Error durante el robo de cartas: {e}")
            return JSONResponse(content = content, status_code = 406)