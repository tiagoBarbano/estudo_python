from fastapi import APIRouter, Body, HTTPException, status, Depends, Request, Response
from app.schema import UserSchema, UserSchemaUpdate
from app.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.repository import *
from fastapi_cache.decorator import cache
from fastapi_cache.coder import JsonCoder
from app.config import key_all_users, key_user_by_id

router = APIRouter()


@router.get("/",
            status_code=status.HTTP_200_OK,
            response_model=list[UserSchema])
@cache(expire=60,
       coder=JsonCoder,
       key_builder=key_all_users,
       namespace="GetAllUsers")
async def get_users_default(db: AsyncSession = Depends(get_db)):
    return await get_all_users(db)


@router.get("/{id}")
@cache(expire=60,
       coder=JsonCoder,
       key_builder=key_user_by_id,
       namespace="GetUsersById")
async def get_user_data(id: int,
                        request: Request,
                        response: Response,
                        db: AsyncSession = Depends(get_db)):
    user = await get_user_by_id(db, id)

    if user:
        return user

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="User not found")


@router.post("/",
             status_code=status.HTTP_201_CREATED,
             response_model=UserSchema)
async def new_user(user: UserSchemaUpdate = Body(...),
                   db: AsyncSession = Depends(get_db)):
    try:
        return await add_user(db, user)
    except HTTPException:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="User ErroR")


@router.put("/{id}", status_code=status.HTTP_200_OK)
async def update_user_data(id: int,
                           req: UserSchemaUpdate = Body(...),
                           db: AsyncSession = Depends(get_db)):
    try:
        flag_update = await update_user(db, id, req)

        if flag_update:
            return {"message": "User Updated"}

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User not found")
    except HTTPException as ex:
        raise HTTPException(status_code=ex.status_code, detail=ex.detail)


@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def delete_user_data(id: int, db: AsyncSession = Depends(get_db)):
    try:
        flag_delete = await delete_user(db, id)
        if flag_delete:
            return {"message": "User Deleted"}

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User not found")
    except HTTPException as ex:
        raise HTTPException(status_code=ex.status_code, detail=ex.detail)
