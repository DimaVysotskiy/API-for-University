from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, BigInteger, ForeignKey, TIMESTAMP, Integer as SERIAL
from datetime import datetime
from .enums import RoleInSystem

from ..core import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_login: Mapped[str] = mapped_column(nullable=False, unique=True)
    user_role: Mapped[str] = mapped_column(String(50), nullable=False)  # Храним как строку
    password_hash: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now())
    
    @property
    def role_enum(self) -> RoleInSystem:
        """Возвращает роль как enum."""
        return RoleInSystem[self.user_role]