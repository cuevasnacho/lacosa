from pony.orm import db_session
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from db.database import Player, Card
from pony.orm import db_session, commit
from api.card.alejate import adjacent_players
from definitions import player_roles
from api.messages import message_quarentine,fin_turno,iniciar_defensa,sol_intercambio

router = APIRouter()

#POSIBLE ERROR ES QUE NO ESTEN CON LOS MISMOS NOMBRES

@db_session
async def quarentine_message(match_id,player,card,new_card):
    if player.player_quarentine_count > 0 :
        data = f"El jugador {player.player_name} intercambio {card}"
        await message_quarentine(match_id,data)
        data = f"El jugador {player.player_name} recibio {new_card}"
        await message_quarentine(match_id,data)
        
@db_session
def valid_card(card_id,role):
    if role == player_roles.THE_THING.value:
        not_valid_cards = ["lacosa"]
    elif role == player_roles.HUMAN.value:
        not_valid_cards = ["infectado"] 
    elif role == player_roles.INFECTED.value:
        not_valid_cards = []

    card = Card[card_id]
    if card.card_cardT.cardT_name in not_valid_cards: 
        return False 
    return True

@db_session
def valid_oponent(player_id,oponent_id,role,oponent_at_left,oponent_at_right,card_id,motive):
    oponent = Player[oponent_id]    
    card = Card[card_id]
    oponent = Player[oponent_id]
    oponent_role = oponent.player_role
    valid = True

    if role != player_roles.THE_THING.value:
        player_hand = Card.select(lambda card : card.card_player.player_id == player_id and 
                                    card.card_cardT.cardT_name == "infectado") 
        infect_card = 0
        for card in player_hand:
            infect_card += 1

        #no tengo mas de una carta infectado o no se la doy a la cosa
        if card.card_cardT.cardT_name == "infectado":
            if role == player_roles.INFECTED.value:
                if infect_card <= 1 or oponent_role != player_roles.THE_THING.value:
                    valid = valid and False 

        #no se da el intercambio si tengo todas cartas de infectado -> superinfeccion
        if role == player_roles.HUMAN.value:
            if infect_card == 6:
                valid = valid and False 
    
    #carta no es seducion -> derecha o izq
    if motive != "seduccion" and motive != "seduccion_response":
        if not (oponent_at_left or oponent_at_right): #el jugador no es adyecente
            valid = valid and False 

        #caso puerta atrancada
        if ((not oponent.player_exchangeL) and oponent_at_left) or ((not oponent.player_exchangeR) and oponent_at_right):
            valid = valid and False    

    return valid

@db_session
def have_defense_card(oponent_id):
    response = []
    defense_cards = ["aterrador","no_gracias","fallaste"]  
    cards = Card.select(lambda card : card.card_player.player_id == oponent_id)
    for card in cards : 
        if card.card_cardT.cardT_name in defense_cards:
            response.append(card.card_cardT.cardT_name) 
    defense = True if len(response) > 0 else False
    return (defense,response)

#encargado de ver si se cumplen todas las condiciones para poder intercambiar
#motive : motivo del intercambio, si es una carta es su nombre si es por intercambio normal es "intercambio"
#motive : inicio_intercambio -> lo mando solo el primero
#motive : seduccion en caso de ser victima y atacante de seduccion 
@router.get("/intercambio/valido/{player_id}/{oponent_id}/{player_card_id}/{motive}")
async def exchange_valid(player_id : int, oponent_id : int, player_card_id : int, motive : str):
    with db_session:
        try: 
            player = Player[player_id]
        except:
            content = "El objeto no existe"
            return JSONResponse(content = content, status_code = 404)
        
    oponent_position = adjacent_players(player_id,oponent_id) 
    is_card_valid = valid_card(player_card_id,player.player_role)
    is_oponent_valid = valid_oponent(player_id,oponent_id,player.player_role,oponent_position[0],oponent_position[1],player_card_id,motive)
    if motive == "inicio_intercambio":
        motive = "response"
        await sol_intercambio(player.player_current_match_id.match_id,oponent_id,player_card_id,motive,player_id) # falta el oponent id
    if motive == "seduccion":
        motive = "seduccion_response"
        await sol_intercambio(player.player_current_match_id.match_id,oponent_id,player_card_id,motive,player_id)

    exchange = is_card_valid and is_oponent_valid
    code = 200 if exchange else 401
    return JSONResponse(content = exchange, status_code = code)

#encargado solamente de chequear si se puede defender
@router.get("/intercambio/defensa/{player_defense_id}/{attacker_id}/{attacker_card}")
async def exchange_defense(player_defense_id : int, attacker_id : int, attacker_card : int): 
    defense = have_defense_card(player_defense_id)
    with db_session:
        player = Player[player_defense_id]
        attacker_card = Card[attacker_card]
        match_id = player.player_current_match_id.match_id
        if defense[0]:
            await iniciar_defensa(match_id,player_defense_id,defense[1],attacker_id,attacker_card.card_cardT.cardT_name,"intercambio")
    return JSONResponse(content = {'data': defense[0]}, status_code = 200)

#swap de cartas 
@router.put("/intercambio/cartas/{player_id}/{card1_id}/{oponent_id}/{card2_id}/{motive}")
async def swap_cards(player_id : int, card1_id : int, oponent_id : int, card2_id : int, motive : str):
    with db_session:
        try: 
            player = Player[player_id]
            oponent = Player[oponent_id]
            player_card = Card.get(card_id = card1_id)
            oponent_card = Card.get(card_id = card2_id)
            match_id = player.player_current_match_id.match_id
        except:
            content = "El objeto no existe"
            return JSONResponse(content = content, status_code = 404)

        player_card.card_player = oponent_id
        oponent_card.card_player = player_id

        if player_card.card_cardT.cardT_name == "infectado" and motive != "fallaste":
            oponent.player_role = player_roles.INFECTED.value        
        commit()

        quarentine_message(match_id,player,player_card.card_cardT.cardT_name,oponent_card.card_cardT.cardT_name)
        quarentine_message(match_id,oponent,oponent_card.card_cardT.cardT_name,player_card.card_cardT.cardT_name)

        await fin_turno(match_id,oponent_id)

        content = "Cambio realizado"
        return JSONResponse(content = content, status_code = 200)

