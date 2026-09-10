from fastapi import APIRouter, Depends, HTTPException, status
from core.security import get_current_user_email
from databases.database import users_collection

router = APIRouter()

@router.get("/my-friends")
async def get_my_friends(current_email:str = Depends(get_current_user_email)):

    user = await users_collection.find_one({"email": current_email})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User not found"
        )

    friend_emails = user.get("friends", [])
    if not friend_emails:
        return []

    cursor = users_collection.find({"email": {"$in": friend_emails}})
    friends_data = await cursor.to_list(length=50)

    result = []
    for friend in friends_data:
        result.append({
            "first_name": friend.get("first_name"),
            "last_name": friend.get("last_name"),
            "email": friend.get("email"),
            "is_online": True 
        })
        
    return result
