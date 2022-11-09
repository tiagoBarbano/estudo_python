from fastapi import APIRouter, Body, HTTPException, status
from app.schema import UserSchema, UpdateUserModel
from app.database import (add_user, get_all_users, get_user_by_id, update_user,
                          delete_user)

router = APIRouter()


@router.post("/",
             response_model=UserSchema,
             status_code=status.HTTP_201_CREATED)
async def new_user(user: UserSchema = Body(...)):
    return await add_user(user)


@router.get("/", response_model=list[UserSchema],
            status_code=status.HTTP_200_OK)
async def get_users():
    return await get_all_users()


@router.get("/{id}", response_model=UserSchema, status_code=status.HTTP_200_OK)
async def get_user_data(id: str):
    if (user := await get_user_by_id(id)) is not None:
        return user

    raise HTTPException(status_code=404, detail=f"User {id} not found")


@router.put("/{id}", status_code=status.HTTP_200_OK)
async def update_user_data(id: str, req: UpdateUserModel = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_user = await update_user(id, req)

    if updated_user:
        return {"id": format(id), "message": "User Updated"}

    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                        detail="User Not Updated")


@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def delete_user_data(id: str):
    user = await delete_user(id)

    if user:
        return {"id": format(id), "message": "User Deleted"}

    raise HTTPException(status_code=404, detail=f"User {id} not found")
