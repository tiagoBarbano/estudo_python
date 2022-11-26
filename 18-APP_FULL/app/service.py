from fastapi import APIRouter, Body, HTTPException, status, Depends, Request, Response, Header
from app.schema import UserSchema, UserSchemaUpdate
from app.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.repository import *
from fastapi_cache.decorator import cache
from fastapi_cache.coder import JsonCoder
from app.config import key_all_users, key_user_by_id, key_add_user, logger, Settings
from opentelemetry.instrumentation.aiohttp_client import create_trace_config
import uuid, aiohttp


router = APIRouter()

@router.get("/teste")
async def get_users_teste(request: Request,
                          response: Response):
    my_uuid = uuid.uuid4()
    
    try:
        logger.info("REALIZAR CONSULTA DE TODOS OS USUARIOS", 
                    extra={"tags": {"uuid": str(my_uuid),
                                    "service": "get_users_default"},})
        #trace_configs=[create_trace_config()]
        async with aiohttp.ClientSession() as session:
            async with session.get(Settings().url_teste, ssl=False) as response:
                if response.status != 200:
                    return -1 
                resposta = await response.json()
                
        logger.info("TERMINO CONSULTA DE TODOS OS USUARIOS", 
                    extra={"tags": {"uuid": str(my_uuid),
                                    "service": "get_users_default"},})
        return resposta
    except HTTPException as ex:
        logger.exception("ERRO AO BUSCAR OS USUÁRIOS")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=ex.detail)


@router.get("/",
            status_code=status.HTTP_200_OK,
            response_model=list[UserSchema])
@cache(expire=60,
       coder=JsonCoder,
       key_builder=key_all_users,
       namespace="GetAllUsers")
async def get_users_default(request: Request,
                            response: Response,
                            db: AsyncSession = Depends(get_db)):
    my_uuid = uuid.uuid4()
    
    try:
        logger.info("REALIZAR CONSULTA DE TODOS OS USUARIOS", 
                    extra={"tags": {"uuid": str(my_uuid),
                                    "service": "get_users_default"},})
        
        users = await get_all_users(db, my_uuid)

        logger.info("TERMINO CONSULTA DE TODOS OS USUARIOS", 
                    extra={"tags": {"uuid": str(my_uuid),
                                    "service": "get_users_default"},})
        return users
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
    my_uuid = uuid.uuid4()
    try:
        logger.info("BUSCAR O USUÁRIO POR ID: %d", id, 
                    extra={"tags": {"uuid": str(my_uuid),
                                    "service": "get_user_data"},})
        user = await get_user_by_id(db, id)

        if user:
            logger.info("USUARIO ENCONTRADO: %s", user.__dict__, 
                    extra={"tags": {"uuid": str(my_uuid),
                                    "service": "get_user_data"},})           
            return user

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User not found")
    except HTTPException as ex:
        logger.exception("ERRO AO BUSCAR O USUÁRIO: %s", ex.detail, 
                    extra={"tags": {"uuid": str(my_uuid),
                                    "service": "get_user_data"},})
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
    my_uuid = uuid.uuid4()
    try:
        logger.info("INCLUIR NOVO USUÁRIO: %s", user, 
                    extra={"tags": {"uuid": str(my_uuid),
                                    "service": "get_user_data"},})
        
        new_user = await add_user(db, user)
        
        logger.info("NOVO USUÁRIO INCLUIDO %s", new_user, 
                    extra={"tags": {"uuid": str(my_uuid),
                                    "service": "get_user_data"},})
        return new_user
    except HTTPException as ex:
        logger.exception("ERRO AO CADASTRAR O USUÁRIO: %s", ex.detail, 
                    extra={"tags": {"uuid": str(my_uuid),
                                    "service": "get_user_data"},})
        if(hasattr(ex, 'status_code')):
            raise HTTPException(status_code=ex.status_code,
                               detail=ex.detail)
                    
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=ex.detail)    


@router.put("/{id}", status_code=status.HTTP_200_OK)
async def update_user_data(id: int,
                           req: UserSchemaUpdate = Body(...),
                           db: AsyncSession = Depends(get_db)):
    my_uuid = uuid.uuid4()
    try:
        logger.info("ALTERAR USUÁRIO - id: %d - BODY: %s - ", id, req, 
                    extra={"tags": {"uuid": str(my_uuid),
                                    "service": "get_user_data"},})
        
        flag_update = await update_user(db, id, req)

        if flag_update:
            logger.info("USUÁRIO ALTERADO", 
                    extra={"tags": {"uuid": str(my_uuid),
                                    "service": "get_user_data"},})
            return {"message": "User Updated"}

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User not found")
    except HTTPException as ex:
        logger.exception("ERRO AO ALTERAR O USUÁRIO: %s", ex.detail, 
                    extra={"tags": {"uuid": str(my_uuid),
                                    "service": "get_user_data"},})
        if(hasattr(ex, 'status_code')):
            raise HTTPException(status_code=ex.status_code,
                               detail=ex.detail)
                    
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=ex.detail)    


@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def delete_user_data(id: int, db: AsyncSession = Depends(get_db)):
    my_uuid = uuid.uuid4()
    try:
        logger.info("DELATAR USUÁRIO - id: %d", id, 
                    extra={"tags": {"uuid": str(my_uuid),
                                    "service": "get_user_data"},})
        
        flag_delete = await delete_user(db, id)
        
        if flag_delete:
            logger.info("USUÁRIO DELETADO", 
                    extra={"tags": {"uuid": str(my_uuid),
                                    "service": "get_user_data"},})
            return {"message": "User Deleted"}

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User not found")
    except HTTPException as ex:
        logger.exception("ERRO AO DELETAR O USUÁRIO: %s", ex.detail, 
                    extra={"tags": {"uuid": str(my_uuid),
                                    "service": "get_user_data"},})
        if(hasattr(ex, 'status_code')):
            raise HTTPException(status_code=ex.status_code,
                               detail=ex.detail)
                    
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=ex.detail)    
