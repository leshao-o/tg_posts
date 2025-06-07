from fastapi import APIRouter, Request, Response

from src.exceptions import (
    InvalidInputException,
    InvalidInputHTTPException,
    InvalidSessionException,
    UserNotFoundException,
    UserNotFoundHTTPException,
    WrongPasswordException,
    WrongPasswordHTTPException,
    InvalidSessionHTTPException,
)
from src.services.auth import AuthService
from src.utils.dependencies import DBDep
from src.schemas.user import UserRegister, UserLogin


router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])


@router.post("/register", summary="Регистрация пользователя",)
async def register_user(db: DBDep, user_data: UserRegister):
    try:
        new_user = await AuthService(db).register_user(user_data)
    except InvalidInputException:
        raise InvalidInputHTTPException
    return {"data": new_user}


@router.post("/login", summary="Авторизация пользователя")
async def login_user(db: DBDep, user_data: UserLogin, response: Response):
    try:
        access_token = await AuthService(db).login_user(user_data=user_data, response=response)
    except UserNotFoundException:
        raise UserNotFoundHTTPException
    except WrongPasswordException:
        raise WrongPasswordHTTPException
    return {"data": access_token}


@router.post("/", summary="Разлогинивание пользователя")
async def logout(request: Request, response: Response):
    try:
        await AuthService().logout_user(request=request, response=response)
    except InvalidSessionException:
        raise InvalidSessionHTTPException
    return {"data": "Вы успешно разлогинились"}
