from dataclasses import dataclass

from src.exceptions.user import PermissionDeniedException
from src.repositories.user import UserRepository
from src.schemas.user import Role, UserOutSchema


@dataclass
class UpdateUserRoleUseCase:

    _user_repository: UserRepository

    async def execute(self, user_id: int, admin: UserOutSchema, new_role: Role) -> UserOutSchema:

        if not admin.role == 'admin':
            raise PermissionDeniedException()
        
        return await self._user_repository.update(user_id=user_id, data={'role': new_role})
        
