from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    mongodb_url : str
    secret_key : str
    algorithm : str = "HS256"
    access_token_time :int =  5

    class Config:
        env_file = ".env"

settings = Settings()   
