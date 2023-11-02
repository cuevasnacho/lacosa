from pony.orm import db_session
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from api.player.steal_card import get_match
from db.database import Player, Match, Card
from pony.orm import db_session, commit
from api.card.alejate import adjacent_players

router = APIRouter()
#reason == 0 -> causaso normales
#reaso == 1 -> por carta seduccion

@db_session
def valid_card(card_id):
    not_valid_cards = ["la_cosa", "infectado"] #OJO QUE ESTEN LOS MISMOS NOMBRES, #FALTA LOGICA DE INFECTADO
    card = Card[card_id]
    if card.card_cardT.cardT_name in not_valid_cards: 
        return False 
    return True

@db_session
def valid_oponent(oponent_id,left,right,reason):
    valid = True
    oponent = Player[oponent_id]    
    if reason:
        if oponent.player_quarentine_count > 0 or ((not oponent.player_exchangeL) and left) or ((not oponent.player_exchangeR) and right):
            valid = False
    else: 
        if oponent.player_quarentine_count > 0 :
            valid = False
    return valid

@router.get("/intercambio/peticion/{player_id}/{oponent_id}/{player_card_id}/{reason}")
async def exchange_petition(player_id : int, oponent_id : int, player_card_id : int, reason : int):
    try: 
        player = Player[player_id]
        player_card = Card[player_card_id]
        oponent = Player[oponent_id]
    except:
        content = "El objeto no existe"
        return JSONResponse(content = content, status_code = 404)

    #valida la carta 
    if not valid_card:
        return JSONResponse(content = "Carta invalida", status_code = 400)
    
    #valida al jugador oponente 
    adjacent = adjacent_players(player_id,oponent_id) 
    if not valid_oponent(oponent_id,adjacent[0],adjacent[1]):
        return JSONResponse(content = "Jugador invalida", status_code = 400)
    
    #tiene que intercambiar con alguien del costado
    if (not (adjacent[0] or adjacent[1])) and reason:
        return JSONResponse(content = "El jugador no es adyecente", status_code = 400)
        
    #enviar mensaje por socket de peticion de intercambio 
    return JSONResponse(content = "Succes", status_code = 200)

@db_session
def have_defense_card(oponent_id,reason):
    not_valid_cards = ["aterrador","no_gracias","fallaste"] #OJO QUE ESTEN LOS MISMOS NOMBRES, FALTA IMPLEMETAR FALLASTE 
    cards = Card.select(lambda card : card.card_player == oponent_id)
    for card in cards : 
        if card.card_cardT.cardT_name in not_valid_cards:
            return True 
    return False

@router.get("/intercambio/aceptacion/{player_id}/{card_id}/{reason}")
async def exchange_accept(player_id : int, card_id : int, reason : int):
    #player_id es el oponent del endpoind anterior 
    contet = False
    if have_defense_card(player_id,reason):
        contet = True    

        #si el jugador se defiende no se genera el intercambio
    #si la carta no se valida no se genera el intercambio
    return JSONResponse(content = contet, status_code = 200)

@router.put("/intercambio/cartas/{match_id}/{player_id}/{card1_id}/{oponent_id}/{card2_id}")
async def exchange_accept(match_id: int, player_id : int, card1_id : int, oponent_id : int, card2_id : int):
    try: 
        player = Player[player_id]
        player_card = Card[card1_id]
        oponent = Player[oponent_id]
        oponent_card = Card[card2_id]
    except:
        content = "El objeto no existe"
        return JSONResponse(content = content, status_code = 404)

    with db_session :
        player_card.card_player = oponent.player_id
        oponent_card.card_player = player.player_id

    content = "Cambio realizado"
    return JSONResponse(content = content, status_code = 200)
