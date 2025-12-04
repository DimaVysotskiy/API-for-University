# main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI
from .routers import auth_router, user_router
from .core.psql import sessionmanager
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Менеджер контекста жизненного цикла приложения.
    - Выполняется при старте: инициализирует DB Engine.
    - Выполняется при завершении: закрывает соединения DB.
    """
    sessionmanager.init_db()
    yield
    await sessionmanager.close()


app = FastAPI(lifespan=lifespan)

app.include_router(auth_router)
app.include_router(user_router)