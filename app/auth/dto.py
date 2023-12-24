from app.base.dto import DTO


class AskResetPasswordDTO(DTO):
    email: str


class ResetPasswordDTO(DTO):
    new_password: str
    old_password: str
    reset_id: str
