from fastapi_router_controller import Controller
from fastapi import Body, HTTPException, status, APIRouter
from .schema import *
from .service import get_users_default, get_user_data, new_user, delete_user_data, receve_msg_kafka, update_user_data
import aiokafka, uuid, asyncio
from fastapi.encoders import jsonable_encoder


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
            return users
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

    @controller.route.post("/v1/user/kafka", status_code=status.HTTP_202_ACCEPTED)
    async def createUserKafka(self, user: UserSchema):
        try:
            myuuid = uuid.uuid4()
            userKafka = UserSchemaKafka(myuuid, user.nome_item, user.num_item)
            
            producer = aiokafka.AIOKafkaProducer(bootstrap_servers="host.docker.internal:29092")        

            await producer.start()
            await producer.send_and_wait("default", bytes(str(jsonable_encoder(userKafka)),'UTF-8'))
            return {"message": "User Recebido", "uuid": str(myuuid)}    
        except HTTPException as ex:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=str(ex))
        finally:
            await producer.stop()
            
    @controller.route.get("/v1/user/kafka/get")
    async def getUserKafka(self):
        try:
            consumer = aiokafka.AIOKafkaConsumer("default", bootstrap_servers="host.docker.internal:29092")
            await consumer.start()

            async for msg in consumer:
                print("{}:{:d}:{:d}: key={} value={} timestamp_ms={}".format(msg.topic, msg.partition, msg.offset, msg.key, msg.value, msg.timestamp))
                await receve_msg_kafka(msg)
        except HTTPException as ex:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=str(ex))
        finally:
            await consumer.stop()            

