from fastapi import APIRouter, HTTPException
import requests
from requests.compat import urljoin
from requests.auth import HTTPBasicAuth
from fastapi_restful.tasks import repeat_every

router = APIRouter()


@repeat_every(seconds=60)  # 1 hour
@router.get("/hello", status_code=200)
async def teste():
    print("Inicio check")
    uri='https://jackal.rmq.cloudamqp.com/api/queues/gjnvdcak/teste'
    resp = requests.get(uri, auth=HTTPBasicAuth('gjnvdcak','vmtBLN9uBEWxT2DZmexo6CxTiz8pnc-L'))
    
    print(resp.json())
    
    if resp.status_code != 200 or resp.json() == []:
        raise HTTPException(status_code=500) 
            
    queues = resp.json()
    if int(queues["consumers"]) == 0:
        raise HTTPException(status_code=500) 
    
    return queues