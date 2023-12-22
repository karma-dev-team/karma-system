from typing import Any, Callable
import inspect

import loguru

from app import user, server, games, karma, auth, files


def filter_workflow(params: list[str], workflow: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in workflow.items()
            if key in params}


class ModuleLoader:
    def __init__(self, modules: list[Callable[..., None]], workflow_data: dict[str, Any], logger=loguru.logger):
        self.modules = modules
        self.workflow_data = workflow_data
        self.workflow_data["data"] = self.workflow_data
        self.logger = logger or None

    def load(self):

        for module in self.modules:
            sig = inspect.signature(module)

            partial_data = filter_workflow(list(sig.parameters.keys()), self.workflow_data)
            try:
                module(**partial_data)
            except Exception as exc:
                if self.logger:
                    self.logger.exception(exc)
                raise
            else:
                self.logger.info(f"Loaded {module.__module__} module")


def configure_module_loader(workflow_data: dict[str, Any]) -> ModuleLoader:
    module = ModuleLoader(modules=[
        auth.load_module,
        user.load_module,
        server.load_module,
        games.load_module,
        karma.load_module,
        files.load_module,
    ], workflow_data=workflow_data)

    return module
