
from pydantic import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    user_db: str
    database_db: str
    host_db: str
    password_db: str
    port_db: int
    url_token: str
    user_token: str
    password_token: str
    secret_key: str
    algorithm: str    
    url_items: str
   
    class Config:
        env_file = ".env"
       
@lru_cache()        
def get_settings():
    return Settings()
