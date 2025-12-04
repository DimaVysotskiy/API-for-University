from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator
from .core import sessionmanager

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async for session in sessionmanager.get_session():
        yield session