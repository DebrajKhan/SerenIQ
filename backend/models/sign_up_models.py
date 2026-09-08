from pydantic import BaseModel, EmailStr


class SignUpData(BaseModel):
    first_name:str
    last_name:str
    email:EmailStr
    address:str
    country:str
    state:str
    city:str
    pincode:int

class SignUpDataAuth(SignUpData):
    password:str      