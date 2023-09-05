from app.schema import ApoliceSchema, ApoliceSchemaUpdate
from app.model import UserModel
from sqlalchemy import update, delete, Text, func, cast
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.encoders import jsonable_encoder
from sqlalchemy.dialects.postgresql import JSONB, ARRAY, array


async def get_all_users(db: AsyncSession):
    async with db as session:
        query = select(UserModel)
        users = await session.execute(query)
        users = users.scalars().all()
        return users


async def get_user_by_id(db: AsyncSession, id: int) -> dict:
    query = select(UserModel).where(UserModel.id == id).order_by(UserModel.id)
    users = await db.execute(query)
    user = users.scalar_one_or_none()

    return user


async def get_user_by_id_product(db: AsyncSession, id_product: str) -> dict:
    elem = func.jsonb_array_elements(UserModel.detalhe, type_=JSONB).column_valued("productid")
    print(select(elem))

    stmt = select(UserModel).where(
            cast("example code", ARRAY(Text)).contained_by(
                array([select(elem['code'].astext).scalar_subquery()])
            )
        )
    print(stmt)




    users = await db.execute(query)
    user = users.scalars().all()
    return user    

    # query = text("""SELECT arr.item_object
    #             FROM apolice a, jsonb_array_elements(a.detalhe)
    #             with ordinality arr(item_object, position) 
    #             WHERE item_object->>'productid' = '{id_product}'
    #             ORDER BY id;""".format(id_product=id_product))
    # async with db as session:
    #     query = select(UserModel).where(UserModel.detalhe.op('->>')('productid') == id_product)
    #     users = await session.execute(query)
    #     users = users.scalars().all()
    #     return users

        # query = select(UserModel).filter(UserModel.detalhe['id_product'] == id_product)

        # users = await db.execute(query)
        # user = users.scalars().all()
        # return user


async def add_user(db: AsyncSession,
                   req: ApoliceSchema) -> ApoliceSchema:
    new_user = UserModel(id=req.id,
                         create_time=req.create_time,
                         detalhe=jsonable_encoder(req.detalhe))
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
