from dataclasses import dataclass
from src.exceptions.user import PasswordsDoNotMatchException, UserAlreadyExistsException
from src.schemas.user import CreateUserSchema, UserOutSchema
from src.repositories.user import UserRepository
from src.models.user import User
from src.services.hashing_password import HashingService



@dataclass
class RegisterUserUseCase:

    _user_repository: UserRepository
    _hashing_service: HashingService

    async def execute(self, new_user: CreateUserSchema) -> UserOutSchema:

        if new_user.password != new_user.password_confirm:
            raise PasswordsDoNotMatchException()

        user: User | None = await self._user_repository.get_by_email(email=new_user.email)

        if user:
            raise UserAlreadyExistsException()


        hashing_password: str = self._hashing_service.hash_password(new_user.password)

        user = User(**new_user.model_dump(exclude={'password', 'password_confirm'}), password_hash=hashing_password)
        new_user: User = await self._user_repository.add(user)
        return UserOutSchema.model_validate(new_user)