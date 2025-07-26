from os import environ as env
from pydantic import Field, BaseModel


class PostgresConfig(BaseModel):
    host: str = Field(alias='POSTGRES_HOST')
    port: int = Field(alias='POSTGRES_PORT')
    login: str = Field(alias='POSTGRES_USER')
    password: str = Field(alias='POSTGRES_PASSWORD')
    database: str = Field(alias='POSTGRES_DB')


class JWT(BaseModel):
    secret_key: str = Field(alias='JWT_SECRET_KEY')
    algorithm: str = Field(alias='ALGORITHM')
    access_token_expire_minutes: int = Field(alias='ACCESS_TOKEN_EXPIRE_MINUTES')



class Config(BaseModel):
    postgres: PostgresConfig = Field(default_factory=lambda: PostgresConfig(**env))
    jwt: JWT = Field(default_factory=lambda: JWT(**env))
