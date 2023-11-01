from typing import Annotated

from fastapi import APIRouter, Depends

from app.base.ioc import AbstractIoContainer

router = APIRouter()


def get_user_by_id(
	ioc: Annotated[AbstractIoContainer, Depends()],
):
	pass
