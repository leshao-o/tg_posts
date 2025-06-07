from src.exceptions import InvalidInputException
from src.schemas.post import Post, PostAdd, PostPatch, PostResponse
from src.services.base import BaseService


class PostService(BaseService):
    async def create_post(self, post_data: PostAdd) -> PostResponse:
        try:
            new_post = await self.db.post.create(data=post_data)
        except InvalidInputException:
            raise InvalidInputException
        await self.db.commit()
        return PostResponse(**new_post.model_dump())
    
    async def get_posts_titles(self) -> list[str]:
        posts = await self.db.post.get_all()
        return [post.title for post in posts]
    
    async def get_post_by_title(self, title: str) -> PostResponse:
        post = await self.db.post.get_post_by_title(title=title)
        return PostResponse(**post.model_dump())
    
    async def edit_post(self, id: int, post_data: PostPatch) -> PostResponse:
        edited_post = await self.db.post.update(data=post_data, id=id)
        await self.db.commit()
        return PostResponse(**edited_post.model_dump())
    
    async def delete_post(self, id: int) -> PostResponse:
        deleted_post = await self.db.post.delete(id=id)
        await self.db.commit()
        return PostResponse(**deleted_post.model_dump())
