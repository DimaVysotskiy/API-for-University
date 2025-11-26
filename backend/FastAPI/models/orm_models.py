from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, BigInteger, ForeignKey, TIMESTAMP, Integer as SERIAL
from datetime import datetime
from .enums import RoleInSystem

from ..db import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_login: Mapped[str] = mapped_column(nullable=False, unique=True)
    user_role: Mapped[RoleInSystem] = mapped_column(nullable=False)
    password_hash: Mapped[bytes] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now())