from jose import JWTError, jwt, ExpiredSignatureError
from fastapi import Header, HTTPException, status
from .config import get_settings


settings = get_settings()

async def validar_token(token: str = Header()):
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
    except ExpiredSignatureError as ex:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Token expired. Please log in again - "+str(ex),
        )
    except JWTError as ex:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Could not validate credentials - "+str(ex),
        )
    return payload