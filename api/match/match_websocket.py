from pydantic import *
from api.player.player import get_jugador
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
from pony.orm import db_session
from db.database import Match
from api.websocket import ConnectionManager
from api.player.finalize_action import fullfile_action

router = APIRouter()

manager = ConnectionManager()

manager_activo = ConnectionManager()
show_cards_to_all = ['whisky']

@db_session
async def first_player(match_id):
    player_id = (Match.get(match_id = match_id)).match_currentP
    content = {'action' : 'iniciar_turno','data' : {}}
    await manager_activo.send_data_to(content, match_id, player_id)

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
                #data ={defensor_id, attack_card_name}
                fullfile_action(ws['data']['defensor_id'], ws['data']['attack_card_name'])
                # ver si es nescesario enviar un mensaje
            
            elif ws['action'] == 'end_game':
                content = {'action' : 'end_game', 'data' : ws['data']}
                await manager.broadcast(content,match_id)

            elif ws['action'] == 'message':
                content = {'action': 'message', 'data': ws['data']}
                await manager.broadcast(content,match_id)
        
    except WebSocketDisconnect:
        manager.disconnect(websocket,match_id,player_id)
        content = "Websocket desconectado"
        return JSONResponse(content = content, status_code = 200) 
"""
"""
@router.websocket("/ws/match/activo/{match_id}/{player_id}")
async def match_websocket(websocket : WebSocket,match_id : int, player_id : int):  
    await manager_activo.connect(websocket,match_id,player_id)
    try:
        print("antes de enviar el mensaje")
        await first_player(match_id)
        print("despues de enviar el mensaje")
        while True:
             ws = await websocket.receive_json()

    except WebSocketDisconnect:
        manager_activo.disconnect(websocket,match_id,player_id)
        content = "Websocket desconectado"
        return JSONResponse(content = content, status_code = 200) 
