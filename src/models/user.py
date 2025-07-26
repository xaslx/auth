from src.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column


class User(Base):
    __tablename__ = 'users'

    first_name: Mapped[str]
    last_name: Mapped[str]
    middle_name: Mapped[str] = mapped_column(nullable=True)
    email: Mapped[str]
    password_hash: Mapped[str]
    is_active: Mapped[bool] = mapped_column(default=True)
    role: Mapped[str] = mapped_column(default='user')