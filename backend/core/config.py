from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    mongodb_url : str
    secret_key : str
    algorithm : str 
    access_token_time :int

    class Config:
        env_file = ".env"

settings = Settings()   
