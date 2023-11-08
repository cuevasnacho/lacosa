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
from api.messages import iniciar_defensa, iniciar_intercambio
from api.player.defend import discard_Card
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
def can_player_defend_himself(id_player,id_card):
    #chequear que {id_player} tenga una carta de defensa que contrareste a {id_card} 
    card = Card.get(card_id = id_card)
    player = Player.get(player_id = id_player)
    #obtengo cartas tipo defensa del jugador
    cards_player = Card.select(lambda card : card.card_player.player_id == id_player 
                               and card.card_cardT.cardT_subtype == cards_subtypes.DEFENSE.value
                               and player.player_current_match_id == card.card_match)
    #tiene o no cartas de defensa     
    if (cards_player):
        #alguna de las cartas de defensa puede anular efecto de {id_card}
        defense = False
        for cards in cards_player:
            if (card.card_cardT.cardT_name == "lanzallamas" and cards.card_cardT.cardT_name == "nada_de_barbacoas"):
                defense = True
            if (card.card_cardT.cardT_name == "mas_vale_que_corras" and cards.card_cardT.cardT_name == "aqui_estoy_bien"):
                defense = True
            if (card.card_cardT.cardT_name == "cambio_de_lugar" and cards.card_cardT.cardT_name == "aqui_estoy_bien"):
                defense = True
            #HAY QUE AGREGAR TODAS LAS CONVINACIONES DE CARTA ATAQUE-CARTA DEFENSA POSIBLES
            #elif (....) 
        return defense
    else:
        return False #CAMBIAR POR FALSE

@db_session
def get_match_id(player_id):
    player = Player.get(player_id = player_id)
    return player.player_current_match_id.match_id

@db_session
def get_card_name(id_card):
    card = Card.get(card_id = id_card)
    card_type = CardTemplate.get(cardT_id = card.card_cardT.cardT_id)
    return card_type.cardT_name

def apply_card_efect(card_id, oponent_id,player_id):
    name = get_card_name(card_id)
    card_tamplate = Template_Diccionary[name]
    if card_tamplate.valid_play(player_id,oponent_id):
        content = card_tamplate.aplicar_efecto(oponent_id,player_id) 
        return (True,content)
    else:
        content = "No se puede realizar la jugada"
        return (False,content)
    
#atributos que pueden cambiar despues de ejecutar una carta
class data_item(BaseModel):
    player_id : int
    player_ingame : int    
    player_position : int
    player_exchangeR : int
    player_exchangeL : int
    player_role : int
    player_dead : bool
    player_defense : bool
    card_name : List[str]
    end_game : bool

@db_session
def posible_response(card_id):
    card_name = (Card.get(card_id = card_id)).card_cardT.cardT_name 
    if(card_name == "lanzallamas"):
        return ["nada_de_barbacoas"]
    if(card_name == "mas_vale_que_corras" or card_name =="cambio_de_lugar"):
        return ["aqui_estoy_bien"]

    return []

@db_session
def fullfile_efect(target_id,id_card):
    card_name = (Card.get(card_id = id_card)).card_cardT.cardT_name 
    card_used = Template_Diccionary[card_name]
    card_used.fullfile_efect(target_id)


@db_session
def players_status_after_play_card(id_player,oponent_id,defense,cards_names,is_end_game,defense_with):
    response = []

    player_status = orm.select((player.player_id,player.player_ingame,player.player_position,player.player_exchangeR,player.player_exchangeL,player.player_role,player.player_dead,False)
                               for player in Player if player.player_id == id_player).first()
    oponent_status = orm.select((player.player_id,player.player_ingame,player.player_position,player.player_exchangeR,player.player_exchangeL,player.player_role,player.player_dead,defense)
                               for player in Player if player.player_id == oponent_id).first()

    response.append(data_item(player_id = player_status[0],player_ingame=player_status[1],player_position=player_status[2],player_exchangeR=player_status[3],
            player_exchangeL = player_status[4],player_role = player_status[5],player_dead = player_status[6],player_defense=player_status[7], card_name = cards_names,end_game=is_end_game))
    
    response.append(data_item(player_id = oponent_status[0],player_ingame=oponent_status[1],player_position=oponent_status[2],player_exchangeR=oponent_status[3],
            player_exchangeL = oponent_status[4],player_role = oponent_status[5],player_dead = oponent_status[6],player_defense=oponent_status[7],card_name = defense_with,end_game=is_end_game))

    return json.loads(json.dumps([obj.dict() for obj in response]))

@db_session
def is_end_game(id_card):
    response = True
    humans_alive = True
    match_id = (Card.get(card_id = id_card)).card_match.match_id
    players = Player.select(lambda player : player.player_current_match_id.match_id == match_id
                            and player.player_role != player_roles.THE_THING.value)
                            
    lacosa = Player.select(lambda player : player.player_current_match_id.match_id == match_id 
                           and player.player_role == player_roles.THE_THING.value).first()
    
    if not lacosa.player_dead:
        for player in players:
            infected = player.player_role == player_roles.INFECTED.value
            dead = player.player_dead  
            humans_alive = humans_alive and (infected or dead) #todos los humanos estan infectados o elimindados
        response = humans_alive
    return response

@router.put("/carta/jugar/{player_id}/{card_id}/{oponent_id}")
async def play_card(player_id : int, card_id : int, oponent_id : int):
    if check_pre_conditions(player_id, card_id):
        response = apply_card_efect(card_id, oponent_id,player_id)
        valid_play = response[0]
        card_name = response[1]
        end_game = is_end_game(card_id)
        match_id = get_match_id(player_id)
        if valid_play:
            if can_player_defend_himself(oponent_id,card_id) and oponent_id != player_id:
                defend_with = posible_response(card_id)
                content = players_status_after_play_card(player_id,oponent_id,True,card_name,end_game,defend_with)
                discard_Card(card_id)
                await iniciar_defensa(match_id,oponent_id,defend_with,player_id,get_card_name(card_id))               
            else:
                content = players_status_after_play_card(player_id,oponent_id,False,card_name,end_game,[])
                fullfile_efect(oponent_id,card_id)
                discard_Card(card_id)
                await iniciar_intercambio(match_id,player_id)
            return JSONResponse(content = content, status_code = 200)
        else:
            content = "Jugada invalida"
            return JSONResponse(content = content, status_code = 401)
    else: 
        content = "No se cumplen las precondiciones"
        return JSONResponse(content = content, status_code = 401)
   

