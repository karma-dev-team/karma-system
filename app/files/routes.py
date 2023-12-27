from typing import Annotated

from fastapi import APIRouter, Depends, Form, UploadFile

from app.base.api.ioc import ioc_provider
from app.base.ioc import AbstractIoContainer
from app.files.dtos.files import FileDTOTypes
from app.files.dtos.input_file import InputFileType, InputFile

router = APIRouter(prefix="/file", tags=["file"])


@router.post('/upload', name="file:upload-file")
async def upload_file(
	file: InputFileType,
	ioc: Annotated[AbstractIoContainer, Depends(ioc_provider)],
) -> FileDTOTypes:
	return await ioc.file_service().upload_file(file)


@router.post('/upload/form', name='file:upload-file-form')
async def upload_file_form(
	file: UploadFile,
	ioc: Annotated[AbstractIoContainer, Depends(ioc_provider)],
) -> FileDTOTypes:
	return await ioc.file_service().upload_file(
		InputFile(
			mime_type=file.content_type,
			file=await file.read(),
		)
	)
