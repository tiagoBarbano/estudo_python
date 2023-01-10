from fastapi_router_controller import Controller
from fastapi import Body, HTTPException, status, APIRouter, Depends
from .database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from .schema import *
from .service import get_users_default, get_user_data, new_user, delete_user_data, update_user_data
from fastapi.responses import ORJSONResponse

router = APIRouter()
controller = Controller(router)


@controller.resource()
class UserController:
    
    @controller.route.get("/v1/user", 
                          status_code=status.HTTP_200_OK, 
                          response_model=list[UserSchema])
    async def getAllUsers(self) -> list[UserSchema]:
        try:
            users = await get_users_default()
            return ORJSONResponse(content=users)
        except HTTPException:            
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

        
    @controller.route.get("/v1/user/{id}", status_code=status.HTTP_200_OK, response_model=UserSchema)
    async def getUserbyID(self, id: int) -> UserSchema:
        try:
            user: UserSchema = await get_user_data(id)
            
            if user:
                return user

            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="User not found")

        except HTTPException as ex:            
            raise HTTPException(status_code=ex.status_code, detail=ex.detail)
        
    @controller.route.post("/v1/user", status_code=status.HTTP_201_CREATED, response_model=UserSchema)
    async def createUser(self, user: UserSchema) -> UserSchema:
        try:
            newUser = await new_user(user)
            
            return newUser
        except HTTPException:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="User ErroR")
            
    @controller.route.put("/v1/user/{id}", status_code=status.HTTP_200_OK)
    async def changeUser(self, id: int, req: UserSchemaUpdate = Body(...)):
        try:
            flag_update = await update_user_data(id, req)
            
            if flag_update :
                return {"message" : "User Updated"}

            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="User not found")
            
        except HTTPException as ex:
            raise HTTPException(status_code=ex.status_code,
                            detail=ex.detail)

            
    @controller.router.delete("/v1/user/{id}", status_code=status.HTTP_202_ACCEPTED)
    async def deleteUser(self, id: int):
        try:
            flag_delete = await delete_user_data(id)
      
            if flag_delete:
                return {"message" : "User Deleted"}
            
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User not found")
        except HTTPException as ex:
            raise HTTPException(status_code=ex.status_code,
                            detail=ex.detail)
