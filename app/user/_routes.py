from typing import Annotated

from fastapi import APIRouter, Depends

from app.infrastructure.ioc import AbstractIoContainer

router = APIRouter()


@router.get("/")
def get_user_by_id(
	ioc: Annotated[AbstractIoContainer, Depends()],
):
	pass
