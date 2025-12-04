from pydantic import BaseModel, Field
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