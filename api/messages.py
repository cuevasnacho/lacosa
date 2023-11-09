from api.match.match_websocket import manager_activo
from db.database import Player


def genrate_posible_play(player_id):
    return True

async def message_quarentine(match_id,data):
    content = {'action' : "cuarentena", 'data' : data}
    await manager_activo.broadcast(content,match_id)

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
    data = {'card_to_defend' :card_name, 'atacker_id' : atacker_id, 'atack_card_name' : atack_card_name}
    content = { 'action' : 'iniciar_defensa', 'data' :data }
    await manager_activo.send_data_to(content,match_id,player_id)

async def iniciar_intercambio(match_id,player_id):
    content = { 'action' : 'iniciar_intercambio', 'data':{}}
    await manager_activo.send_data_to(content,match_id,player_id)

async def sol_intercambio(match_id,player_id,card_id,motive,oponent_id):
    breakpoint()
    content = { 'action' : 'sol_intercambio', 'data':{'card_id': card_id,'motive' : motive, 'oponent_id': oponent_id}}
    await manager_activo.send_data_to(content,match_id,player_id)

async def fin_turno(match_id,player_id):
    content = { 'action' : 'fin_turno', 'data':{}}
    await manager_activo.send_data_to(content,match_id,player_id)
