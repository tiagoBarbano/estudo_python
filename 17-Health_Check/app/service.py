from fastapi import APIRouter, Body, HTTPException, status, Depends, Request, Response
from app.schema import UserSchema, UserSchemaUpdate
from app.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.repository import *
from fastapi_cache.decorator import cache
from fastapi_cache.coder import JsonCoder
from app.config import key_all_users, key_user_by_id, key_add_user, logger

router = APIRouter()


@router.get("/",
            status_code=status.HTTP_200_OK,
            response_model=list[UserSchema])
@cache(expire=60,
       coder=JsonCoder,
       key_builder=key_all_users,
       namespace="GetAllUsers")
async def get_users_default(db: AsyncSession = Depends(get_db)):
    try:
        logger.info("REALIZAR CONSULTA DE TODOS OS USUARIOS")
        
        return await get_all_users(db)
    except HTTPException as ex:
        logger.exception("ERRO AO BUSCAR OS USUÁRIOS")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=ex.detail)
            

@router.get("/{id}")
@cache(expire=60,
       coder=JsonCoder,
       key_builder=key_user_by_id,
       namespace="GetUsersById")
async def get_user_data(id: int,
                        request: Request,
                        response: Response,
                        db: AsyncSession = Depends(get_db)):
    try:
        logger.info("BUSCAR O USUÁRIO POR ID: %d", id)
        user = await get_user_by_id(db, id)

        if user:
            logger.info("USUARIO ENCONTRADO: %s", user.__dict__)            
            return user

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User not found")
    except HTTPException as ex:
        logger.exception("ERRO AO BUSCAR O USUÁRIO: %s", ex.detail)
        if(hasattr(ex, 'status_code')):
            raise HTTPException(status_code=ex.status_code,
                               detail=ex.detail)
                    
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=ex.detail)    

@router.post("/",
             status_code=status.HTTP_201_CREATED,
             response_model=UserSchema)
@cache(expire=20,
       coder=JsonCoder,
       key_builder=key_add_user,
       namespace="AddUsers")
async def new_user(user: UserSchemaUpdate, db: AsyncSession = Depends(get_db)):
    try:
        logger.info("INCLUIR NOVO USUÁRIO: %s", user)
        
        new_user = await add_user(db, user)
        
        logger.info("NOVO USUÁRIO INCLUIDO %s", new_user.__dict__)
        return new_user
    except HTTPException as ex:
        logger.exception("ERRO AO CADASTRAR O USUÁRIO: %s", ex.detail)
        if(hasattr(ex, 'status_code')):
            raise HTTPException(status_code=ex.status_code,
                               detail=ex.detail)
                    
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=ex.detail)    


@router.put("/{id}", status_code=status.HTTP_200_OK)
async def update_user_data(id: int,
                           req: UserSchemaUpdate = Body(...),
                           db: AsyncSession = Depends(get_db)):
    try:
        logger.info("ALTERAR USUÁRIO - id: %d - BODY: %s - ", id, req)
        
        flag_update = await update_user(db, id, req)

        if flag_update:
            logger.info("USUÁRIO ALTERADO")
            return {"message": "User Updated"}

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User not found")
    except HTTPException as ex:
        logger.exception("ERRO AO ALTERAR O USUÁRIO: %s", ex.detail)
        if(hasattr(ex, 'status_code')):
            raise HTTPException(status_code=ex.status_code,
                               detail=ex.detail)
                    
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=ex.detail)    


@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def delete_user_data(id: int, db: AsyncSession = Depends(get_db)):
    try:
        logger.info("DELATAR USUÁRIO - id: %d", id)
        
        flag_delete = await delete_user(db, id)
        
        if flag_delete:
            logger.info("USUÁRIO DELETADO")
            return {"message": "User Deleted"}

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User not found")
    except HTTPException as ex:
        logger.exception("ERRO AO DELETAR O USUÁRIO: %s", ex.detail)
        if(hasattr(ex, 'status_code')):
            raise HTTPException(status_code=ex.status_code,
                               detail=ex.detail)
                    
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=ex.detail)    
