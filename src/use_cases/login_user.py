from dataclasses import dataclass
from src.exceptions.user import InvalidCredentialsException
from src.models.user import User
from src.services.auth import AuthService
from src.services.hashing_password import HashingService
from src.schemas.user import LoginUserSchema
from src.services.jwt import JWTService
from src.schemas.jwt_token import JWTResponse


@dataclass
class LoginUserUseCase:
    _hashing_service: HashingService
    _auth_service: AuthService
    _jwt_service: JWTService

    async def execute(self, schema: LoginUserSchema) -> JWTResponse:
        
        user: User | None = await self._auth_service.authenticate_user(email=schema.email)

        if not user:
            raise InvalidCredentialsException()
        
        if not self._hashing_service.verify_password(plain=schema.password, hashed=user.password_hash):
            raise InvalidCredentialsException()
        
        token: str = self._jwt_service.create_access_token(user_id=user.id)
        return JWTResponse(access_token=token)

        
