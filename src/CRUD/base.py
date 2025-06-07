from pydantic import BaseModel
from sqlalchemy import delete, insert, select, update
from sqlalchemy.exc import NoResultFound, IntegrityError, ProgrammingError

from src.exceptions import InvalidInputException, ObjectNotFoundException


class BaseCRUD:
    model = None
    schema: BaseModel = None

    def __init__(self, session):
        self.session = session

    async def create(self, data: BaseModel) -> BaseModel:
        stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        try:
            result = await self.session.execute(stmt)
        except IntegrityError:
            raise InvalidInputException
        # Валидация (приведение результата к pydantic модели)
        model = self.schema.model_validate(result.scalars().one(), from_attributes=True)
        return model

    async def get_all(self) -> list[BaseModel]:
        try:
            query = select(self.model)
            result = await self.session.execute(query)
            models = [
                self.schema.model_validate(one, from_attributes=True)
                for one in result.scalars().all()
            ]
            return models
        except NoResultFound:
            raise ObjectNotFoundException

    async def get_by_id(self, id: int) -> BaseModel:
        try:
            query = select(self.model).filter(self.model.id == id)
            result = await self.session.execute(query)
            model = self.schema.model_validate(result.scalars().one(), from_attributes=True)
            return model
        except NoResultFound:
            raise ObjectNotFoundException

    async def update(self, data: BaseModel, **filter_by) -> BaseModel:
        stmt = (
            update(self.model)
            .filter_by(**filter_by)
            .values(**data.model_dump(exclude_unset=True))
            .returning(self.model)
        )
        try:
            result = await self.session.execute(stmt)
        except (IntegrityError, ProgrammingError):
            raise InvalidInputException

        try:
            model = self.schema.model_validate(result.scalars().one(), from_attributes=True)
        except NoResultFound:
            raise ObjectNotFoundException

        return model

    async def delete(self, **filter_by) -> BaseModel:
        stmt = delete(self.model).filter_by(**filter_by).returning(self.model)
        result = await self.session.execute(stmt)
        try:
            model = self.schema.model_validate(result.scalars().one(), from_attributes=True)
        except NoResultFound:
            raise ObjectNotFoundException
        return model
