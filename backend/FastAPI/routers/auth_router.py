from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy import select 
from ..db import get_session
from ..models import PasswordParam, LoginParam
from ..services.auth_service import AuthService
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession


auth_router = APIRouter(prefix="/auth", tags=["Аутентификация пользователей в сети."])

@auth_router.post("/", summary="Получение jwt токена.")
async def auth(user_login: LoginParam, password: PasswordParam,
            session: AsyncSession = Depends(get_session)):
    try:
        service = AuthService()
        result = await service.auth_user(session=session, user_login=user_login, password=password)
        return result
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))