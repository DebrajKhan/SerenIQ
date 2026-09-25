from fastapi import APIRouter
from databases.database import users_message_collection
from chat_socket import get_room_id

router = APIRouter(prefix="/ws")


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