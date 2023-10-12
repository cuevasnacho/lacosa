from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        self.active_connections = {}

    async def connect(self, websocket : WebSocket,lobby_id,player_id):
        await websocket.accept()
        if lobby_id not in self.active_connections:
            self.active_connections[lobby_id] = []
        self.active_connections[lobby_id].append((player_id, websocket))
        
    def disconnect(self, websocket : WebSocket,lobby_id,player_id):
        self.active_connections[lobby_id].remove((player_id,websocket))

    async def send_data(self, data, websocket : WebSocket):
        await websocket.send_json(data)

    async def broadcast(self, data, lobby_id):
        if lobby_id in self.active_connections:
            for connection in self.active_connections[lobby_id]:
                await connection[1].send_json(data)     