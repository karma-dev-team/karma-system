from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Request, Depends
from pydantic import Field
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates

from app.auth.providers import optional_user
from app.base.dto import DTO
from app.templating.provider import templating_provider
from app.user.entities import UserEntity

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def home(
	request: Request,
	user: Annotated[UserEntity, Depends(optional_user)],
	templates: Annotated[Jinja2Templates, Depends(templating_provider)],
):
	return templates.TemplateResponse('home.html', {'user': user, 'request': request})


@router.get('/about', response_class=HTMLResponse)
async def about(
	request: Request,
	user: Annotated[UserEntity, Depends(optional_user)],
	templates: Annotated[Jinja2Templates, Depends(templating_provider)],
):
	return templates.TemplateResponse('about.html', {'user': user, 'request': request})


class HealthCheckResponse(DTO):
	ok: bool
	time: datetime = Field(default_factory=datetime.now)


@router.get("/healthcheck", name='healthcheck')
async def healthcheck() -> HealthCheckResponse:
	return HealthCheckResponse(ok=True)
