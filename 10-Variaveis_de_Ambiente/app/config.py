from functools import lru_cache
from pydantic import BaseSettings
import motor.motor_asyncio


class Settings(BaseSettings):
    password_mongodb: str
    user_mongodb: str
    host_mongodb: str
    collection_mongodb: str
    database_mongodb: str

    class Config:     
        env_file = '.env'
        secrets_dir = '/var/run'  
        env_file_encoding = 'utf-8'
        
@lru_cache()
def get_settings():
    return Settings()


def start_mongodb():
    set = get_settings()

    mongodb_uri = f'mongodb+srv://{set.user_mongodb}:{set.password_mongodb}@{set.host_mongodb}'
    client = motor.motor_asyncio.AsyncIOMotorClient(mongodb_uri)
    database = client[set.database_mongodb]
    user_collection = database.get_collection(set.collection_mongodb)

    return user_collection