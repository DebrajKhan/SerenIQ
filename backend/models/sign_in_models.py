from pydantic import BaseModel

class LogInData(BaseModel):
    email:str

class LogInDataAuth(LogInData):
    password:str  

