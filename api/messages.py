from api.match.match_websocket import manager_activo,manager
from db.database import Player, Match
from pony.orm import db_session
from api.utilsfunctions import can_exchange, get_next_player_id



async def end_or_exchange(match_id,player_id):
    try:
        motive = "inicio_intercambio"
        next_player_id = get_next_player_id(player_id, match_id)
        if can_exchange(player_id,match_id):
            await iniciar_intercambio(match_id,player_id,motive,next_player_id)
        else:
            await fin_turno(match_id, player_id)
    except:
        print("Error en end_or_exchange")

async def start_exchange_seduction(match_id,player_id,objective_id):
    try :
        motive = "seduccion"
        await iniciar_intercambio(match_id,player_id,motive,objective_id)
    except: 
        print("Error start_exchange_seduction")



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

async def iniciar_defensa(match_id,player_id,card_name,attacker_id,attack_card_name, attack_card_id, motive):
    try:
        data = {'card_to_defend' :card_name, 'attacker_id' : attacker_id, 'attack_card_name' : attack_card_name,'motive': motive,
                'attack_card_id': attack_card_id}
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

async def show_cards_all(match_id,player_id,cards_to_show):
    try:
        content = {'action': 'show_cards', 'data': cards_to_show}
        await manager.broadcast(content,match_id,player_id)
    except:
         print("Error en show_cards")

async def show_cards_one(match_id,player_id,cards_to_show):
    try:
        content = {'action': 'show_cards', 'data': cards_to_show}
        await manager.send_data_to(content,match_id,player_id)
    except:
        print("Error en show_cards")