from pydantic import BaseModel, EmailStr

class LogInData(BaseModel):
    email:EmailStr

class LogInDataAuth(LogInData):
    password:str  

