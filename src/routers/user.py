from fastapi import APIRouter, status
from dishka.integrations.fastapi import inject, FromDishka as Depends
from src.use_cases.delete_user import DeleteUserUseCase
from src.schemas.user import Role, SuccessResponse, UpdateUserSchema, UserOutSchema
from src.use_cases.update_user import UpdateUserUseCase
from src.use_cases.update_role import UpdateUserRoleUseCase

router: APIRouter = APIRouter()


@router.delete(
    '/users',
    description='Эндпоинт для удаления своего профиля',
    status_code=status.HTTP_200_OK,
)
@inject
async def delete_user(
    user: Depends[UserOutSchema],
    use_case: Depends[DeleteUserUseCase],
) -> SuccessResponse:
    
    res = await use_case.execute(user_id=user.id)
    if res:
        return SuccessResponse(detail='Успешно удален')
    

@router.get(
    '/users/me',
    description='Эндпоинт для отображения своего профиля',
    status_code=status.HTTP_200_OK,
)
@inject
async def get_profile(
    user: Depends[UserOutSchema],
) -> UserOutSchema:
    
    return user


@router.put(
    '/users',
    description='Эндпоинт для обновления пользователя',
    status_code=status.HTTP_200_OK,
)
@inject
async def update_user(
    update_schema: UpdateUserSchema,
    user: Depends[UserOutSchema],
    use_case: Depends[UpdateUserUseCase]
) -> UserOutSchema:
    
    return await use_case.execute(schema=update_schema, user_id=user.id)

@router.patch(
    '/users/{user_id}',
    description='Эндпоинт для изменения роли пользователя',
    status_code=status.HTTP_200_OK,
)
@inject
async def update_user_role(
    user_id: int,
    new_role: Role,
    user: Depends[UserOutSchema],
    use_case: Depends[UpdateUserRoleUseCase],
) -> UserOutSchema:
    
    return await use_case.execute(user_id=user_id, admin=user, new_role=new_role)

    