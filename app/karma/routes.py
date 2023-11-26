from typing import Annotated

from fastapi import APIRouter, Depends

from app.base.ioc import AbstractIoContainer
from app.karma.dtos.ban import BanDTO

router = APIRouter()


@router.post(
	'/ban',
	name="karma:handle_ban",
)
async def handle_ban(
	ioc_container: Annotated[AbstractIoContainer, Depends(ioc_provider)],
) -> BanDTO:
	pass
