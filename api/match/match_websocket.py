from pydantic import *
from api.player.player import get_jugador
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
from pony.orm import db_session
from db.database import Lobby
from api.websocket import ConnectionManager

router = APIRouter()

@db_session
def get_lobby_id(id_match):
    lobby = Lobby.get(id_match)
    print(lobby.lobby_id)
    return lobby.lobby_id

'''
@router.websocket("/ws/match/{match_id}/{player_id}")
async def players_in_lobby(match_id : int, player_id : int, websocket : WebSocket):  
    await manager.connect(websocket,get_lobby_id(match_id),player_id)
    #try:
    while True:
        ws = await websocket.receive_json()
        if ws['action'] == 'discard_card': 
            card_type = ws['data']
            content = {'action' : 'discard_card','data' : card_type }
            await manager.broadcast(content,get_lobby_id(match_id))
        
#    except WebSocketDisconnect:
#        manager.disconnect(websocket,get_lobby_id(match_id),player_id)
#        content = "Websocket desconectado"
#        return JSONResponse(content = content, status_code = 200) 
'''