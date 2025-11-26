import jwt
import datetime
from typing import Dict, Any
from ..models import RoleInSystem
import os

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")


def create_jwt_token(user_id: int, roles: list[RoleInSystem]) -> str:
    """
    Генерирует JWT токен, включающий ID пользователя, роли и срок действия.
    """

    payload = {
        "sub": str(user_id),  
        "roles": roles,       
        "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=5), # "exp" (Expiration Time)
        "iat": datetime.datetime.now(datetime.timezone.utc), # "iat" (Issued At)
    }

    encoded_jwt = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )
    return encoded_jwt


def decode_jwt_token(token: str) -> Dict[str, Any]:
    """
    Декодирует JWT токен и возвращает его полезную нагрузку.
    """
    try:
        # 1. Декодирование и верификация подписи
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        return payload
    except jwt.ExpiredSignatureError:
        # Токен просрочен
        raise Exception("Token has expired")
    except jwt.InvalidTokenError:
        # Неверная подпись или другие ошибки валидации
        raise Exception("Invalid token")