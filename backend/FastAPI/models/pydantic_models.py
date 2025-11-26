from fastapi import  Body
from typing import Annotated
from pydantic import Field


LoginParam = Annotated[
    str, 
    Body(
        ..., 
        min_length=4, 
        max_length=50, 
        description="Уникальный логин пользователя (минимум 4 символа)."
    )
]


PasswordParam = Annotated[
    str, 
    Body(
        ..., 
        min_length=8,
        # pattern=r"^(?=.*[A-Z])(?=.*[^a-zA-Z0-9]).{8,}$", 
        description="Пароль должен быть ≥ 8 символов, содержать 1+ заглавную лат. букву и 1+ спецсимвол."
    )
]

