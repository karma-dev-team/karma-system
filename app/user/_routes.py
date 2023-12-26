from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, UploadFile
from fastapi.params import File
from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates

from app.auth.providers import user_provider
from app.base.api.ioc import ioc_provider
from app.base.ioc import AbstractIoContainer
from app.files.dtos.input_file import InputFile
from app.templating.provider import templating_provider
from app.user.dto.user import UserDTO, GetUserDTO, CreateRegCode, RegCodeDTO, UpdateUserDataDTO, UpdateUserDTO
from app.user.entities import UserEntity
from app.user.value_objects import UserID

router = APIRouter()


@router.get("/user/{user_id}", name="user:get-user-by-id")
async def get_user_by_id(
	user_id: str,
	ioc: Annotated[AbstractIoContainer, Depends(ioc_provider)],
) -> UserDTO:
	return await ioc.user_service().get_user(
		GetUserDTO(
			user_id=UserID.from_uuid(UUID(user_id)),
		)
	)


@router.get("/account", name="user:get-account", response_class=HTMLResponse)
async def get_account(
	request: Request,
	user: Annotated[UserEntity, Depends(user_provider)],
	templates: Annotated[Jinja2Templates, Depends(templating_provider)],
):
	return templates.TemplateResponse("user/account-info.html", {'request': request, 'user': user})


@router.post("/register_code", name="user:add-register-code")
async def add_register_code(
	ioc: Annotated[AbstractIoContainer, Depends(ioc_provider)],
) -> RegCodeDTO:
	return await ioc.user_service().create_reg_code()


@router.patch("/user/{user_id}", name='user:update-user')
async def update_user(
	user_id: UserID,
	dto: UpdateUserDataDTO,
	ioc: Annotated[AbstractIoContainer, Depends(ioc_provider)],
) -> UserDTO:
	return await ioc.user_service().update_user(
		UpdateUserDTO(
			user_id=user_id,
			data=dto,
		)
	)


@router.patch("/user/image", name="user:upload-user-photo")
async def update_user_photo(
	image: UploadFile,
	user: Annotated[UserEntity, Depends(user_provider)],
	ioc: Annotated[AbstractIoContainer, Depends(ioc_provider)]
) -> UserDTO:
	return await ioc.user_service().update_user(
		UpdateUserDTO(
			user_id=user.id,
			data=UpdateUserDataDTO(
				image=InputFile(file=(await image.read())),
			)
		)
	)
