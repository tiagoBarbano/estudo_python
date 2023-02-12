from .schema import UserSchema, UserSchemaUpdate
from .repository import *



async def get_users_default():
    return await get_all_users()


async def get_user_data(id: int):
    return  await get_user_by_id(id)
  

async def new_user(user: UserSchema):
    return await add_user(user)


async def update_user_data(id: int, req: UserSchemaUpdate):
    return await update_user(id, req)


async def delete_user_data(id: int):
    return await delete_user(id)

async def receve_msg_kafka(msg: dict):
    print("Hellow")
    print("{}:{:d}:{:d}: key={} value={} timestamp_ms={}".format(msg.topic, msg.partition, msg.offset, msg.key, msg.value, msg.timestamp))
    tst = msg.value(0).decode('utf-8')
    print(tst)
    newUser = UserSchema(nome_item=tst['nome_item'], num_item=tst['num_item'], myuuid=tst['id'])
    print(newUser)