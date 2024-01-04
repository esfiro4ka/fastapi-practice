from fastapi import APIRouter, Depends

from ..auth.dependecies import get_user_from_token, check_permisson
from ..auth.security import get_user

router = APIRouter()


@router.get("/resource", dependencies=[Depends(check_permisson("read"))])
async def get_resource():
    return {"message": "Success"}


@router.post("/resource", dependencies=[Depends(check_permisson("create"))])
async def post_resource():
    return {"message": "Success"}


@router.put("/resource", dependencies=[Depends(check_permisson("update"))])
async def put_resource():
    return {"message": "Success"}


@router.delete("/resource", dependencies=[Depends(check_permisson("delete"))])
async def delete_resource():
    return {"message": "Success"}


@router.get("/protected_resource")
async def get_protected_resource(
    current_user: str = Depends(get_user_from_token)
):
    user = get_user(current_user)
    if user:
        return {"message": "Success"}
    return {"error": "User not found"}
