from sqlalchemy import select
from sqlalchemy.exc import NoResultFound


from src.exceptions import ObjectNotFoundException
from src.schemas.post import Post
from src.models import PostsORM
from src.CRUD.base import BaseCRUD


class PostCRUD(BaseCRUD):
    model = PostsORM
    schema = Post

    async def get_post_by_title(self, title: str) -> Post:
        try:
            query = select(self.model).filter(self.model.title == title)
            result = await self.session.execute(query)
            return self.schema.model_validate(result.scalars().one(), from_attributes=True)
        except NoResultFound:
            raise ObjectNotFoundException
        