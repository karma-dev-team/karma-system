import uuid
from typing import Sequence

from sqlalchemy import Column, String, Integer, Table
from sqlalchemy.orm import registry as registry_class

from app.base.database.consts import STRING_URL_LENGTH, STRING_MAX_LENGTH, STRING_MIN_LENGTH
from app.base.database.models import timed_columns
from app.base.database.types import GUID
from app.files.entities import PhotoEntity, VideoEntity, DocumentEntity


def files_columns() -> Sequence[Column]:
	return [
		Column("file_id", GUID, primary_key=True, default=uuid.uuid4, index=True, nullable=False, unique=True),
		Column("file_url", String(length=STRING_URL_LENGTH), unique=True, nullable=False),
		Column("file_name", String(length=STRING_MAX_LENGTH), nullable=True),
		Column("mime_type", String(length=STRING_MIN_LENGTH), nullable=True),
		Column("file_size", Integer, nullable=True),
	]


def load_models(registry: registry_class):
	video_table = Table(
		"videos",
		registry.metadata,
		*timed_columns(),
		*files_columns(),
		Column("width", Integer, nullable=False),
		Column("height", Integer, nullable=False),
		Column("duration", Integer, nullable=False),
	)

	photo_table = Table(
		"photos",
		registry.metadata,
		*timed_columns(),
		*files_columns(),
		Column("width", Integer, nullable=False),
		Column("height", Integer, nullable=False),
	)

	document_table = Table(
		"documents",
		registry.metadata,
		*timed_columns(),
		*files_columns(),
	)

	registry.map_imperatively(
		VideoEntity,
		video_table,
	)
	registry.map_imperatively(
		PhotoEntity,
		photo_table,
	)
	registry.map_imperatively(
		DocumentEntity,
		document_table,
	)

