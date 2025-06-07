from fastapi import HTTPException


class TgBlogException(Exception):
    detail = "Неожиданная ошибка"

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(self.detail, *args, **kwargs)


class TokenDecodeException(TgBlogException):
    detail = "Неверный токен"


class TokenExpireException(TgBlogException):
    detail = "Токен доступа просрочен"


class InvalidSessionException(TgBlogException):
    detail = "Сессия недействительна"


class WrongPasswordException(TgBlogException):
    detail = "Неправильный пароль"


class ObjectNotFoundException(TgBlogException):
    detail = "Объект не найден"


class UserNotFoundException(TgBlogException):
    detail = "Пользователь не найден"


class InvalidInputException(TgBlogException):
    detail = "Некорректно введены данные"


class TgBlogHTTPException(HTTPException):
    status_code = 500
    detail = None

    def __init__(self) -> None:
        super().__init__(status_code=self.status_code, detail=self.detail)


class TokenHTTPException(TgBlogHTTPException):
    status_code = 401
    detail = "Вы не авторизованы"


class TokenExpireHTTPException(TgBlogHTTPException):
    status_code = 401
    detail = "Токен доступа просрочен"


class TokenDecodeHTTPException(TgBlogHTTPException):
    status_code = 401
    detail = "Неверный токен"


class InvalidSessionHTTPException(TgBlogHTTPException):
    status_code = 401
    detail = "Сессия недействительна"


class WrongPasswordHTTPException(TgBlogHTTPException):
    status_code = 401
    detail = "Неправильный пароль"


class ObjectNotFoundHTTPException(TgBlogHTTPException):
    status_code = 404
    detail = "Объект не найден"


class UserNotFoundHTTPException(ObjectNotFoundHTTPException):
    detail = "Пользователь не найден"


class InvalidInputHTTPException(TgBlogHTTPException):
    status_code = 400
    detail = "Неверно введенны данные"
