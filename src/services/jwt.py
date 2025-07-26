import jwt
from jwt import ExpiredSignatureError, InvalidTokenError
from datetime import datetime, timedelta
from dataclasses import dataclass
from src.exceptions.jwt import IncorrectTokenException, TokenExpiredException
from src.config import JWT



@dataclass
class JWTService:
    config: JWT

    def create_access_token(self, user_id: int) -> str:
        to_encode = {
            'sub': str(user_id),
            'exp': datetime.now() + timedelta(minutes=self.config.access_token_expire_minutes),
        }
        return jwt.encode(to_encode, self.config.secret_key, algorithm=self.config.algorithm)

    def decode_access_token(self, token: str) -> int:
        try:
            payload = jwt.decode(
                token,
                self.config.secret_key,
                algorithms=[self.config.algorithm]
            )
            user_id = payload.get('sub')
            if user_id is None:
                raise IncorrectTokenException()
            return int(user_id)
        except ExpiredSignatureError:
            raise TokenExpiredException()
        except InvalidTokenError():
            raise IncorrectTokenException()

