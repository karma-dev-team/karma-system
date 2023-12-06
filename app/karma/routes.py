from typing import Annotated

from fastapi import APIRouter, Depends

from app.base.api.ioc import ioc_provider
from app.base.ioc import AbstractIoContainer
from app.games.dto.player import PlayerDTO
from app.karma.dtos.ban import HandleBanDTO

router = APIRouter()


@router.post(
    '/ban',
    name="karma:handle_ban",
)
async def handle_ban(
        dto: HandleBanDTO,
        ioc_container: Annotated[AbstractIoContainer, Depends(ioc_provider)],
) -> PlayerDTO:
    return await ioc_container.karma_service().handle_ban(dto)
