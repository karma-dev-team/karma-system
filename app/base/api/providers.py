from app.base.config import GlobalConfig
from app.base.ioc import AbstractIoContainer


def ioc_provider() -> AbstractIoContainer:
	...


def config_provider() -> GlobalConfig:
	...
