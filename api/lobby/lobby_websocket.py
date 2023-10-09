from fastapi import WebSocket
import json 

class ConnectionManager:
    def __init__(self):
        self.active_connctions: list[WebSocket]

    async def connect(self, websocket : WebSocket):
        await websocket.accept()
        self.active_connctions.append(websocket)

    def disconnect(self, websocket : WebSocket):
        self.active_connctions.remove(websocket)

    async def send_data(self, data : json, websocket : WebSocket):
        await websocket.send_json(data)

    async def broadcast(self, data : json):
        for connection in self.active_connctions:
            await connection.send_json(data)     
