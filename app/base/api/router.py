from typing import Annotated

from fastapi import APIRouter, Request, Depends
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates

from app.auth.providers import optional_user
from app.templating.provider import templating_provider
from app.user.entities import UserEntity

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def home(
	request: Request,
	user: Annotated[UserEntity, Depends(optional_user)],
	templates: Annotated[Jinja2Templates, Depends(templating_provider)],
):
	return templates.TemplateResponse('base.html', {'user': user, 'request': request})


@router.get('/about', response_class=HTMLResponse)
async def about(
	request: Request,
	user: Annotated[UserEntity, Depends(optional_user)],
	templates: Annotated[Jinja2Templates, Depends(templating_provider)],
):
	return templates.TemplateResponse('about.html', {'user': user, 'request': request})
