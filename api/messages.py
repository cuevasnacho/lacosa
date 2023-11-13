from api.match.match_websocket import manager_activo
from db.database import Player, Match,Lobby
from pony.orm import db_session, commit

@db_session
def get_next_player_id(player_id, match_id):
    fetch_lobby = Lobby[match_id]

    fetch_match = fetch_lobby.lobby_match

    player_counter = fetch_lobby.lobby_pcount
    match_direction = fetch_match.match_direction

    current_player_obj = Player[player_id]
    current_player_pos = current_player_obj.player_position

    if match_direction:
        next_player_pos = (current_player_pos + 1) % player_counter
        next_player_obj = Player.get(lambda next: next.player_position == next_player_pos and next.player_current_match_id.match_id  == match_id)
        while next_player_obj.player_dead == True:
            next_player_pos = (next_player_pos + 1) % player_counter
            next_player_obj = Player.get(lambda next: next.player_position == next_player_pos and next.player_current_match_id.match_id  == match_id)
        next_player_id = next_player_obj.player_id
    else:
        next_player_pos = (current_player_pos - 1) % player_counter
        next_player_obj = Player.get(lambda next: next.player_position == next_player_pos and next.player_current_match_id.match_id  == match_id)
        while next_player_obj.player_dead == True:
            next_player_pos = (next_player_pos - 1) % player_counter
            next_player_obj = Player.get(lambda next: next.player_position == next_player_pos and next.player_current_match_id.match_id  == match_id)
        next_player_id = next_player_obj.player_id

    return next_player_id

@db_session
def can_exchange(player_id, match_id):
    player = Player[player_id]
    match = Match[match_id]

    if match.match_direction: # ronda va hacia la derecha
        locked_door = not (player.player_exchangeL)
    else: # ronda va hacia la izquierda
        locked_door = not (player.player_exchangeR)

    return not locked_door


async def end_or_exchange(match_id,player_id):
    motive = "inicio_intercambio"
    next_player_id = get_next_player_id(player_id, match_id)
    if can_exchange(next_player_id,match_id):
        print("can exchange")
        await iniciar_intercambio(match_id,player_id,motive,next_player_id)
    else:
        print("cant exchange")
        await fin_turno(match_id, player_id)

async def start_exchange_seduction(match_id,player_id,objective_id):
    motive = "seduccion"
    await iniciar_intercambio(match_id,player_id,motive,objective_id)

def genrate_posible_play(player_id):
    return True

async def message_quarentine(match_id,data):
    try:
        content = {'action' : "cuarentena", 'data' : data}
        await manager_activo.broadcast(content,match_id)
    except:
        print("Error en message_quarentine")

async def start_next_turn(match_id,next_player_id):
    content = {'action' : 'iniciar_turno', 'data':{}} #forma de return para las cartas
    await manager_activo.send_data_to(content,match_id,next_player_id)

async def forzar_jugada(match_id,player_id,card_id):
    content = {'action' : 'forzar_jugada', 'data' :{"card_to_play":card_id}} #forma de return para las cartas
    await manager_activo.send_data_to(content,match_id,player_id)

async def elegir_jugada(match_id,player_id):
    content = {'action' : 'elegir_jugada', 'data':{}} #forma de return para las cartas
    await manager_activo.send_data_to(content,match_id,player_id)

async def iniciar_defensa(match_id,player_id,card_name,atacker_id,atack_card_name):
    try:
        data = {'card_to_defend' :card_name, 'atacker_id' : atacker_id, 'atack_card_name' : atack_card_name}
        content = { 'action' : 'iniciar_defensa', 'data' :data }
        await manager_activo.send_data_to(content,match_id,player_id)
    except:
        print("Error en iniciar_defensa")

async def iniciar_intercambio(match_id,player_id,motive,oponent_id):
    content = { 'action' : 'iniciar_intercambio', 'data':{'motive' : motive, 'oponent_id': oponent_id}}
    await manager_activo.send_data_to(content,match_id,player_id)

async def sol_intercambio(match_id,player_id,card_id,motive,oponent_id):
    try:
        content = { 'action' : 'sol_intercambio', 'data':{'card_id': card_id,'motive' : motive, 'oponent_id': oponent_id}}
        await manager_activo.send_data_to(content,match_id,player_id)
    except:
        print("Error en sol_intercambio")

async def fin_turno(match_id,player_id):
    try:
        content = { 'action' : 'fin_turno', 'data':{}}
        await manager_activo.send_data_to(content,match_id,player_id)
    except:
        print("Error en fin_turno")

async def revelaciones(match_id,player_id):
    content = { 'action' : 'revelaciones', 'data':{}}
    await manager_activo.send_data_to(content, match_id, player_id)
