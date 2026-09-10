from pydantic import BaseModel, EmailStr

class AddFriendRequest(BaseModel):
    friend_email: EmailStr