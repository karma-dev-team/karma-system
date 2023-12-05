from typing import Annotated

from fastapi import Body, Depends, APIRouter
from starlette.requests import Request
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates

from app.auth.consts import AUTH_KEY
from app.auth.providers import auth_session_provider
from app.auth.secuirty import generate_session_id
from app.auth.session import AbstractAuthSession
from app.base.api.providers import ioc_provider, config_provider
from app.base.config import GlobalConfig
from app.base.ioc import AbstractIoContainer
from app.templating.provider import templating_provider
from app.user.dto.user import CreateUserDTO, GetUserDTO
from app.user.entities import UserEntity
from app.user.exceptions import UserAlreadyExists, UserDoesNotExists

router = APIRouter()


@router.route("/register", name="register-user")
async def register_user(
    request: Request,
    username: Annotated[str, Body(...)],
    email: Annotated[str, Body(...)],
    password: Annotated[str, Body(...)],
    registration_code: Annotated[str, Body(...)],
    config: Annotated[GlobalConfig, Depends(config_provider)],
    templates: Annotated[Jinja2Templates, templating_provider],
    ioc: Annotated[AbstractIoContainer, Depends(ioc_provider)],
    auth_session: Annotated[AbstractAuthSession, Depends(auth_session_provider)],
):
    if request.method == "POST":
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
    return templates.TemplateResponse("user/register.html", {'request': request})


@router.route("/login", name='login-user')
async def login_user(
    request: Request,
    username: Annotated[str, Body(...)],
    password: Annotated[str, Body(...)],
    config: Annotated[GlobalConfig, Depends(config_provider)],
    templates: Annotated[Jinja2Templates, Depends(templating_provider)],
    ioc: Annotated[AbstractIoContainer, Depends(ioc_provider)],
    auth_session: Annotated[AbstractAuthSession, Depends(auth_session_provider)],
):
    if request.cookies.get(AUTH_KEY):
        response = RedirectResponse("/", status_code=302)

        return response
    if request.method == "POST":
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

    return templates.TemplateResponse("user/login.html", {'request': request})
