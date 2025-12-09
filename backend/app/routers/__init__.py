from .auth_router import auth_router
from .user_router import user_router
from .group_router import group_router
from .student_info_router import student_info_router

__all__ = [
    "auth_router",
    "user_router",
    "group_router",
    "student_info_router"
]