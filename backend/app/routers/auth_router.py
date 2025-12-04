from fastapi import APIRouter, Depends, HTTPException
from ..dependencies import get_db
from ..models import AuthData
from ..services.auth_service import AuthService
from sqlalchemy.ext.asyncio import AsyncSession


auth_router = APIRouter(prefix="/auth", tags=["Аутентификация пользователей в сети."])

@auth_router.post("/log-in", summary="Получение jwt токена.")
async def auth(auth_data: AuthData,
            session: AsyncSession = Depends(get_db)):
    try:
        service = AuthService()
        result = await service.auth_user(session=session, user_login=auth_data.user_login, password=auth_data.user_password)
        return result
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))