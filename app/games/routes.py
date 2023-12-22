from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Request
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates

from app.auth.providers import optional_user
from app.base.api.ioc import ioc_provider
from app.base.ioc import AbstractIoContainer
from app.games.dto.category import AddCategoryDTO, CategoryDTO, GetCategoryDTO, UpdateCategoryDataDTO, UpdateCategoryDTO
from app.games.dto.game import AddGameDTO, GameDTO, GetGameDTO, UpdateGameDTO, UpdateGameDataDTO
from app.games.value_objects.ids import CategoryID, GameID
from app.templating.provider import templating_provider
from app.user.entities import UserEntity

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
	"/",
	name="game:add-page-page",
	response_class=HTMLResponse,
)
async def add_game_page(
	request: Request,
	templates: Annotated[Jinja2Templates, Depends(templating_provider)],
	user: Annotated[UserEntity, Depends(optional_user)]
):
	return templates.TemplateResponse("game/create-page.html", {'request': request, 'user': user})


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


@game_router.delete(
	"/{game_id}/delete",
	name="game:delete-game",
)
async def delete_game(
	game_id: GameID,
	ioc: Annotated[AbstractIoContainer, Depends(ioc_provider)],
) -> GameDTO:
	return await ioc.game_service().delete_game(
		game_id,
	)


@game_router.patch(
	"/{game_id}/update",
	name="game:update-game",
)
async def update_game(
	game_id: GameID,
	data: UpdateGameDataDTO,
	ioc: Annotated[AbstractIoContainer, Depends(ioc_provider)],
) -> GameDTO:
	return await ioc.game_service().update_game(
		UpdateGameDTO(
			game_id=game_id,
			data=data,
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


@category_router.delete(
	'{category_id}/delete',
	name="category:delete-category",
)
async def delete_category(
	category_id: CategoryID,
	ioc: Annotated[AbstractIoContainer, Depends(ioc_provider)],
) -> CategoryDTO:
	return await ioc.category_service().delete_category(
		category_id=category_id,
	)


@category_router.patch(
	"/{category_id}/update",
	name="category:update-category",
)
async def update_category(
	category_id: CategoryID,
	data: UpdateCategoryDataDTO,
	ioc: Annotated[AbstractIoContainer, Depends(ioc_provider)],
) -> CategoryDTO:
	return await ioc.category_service().update_category(UpdateCategoryDTO(
		category_id=category_id,
		data=data,
	))
