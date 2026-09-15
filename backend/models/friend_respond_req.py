from pydantic import BaseModel, EmailStr

class RespondRequest(BaseModel):
    email : EmailStr
    action : str