
from db.database import Lobby, Match, Player
from pony.orm import db_session
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from api.lobby.lobby_websocket import ConnectionManager
from fastapi.responses import JSONResponse
from definitions import match_status
from pydantic import BaseModel
from pony import orm 
import json

router = APIRouter()

manager = ConnectionManager()

class data_item(BaseModel):
    lobby_id : int
    match_id : int    
    lobby_name : str
    number_of_players : int
    host_name : str
    max_players : int
    min_players : int
    is_private : bool

@db_session 
def get_not_initialized_matches():
    response = [] 

    #query que obtiene de todas las partidas disponibles y los datos para completar data_item
    data_from_available_matches = orm.select( 
        (lobby.lobby_id, match.match_id, lobby.lobby_name, lobby.lobby_pcount, lobby.lobby_max, lobby.lobby_min, lobby.lobby_password) 
        for match in Match for lobby in Lobby 
            if lobby.lobby_match.match_id == match.match_id and match.match_status == match_status.NOT_INITIALIZED.value) 

    #crear lista de objetos data_item 
    for data in data_from_available_matches:
        match_id  = data[1] #query adicional para obtener el host_name
        private_game = True if data[6] != None else False
        host_name = Player.select(lambda player : 
                            player.player_current_match_id.match_id == match_id and player.player_isHost).first()

        if host_name != None:
            response.append(data_item(lobby_id = data[0], match_id = data[1], lobby_name = data[2], number_of_players = data[3],
                                    host_name = host_name.player_name, max_players = data[4], min_players = data[5], is_private = private_game))        
    
    #convertir y devolver la lista de objetos data_item en formato json
    return json.loads(json.dumps([obj.dict() for obj in response]))

@router.get("/partidas/listar")
async def show_matches():
    try:
        content = get_not_initialized_matches() 
        return JSONResponse(content = content, status_code = 200) 
    except: 
            content = "No hay partidas disponibles"
            return JSONResponse(content = content, status_code = 404) 

'''
@router.get("/partidas/listar")
async def show_matches(websocket : WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            try :
                data = await websocket.receive_json()
                content = get_not_initialized_matches() 
                response = JSONResponse(content = content, status_code = 200) 
            except :
                content = "No hay partidas disponibles"
                response = JSONResponse(content = content, status_code = 404) 
            await manager.send_data(response)
            await manager.broadcast(response)
    except WebSocketDisconnect: 
            manager.disconnect(websocket)
            content = "Websocket desconectado"
            return JSONResponse(content = content, status_code = 200) 
'''    

