import datetime
from fastapi import APIRouter, Body, HTTPException, status, Depends
from app.db.model.model import UserModel
from app.schema.schema import User
from app.db.repository.user_repository import get_all_users, get_user_by_id, get_user_by_name
from app.utils.config import get_settings
from app.utils.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.utils.secutiry import get_current_active_user, get_password_hash


settings = get_settings()
router = APIRouter()


@router.post("/", 
             status_code=status.HTTP_201_CREATED, 
             response_model=User)
async def add_user(db: AsyncSession = Depends(get_db), user: User = Body(...)):
    
    findUser = await get_user_by_name(db, user.username)
    
    if findUser:
        raise HTTPException(status_code=400, detail="User Exists!!!")
    
    data_criacao = datetime.datetime.now()
    new_user = UserModel(username=user.username,
                        password=get_password_hash(user.password),    
                        email=user.email,
                        full_name=user.full_name,
                        disabled=user.disabled,    
                        id_cadastro=1,
                        data_criacao=data_criacao)
    
    user_created = await add_user(db=db, user=new_user)
    return user_created


@router.get("/", 
            status_code=status.HTTP_200_OK, 
            response_model=list[User])
async def get_users(db: AsyncSession = Depends(get_db),
                    current_user: User = Depends(get_current_active_user)):
    try:
        users = await get_all_users(db)

        if users == []:
            raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)

        return users
    except HTTPException as ex:
        if(hasattr(ex, 'status_code')):
            raise HTTPException(status_code=ex.status_code)
        
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get("/{id}", 
            status_code=status.HTTP_200_OK, 
            response_model=User)
async def get_user(id: int, 
                   db: AsyncSession = Depends(get_db), 
                   current_user: User = Depends(get_current_active_user)):
    user = await get_user_by_id(db, id)
    if user:
        return user
    
    raise HTTPException(status_code=status.HTTP_204_NO_CONTENT) 



@router.get("/{id}", 
            status_code=status.HTTP_200_OK, 
            response_model=User)
async def get_user(username: str, 
                   db: AsyncSession = Depends(get_db), 
                   current_user: User = Depends(get_current_active_user)):
    user = await get_user_by_name(db=db, username=username)
    
    if user:
        return user
    
    raise HTTPException(status_code=status.HTTP_204_NO_CONTENT) 




# @router.put("/{id}")
# async def update_user(id: str, req: User = Body(...), db: AsyncSession = Depends(get_db)):
#     data_criacao = datetime.datetime.now()
#     req.data_criacao = data_criacao
    
#     query = (update(UserModel).where(UserModel.id == id).values(req).execution_options(synchronize_session="fetch"))

#     updated_user = await db.execute(query)

#     try:
#         await db.commit()
#     except Exception:
#         await db.rollback()
#         raise    
    
#     if updated_user:
#         return updated_user

#     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Problema na atualizacao")

    
# @router.delete("/{id}")
# async def delete_user_data(id: str,  
#                            db: AsyncSession = Depends(get_db), 
#                            current_user: User = Depends(get_current_active_user)):
#     query = delete(UserModel).where(UserModel.id == id)
#     async with async_session() as session:
#         user_delete = await session.execute(query)
#         try:
#             await db.commit()
#         except Exception:
#             await db.rollback()
#             user_delete
#         return True