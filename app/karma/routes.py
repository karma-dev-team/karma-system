from typing import Annotated

from fastapi import APIRouter, Depends

from app.auth.dependencies import role_required
from app.base.api.ioc import ioc_provider
from app.base.ioc import AbstractIoContainer
from app.server.dto.player import PlayerDTO
from app.karma.dtos.ban import HandleBanDTO
from app.karma.dtos.karma import ChangeKarmaDTO
from app.karma.dtos.warn import HandleWarnDTO
from app.karma.requests import HandleBanRequest, HandleWarnRequest
from app.server.entities.server import ServerEntity
from app.server.providers import server_provider
from app.user.enums import UserRoles

router = APIRouter(prefix="/server")


@router.post(
    '/ban',
    name="karma:handle_ban",
)
async def handle_ban(
    data: HandleBanRequest,
    ioc_container: Annotated[AbstractIoContainer, Depends(ioc_provider)],
    server: Annotated[ServerEntity, Depends(server_provider)],
) -> PlayerDTO:
    return await ioc_container.karma_service().handle_ban(
        HandleBanDTO(
            reason=data.reason,
            server_id=server.id,
            duration=data.duration,
            ply_id=data.player_id,
        )
    )


@router.post(
    '/warn',
    name='karma:handle_warn',
)
async def handle_warn(
    data: HandleWarnRequest,
    ioc_container: Annotated[AbstractIoContainer, Depends(ioc_provider)],
    server: Annotated[ServerEntity, Depends(server_provider)],
) -> PlayerDTO:
    return await ioc_container.karma_service().handle_warn(
        HandleWarnDTO(
            server_id=server.id,
            reason=data.reason,
            ply_id=data.player_id,
        )
    )


@router.post(
    '/change_karma',
    name="karma:change_karma",
    dependencies=[Depends(role_required(UserRoles.admin))],
)
async def change_karma(
    data: ChangeKarmaDTO,
    ioc_container: Annotated[AbstractIoContainer, Depends(ioc_provider)],
) -> PlayerDTO:
    return await ioc_container.karma_service().change_karma(data)
