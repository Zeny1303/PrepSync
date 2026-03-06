from fastapi import WebSocket

class ConnectionManager:

    def __init__(self):
        self.rooms = {}

    async def connect(self, websocket: WebSocket, room_id: str):
        await websocket.accept()

        if room_id not in self.rooms:
            self.rooms[room_id] = []

        self.rooms[room_id].append(websocket)

    def disconnect(self, websocket: WebSocket, room_id: str):

        if room_id in self.rooms:
            self.rooms[room_id].remove(websocket)

    async def broadcast(self, room_id: str, message: dict):

        if room_id not in self.rooms:
            return

        for connection in self.rooms[room_id]:
            await connection.send_json(message)


manager = ConnectionManager()