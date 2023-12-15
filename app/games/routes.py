from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends

from app.base.api.ioc import ioc_provider
from app.base.ioc import AbstractIoContainer
from app.games.dto.category import AddCategoryDTO, CategoryDTO, GetCategoryDTO
from app.games.dto.game import AddGameDTO, GameDTO, GetGameDTO

game_router = APIRouter(prefix="/game", tags=["game"])
category_router = APIRouter(prefix="/category", tags=["category"])


@game_router.post(
	"/",
	name="game:add-game",
)
async def add_game(
	dto: AddGameDTO,
	ioc: Annotated[AbstractIoContainer, Depends(ioc_provider)],
) -> GameDTO:
	return await ioc.game_service().add_game(dto)


@game_router.get(
	"/{game_id}/id",
	name="game:get-game"
)
async def get_game(
	game_id: UUID,
	ioc: Annotated[AbstractIoContainer, Depends(ioc_provider)],
) -> GameDTO:
	return await ioc.game_service().get_game(
		GetGameDTO(
			game_id=game_id,
		)
	)


@game_router.get(
	"/{name}/name",
	name="game:get-game-by-name",
)
async def get_game_name(
	name: str,
	ioc: Annotated[AbstractIoContainer, Depends(ioc_provider)],
) -> GameDTO:
	return await ioc.game_service().get_game(
		GetGameDTO(
			name=name,
		)
	)


@category_router.post(
	"/",
	name="game:add-category",
)
async def add_category(
	dto: AddCategoryDTO,
	ioc: Annotated[AbstractIoContainer, Depends(ioc_provider)],
) -> CategoryDTO:
	return await ioc.category_service().add_category(dto)


@category_router.get(
	"/{category_id}",
	name="category:get-category",
)
async def get_category(
	category_id: UUID,
	ioc: Annotated[AbstractIoContainer, Depends(ioc_provider)],
) -> CategoryDTO:
	return await ioc.category_service().get_category(
		GetCategoryDTO(
			category_id=category_id,
		)
	)


@category_router.get(
	"/{name}/name",
	name="category:get-category-by-name",
)
async def get_category_by_name(
	name: str,
	ioc: Annotated[AbstractIoContainer, Depends(ioc_provider)],
) -> CategoryDTO:
	return await ioc.category_service().get_category(
		GetCategoryDTO(
			name=name,
		)
	)
