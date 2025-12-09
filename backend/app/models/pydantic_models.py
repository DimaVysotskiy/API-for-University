from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import date
from .enums import RoleInSystem 



class UserCreate(BaseModel):
    """Модель для создания нового пользователя."""
    
    user_login: str = Field(
        ..., 
        min_length=4, 
        max_length=50, 
        description="Уникальный логин пользователя (минимум 4 символа)."
    )
    
    user_password: str = Field(
        ..., 
        min_length=8,
        description="Пароль должен быть ≥ 8 символов"
    )
    
    role: RoleInSystem = Field(
        ...,
        description="Роль пользователя в системе."
    )
    
    
    class Config:
        json_schema_extra = {
            "example": {
                "user_login": "john_doe",
                "user_password": "securepassword123",
                "role": RoleInSystem.student 
            }
        }

class AuthData(BaseModel):
    """Модель для запроса авторизации(/auth/sing-in)."""
    
    user_login: str = Field(
        ..., 
        min_length=4, 
        max_length=50, 
        description="Уникальный логин пользователя (минимум 4 символа)."
    )
    
    user_password: str = Field(
        ..., 
        min_length=8,
        description="Пароль должен быть ≥ 8 символов"
    )
    
    
    class Config:
        json_schema_extra = {
            "example": {
                "user_login": "admin",
                "user_password": "AdminPass1!"
            }
        }


class GroupCreate(BaseModel):
    """Модель для создания группы."""
    
    timetable: Dict[str, Any] = Field(
        default_factory=dict,
        description="Расписание группы в формате JSON."
    )
    
    faculty: str = Field(
        ...,
        max_length=100,
        description="Название факультета."
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "timetable": {"monday": ["Math", "Physics"], "tuesday": ["Chemistry"]},
                "faculty": "Информационные технологии"
            }
        }


class GroupUpdate(BaseModel):
    """Модель для обновления группы."""
    
    timetable: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Расписание группы в формате JSON."
    )
    
    faculty: Optional[str] = Field(
        default=None,
        max_length=100,
        description="Название факультета."
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "timetable": {"monday": ["Math", "Physics"], "tuesday": ["Chemistry"]},
                "faculty": "Информационные технологии"
            }
        }


class GroupResponse(BaseModel):
    """Модель для ответа с данными группы."""
    
    id: int
    timetable: Dict[str, Any]
    faculty: str
    
    class Config:
        from_attributes = True


class StudentInfoCreate(BaseModel):
    """Модель для создания информации о студенте."""
    
    user_id: int = Field(
        ...,
        description="ID пользователя (должен быть уникальным)."
    )
    
    group_id: int = Field(
        ...,
        description="ID группы."
    )
    
    first_name: str = Field(
        ...,
        max_length=100,
        description="Имя студента."
    )
    
    last_name: str = Field(
        ...,
        max_length=100,
        description="Фамилия студента."
    )
    
    date_of_birth: date = Field(
        ...,
        description="Дата рождения студента."
    )
    
    zach_number: str = Field(
        ...,
        max_length=100,
        description="Номер зачетной книжки (должен быть уникальным)."
    )
    
    status: str = Field(
        ...,
        max_length=100,
        description="Статус студента."
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "user_id": 2,
                "group_id": 1,
                "first_name": "Иван",
                "last_name": "Иванов",
                "date_of_birth": "2000-01-15",
                "zach_number": "Z12345",
                "status": "активный"
            }
        }


class StudentInfoUpdate(BaseModel):
    """Модель для обновления информации о студенте."""
    
    group_id: Optional[int] = Field(
        default=None,
        description="ID группы."
    )
    
    first_name: Optional[str] = Field(
        default=None,
        max_length=100,
        description="Имя студента."
    )
    
    last_name: Optional[str] = Field(
        default=None,
        max_length=100,
        description="Фамилия студента."
    )
    
    date_of_birth: Optional[date] = Field(
        default=None,
        description="Дата рождения студента."
    )
    
    zach_number: Optional[str] = Field(
        default=None,
        max_length=100,
        description="Номер зачетной книжки (должен быть уникальным)."
    )
    
    status: Optional[str] = Field(
        default=None,
        max_length=100,
        description="Статус студента."
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "group_id": 1,
                "first_name": "Иван",
                "last_name": "Иванов",
                "date_of_birth": "2000-01-15",
                "zach_number": "Z12345",
                "status": "активный"
            }
        }


class StudentInfoResponse(BaseModel):
    """Модель для ответа с данными студента."""
    
    id: int
    user_id: int
    group_id: int
    first_name: str
    last_name: str
    date_of_birth: date
    zach_number: str
    status: str
    
    class Config:
        from_attributes = True