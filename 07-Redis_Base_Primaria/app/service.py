from fastapi import APIRouter, HTTPException, status
from app.schema import Orquestrador
from aredis_om import Migrator

router = APIRouter()


@router.get("/",
            status_code=status.HTTP_200_OK,
            response_model=list[Orquestrador])
async def get_all():
    await Migrator().run()
    res = await Orquestrador.find().all()
    return res


@router.get('/{pk}',
            status_code=status.HTTP_200_OK,
            response_model=Orquestrador)
async def get_by_pk(pk: str):
    await Migrator().run()
    try:
        res = await Orquestrador.get(pk)
        return res
    except Exception:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Registro não encontrado")


@router.post('/',
             status_code=status.HTTP_201_CREATED,
             response_model=Orquestrador)
async def create(req: Orquestrador):
    await req.save()
    return req


@router.delete('/', status_code=status.HTTP_200_OK)
async def delete_by_pk(pk: str):
    flag = await Orquestrador.delete(pk)

    if flag == 1:
        return {"message": "Orquestrador Deletado"}

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Registro não encontrado")
