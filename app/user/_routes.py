from typing import Annotated

from fastapi import APIRouter, Depends, Request
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates

from app.base.api.providers import ioc_provider
from app.base.ioc import AbstractIoContainer
from app.templating.provider import templating_provider
from app.user.dto.user import CreateUserDTO

router = APIRouter()


@router.get("/", name="get-user-by-id")
def get_user_by_id(
	ioc: Annotated[AbstractIoContainer, Depends(ioc_provider)],
) -> None:
	ioc.user_service().get_user()


@router.post("/register", name="register-user", response_class=HTMLResponse)
async def register_user(
	request: Request,
	templates: Annotated[Jinja2Templates, templating_provider],
	ioc: Annotated[AbstractIoContainer, Depends(ioc_provider)],
):
	if request.method == "POST":
		await ioc.user_service().create_user(CreateUserDTO(**request.form()))  # TODO!
	return templates.TemplateResponse("user/register.html", {'request': request})
