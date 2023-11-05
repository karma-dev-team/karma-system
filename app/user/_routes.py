from typing import Annotated

from fastapi import APIRouter, Depends

from app.infrastructure.ioc import AbstractIoContainer

router = APIRouter()


@router.get("/", name="get-user-by-id")
def get_user_by_id(
	ioc: Annotated[AbstractIoContainer, Depends()],
) -> None:
	pass
