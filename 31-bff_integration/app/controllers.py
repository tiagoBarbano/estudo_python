from fastapi_router_controller import Controller
from fastapi import HTTPException, status, APIRouter
from .connectors import proxy_get_items, proxy_token


router = APIRouter()
controller = Controller(router)


@controller.resource()
class BffController:
    
    @controller.route.get("/v1/item", status_code=status.HTTP_200_OK)
    async def getAllItems(self):
        try:
            token = await proxy_token()
            return await proxy_get_items(token)
        except HTTPException:            
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)