import json
from typing import Annotated, TYPE_CHECKING

from fastapi import Body, Depends, APIRouter, Form, status, Response
from fastapi_csrf_protect import CsrfProtect
from starlette.requests import Request
from starlette.responses import RedirectResponse, HTMLResponse
from starlette.templating import Jinja2Templates

from app.auth.consts import AUTH_KEY
from app.auth.dependencies import user_dependency
from app.auth.dto import ResetPasswordDTO, AskResetPasswordDTO
from app.auth.exceptions import AccessDenied
from app.auth.providers import auth_session_provider
from app.auth.secuirty import generate_session_id
from app.auth.session import AbstractAuthSession
from app.base.api.providers import config_provider
from app.base.api.ioc import ioc_provider

from app.base.ioc import AbstractIoContainer
from app.templating.provider import templating_provider
from app.user.dto.user import CreateUserDTO, GetUserDTO
from app.user.entities import UserEntity
from app.user.exceptions import UserAlreadyExists, UserDoesNotExists, RegistrationCodeIsNotCorrect

if TYPE_CHECKING:
    from app.base.config import GlobalConfig


router = APIRouter()


@router.post("/auth/register", name="auth:register")
async def register_user(
    request: Request,
    config: Annotated["GlobalConfig", Depends(config_provider)],
    templates: Annotated[Jinja2Templates, Depends(templating_provider)],
    ioc: Annotated[AbstractIoContainer, Depends(ioc_provider)],
    auth_session: Annotated[AbstractAuthSession, Depends(auth_session_provider)],
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    registration_code: str = Form(...),
    csrf_protect: CsrfProtect = Depends()
):
    await csrf_protect.validate_csrf(request, cookie_key="csrftoken")
    try:
        user = await ioc.user_service().create_user(
            CreateUserDTO(
                name=username,
                email=email,
                password=password,
                registration_code=registration_code,
            )
        )
    except (UserAlreadyExists, RegistrationCodeIsNotCorrect) as exc:
        response = templates.TemplateResponse(
            "auth/register.html",
            {'request': request, 'error_msg': exc.message()}
        )
    else:
        session_id = generate_session_id(
            username=user.name,
            email=user.email,
            secret_key=config.security.secret_key
        )

        response = RedirectResponse("/", status_code=302)
        response.set_cookie(key=AUTH_KEY, value=session_id, secure=True)

        await auth_session.set(session_id, str(user.id))
    csrf_protect.unset_csrf_cookie(response)  # prevent token reuse
    return response


@router.get("/auth/register", name="auth:register-get", response_class=HTMLResponse)
async def register_user(
    request: Request,
    templates: Annotated[Jinja2Templates, Depends(templating_provider)],
    csrf_protect: CsrfProtect = Depends(),
):
    if request.cookies.get(AUTH_KEY, None):
        response = RedirectResponse("/", status_code=302)

        return response
    csrf_token, signed_token = csrf_protect.generate_csrf_tokens()
    response = templates.TemplateResponse("auth/register.html", {'request': request, "csrf_token": csrf_token})

    csrf_protect.set_csrf_cookie(signed_token, response)
    return response


