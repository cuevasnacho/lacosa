from api.match.match_websocket import manager_activo
from db.database import Player


def genrate_posible_play(player_id):
    return True



async def start_next_turn(match_id,next_player_id):
    content = {'action' : 'iniciar_turno'} #forma de return para las cartas
    await manager_activo.send_data_to(content,match_id,next_player_id)

async def forzar_jugada(match_id,player_id,card_id):
    content = {'action' : 'forzar_jugada', 'data' :{"card_to_play":card_id}} #forma de return para las cartas
    await manager_activo.send_data_to(content,match_id,player_id)

async def elegir_jugada(match_id,player_id):
    content = {'action' : 'elegir_jugada'} #forma de return para las cartas
    await manager_activo.send_data_to(content,match_id,player_id)

async def iniciar_defensa(match_id,player_id,card_name):
    content = { 'action' : 'iniciar_defensa', 'data' : card_name}
    await manager_activo.send_data_to(content,match_id,player_id)

async def iniciar_intercambio(match_id,player_id):
    content = { 'action' : 'iniciar_intercambio'}
    await manager_activo.send_data_to(content,match_id,player_id)

async def sol_intercambio(match_id,player_id):
    content = { 'action' : 'sol_intercambio'}
    await manager_activo.send_data_to(content,match_id,player_id)

async def fin_turno(match_id,player_id):
    content = { 'action' : 'fin_turno'}
    await manager_activo.send_data_to(content,match_id,player_id)
