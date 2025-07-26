from dishka import Provider, Scope, provide, from_context
from src.exceptions.jwt import TokenAbsentException
from src.schemas.jwt_token import JWTResponse
from src.schemas.user import UserOutSchema
from src.repositories.user import UserRepository
from src.config import Config
from fastapi import Request
from src.database.postgres import new_session_maker
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from typing import AsyncIterable
from src.services.jwt import JWTService
from src.services.hashing_password import HashingService
from src.use_cases.register_user import RegisterUserUseCase
from src.models.user import User
from src.services.auth import AuthService
from src.use_cases.login_user import LoginUserUseCase
from src.use_cases.delete_user import DeleteUserUseCase
from src.use_cases.update_user import UpdateUserUseCase
from src.use_cases.update_role import UpdateUserRoleUseCase



class AppProvider(Provider):

    config = from_context(provides=Config, scope=Scope.APP)
    request: Request = from_context(provides=Request, scope=Scope.REQUEST)


    @provide(scope=Scope.APP)
    def get_session_maker(self, config: Config) -> async_sessionmaker[AsyncSession]:
        return new_session_maker(config.postgres)

    @provide(scope=Scope.REQUEST)
    async def get_session(self, session_maker: async_sessionmaker[AsyncSession]) -> AsyncIterable[AsyncSession]:
        async with session_maker() as session:
            yield session

        
    #repository
    @provide(scope=Scope.REQUEST)
    def get_user_repository(self, session: AsyncSession) -> UserRepository:

        return UserRepository(_session=session)

    #use cases
    @provide(scope=Scope.REQUEST)
    def get_register_user_use_case(self, user_repository: UserRepository, hashing_service: HashingService) -> RegisterUserUseCase:
        
        return RegisterUserUseCase(_user_repository=user_repository, _hashing_service=hashing_service)
    
    @provide(scope=Scope.REQUEST)
    def get_login_user_use_case(
        self,
        hashing_service: HashingService,
        auth_service: AuthService,
        jwt_service: JWTService,
    ) -> LoginUserUseCase:

        return LoginUserUseCase(
            _hashing_service=hashing_service,
            _auth_service=auth_service,
            _jwt_service=jwt_service,
        )
    
    @provide(scope=Scope.REQUEST)
    def get_delete_user_use_case(self, user_repository: UserRepository) -> DeleteUserUseCase:

        return DeleteUserUseCase(_user_repository=user_repository)
    
    @provide(scope=Scope.REQUEST)
    def get_update_user_use_case(self, user_repository: UserRepository) -> UpdateUserUseCase:

        return UpdateUserUseCase(_user_repository=user_repository)
    

    @provide(scope=Scope.REQUEST)
    def get_update_user_role_use_case(self, user_repository: UserRepository) -> UpdateUserRoleUseCase:

        return UpdateUserRoleUseCase(_user_repository=user_repository)

    #services
    @provide(scope=Scope.REQUEST)
    def get_hashing_service(self) -> HashingService:

        return HashingService()
    
    @provide(scope=Scope.REQUEST)
    def get_auth_service(self, user_repository: UserRepository, jwt_service: JWTService) -> AuthService:

        return AuthService(_user_repository=user_repository, _jwt_service=jwt_service,)
    
    @provide(scope=Scope.REQUEST)
    def get_jwt_service(self, config: Config) -> JWTService:

        return JWTService(config=config.jwt)
    
  
    

    #depends
    @provide(scope=Scope.REQUEST)
    async def get_current_user(self, auth_service: AuthService, request: Request) -> UserOutSchema:
        
        token: str | None = request.cookies.get('user_access_token')

        if not token:
            raise TokenAbsentException()

        user = await auth_service.get_current_user(token=token)

        if user:
            return UserOutSchema.model_validate(user)
        return None