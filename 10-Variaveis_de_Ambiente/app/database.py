from fastapi.encoders import jsonable_encoder
from app.schema import UserSchema
from app.config import start_mongodb

user_collection = start_mongodb()

async def get_all_users():
    users: UserSchema = []
    async for user in user_collection.find():
        users.append(user)
    return users


async def add_user(user_data: UserSchema) -> dict:
    user_request = jsonable_encoder(user_data)
    user = await user_collection.insert_one(user_request)
    new_user = await user_collection.find_one({"_id": user.inserted_id})
    return new_user


async def get_user_by_id(id: str) -> dict:
    user = await user_collection.find_one({"_id": id})
    if user:
        return user


async def update_user(id: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    user = await user_collection.find_one({"_id": id})
    if user:
        updated_user = await user_collection.update_one({"_id": id},
                                                        {"$set": data})
        if updated_user:
            return True
        return False


# Delete a user from the database
async def delete_user(id: str):
    user = await user_collection.find_one({"_id": id})
    if user:
        await user_collection.delete_one({"_id": id})
        return True
