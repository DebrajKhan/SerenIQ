from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import Dict
from datetime import datetime, timezone
from databases.database import users_message_collection

router = APIRouter()

def get_room_id(email1:str, email2:str):
    return "_".join(sorted([email1,email2]))

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
        room_id = get_room_id(sender_email, target_email)
        msg_doc = {
            "room_id" : room_id,
            "sender_email" : sender_email,
            "target_email" : target_email,
            "message" : message,
            "timestamp" : datetime.now(timezone.utc)
        }

        await users_message_collection.insert_one(msg_doc)

        if target_email in self.active_connections:
            payload = {
                "sender_email" : sender_email,
                "message" : message,
                "timestamp" : msg_doc["timestamp"].isoformat()
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


@router.get("/ws/chat-history")
async def get_chat_history(sender_email:str, target_email:str, sk:int = 0):
    room_id = get_room_id(sender_email, target_email)

    cursor = users_message_collection.find({"room_id":room_id}).sort("timestamp", -1).skip(sk).limit(50)
    messages = await cursor.to_list(length=50)

    history = []
    for msg in messages:
        history.append(
            {
            "sender_email": msg["sender_email"],
            "message": msg["message"],
            "timestamp": msg["timestamp"].isoformat()
            }
        )

    return history    