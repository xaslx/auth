from .base import BaseException


class TokenExpiredException(BaseException):
    status_code = 401
    detail = 'Срок действия токена истек'


class TokenAbsentException(BaseException):
    status_code = 401
    detail = 'Токен отсутствует'


class IncorrectTokenException(BaseException):
    status_code = 403
    detail = 'Недействительный токен'
