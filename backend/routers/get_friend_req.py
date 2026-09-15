from fastapi import APIRouter, Depends, HTTPException, status
from core.security import get_current_user_email
from databases.database import users_collection

router = APIRouter()

@router.get("/friend-req")
async def get_friend_requests(current_email : str = Depends(get_current_user_email)):
    try:
        user = await users_collection.find_one({"email" : {"$regex" : f"^{current_email}$", "$options" : "i"}})
        if not user:
            raise HTTPException(
                status_code= status.HTTP_404_NOT_FOUND,
                detail = "Email not found!"
            )

        pending_emails = user.get("pending_requests", [])
        if not pending_emails:
            return []

        cursor = users_collection.find({"email" : {"$in" : pending_emails }})
        request_data = await cursor.to_list(length=50)

        result = []
        for req in request_data:
            result.append({
            "first_name": req.get("first_name"),
            "email": req.get("email")
        })
        return result

    except HTTPException:
        raise

    except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Internal Server error: {e}"
            )