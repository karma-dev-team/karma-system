from typing import Annotated, TYPE_CHECKING

from fastapi import Body, Depends, APIRouter
from starlette.requests import Request
from starlette.responses import RedirectResponse, HTMLResponse
from starlette.templating import Jinja2Templates

from app.auth.consts import AUTH_KEY
from app.auth.providers import auth_session_provider
from app.auth.secuirty import generate_session_id
from app.auth.session import AbstractAuthSession
from app.base.api.providers import config_provider
from app.base.api.ioc import ioc_provider

from app.base.ioc import AbstractIoContainer
from app.templating.provider import templating_provider
from app.user.dto.user import CreateUserDTO, GetUserDTO
from app.user.entities import UserEntity
from app.user.exceptions import UserAlreadyExists, UserDoesNotExists


if TYPE_CHECKING:
    from app.base.config import GlobalConfig


router = APIRouter()


@router.post("/register", name="register-user")
async def register_user(
    request: Request,
    config: Annotated["GlobalConfig", Depends(config_provider)],
    templates: Annotated[Jinja2Templates, Depends(templating_provider)],
    ioc: Annotated[AbstractIoContainer, Depends(ioc_provider)],
    auth_session: Annotated[AbstractAuthSession, Depends(auth_session_provider)],
    username: str = Body(...),
    email: str = Body(...),
    password: str = Body(...),
    registration_code: str = Body(...),
):
    try:
        user = await ioc.user_service().create_user(
            CreateUserDTO(
                name=username,
                email=email,
                password=password,
                registration_code=registration_code,
            )
        )
    except UserAlreadyExists as exc:
        return templates.TemplateResponse("user/register.html", {'request': request, 'error_msg': exc.message()})
    else:
        session_id = generate_session_id(
            username=user.name,
            email=user.email,
            secret_key=config.security.secret_key
        )

        response = RedirectResponse("/", status_code=302)
        response.set_cookie(key=AUTH_KEY, value=session_id)

        await auth_session.set(session_id, str(user.id))

        return response


@router.get("/register", name="register-user-get", response_class=HTMLResponse)
async def register_user(
    request: Request,
    templates: Annotated[Jinja2Templates, Depends(templating_provider)],
):
    if request.cookies.get(AUTH_KEY):
        response = RedirectResponse("/", status_code=302)

        return response
    return templates.TemplateResponse("user/register.html", {'request': request})


@router.post("/login", name='login-user')
async def login_user(
    request: Request,
    config: Annotated["GlobalConfig", Depends(config_provider)],
    templates: Annotated[Jinja2Templates, Depends(templating_provider)],
    ioc: Annotated[AbstractIoContainer, Depends(ioc_provider)],
    auth_session: Annotated[AbstractAuthSession, Depends(auth_session_provider)],
    username: str = Body(default=None),
    password: str = Body(default=None),
):
    try:
        user = await ioc.user_service().get_user(
            GetUserDTO(
                name=username,
            )
        )
    except UserDoesNotExists:
        try:
            user = await ioc.user_service().get_user(
                GetUserDTO(
                    email=username,
                )
            )
        except UserDoesNotExists as exc:
            return templates.TemplateResponse("user/login.html", {'request': request, 'error_msg': exc.message()})

    if not UserEntity.verify_password(password, user.hashed_password):
        return templates.TemplateResponse(
            "user/login.html",
            {
                'request': request,
                'error_msg': 'Password or username is not correct'
            }
        )
    session_id = generate_session_id(
        username=user.name,
        email=user.email,
        secret_key=config.security.secret_key
    )

    response = RedirectResponse("/", status_code=302)
    response.set_cookie(key=AUTH_KEY, value=session_id)

    await auth_session.set(session_id, str(user.id))

    return response


@router.get("/login", name='login-user', response_class=HTMLResponse)
async def login_user(
    request: Request,
    templates: Annotated[Jinja2Templates, Depends(templating_provider)],
):
    if request.cookies.get(AUTH_KEY):
        response = RedirectResponse("/", status_code=302)

        return response

    return templates.TemplateResponse("user/login.html", {'request': request})
