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

@router.get("/ws/unread-counts/{user_email}")
async def get_unread_counts(user_email : str):
    pipeline = [
        {
            "$match":
            {
                "target_email" : user_email,
                "is_read" : False 
            }
        },
        {
            "$group":
            {
                "_id" : "$sender_email", 
                "count" : {"$sum" : 1}
            }
        }
    ]

    cursor = users_message_collection.aggregate(pipeline)
    result = cursor.to_list(length = 100)
    return {doc["_id"] : doc["count"] for doc in result} 


@router.get("/ws/mark-read")
async def mark_messages_read(user_email:str, sender_email:str):
    await users_message_collection.update_many(
        {"target_email" : user_email, "sender_email" : sender_email, "is_read" : False},
        {"$set" : {"is_read" : True}}
    )

    return {"status" : "success"}