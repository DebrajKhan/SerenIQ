from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import Dict

router = APIRouter()

class ConnectionManager():
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, websocket:WebSocket, email:str):
        await websocket.accept()
        self.active_connections[email] = websocket

    def disconnect(self, email:str):
        if email in self.active_connections:
            del self.active_connections[email]

    async def send_personal_message(self, message:str, sender_email:str, target_email:str):
        if target_email in self.active_connections:
            payload = {
                "sender_email" : sender_email,
                "message" : message
                }
            
            await self.active_connections[target_email].send_json(payload)

manager = ConnectionManager()

@router.websocket("/ws/chat/{user_email}")
async def websocket_endpoint(websocket:WebSocket, user_email : str):
    await manager.connect(websocket, user_email)
    try:
        while True:
            data = await websocket.receive_json()
            target = data.get("target_email")
            message = data.get("message")
            await manager.send_personal_message(message, user_email, target)

    except WebSocketDisconnect:
        manager.disconnect(user_email)
