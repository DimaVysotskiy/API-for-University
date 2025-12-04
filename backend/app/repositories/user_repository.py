from typing import List, Optional
from sqlalchemy import select, insert, update
from sqlalchemy.ext.asyncio import AsyncSession
from .base_repository import BaseRepository
from ..models import User, RoleInSystem
from datetime import datetime
from ..core import hash_password, verify_password


class UserRepository(BaseRepository[User]):
    def __init__(self):
        super().__init__(User)

    async def get_user_by_id(self, session: AsyncSession, id: int) -> Optional[User]:
        """Получаем User по id."""
        stmt = select(User).where(User.id == id)
        result = await session.scalar(statement=stmt)
        return result
    
    async def check_user_in_db_by_login(self, session: AsyncSession, user_login: str) -> bool:
        """Поиск пользователя в бд по его user_login."""
        stmt = select(select(User).where(User.user_login == user_login).exists())
        result = await session.scalar(statement=stmt)
        return result
    
    async def add_user(self, session: AsyncSession, user_login: str, role: RoleInSystem, password: str) -> Optional[int]:
        """Добавляем пользователя в бд."""
        # Проверяем, не существует ли уже пользователь с таким логином
        if await self.check_user_in_db_by_login(session, user_login):
            raise ValueError(f"User with login '{user_login}' already exists")
        
        # Конвертируем enum в строку (role.name вернет 'student', 'teacher' или 'admin')
        role_str = role.name
        
        # Await hash_password, так как это async функция
        password_hash = await hash_password(password)
        
        stmt = insert(User).values(
            user_login=user_login, 
            user_role=role_str,  # Используем строку вместо enum
            password_hash=password_hash, 
            created_at=datetime.now()
        ).returning(User.id)
        result = await session.execute(statement=stmt)
        new_user_id = result.scalar_one_or_none()
        await session.commit()
        return new_user_id
    
    async def auth(self, session: AsyncSession, user_login: str, password: str) -> int | None:
        """Аутентификация пользователя по логину и паролю."""
        stmt = select(User).where(User.user_login == user_login)
        user = await session.scalar(stmt)
        if user and await verify_password(password, user.password_hash):
            return user.id
        return None