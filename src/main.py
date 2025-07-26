from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
from src.ioc import AppProvider
from src.routers.auth import router as auth_router
from dishka import AsyncContainer, make_async_container
from src.routers.user import router as user_router
from dishka.integrations import fastapi as fastapi_integration
from src.config import Config


@asynccontextmanager
async def lifespan(app: FastAPI):

    yield


def create_app() -> FastAPI:

    config: Config = Config()
    container: AsyncContainer = make_async_container(AppProvider(), context={Config: config})

    app: FastAPI = FastAPI(title='Auth', lifespan=lifespan)
    app.include_router(auth_router, prefix='/api/auth', tags=['Регистрация/Вход'])
    app.include_router(user_router, prefix='/api', tags=['Пользователи'])
    fastapi_integration.setup_dishka(container=container, app=app)
    

    return app

