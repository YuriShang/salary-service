from typing import Union, Any
from datetime import datetime, timedelta
import random
import string
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from pydantic import ValidationError
import jwt
from passlib.context import CryptContext
from salary_service.schemas.schemas import TokenPayload, LoggedInUser
from salary_service.db.models import users_table
from salary_service.db.database import engine


ACCESS_TOKEN_EXPIRE_MINUTES = 3#float(os.environ['ACCESS_TOKEN_EXPIRE_MINUTES'])
ALGORITHM = "HS256"
JWT_SECRET_KEY = "33"#os.environ['JWT_SECRET_KEY']     # should be kept secret

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl="/login",
    scheme_name="JWT"
)


def get_hashed_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, hashed_pass: str) -> bool:
    return password_context.verify(password, hashed_pass)


def create_access_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + timedelta(minutes=expires_delta)
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, ALGORITHM)
    return encoded_jwt


# Проверяем входящий токен, если все ок, возвращаем данные пользователя
# для дальнейшего разрешения доступа к защищенным маршрутам
async def get_current_user(token: str = Depends(reuseable_oauth)) -> LoggedInUser:
    try:
        payload = jwt.decode(
            token, JWT_SECRET_KEY, algorithms=[ALGORITHM]
        )
        token_data = TokenPayload(**payload)

        # Проверяем актуальность токена
        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    # Если токен некорректный:
    except(jwt.PyJWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    async with engine.connect() as connection:
        user = await connection.execute(select(users_table).where(users_table.c.username == token_data.sub))
        user_data = user.mappings().one()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user",
        )

    return user_data