from fastapi import APIRouter, Body, HTTPException, status, Depends
from app.schema import UserSchema, UserSchemaUpdate
from app.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.model import UserModel
from sqlalchemy import update, delete
from sqlalchemy.future import select
# from fastapi_pagination.ext.sqlalchemy_future import paginate
# from fastapi_pagination import Page, paginate, LimitOffsetPage

router = APIRouter()


#@router.get("/", status_code=status.HTTP_200_OK, response_model=Page[UserSchema])
#@router.get("/limit-offset", response_model=LimitOffsetPage[UserSchema])
@router.get("/", status_code=status.HTTP_200_OK, response_model=list[UserSchema])
async def get_users_default(db: AsyncSession = Depends(get_db)):
    #return await paginate(db, select(UserModel))
    async with db as session:
        query = select(UserModel)
        users = await session.execute(query)
        users = users.scalars().all()

        return users


@router.get("/{id}")
async def get_user_data(id: int, db: AsyncSession = Depends(get_db)):
    query = select(UserModel).where(UserModel.id == id)
    users = await db.execute(query)
    user = users.scalar_one_or_none()

    if user:
        return user

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="User not found")

@router.post("/",
             status_code=status.HTTP_201_CREATED,
             response_model=UserSchema)
async def add_user(user: UserSchemaUpdate = Body(...),
                   db: AsyncSession = Depends(get_db)):
    new_user = UserModel(nome=user.nome, idade=user.idade, email=user.email)
    db.add(new_user)
    await db.commit()
    return new_user


@router.put("/{id}", status_code=status.HTTP_200_OK)
async def update_user_data(id: int,
                           req: UserSchemaUpdate = Body(...),
                           db: AsyncSession = Depends(get_db)):
    query = (update(UserModel).where(
        UserModel.id == id).values(req.dict()).execution_options(
            synchronize_session="fetch"))
    updated_user = await db.execute(query)

    if updated_user:
        await db.commit()
        return HTTPException(status_code=status.HTTP_200_OK,
                        detail="User Updated")

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="User not found")


@router.delete("/{id}",
               status_code=status.HTTP_200_OK)
async def delete_user_data(id: int, db: AsyncSession = Depends(get_db)):
    query = delete(UserModel).where(UserModel.id == id)
    await db.execute(query)

    try:
        await db.commit()
        return HTTPException(status_code=status.HTTP_200_OK,
                        detail="User Deleted")
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="User ErroR")


