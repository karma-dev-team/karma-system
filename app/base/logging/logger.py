import logging
import sys

from fastapi import FastAPI
from loguru import logger

from app.base.logging.config import LoggingConfig

_loglevel_mapping = {
	50: 'CRITICAL',
	40: 'ERROR',
	30: 'WARNING',
	20: 'INFO',
	10: 'DEBUG',
	0: 'NOTSET',
}


class InterceptHandler(logging.Handler):

	def emit(self, record):
		try:
			level = logger.level(record.levelname).name
		except AttributeError:
			level = _loglevel_mapping[record.levelno]

		frame, depth = logging.currentframe(), 2
		while frame.f_code.co_filename == logging.__file__:
			frame = frame.f_back
			depth += 1

		log = logger.bind(request_id='app')
		log.opt(
			depth=depth,
			exception=record.exc_info
		).log(level, record.getMessage())


class CustomizeLogger:
	def __init__(self, config: LoggingConfig) -> None:
		self.config = config

	def make_logger(self):
		config = self.config

		logger_ = self.customize_logging(
			config.path,
			level=config.logging_level,
			retention=config.retention,
			rotation=config.rotation,
		)
		return logger_

	def customize_logging(
			self,
			filepath: str,
			level: str,
			rotation: str,
			retention: str,
	):
		logger.remove()
		logger.add(
			sys.stdout,
			enqueue=True,
			backtrace=True,
			level=level.upper(),
		)
		if filepath:
			logger.add(
				filepath,
				rotation=rotation,
				retention=retention,
				enqueue=True,
				backtrace=True,
				level=level.upper(),
			)
		logging.basicConfig(handlers=[InterceptHandler()], level=0)
		logging.getLogger("uvicorn.access").handlers = [InterceptHandler()]
		for _log in [
			'uvicorn',
			'uvicorn.error',
			'fastapi',
		]:
			_logger = logging.getLogger(_log)
			_logger.handlers = [InterceptHandler()]

		return logger.bind(request_id=None, method=None)


def get_logger(*args, **kwargs):
	return logger


def configure_logging(config: LoggingConfig):
	logger = CustomizeLogger(config)
	return logger.make_logger()
