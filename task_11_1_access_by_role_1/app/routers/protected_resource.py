from fastapi import APIRouter, Depends

from ..auth.dependecies import get_user_from_token, check_admin_role
from ..auth.security import get_user

router = APIRouter()


@router.get("/protected_resource")
async def get_protected_resource(
    current_user: str = Depends(get_user_from_token)
):
    user = get_user(current_user)
    if user:
        return {"message": "Success"}
    return {"error": "User not found"}


@router.get("/resource")
async def get_resource():
    return {"message": "Success"}


@router.post("/resource", dependencies=[Depends(check_admin_role)])
async def post_resource():
    return {"message": "Success"}


@router.put("/resource")
async def put_resource(
    current_user: str = Depends(get_user_from_token)
):
    user = get_user(current_user)
    if user:
        return {"message": "Success"}
    return {"error": "User not found"}


@router.delete("/resource", dependencies=[Depends(check_admin_role)])
async def delete_resource():
    return {"message": "Success"}
