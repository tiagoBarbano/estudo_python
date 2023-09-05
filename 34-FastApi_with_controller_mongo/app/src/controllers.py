from fastapi_router_controller import Controller
from fastapi import Body, HTTPException, status, APIRouter
from .schema import *
from .service import get_user_data, get_users_default, new_user
from fastapi.responses import UJSONResponse
from fastapi_cache.decorator import cache
from fastapi_cache.coder import JsonCoder
from .config import key_all_users, key_user_by_id


router = APIRouter()
controller = Controller(router)


@controller.resource()
class UserController:

    def __init__(self) -> None:
        pass

    @controller.route.post("/v1/user", status_code=status.HTTP_201_CREATED, response_model=UserSchema)
    async def createUser(self, user: UserSchema) -> UserSchema:
        try:
            newUser = await new_user(user)
            
            return newUser
        except HTTPException:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="User ErroR")

    
    @controller.route.get("/v1/user", 
                          status_code=status.HTTP_200_OK, 
                          response_model=list[UserSchema],
                          response_class=UJSONResponse)
    @cache(expire=60,
       coder=JsonCoder,
       key_builder=key_all_users,
       namespace="GetAllUsers")
    async def getAllUsers(self) -> list[UserSchema]:
        try:
            print("entrou no get")
            users = await get_users_default()
            return users
        except HTTPException:            
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

        
    @controller.route.get("/v1/user/{id}", 
                          status_code=status.HTTP_200_OK, 
                          response_model=UserSchema,
                          response_class=UJSONResponse)
    @cache(expire=60,
       coder=JsonCoder,
       key_builder=key_user_by_id,
       namespace="GetByIdUser")
    async def getUserbyID(self, id: str) -> UserSchema:
        try:
            user: UserSchema = await get_user_data(id)
            
            if user:
                return user

            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="User not found")

        except HTTPException as ex:            
            raise HTTPException(status_code=ex.status_code, detail=ex.detail)
                    
    # @controller.route.put("/v1/user/{id}", status_code=status.HTTP_200_OK)
    # async def changeUser(self, id: int, req: UserSchemaUpdate = Body(...)):
    #     try:
    #         flag_update = await update_user_data(id, req, self.db)
            
    #         if flag_update :
    #             return {"message" : "User Updated"}

    #         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                             detail="User not found")
    #     except HTTPException:
    #         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #                             detail="User ErroR")
            
    # @controller.router.delete("/v1/user/{id}", status_code=status.HTTP_202_ACCEPTED)
    # async def deleteUser(self, id: int):
    #     try:
    #         flag_delete = await delete_user_data(self.db, id)
      
    #         if flag_delete:
    #             return {"message" : "User Deleted"}
            
    #         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                         detail="User not found")
    #     except HTTPException as ex:
    #         raise HTTPException(status_code=ex.status_code,
    #                         detail=ex.detail)
