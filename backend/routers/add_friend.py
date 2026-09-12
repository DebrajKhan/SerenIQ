from fastapi import APIRouter, Depends, HTTPException, status
from models.add_friend_req import AddFriendRequest
from core.security import get_current_user_email
from databases.database import users_collection

router = APIRouter()

@router.get("/search-users")
async def search_users(name: str):
    query = {
        "$or": [
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
async def add_friend(request: AddFriendRequest, current_email: str = Depends(get_current_user_email)):
    
    if str(request.friend_email).lower() == current_email.lower():
        raise HTTPException(status_code=400, detail="Cannot add yourself!")

    
    current_user = await users_collection.find_one({"email": {"$regex": f"^{current_email}$", "$options": "i"}})
    if not current_user:
        raise HTTPException(status_code=404, detail="Your account was not found.")

    
    target_friend = await users_collection.find_one({"email": {"$regex": f"^{request.friend_email}$", "$options": "i"}})
    if not target_friend:
        raise HTTPException(status_code=404, detail="Friend not found in the database.")

    
    exact_friend_email = target_friend.get("email")

    if exact_friend_email in current_user.get("friends", []):
        raise HTTPException(status_code=400, detail="This person is already in your friend list!")

    
    await users_collection.update_one(
        {"_id": current_user["_id"]},
        {"$addToSet": {"friends": exact_friend_email}}
    )

    return {"message": f"Successfully added {target_friend.get('first_name')}!"}