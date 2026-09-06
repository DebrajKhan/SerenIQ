from pydantic import BaseModel

class LogInData(BaseModel):
    email:str

class LogInDataAuth(LogInData):
    password:str  


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