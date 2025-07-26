from fastapi import APIRouter, status, HTTPException, Response
from dishka.integrations.fastapi import inject, FromDishka as Depends
from src.schemas.jwt_token import JWTResponse
from src.exceptions.user import InvalidCredentialsException, PasswordsDoNotMatchException, UserAlreadyExistsException
from src.schemas.user import CreateUserSchema, LoginUserSchema, UserOutSchema
from src.use_cases.register_user import RegisterUserUseCase
from src.use_cases.login_user import LoginUserUseCase


router: APIRouter = APIRouter()



@router.post(
    '/register',
    status_code=status.HTTP_201_CREATED,
    description='Эндпоинт для регистрации пользователя',
    responses={
        status.HTTP_201_CREATED: {'model': UserOutSchema},
        status.HTTP_400_BAD_REQUEST: {'description': 'Пароли не совпадают'},
        status.HTTP_409_CONFLICT: {'description': 'Пользователь с таким email уже существует'},
    },
)
@inject
async def register_user(
    new_user: CreateUserSchema,
    use_case: Depends[RegisterUserUseCase],
) -> UserOutSchema:

    return await use_case.execute(new_user)

    

@router.post(
    '/login',
    status_code=status.HTTP_200_OK,
    description='Эндпоинт для входа пользователя',
    responses={
        status.HTTP_200_OK: {'model': JWTResponse},
        status.HTTP_401_UNAUTHORIZED: {'description': 'Неверный email или пароль'},
    },
    
)
@inject
async def login_user(
    login_schema: LoginUserSchema,
    use_case: Depends[LoginUserUseCase],
    response: Response,
) -> JWTResponse:
    
    token: JWTResponse = await use_case.execute(schema=login_schema)
    response.set_cookie(key='user_access_token', value=token.access_token)

    return token


@router.post(
    '/logout',
    description='Эндпоинт для выхода пользователя',
    status_code=status.HTTP_204_NO_CONTENT,
)
async def logout_user(response: Response) -> None:

    response.delete_cookie(key='user_access_token')
