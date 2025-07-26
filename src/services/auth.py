from dataclasses import dataclass
from src.exceptions.user import UserNotFoundException
from src.models.user import User
from src.services.jwt import JWTService
from src.repositories.user import UserRepository


@dataclass
class AuthService:
    _user_repository: UserRepository
    _jwt_service: JWTService

    async def authenticate_user(self, email: str) -> User | None:
        user: User | None = await self._user_repository.get_by_email(email=email)

        if not user:
            raise UserNotFoundException()
        
        return user

    async def get_current_user(self, token: str) -> User | None:
  
        user_id = self._jwt_service.decode_access_token(token)
 

        if not user_id:
            return None

        user: User | None = await self._user_repository.get_by_id(user_id=int(user_id))

        if not user:
            raise UserNotFoundException()

        return user
