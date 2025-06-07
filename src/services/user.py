from src.exceptions import ObjectNotFoundException, UserNotFoundException
from src.schemas.user import UserResponse
from src.services.base import BaseService


class UserService(BaseService):
    async def get_user_by_id(self, user_id: int) -> UserResponse:
        try:
            user = await self.db.user.get_by_id(user_id)
            return UserResponse(**user.model_dump())
        except ObjectNotFoundException:
            raise UserNotFoundException
