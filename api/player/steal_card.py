from pydantic import *
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from db.database import Match, Player, Card
from pony.orm import db_session, commit ,select, ObjectNotFound
from definitions import match_status , card_position

router = APIRouter()

class carta_robada(BaseModel):
    cartaNombre : str
    id : int
    tipo : bool


@db_session
def get_match(id_match):
    match = Match.get(match_id=id_match)
    if match is None:
        raise ObjectNotFound("La partida asociada al jugador no existe")
    return match

@db_session
def get_player(id_player):
    player = Player.get(player_id = id_player)
    
    if player is None:
        raise ObjectNotFound("El jugador no existe")
    
    print(f"player {id_player} is  = {player}") 

    return player

@db_session
def discard_to_deck(match_id):
    discard = list(Card.select(lambda c : c.card_match.match_id == match_id and
                           c.card_location == card_position.DISCARD.value))
    match = get_match(match_id)
    
    for card in discard:
        card.card_location = card_position.DECK.value
        match.match_cardsCount += 1
        commit()


@db_session
def get_card_from_deck(match_id):
        deck_cards = Card.select(lambda c : c.card_match.match_id == match_id and
                           c.card_location == card_position.DECK.value)

        if not deck_cards:
            discard_to_deck(match_id)
            deck_cards = Card.select(lambda c : c.card_match.match_id == match_id and
                           c.card_location == card_position.DECK.value)

        if deck_cards :
            card_steal = deck_cards.random(1)[0]
            return card_steal


        return deck_cards

@router.post("/card/{player_id}")
async def steal_card(player_id : int)-> carta_robada:
    with db_session:
        try:
    
            player = Player.get(player_id = player_id)

            if player is None:
                content = "El jugador no existe"
                return JSONResponse(content=content, status_code=404)
            
            if not(player.player_ingame):
                content = "El jugador no esta en una partida"
                return JSONResponse(content = content, status_code = 406)
            
            match = Match.get(match_id=player.player_current_match_id.match_id)
            
            if match is None:
                content = "La partida asociada al jugador no existe"
                return JSONResponse(content = content, status_code = 404)

            if (match.match_status != match_status.INITIALIZED.value):
                content = "La partida no esta inicializada o ya finalizo"
                return JSONResponse(content = content, status_code = 406)

            
            if (player.player_id != match.match_currentP):
                content = "No es el turno del jugador"
                return JSONResponse(content = content, status_code = 406)
            
            card = get_card_from_deck(match.match_id)

            if not card:
                content = "No hay cartas asociadas a la partida"
                return JSONResponse(content = content, status_code = 404)

            card.card_location = card_position.PLAYER.value
            card.card_player = player
            match.match_cardsCount -= 1
            commit()

            content = carta_robada(cartaNombre = card.card_cardT.cardT_name,
                                  id = card.card_id, 
                                  tipo = card.card_cardT.cardT_type)

            return content

        except ObjectNotFound as e:
            print(f"Exception type: {type(e)}")
            content = str(e)
            return JSONResponse(content=content, status_code=404)
        
        except Exception as e:
            print(f"Exception type: {type(e)}")
            print(f"Error durante el robo de cartas: {e}")
            content = str(f"Error durante el robo de cartas: {e}")
            return JSONResponse(content = content, status_code = 406)