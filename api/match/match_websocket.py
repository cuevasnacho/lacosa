from pydantic import *
from api.player.player import get_jugador
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
from pony.orm import db_session
from db.database import Lobby
from api.websocket import ConnectionManager

router = APIRouter()

manager = ConnectionManager()

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
            if ws['action'] == 'show_cards':
                pass
            
    except WebSocketDisconnect:
        manager.disconnect(websocket,match_id,player_id)
        content = "Websocket desconectado"
        return JSONResponse(content = content, status_code = 200) 