@router.post("/auth/login", name='auth:login-post')
async def login_user(
    request: Request,
    config: Annotated["GlobalConfig", Depends(config_provider)],
    templates: Annotated[Jinja2Templates, Depends(templating_provider)],
    ioc: Annotated[AbstractIoContainer, Depends(ioc_provider)],
    auth_session: Annotated[AbstractAuthSession, Depends(auth_session_provider)],
    username: str = Form(None),
    password: str = Form(None),
    csrf_protect: CsrfProtect = Depends()
):
    await csrf_protect.validate_csrf(request)
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
            return templates.TemplateResponse(
                "auth/login.html",
                {
                    'request': request,
                    'error_msg': exc.message(),
                    'csrf_token': csrf_protect.get_csrf_from_body(await request.body())
                }
            )

    if not UserEntity.verify_password(password, user.hashed_password):
        response = templates.TemplateResponse(
            "auth/login.html",
            {
                'request': request,
                'error_msg': 'Password or username is not correct',
                'csrf_token': csrf_protect.get_csrf_from_body(await request.body())
            }
        )
        csrf_protect.unset_csrf_cookie(response)  # prevent token reuse
        return response
    response = RedirectResponse("/", status_code=302)
    if request.cookies.get(AUTH_KEY, None):
        return response
    session_id = generate_session_id(
        username=user.name,
        email=user.email,
        secret_key=config.security.secret_key
    )

    response.set_cookie(key=AUTH_KEY, value=session_id, secure=True)

    await auth_session.set(session_id, str(user.id))
    csrf_protect.unset_csrf_cookie(response)  # prevent token reuse

    return response


@router.get("/auth/login", name='auth:login', response_class=HTMLResponse)
async def login_user(
    request: Request,
    templates: Annotated[Jinja2Templates, Depends(templating_provider)],
    csrf_protect: CsrfProtect = Depends(),
):

    if request.cookies.get(AUTH_KEY):
        response = RedirectResponse("/", status_code=302)

        return response

    csrf_token, signed_token = csrf_protect.generate_csrf_tokens()
    response = templates.TemplateResponse("auth/login.html", {'request': request, 'csrf_token': csrf_token})
    csrf_protect.set_csrf_cookie(signed_token, response)

    return response


@router.get("/auth/reset-password", name="auth:reset-password-page", response_class=HTMLResponse)
async def reset_password_page(
    request: Request,
    templates: Annotated[Jinja2Templates, Depends(templating_provider)],
):
    if request.cookies.get(AUTH_KEY, None):
        response = RedirectResponse("/", status_code=302)

        return response

    return templates.TemplateResponse("auth/reset-password.html", {'request': request})


@router.post("/auth/reset-password", name="auth:reset-password")
async def ask_reset_password(
    request: Request,
    dto: AskResetPasswordDTO,
    ioc: Annotated[AbstractIoContainer, Depends(ioc_provider)],
) -> Response:
    try:
        await ioc.auth_service().ask_reset_password(dto, str(request.base_url))
    except UserDoesNotExists as exc:
        return Response(
            content=json.dumps({'message': exc.message(), "ok": False}),
            status_code=status.HTTP_400_BAD_REQUEST,
        )


@router.get(
    "/auth/password-reset/{reset_token}",
    name="auth:handle-reset-password-page",
    response_class=HTMLResponse,
)
async def handle_reset_password_page(
    request: Request,
    reset_token: str,
    templates: Annotated[Jinja2Templates, Depends(templating_provider)],
    ioc: Annotated[AbstractIoContainer, Depends(ioc_provider)],
):
    response = RedirectResponse("/", status_code=302)
    if request.cookies.get(AUTH_KEY, None):
        return response

    try:
        await ioc.auth_service().verify_reset_password(reset_token)
    except AccessDenied:
        return response
    return templates.TemplateResponse("auth/handle_reset_password_page.html", {'request': request})


@router.post(
    "/auth/password-reset/{reset_token}",
    name="auth:handle-reset-password",
)
async def handle_reset_password(
    reset_token: str,
    new_password: Annotated[str, Form()],
    ioc: Annotated[AbstractIoContainer, Depends(ioc_provider)],
):
    await ioc.auth_service().reset_password(
        ResetPasswordDTO(
            reset_token=reset_token,
            new_password=new_password,
        )
    )
    response = RedirectResponse("/", status_code=302)
    return response


@router.get(
    '/auth/logout',
    name="auth:logout",
    response_class=HTMLResponse,
)
async def logout():
    response = RedirectResponse('/', status_code=status.HTTP_302_FOUND)
    response.delete_cookie(AUTH_KEY, secure=True)

    return response
