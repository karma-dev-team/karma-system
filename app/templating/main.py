from fastapi import FastAPI
from starlette.templating import Jinja2Templates

from .provider import templating_provider


def load_templating(app: FastAPI, template_directory: str) -> None:
    templates = Jinja2Templates(directory=template_directory)

    app.dependency_overrides[templating_provider] = lambda: templates
