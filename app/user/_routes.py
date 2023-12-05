from typing import Annotated

from fastapi import APIRouter, Depends
from app.base.api.providers import ioc_provider
from app.base.ioc import AbstractIoContainer
from app.user.dto.user import UserDTO

router = APIRouter()


@router.get("/{user_id}", name="get-user-by-id")
def get_user_by_id(
	ioc: Annotated[AbstractIoContainer, Depends(ioc_provider)],
) -> UserDTO:
	return
