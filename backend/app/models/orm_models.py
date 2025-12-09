from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import JSON, Date, String, ForeignKey, func
from datetime import date, datetime


from ..core import Base

class User(Base):
    __tablename__ = "Users"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_login: Mapped[str] = mapped_column(nullable=False, unique=True)
    user_role: Mapped[str] = mapped_column(String(50), nullable=False) 
    password_hash: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=func.now()) 

    student_info: Mapped["StudentInfo"] = relationship(back_populates="user", uselist=False) 


class StudentInfo(Base):
    __tablename__ = "StudentInfo"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("Users.id"), unique=True)
    group_id: Mapped[int] = mapped_column(ForeignKey("Groups.id")) 
    first_name: Mapped[str] = mapped_column(String(100))
    last_name: Mapped[str] = mapped_column(String(100))
    date_of_birth: Mapped[date] = mapped_column(Date)
    zach_number: Mapped[str] = mapped_column(String(100), unique=True) 
    status: Mapped[str] = mapped_column(String(100))

    user: Mapped["User"] = relationship(back_populates="student_info")
    group: Mapped["Group"] = relationship(back_populates="student_info")


class Group(Base):
    __tablename__ = "Groups"

    id: Mapped[int] = mapped_column(primary_key=True)
    timetable: Mapped[dict] = mapped_column(JSON) 
    faculty: Mapped[str] = mapped_column(String(100))

    student_info: Mapped[list["StudentInfo"]] = relationship(back_populates="group")