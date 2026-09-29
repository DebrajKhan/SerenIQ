from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import Dict
from datetime import datetime, timezone
from databases.database import users_message_collection

router = APIRouter()

def get_room_id(email1:str, email2:str):
    clean1 = email1.strip().lower()
    clean2 = email2.strip().lower()
    return "_".join(sorted([clean1, clean2]))

class ConnectionManager():
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, websocket:WebSocket, email:str):
        await websocket.accept()
        clean_email = email.strip().lower()
        self.active_connections[clean_email] = websocket

    def disconnect(self, email:str):
        clean_email = email.strip().lower()
        if clean_email in self.active_connections:
            del self.active_connections[clean_email]

    async def send_personal_message(self, message:str, sender_email:str, target_email:str):
        
        clean_sender = sender_email.strip().lower()
        clean_target = target_email.strip().lower()
        
        room_id = get_room_id(clean_sender, clean_target)
        msg_doc = {
            "room_id" : room_id,
            "sender_email" : clean_sender,
            "target_email" : clean_target,
            "message" : message,
            "timestamp" : datetime.now(timezone.utc),
            "is_read" : False
        }

        await users_message_collection.insert_one(msg_doc)

        if clean_target in self.active_connections:
            payload = {
                "sender_email" : clean_sender,
                "message" : message,
                "timestamp" : msg_doc["timestamp"].isoformat()
            }
            await self.active_connections[clean_target].send_json(payload)
            

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