from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from ..repositories import UserRepository
from ..models import LoginParam, PasswordParam
from ..utils import create_jwt_token, decode_jwt_token
from ..models import User
from typing import Dict, Any

class AuthService:
    def __init__(self, user_repo: UserRepository = UserRepository()):
        self.user_repo = user_repo 
        
    async def auth_user(
        self, 
        session: AsyncSession, 
        user_login: LoginParam, 
        password: PasswordParam
    ) -> Dict[str, Any]:
        user_id = await self.user_repo.auth(session=session, user_login=user_login, password=password)
        user: User = await self.user_repo.get_user_by_id(session=session, id=user_id)
        if user:
            return {
                "message": f"Succes aut for user: {user.user_login}",
                "jwt": create_jwt_token(user_id=user_id, roles=[user.user_role.value])
            }
        else:
            raise HTTPException(status_code=401, detail="Authentication failed.")