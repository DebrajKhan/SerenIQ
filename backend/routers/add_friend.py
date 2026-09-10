from fastapi import APIRouter, Depends, HTTPException, status
from models.add_friend_req import AddFriendRequest
from core.security import get_current_user_email
from databases.database import users_collection
router = APIRouter()

@router.get("/search-users")
async def search_users(name:str):
    query = {
        "$or":[
            {"first_name": {"$regex": name, "$options": "i"}},
            {"last_name": {"$regex": name, "$options": "i"}}
        ]
    }

    cursor = users_collection.find(query).limit(5)
    users = await cursor.to_list(length=5)

    results = []
    for user in users:
        results.append({
            "first_name": user.get("first_name"),
            "last_name": user.get("last_name"),
            "email": user.get("email"),
            "state": user.get("state", "Unknown State"),
            "country": user.get("country", "Unknown Country")
        })
        
    return results

@router.post("/add-friend")
async def add_friend(request:AddFriendRequest, current_email: str = Depends(get_current_user_email)):
    if request.friend_email == current_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail = "Cannot add yourself!"
        )

    current_user = await users_collection.find_one({"email" : current_email})
    if current_user and request.friend_email in current_user.get("friends", []):
        raise HTTPException(status_code=400, detail="This person is already in your friend list!")

    target_friend = await users_collection.find_one({"email" : request.friend_email})
    if not target_friend:
        raise HTTPException(status_code=404, detail="User not found in the database.")

    await users_collection.update_one(
        {"email": current_email},
        {"$addToSet": {"friends": request.friend_email}}
    )

    return {"message": f"Successfully added {target_friend['first_name']} to your friends list!"}

