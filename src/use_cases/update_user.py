from dataclasses import dataclass

from src.models.user import User
from src.repositories.user import UserRepository
from src.schemas.user import UpdateUserSchema, UserOutSchema


@dataclass
class UpdateUserUseCase:

    _user_repository: UserRepository
    
    async def execute(self, schema: UpdateUserSchema, user_id: int) -> UserOutSchema:

        user: User | None = await self._user_repository.update(user_id=user_id, data=schema.model_dump())

        if user:
            return UserOutSchema.model_validate(user)