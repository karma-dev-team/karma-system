from fastapi import APIRouter

from app.karma.dtos.ban import BanDTO

router = APIRouter()


@router.post(
	'/ban',
	name="karma:handle_ban",
)
async def handle_ban() -> BanDTO:
	pass
