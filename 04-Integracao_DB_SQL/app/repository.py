from app.schema import UserSchema
from app.model import UserModel
from sqlalchemy import update, delete
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status
from app.database import async_session

# Retrieve all users present in the database
async def get_all_users():
    try:
        async with async_session() as session:
            query = select(UserModel)
            users = await session.execute(query)
            users = users.scalars().all()
            await session.close()
            return users
    except SQLAlchemyError as sql_ex:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(sql_ex))
    except HTTPException as http_ex:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(http_ex))
    finally:
        await session.close()    
    
# Retrieve a user with a matching ID
async def get_user_by_id(db: AsyncSession, id: int) -> dict:
    query = select(UserModel).where(UserModel.id == id)
    users = await db.execute(query)
    user = users.scalar_one_or_none()
    await db.close()
    return user

# Add a new user into to the database
async def add_user(db: AsyncSession, user_data: UserSchema) -> UserSchema:
    new_user = UserModel(nome=user_data.nome, idade=user_data.idade, email=user_data.email)
    await db.add(new_user)
    await db.commit()
    await db.close()
    return new_user

# Update a user with a matching ID
async def update_user(db: AsyncSession, id: str, data: UserSchema):
    query = (update(UserModel).where(UserModel.id == id).values(data).execution_options(synchronize_session="fetch"))
    
    await db.execute(query)
    
    try:
        await db.commit()
    except Exception:
        await db.rollback()
        raise

# Delete a user from the database
async def delete_user(db: AsyncSession, id: int):
    query = delete(UserModel).where(UserModel.id == id)
    await db.execute(query)
    try:
        await db.commit()
    except Exception:
        await db.rollback()
        raise
    return True