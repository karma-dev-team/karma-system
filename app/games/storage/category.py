from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.base.database.repo import SQLAlchemyRepo
from app.base.database.result import Result
from app.games.entities.category import CategoryEntity
from app.games.exceptions import CategoryNotExists, CategoryNameAlreadyTaken
from app.games.interfaces.persistance import GetCategoryFilter, AbstractCategoryRepository


class CategoryRepository(AbstractCategoryRepository, SQLAlchemyRepo):
    def _parse_exception(self, exc: IntegrityError) -> CategoryNameAlreadyTaken:
        if not hasattr(exc.__cause__.__cause__, "constraint_name"):
            raise exc
        match exc.__cause__.__cause__.constraint_name:  # type: ignore
            case "ix_categories_name":
                return CategoryNameAlreadyTaken()

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

    async def update_category(self, category: CategoryEntity) -> Result[CategoryEntity, CategoryNameAlreadyTaken]:
        try:
            await self.session.merge(category)
        except IntegrityError as exc:
            return Result.fail(self._parse_exception(exc))
        return Result.ok(category)

    async def delete_category(self, category: CategoryEntity) -> Result[CategoryEntity, CategoryNotExists]:
        try:
            await self.session.delete(category)
        except Exception:
            return Result.fail(CategoryNotExists())

        return Result.ok(category)
