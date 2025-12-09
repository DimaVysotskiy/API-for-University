from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from .base_repository import BaseRepository
from ..models.orm_models import StudentInfo


class StudentInfoRepository(BaseRepository[StudentInfo]):
    def __init__(self):
        super().__init__(StudentInfo)

    async def get_by_user_id(self, session: AsyncSession, user_id: int) -> Optional[StudentInfo]:
        """Получаем StudentInfo по user_id."""
        stmt = select(StudentInfo).where(StudentInfo.user_id == user_id)
        result = await session.scalar(stmt)
        return result

    async def get_by_group_id(self, session: AsyncSession, group_id: int) -> List[StudentInfo]:
        """Получаем список студентов по group_id."""
        stmt = select(StudentInfo).where(StudentInfo.group_id == group_id)
        result = await session.scalars(stmt)
        return list(result.all())

    async def get_by_zach_number(self, session: AsyncSession, zach_number: str) -> Optional[StudentInfo]:
        """Получаем StudentInfo по номеру зачетной книжки."""
        stmt = select(StudentInfo).where(StudentInfo.zach_number == zach_number)
        result = await session.scalar(stmt)
        return result

    async def check_zach_number_exists(self, session: AsyncSession, zach_number: str) -> bool:
        """Проверяем, существует ли уже студент с таким номером зачетной книжки."""
        stmt = select(select(StudentInfo).where(StudentInfo.zach_number == zach_number).exists())
        result = await session.scalar(stmt)
        return result
