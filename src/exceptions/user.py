from .base import BaseException


class UserNotFoundException(BaseException):
    status_code = 404
    detail = 'Пользователь не найден'


class PasswordsDoNotMatchException(BaseException):
    status_code = 400
    detail = 'Пароли не совпадают'


class UserAlreadyExistsException(BaseException):
    status_code = 409
    detail = 'Пользователь уже существует'


class InvalidCredentialsException(BaseException):
    status_code = 401
    detail = 'Неверная почта или пароль'


class PermissionDeniedException(BaseException):
    status_code = 403
    detail = 'Недостаточно прав'