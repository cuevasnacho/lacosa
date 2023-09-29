#probar endpoind : curl -X PUT http://localhost:8000/descartar_carta/99/77
#es necesario asignar un jugador que este an la base de datos cuando el jugador descarta
#la carta. por lo tanto hay que crear un jugador que no juege, solo que sea para manterne las cartas en desuso

from db.database import Player, Match, Card
from pony.orm import db_session,commit
from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()

discard_player = 99 #discutir con grupo

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


@router.put("/carta/descartar/{player_id}/{id_card}")
async def discard_card(player_id : int, id_card : int):
    #valido los tipos del input
    if (type(player_id) != int or type(id_card) != int):
        message = "El tipo de los datos ingresados son invalidos"
        status_code = 406 # no acceptable
        return JSONResponse(content=message, status_code=status_code)

    if (is_player_turn(player_id) and card_belong_player(player_id, id_card)):
        #actualizo el estado de la carta 
        with db_session:
            card_to_update = Card.get(card_id=id_card)
            card_to_update.card_player = discard_player # jugador de descarte
            commit()
         
        message = "Carta descartada"
        status_code = 200 #OK
        return JSONResponse(content=message, status_code=status_code)    

    else:    
        message = f"No es el turno del jugador {player_id} / No posee la carta" 
        status_code = 405 # metodo no permitido
        return JSONResponse(content=message, status_code=status_code)
