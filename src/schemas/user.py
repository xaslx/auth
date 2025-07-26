from pydantic import BaseModel, ConfigDict, EmailStr, Field
from enum import StrEnum

class Role(StrEnum):
    ADMIN = 'admin'
    USER = 'user'
    


class UserSchema(BaseModel):
    first_name: str
    last_name: str
    middle_name: str | None = None
    email: EmailStr


class CreateUserSchema(UserSchema):
    password: str = Field(min_length=8)
    password_confirm: str = Field(min_length=8)

    

class UpdateUserSchema(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    middle_name: str | None = None


class UpdatePasswordSchema(BaseModel):
    password: str = Field(min_length=8)
    password_confirm: str

class LoginUserSchema(BaseModel):
    email: EmailStr
    password: str


class UserOutSchema(UserSchema):
    id: int
    role: str
    model_config = ConfigDict(from_attributes=True)


class SuccessResponse(BaseModel):
    detail: str