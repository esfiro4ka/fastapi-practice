from fastapi import APIRouter, Depends

from ..utils.dependecies import get_user_from_token
from ..utils.security import get_user

router = APIRouter()


@router.get("/protected_resource")
async def get_protected_resource(
    current_user: str = Depends(get_user_from_token)
):
    user = get_user(current_user)
    if user:
        return {"message": "Success"}
    return {"error": "User not found"}
