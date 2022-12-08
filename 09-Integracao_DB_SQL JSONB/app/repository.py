from app.schema import ApoliceSchema, ApoliceSchemaUpdate
from app.model import UserModel
from sqlalchemy import update, delete, text, func
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession


async def get_all_users(db: AsyncSession):
    async with db as session:
        query = select(UserModel)
        users = await session.execute(query)
        users = users.scalars().all()
        await session.close()
        return users


async def get_user_by_id(db: AsyncSession, id: int) -> dict:
    query = select(UserModel).where(UserModel.id == id)
    users = await db.execute(query)
    user = users.scalar_one_or_none()
    await db.close()
    return user


async def get_user_by_id_product(db: AsyncSession, id_product: str) -> dict:
    query = text("""SELECT arr.item_object
                    FROM apolice, jsonb_array_elements(apolice.detalhe) 
                    with ordinality arr(item_object, position) 
                    WHERE item_object->>'productid' = '{id_product}';""".format(id_product=id_product))
    
    print(query)
    
    users = await db.execute(query)
    user = users.scalars().fetchall()
    return user


async def add_user(db: AsyncSession,
                   user_data: ApoliceSchemaUpdate) -> ApoliceSchema:
    new_user = UserModel(nome=user_data.nome,
                         idade=user_data.idade,
                         email=user_data.email)
    db.add(new_user)
    await db.commit()
    return new_user


async def update_user(db: AsyncSession, id: str, data: ApoliceSchemaUpdate):
    query = (update(UserModel).where(UserModel.id == id).values(
        data.dict()).execution_options(synchronize_session="fetch"))
    updated_user = await db.execute(query)

    if updated_user:
        await db.commit()
        return True

    return False


async def delete_user(db: AsyncSession, id: int):
    query = delete(UserModel).where(UserModel.id == id)
    res = await db.execute(query)

    if res.rowcount == 1:
        await db.commit()
        return True

    return False
