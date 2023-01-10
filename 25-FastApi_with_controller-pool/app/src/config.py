
from pydantic import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    user: str
    database: str
    host: str
    password: str
    port: int
    
   
    class Config:
        env_file = ".env"
       
@lru_cache()        
def get_settings():
    return Settings()
