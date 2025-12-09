from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from .base_repository import BaseRepository
from ..models.orm_models import Group


class GroupRepository(BaseRepository[Group]):
    def __init__(self):
        super().__init__(Group)

    async def get_by_faculty(self, session: AsyncSession, faculty: str) -> List[Group]:
        """Получаем группы по названию факультета."""
        stmt = select(Group).where(Group.faculty == faculty)
        result = await session.scalars(stmt)
        return list(result.all())
