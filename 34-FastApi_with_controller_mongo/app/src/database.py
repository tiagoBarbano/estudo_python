import os
import motor.motor_asyncio
from .config import get_settings

settings = get_settings()

client = motor.motor_asyncio.AsyncIOMotorClient(settings.mongo_uri)

database = client.test

user_collection = database.get_collection("users_python")