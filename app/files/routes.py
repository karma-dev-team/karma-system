from typing import Annotated

from fastapi import APIRouter, Depends

from app.base.api.ioc import ioc_provider
from app.base.ioc import AbstractIoContainer
from app.files.dtos.files import FileDTOTypes
from app.files.dtos.input_file import InputFileType

router = APIRouter(prefix="/file")


@router.post('/upload', name="file:upload-file")
async def upload_file(
	file: InputFileType,
	ioc: Annotated[AbstractIoContainer, Depends(ioc_provider)],
) -> FileDTOTypes:
	return await ioc.file_service().upload_file(file)
