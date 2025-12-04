from fastapi import APIRouter, Depends, HTTPException, status
from ..dependencies import get_db
from ..models import RoleInSystem
from ..repositories import UserRepository
from sqlalchemy.ext.asyncio import AsyncSession
from ..core import role_required
from ..models import UserCreate

user_router = APIRouter(prefix="/user", tags=["Работа с пользователями в бд."])

@user_router.post("/add", summary="Добавление пользователя.")
async def add_user(
    user_data: UserCreate,
    session: AsyncSession = Depends(get_db),
    _ = Depends(role_required([RoleInSystem.admin]))
    ):
    user_repo = UserRepository()
    
    # Проверяем, не существует ли уже пользователь с таким логином
    if await user_repo.check_user_in_db_by_login(session, user_data.user_login):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User with login '{user_data.user_login}' already exists"
        )
    
    try:
        new_user_id = await user_repo.add_user(
            session=session,
            user_login=user_data.user_login,
            role=user_data.role,  # Передаем enum напрямую
            password=user_data.user_password
        )
        
        if new_user_id:
            return {
                "message": f"User '{user_data.user_login}' created successfully",
                "user_id": new_user_id
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create user"
            )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )