from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from src.models.user import User
from dataclasses import dataclass




@dataclass
class UserRepository:
    _session: AsyncSession

    async def get_by_id(self, user_id: int) -> User | None:
        stmt = select(User).where(User.id == user_id, User.is_active.is_(True))
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def add(self, user: User) -> User:
        self._session.add(user)
        await self._session.flush()
        await self._session.refresh(user)
        await self._session.commit()
        return user
    
    async def get_by_email(self, email: str) -> User | None:
        stmt = select(User).where(User.email == email, User.is_active.is_(True))
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def update(self, user_id: int, data: dict) -> User:
        stmt = (
            update(User)
            .where(User.id == user_id, User.is_active.is_(True))
            .values(**data)
            .returning(User)
        )
        result = await self._session.execute(stmt)
        await self._session.commit()
        updated_user = result.scalar_one_or_none()
        return updated_user

    async def soft_delete(self, user_id: int) -> bool:
        stmt = (
            update(User)
            .where(User.id == user_id, User.is_active.is_(True))
            .values(is_active=False)
        )
        result = await self._session.execute(stmt)
        await self._session.commit()
        return result.rowcount > 0

