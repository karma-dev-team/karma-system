import time
import orjson
from fastapi import FastAPI
from pydantic import BaseModel

from starlette.middleware.base import RequestResponseEndpoint, BaseHTTPMiddleware

from starlette.requests import Request
from starlette.responses import Response

from app.base.api.exception import ErrorResult
from app.base.logging.logger import get_logger

PORT = '8000'
EMPTY_VALUE = ""
logger = get_logger()


class RequestJsonLogSchema(BaseModel):
	"""
	Схема части запросов-ответов лога в формате JSON
	"""
	request_uri: str
	request_referer: str
	request_protocol: str
	request_method: str
	request_path: str
	request_host: str
	request_size: int
	request_content_type: str
	request_headers: str
	request_direction: str
	remote_ip: str
	remote_port: str
	duration: float


class LoggingMiddleware(BaseHTTPMiddleware):
	"""
	Middleware для обработки запросов и ответов с целью журналирования
	"""
	def __init__(self, app: FastAPI, debug: bool = False):
		super().__init__(app)
		self.debug = debug

	@staticmethod
	async def get_protocol(request: Request) -> str:
		protocol = str(request.scope.get('type', ''))
		http_version = str(request.scope.get('http_version', ''))
		if protocol.lower() == 'http' and http_version:
			return f'{protocol.upper()}/{http_version}'
		return EMPTY_VALUE

	async def dispatch(
			self, request: Request, call_next: RequestResponseEndpoint,
	):
		start_time = time.monotonic()
		exception_object = None

		server: tuple = request.get('server', ('localhost', PORT))
		request_headers: dict = dict(request.headers.items())
		# Response Side
		try:
			response = await call_next(request)
		except Exception as exc:
			exception_object = exc
			response = Response(
				content=orjson.dumps(ErrorResult(message=str(exc), data={'error': str(exc)}))
			)
		duration: float = time.monotonic() - start_time
		temp_duration = str(duration)[:4]
		duration = float(temp_duration)
		# Инициализация и формирования полей для запроса-ответа
		request_json_fields = RequestJsonLogSchema(
			request_uri=str(request.url),
			request_referer=request_headers.get('referer', EMPTY_VALUE),
			request_protocol=await self.get_protocol(request),
			request_method=request.method,
			request_path=request.url.path,
			request_host=f'{server[0]}:{server[1]}',
			request_size=int(request_headers.get('content-length', 0)),
			request_content_type=request_headers.get(
				'content-type', EMPTY_VALUE),
			request_headers=str(orjson.dumps(request_headers)),
			request_direction='in',
			remote_ip=request.client[0],
			remote_port=str(request.client[1]),
			duration=duration
		).dict()
		# Хочется на каждый запрос читать
		# и понимать в сообщении самое главное,
		# поэтому message мы сразу делаем типовым
		message = (
			f'{"Error" if exception_object else "Response"} '
			f'to this request {request.method} \"{str(request.url)}\", '
			f'in {duration} sec'
		)
		logger.info(
			message,
			extra={
				'request_json_fields': request_json_fields,
				'to_mask': True,
			},
			exc_info=exception_object,
		)
		if exception_object:
			raise exception_object
		return response
