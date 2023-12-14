from sqlalchemy import select

from app.base.database.repo import SQLAlchemyRepo
from app.base.database.result import Result
from app.games.entities.category import CategoryEntity
from app.games.interfaces.persistance import GetCategoryFilter, AbstractCategoryRepository


class CategoryRepository(AbstractCategoryRepository, SQLAlchemyRepo):
    async def by_filter(self, filter: GetCategoryFilter) -> CategoryEntity | None:
        stmt = select(CategoryEntity)

        if filter.category_id is not None:
            stmt = stmt.where(CategoryEntity.id == str(filter.category_id))
        if filter.name is not None:
            stmt = stmt.where(CategoryEntity.name == str(filter.name))

        result = await self.session.execute(stmt)

        return result.unique().scalar_one_or_none()

    async def add_category(self, cat: CategoryEntity) -> Result[CategoryEntity, None]:
        self.session.add(cat)

        try:
            await self.session.commit()
            await self.session.refresh(cat)
        except Exception as exc:
            raise exc
        return Result.ok(cat)
