from .schema import ItemSchema, ItemSchemaUpdate
from .repository import *


async def get_items_default():
    return await get_all_items()


async def get_item_data(id: int):
    return  await get_item_by_id(id)
  

async def new_item(item: ItemSchema):
    return await add_item(item)


async def update_item_data(id: int, req: ItemSchemaUpdate):
    return await update_item(id, req)


async def delete_item_data(id: int):
    return await delete_item(id)

