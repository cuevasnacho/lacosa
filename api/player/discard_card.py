#probar endpoind : curl -X PUT http://localhost:8000/descartar_carta/99/77

from db.database import Player, Match, Card
from pony.orm import db_session,commit
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from definitions import card_position
from api.messages import iniciar_intercambio, fin_turno,end_or_exchange
from api.messages import message_quarentine

router = APIRouter()

@db_session
def is_player_turn(player_id):
    try:
        #obtengo el match_id de la partida que el jugador "player_id" esta jugando
        match_id = Player.select(lambda player : player.player_id == player_id).first().player_current_match_id.match_id
        #filtro todas las partidas en el match_id obtenido 
        player_match = Match.select(lambda match : match.match_id == match_id).first()
        #comparo el id del jugador con el jugador de turno en dicha partida
        return player_match.match_currentP == player_id
    except:
        return False

@db_session      
def card_belong_player(player_id, card_id):
    try:
        #obtengo las cartas del jugador player_id
        player_cards = Card.select(lambda card : card.card_player.player_id == player_id)
        #filtro entra las cartas del jugador la que tiene el id "card_id"
        filter_card = player_cards.filter(lambda card : card.card_id == card_id).first()
        return filter_card.card_id == card_id
    except:
        return False

@db_session
async def next_phase(player_id):
    try : 
        match_id = (Player.get(player_id = player_id)).player_current_match_id.match_id
        await end_or_exchange(match_id,player_id)
    except:
        print("Error en socket next_phase")

@router.put("/carta/descartar/{player_id}/{id_card}")
async def discard_card(player_id : int, id_card : int):
    #valido los tipos del input
    if (type(player_id) != int or type(id_card) != int):
        message = "El tipo de los datos ingresados son invalidos"
        status_code = 406 # no acceptable
        return JSONResponse(content=message, status_code=status_code)
    
    #falta tener en cuenta las cartas que no se pueden descartar
    if (is_player_turn(player_id) and card_belong_player(player_id, id_card)):
        #actualizo el estado de la carta 
        with db_session:
            card_to_update = Card.get(card_id=id_card) 
            card_to_update.card_location = card_position.DISCARD.value
            card_to_update.card_player = None 
            commit()

            player = Player[player_id]

            if player.player_quarentine_count > 0:
                player.player_quarentine_count = player.player_quarentine_count - 1
                commit()
                
            if player.player_quarentine_count > 0:
                data = f"El jugador {player.player_name} descarto {card_to_update.card_cardT.cardT_name}"
                await message_quarentine(player.player_current_match_id.match_id,data)

        await next_phase(player_id)
        message = "Carta descartada"
        status_code = 200 #OK
        return JSONResponse(content=message, status_code=status_code)    

    else:    
        message = f"No es el turno del jugador {player_id} / No posee la carta" 
        status_code = 405 # metodo no permitido
        return JSONResponse(content=message, status_code=status_code)
