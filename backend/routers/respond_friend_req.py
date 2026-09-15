from fastapi import APIRouter, Depends, HTTPException, status
from core.security import get_current_user_email
from models.friend_respond_req import RespondRequest
from databases.database import users_collection

router = APIRouter()

@router.post("/respond-friend-req")
async def respond_friend_req(request:RespondRequest, current_email:str = Depends(get_current_user_email)):
    current_user = await users_collection.find_one({"email" : {"$regex" : f"^{current_email}$", "$options" : "i"}})
    if not current_user:
        raise HTTPException(status_code=404, detail="User not found")
        
    exact_current_email = current_user.get("email")
    exact_sender_email = request.email

    if(request.action == "accept"):
        await users_collection.update_one(
            {"_id": current_user["_id"]},
            {"$addToSet": {"friends": exact_sender_email}}
        )
        await users_collection.update_one(
            {"email": exact_sender_email},
            {"$addToSet": {"friends": exact_current_email}}
        )

    await users_collection.update_one(
        {"_id": current_user["_id"]},
        {"$pull": {"pending_requests": exact_sender_email}}
    )

    return {"message": f"Request {request.action}ed successfully."}    
