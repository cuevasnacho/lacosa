from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket : WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket : WebSocket):
        self.active_connections.remove(websocket)

    async def send_data(self, data, websocket : WebSocket):
        await websocket.send_json(data)

    async def broadcast(self, data):
        for connection in self.active_connections:
            await connection.send_json(data)     
