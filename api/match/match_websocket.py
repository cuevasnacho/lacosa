from pydantic import *
from api.player.player import get_jugador
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
from pony.orm import db_session
from db.database import Match,Player
from api.websocket import ConnectionManager
from api.player.finalize_action import fullfile_action
from api.utilsfunctions import can_exchange, get_next_player_id


router = APIRouter()

manager = ConnectionManager()

manager_activo = ConnectionManager()
show_cards_to_all = ['whisky']

@db_session
async def follow_game(match_id):

    match = Match[match_id]
    player_id = match.match_currentP
    motive = "inicio_intercambio"
    next_player_id = get_next_player_id(player_id, match_id)
    if can_exchange(next_player_id,match_id):
        content = { 'action' : 'iniciar_intercambio', 'data':{'motive' : motive, 'oponent_id': next_player_id}}
        await manager_activo.send_data_to(content,match_id,player_id)
    else:
        content = { 'action' : 'fin_turno', 'data':{}}
        await manager_activo.send_data_to(content,match_id,player_id)

@db_session
async def first_player(match_id,connection_id):
    player_id = (Match.get(match_id = match_id)).match_currentP
    if player_id == connection_id:
        content = {'action' : 'iniciar_turno','data' : {}}
        await manager_activo.send_data_to(content, match_id, player_id)

async def next_stage_revelaciones(player_id, match_id, data):
    if data == False:
        content = {'action': 'revelaciones', 'data': {}}
        id_next = get_next_player_id(player_id, match_id)
        with db_session:
            match = Match[match_id]
            id_iniciador = match.match_currentP
        if id_next != id_iniciador:
            await manager.send_data_to(content, match_id, id_next)
        else:
            await follow_game(match_id)
    else:
        await follow_game(match_id)


@router.websocket("/ws/match/pasivo/{match_id}/{player_id}")
async def match_websocket(websocket : WebSocket,match_id : int, player_id : int):
    await manager.connect(websocket,match_id,player_id)
    try:
        while True:
            ws = await websocket.receive_json()
            if ws['action'] == 'discard_card':
                card_type = ws['data']
                content = {'action' : 'discard_card','data' : card_type} #forma de return para las cartas
                await manager.broadcast(content,match_id)

            elif ws['action'] == 'play_card':
                content_broadcast = {'action': 'play_card', 'data': ws['data']}
                await manager.broadcast(content_broadcast,match_id)

            elif ws['action'] == 'next_turn':
                content = {'action': 'next_turn', 'data': ws['data']}
                await manager.broadcast(content,match_id)

            elif ws['action'] == 'show_cards':
                if len(ws['data']['mostrar']) != 0:
                    content_personal = {'action': 'show_cards', 'data': ws['data']['mostrar']}
                    if ws['data']['card'] in show_cards_to_all:
                        await manager.broadcast(content_personal,match_id)
                    else:
                        await manager.send_data_to(content_personal, match_id, player_id)
            elif ws['action'] == 'notify_defense':
                #ws['data'] = {defensor_id,  attack_card_name,  atacante_id, atacante_username, card_defense_name}
                player_id = ws['data']['defensor_id']

                content = {'action': 'notify_defense', 'data': ws['data']}

                await manager.send_data_to(content, match_id, player_id)
            elif ws['action'] == 'play_defense':
                #data ={username_defensor, nombre_carta, username_atacante}
                content_broadcast = {'action': 'play_defense', 'data': ws['data']}
                await manager.broadcast(content_broadcast,match_id)
            elif ws['action'] == 'no_defense':
                #data ={defensor_id, attack_card_name, defense_from_exchange}
                fullfile_action(ws['data']['defensor_id'], ws['data']['attack_card_name'])
                await follow_game(match_id)
                # ver si es nescesario enviar un mensaje

            elif ws['action'] == 'end_game':
                content = {'action' : 'end_game', 'data' : ws['data']}
                await manager.broadcast(content,match_id)

            elif ws['action'] == 'message':
                content = {'action': 'message', 'data': ws['data']}
                await manager.broadcast(content,match_id)

            elif ws['action'] == 'revelaciones':
                await next_stage_revelaciones(player_id, match_id, ws['data'])

    except WebSocketDisconnect:
        manager.disconnect(websocket,match_id,player_id)
        content = "Websocket desconectado"
        return JSONResponse(content = content, status_code = 200)

@router.websocket("/ws/match/activo/{match_id}/{player_id}")
async def match_websocket(websocket : WebSocket,match_id : int, player_id : int):
    await manager_activo.connect(websocket,match_id,player_id)
    try:
        await first_player(match_id,player_id)
        while True:
             ws = await websocket.receive_json()

    except WebSocketDisconnect:
        manager_activo.disconnect(websocket,match_id,player_id)
        content = "Websocket desconectado"
        return JSONResponse(content = content, status_code = 200)
