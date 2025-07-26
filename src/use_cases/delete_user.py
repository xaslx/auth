from dataclasses import dataclass

from src.repositories.user import UserRepository


@dataclass
class DeleteUserUseCase:

    _user_repository: UserRepository

    async def execute(self, user_id: int) -> bool:

        return await self._user_repository.soft_delete(user_id=user_id)