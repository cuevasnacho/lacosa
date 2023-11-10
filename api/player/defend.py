from db.database import Card, Player
from pony.orm import db_session
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from api.card.load_templates import Template_Diccionary
from api.card.alejate import *
from definitions import cards_subtypes
from pydantic import BaseModel
import json 
from definitions import  cards_subtypes, card_position
from api.messages import iniciar_intercambio
from api.player.steal_card import discard_to_deck

router = APIRouter()

class response_defense(BaseModel):
    atacker_username : str
    defensor_username : str
    card_name : str    

@db_session
def discard_Card(card_id):
    card = Card.get(card_id = card_id)
    card.card_location = card_position.DISCARD.value
    card.card_player = None 
    commit()

def get_card_not_panic(match_id):
        deck_cards = Card.select(lambda c : c.card_match.match_id == match_id and
                           c.card_location == card_position.DECK.value and not(c.card_cardT.cardT_type))

        if not deck_cards:
            discard_to_deck(match_id)
            deck_cards = Card.select(lambda c : c.card_match.match_id == match_id and
                           c.card_location == card_position.DECK.value and not(c.card_cardT.cardT_type))

        if deck_cards :
            card_steal = deck_cards.random(1)[0]
            return card_steal


        return deck_cards


@db_session
def steal_card_not_panic(player_id):
    player = Player.get(player_id = player_id)
    match = player.player_current_match_id
    card = get_card_not_panic(match.match_id)
    if not card:
        content = "No hay cartas asociadas a la partida"
        return JSONResponse(content = content, status_code = 404)

    card.card_location = card_position.PLAYER.value
    card.card_player = player
    match.match_cardsCount -= 1
    commit()

@db_session
def validate_defense(id_card,defensor_id,attacker_id):
    
    card = Card.get(card_id = id_card)
    defensor = Player.get(player_id = defensor_id)
    attacker = Player.get(player_id = attacker_id)
    if card is None:
        messeage = "El id de la carta es invalido"
        response = JSONResponse(content = messeage, status_code = 404)
        return (False,response)
    if defensor is None:
        messeage = "El id del defensor es invalido"
        response = JSONResponse(content = messeage, status_code = 404)
        return (False,response)
    if attacker is None:
        messeage = "El id del atacante es invalido"
        response = JSONResponse(content = messeage, status_code = 404)
        return (False,response)
    
    if card.card_player.player_id != defensor.player_id:
        messeage = "La carta no pertenece al defensor"
        response = JSONResponse(content = messeage, status_code = 406)
        return (False,response)
    
    if defensor.player_current_match_id != attacker.player_current_match_id:
        messeage = "El atacante y el defensor no estan en la misma partida"
        response = JSONResponse(content = messeage, status_code = 406)
        return (False,response)
    
    if card.card_cardT.cardT_cardT_subtype != cards_subtypes.DEFENSE.value:
        messeage = "La carta indicada no es de defensa"
        response = JSONResponse(content = messeage, status_code = 406)
        return (False,response)
    
    card_template = Template_Diccionary[card.card_cardT.cardT_name]


    return (True, card_template)

@router.post("/defensa/{card_id}/{defensor_id}/{attacker_id}/{exchange_card_id}}")
async def defend(defensor_id : int, card_id : int, attacker_id : int,exchange_card_id : int)-> response_defense:

    is_valid = validate_defense(card_id,defensor_id,attacker_id)

    if(is_valid[0]):
        card_to_use = is_valid[1]
        card_to_use.aplay_defense_effect(defensor_id, attacker_id,0)

        card_name = (Card.get(card_id = card_id)).card_cardT.card_name
        defensor_name = (Player.get(player_id = defensor_id)).player_name
        attacker_name = (Player.get(player_id = attacker_id)).player_name
        match_id = (Player.get(player_id = attacker_id)).player_current_match_id.match_id
        
        discard_Card(card_id)

        steal_card_not_panic(defensor_id)

        await iniciar_intercambio(match_id, attacker_id)

        return response_defense(atacker_username =attacker_name,
                                 defensor_username = defensor_name,
                                 card_name = card_name)    
    else :
        return is_valid[1]

@router.post("/defensa/inercambio/{card_id}/{defensor_id}/{attacker_id}/{card_exchange_id}")
async def defend(defensor_id : int, card_id : int, attacker_id : int,card_exchange_id :int):

    is_valid = validate_defense(card_id,defensor_id,attacker_id)

    if(is_valid[0]):
        card_to_use = is_valid[1]
        card_to_use.aplay_defense_effect(defensor_id, attacker_id,card_exchange_id)

        card_name = (Card.get(card_id = card_id)).card_cardT.card_name
        defensor_name = (Player.get(player_id = defensor_id)).player_name
        attacker_name = (Player.get(player_id = attacker_id)).player_name
        match_id = (Player.get(player_id = attacker_id)).player_current_match_id.match_id
        
        discard_Card(card_id)

        steal_card_not_panic(defensor_id)

        iniciar_intercambio(match_id, attacker_id)

        return response_defense(atacker_username =attacker_name,
                                 defensor_username = defensor_name,
                                 card_name = card_name)    
    else :
        return is_valid[1]
