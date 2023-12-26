from datetime import datetime

from pydantic import Field, EmailStr

from app.base.dto import DTO
from app.files.dtos.input_file import InputFileType
from app.user.enums import UserRoles
from app.user.value_objects import UserID


class GetUserDTO(DTO):
	user_id: UserID | None = Field(default=None)
	email: str | None = Field(default=None)
	name: str | None = Field(default=None)


class UserDTO(DTO):
	id: UserID
	name: str
	email: str
	hashed_password: str
	role: UserRoles = UserRoles.user
	blocked: bool = False


class CreateUserDTO(DTO):
	name: str
	email: EmailStr
	password: str
	registration_code: str


class RegCodeDTO(DTO):
	code: str
	created_at: datetime


class CreateRegCode(DTO):
	key: str


class UpdateUserDataDTO(DTO):
	name: str | None
	email: EmailStr | None
	role: UserRoles | None
	image: InputFileType | None


class UpdateUserDTO(DTO):
	user_id: UserID
	data: UpdateUserDataDTO
