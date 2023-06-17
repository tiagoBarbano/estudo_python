from datetime import datetime, timedelta
from fastapi import ( 
    Depends, 
    APIRouter, 
    HTTPException, 
    Security, 
    status
)
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
    SecurityScopes,
)
import jwt
from passlib.context import CryptContext
from pydantic import ValidationError
from app.schema.schema import User, Token, TokenData
from app.db.repository.user_repository import get_user_by_name
from app.utils.config import get_settings
from app.utils.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession


with open("openssl/jwt-key.pem", "r") as key_file:
    private_key = key_file.read()

with open("openssl/jwt-key-public.pem", "r") as key_file:
    public_key = key_file.read()


settings = get_settings()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token",
    scopes={"me": "Read information about the current user.", "items": "Read items."},
)

router = APIRouter()


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


async def authenticate_user(username: str, password: str, db: AsyncSession):
    user = await get_user_by_name(db, username)
    if not user:
        return False
    if user.disabled is True:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, private_key, algorithm="RS256")
    return encoded_jwt


async def get_current_user(
    security_scopes: SecurityScopes,
    db: AsyncSession = Depends(get_db),
    token: str = Depends(oauth2_scheme),
):
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = f"Bearer"
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )
    try:
        payload = jwt.decode(token, public_key, algorithms=["RS256"])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_scopes = payload.get("scopes", [])
        token_data = TokenData(scopes=token_scopes, username=username)
    except (jwt.DecodeError, ValidationError) as ex:
        raise credentials_exception
    user = await get_user_by_name(username=token_data.username, db=db)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    db: AsyncSession = Depends(get_db),
    current_user: User = Security(get_current_user, scopes=["me"]),
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)
):
    user = await authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.username, "scopes": form_data.scopes},
        expires_delta=access_token_expires,
    )
    return {"access_token": access_token, "token_type": "bearer"}
