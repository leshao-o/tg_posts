from fastapi import APIRouter, Body, Depends

from src.exceptions import (
    InvalidInputException,
    InvalidInputHTTPException,
    ObjectNotFoundException,
    ObjectNotFoundHTTPException,
)
from src.services.post import PostService
from src.utils.dependencies import DBDep, get_current_user
from src.schemas.post import PostAdd, PostPatch


router = APIRouter(prefix="/posts", tags=["Посты"], dependencies=[Depends(get_current_user)])


@router.post("", summary="Добавляет пост")
async def add_post(db: DBDep, post_data: PostAdd = Body()):
    try:
        new_post = await PostService(db).create_post(post_data=post_data)
    except InvalidInputException:
        raise InvalidInputHTTPException
    return {"data": new_post}


@router.put("/{id}", summary="Обновляет данные конкретного поста")
async def edit_post(db: DBDep, id: int, post_data: PostPatch = Body(),
):
    try:
        edited_post = await PostService(db).edit_post(id=id, post_data=post_data)
    except InvalidInputException:
        raise InvalidInputHTTPException
    except ObjectNotFoundException:
        raise ObjectNotFoundHTTPException
    return {"data": edited_post}


@router.delete("/{id}", summary="Удаляет пост по его id")
async def delete_post(db: DBDep, id: int):
    try:
        deleted_post = await PostService(db).delete_post(id=id)
    except ObjectNotFoundException:
        raise ObjectNotFoundHTTPException
    return {"data": deleted_post}
