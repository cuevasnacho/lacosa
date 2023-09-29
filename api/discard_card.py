#probar endpoind : curl -X PUT http://localhost:8000/descartar_carta/99/77
#es necesario asignar un jugador que este an la base de datos cuando el jugador descarta
#la carta. por lo tanto hay que crear un jugador que no juege, solo que sea para manterne las cartas en desuso
from db.database import Player, Match, Card
from pony.orm import db_session,select,commit
from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()

discard_player = 99

@db_session
def is_player_turn(player_id):
    try:
        # obtengo el match_id de la partida que el jugador esta jugando
        match_id = Player.select(lambda c : c.player_id == player_id).first().player_current_match_id.match_id
        # obtengo dicha partida 
        player_match = Match.select(lambda c : c.match_id == match_id).first()
        # comparo id
        return player_match.match_currentP == player_id
    except:
        return False

@db_session      
def card_belong_player(player_id, card_id):
    try:
        # get player's cards
        player_cards = Card.select(lambda c : c.card_player.player_id == player_id)
        # filter cards by id
        filter_card = player_cards.filter(lambda c : c.card_id == card_id).first()
        return filter_card.card_id == card_id
    except:
        return False


@router.put("/carta/descartar/{player_id}/{id_card}")
async def discard_card(player_id : int, id_card : int):
    # input validation
    if (type(player_id) != int or type(id_card) != int):
        message = "El tipo de los datos ingresados son invalidos"
        status_code = 406 # not acceptable
        return JSONResponse(content=message, status_code=status_code)

    if (is_player_turn(player_id) and card_belong_player(player_id, id_card)):
        #change card status and save data
        #cambiar en carta que jugador la posee 
        with db_session:
            card_to_update = Card.get(card_id=id_card)
            card_to_update.card_player = discard_player # jugador de descarte
            commit()
        
        #response 
        message = "Carta descartada"
        status_code = 200 #OK
        return JSONResponse(content=message, status_code=status_code)    

    else:    
        message = f"No es el turno del jugador {player_id} / No posee la carta" 
        status_code = 405 # metodo no permitido
        return JSONResponse(content=message, status_code=status_code)
