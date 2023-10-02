from db.database import Card, CardTemplate, Player, Match
from pony.orm import db_session
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from api.load_templates import Template_Diccionary
from api.alejate import *

router = APIRouter()

@db_session
def check_pre_conditions(id_player,id_card):
    #jugador tiene la carta
    get_card = Card.get(card_id = id_card)
    player_has_card = get_card.card_player.player_id == id_player
    #es el turno del jugador
    get_player = Player.get(player_id = id_player)
    get_match = Match.get(match_id = get_player.player_current_match_id.match_id)
    is_player_turn = get_match.match_currentP == id_player
    return (player_has_card and is_player_turn)
    

@db_session
def get_card_name(id_card):
    card = Card.get(card_id = id_card)
    card_type = CardTemplate.get(cardT_id = card.card_cardT.cardT_id)
    return card_type.cardT_name

def apply_card_efect(card_id, oponent_id):
    name = get_card_name(card_id)
    
    card_tamplate = Template_Diccionary[name]
    card_tamplate.aplicar_efecto(oponent_id)


@router.put("/carta/jugar/{player_id}/{card_id}/{oponent_id}")
async def play_card(player_id : int, card_id : int, oponent_id : int):
    if check_pre_conditions(player_id, card_id):
        try:
            apply_card_efect(card_id, oponent_id)
            content = f"El jugador {player_id} aplico efecto sobre {oponent_id}"
            return JSONResponse(content = content, status_code = 200)
        except:
            content = "Error aplicando efecto"
            return JSONResponse(content = content, status_code = 404)
    else :
        content = "No se cumplen las precondiciones "
        return JSONResponse(content = content, status_code = 401)
