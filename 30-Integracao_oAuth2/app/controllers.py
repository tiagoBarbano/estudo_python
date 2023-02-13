from fastapi_router_controller import Controller
from fastapi import Body, HTTPException, status, APIRouter, Depends
from .schema import *
from .service import get_items_default, get_item_data, new_item, delete_item_data, update_item_data
from fastapi.responses import ORJSONResponse
from .security import validar_token


router = APIRouter()
controller = Controller(router)


@controller.resource()
class ItemController:
    
    @controller.route.get("/v1/item", 
                          status_code=status.HTTP_200_OK, 
                          response_model=list[ItemSchema])
    async def getAllItems(self, current_user = Depends(validar_token)) -> list[ItemSchema]:
        try:
            print(str(current_user))
            items = await get_items_default()
            return items
        except HTTPException:            
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

        
    @controller.route.get("/v1/item/{id}", status_code=status.HTTP_200_OK, response_model=ItemSchema)
    async def getItembyID(self, id: int) -> ItemSchema:
        try:
            item: ItemSchema = await get_item_data(id)
            
            if item:
                return item

            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="item not found")

        except HTTPException as ex:            
            raise HTTPException(status_code=ex.status_code, detail=ex.detail)
        
    @controller.route.post("/v1/item", status_code=status.HTTP_201_CREATED, response_model=ItemSchema)
    async def createItem(self, item: ItemSchema) -> ItemSchema:
        try:
            newitem = await new_item(item)
            
            return newitem
        except HTTPException:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="item ErroR")
            
    @controller.route.put("/v1/item/{id}", status_code=status.HTTP_200_OK)
    async def changeItem(self, id: int, req: ItemSchemaUpdate = Body(...)):
        try:
            flag_update = await update_item_data(id, req)
            
            if flag_update :
                return {"message" : "item Updated"}

            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="item not found")
            
        except HTTPException as ex:
            raise HTTPException(status_code=ex.status_code,
                            detail=ex.detail)

            
    @controller.router.delete("/v1/item/{id}", status_code=status.HTTP_202_ACCEPTED)
    async def deleteItem(self, id: int):
        try:
            flag_delete = await delete_item_data(id)
      
            if flag_delete:
                return {"message" : "item Deleted"}
            
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="item not found")
        except HTTPException as ex:
            raise HTTPException(status_code=ex.status_code,
                            detail=ex.detail)
