from pydantic import *
from api.player.player import get_jugador
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
from pony.orm import db_session
from db.database import Lobby
from api.websocket import ConnectionManager

router = APIRouter()

manager = ConnectionManager()

show_cards_to_all = ['whiskey']

@router.websocket("/ws/match/{match_id}/{player_id}")
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
