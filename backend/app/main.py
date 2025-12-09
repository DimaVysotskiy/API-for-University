# main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI
from .routers import auth_router, user_router, group_router, student_info_router
from .core.psql import sessionmanager
from dotenv import load_dotenv
from pathlib import Path

# Загружаем переменные окружения из .env файла (если он существует)
# В Docker переменные окружения загружаются через env_file в docker-compose
env_path = Path(__file__).parent.parent.parent / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=env_path)


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
app.include_router(group_router)
app.include_router(student_info_router)