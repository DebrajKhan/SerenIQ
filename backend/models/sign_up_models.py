from pydantic import BaseModel


class SignUpData(BaseModel):
    first_name:str
    last_name:str
    email:str
    address:str
    country:str
    state:str
    city:str
    pincode:int

class SignUpDataAuth(SignUpData):
    password:str      