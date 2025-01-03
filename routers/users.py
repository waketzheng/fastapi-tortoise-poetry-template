from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from models.users import Group, User
from schemas import GroupInPydantic, Status, UserInPydantic, UserPydantic

router = APIRouter()


@router.get("/", response_model=list[UserPydantic])
async def user_list():
    return await UserPydantic.from_queryset(User.all())


@router.post("/", response_model=UserPydantic)
async def create_user(user: UserInPydantic):
    user_obj = await User.create(**user.model_dump(exclude_unset=True))
    return await UserPydantic.from_tortoise_orm(user_obj)


@router.get("/user/{user_id}", response_model=UserPydantic)
async def get_user(user_id: int):
    return await UserPydantic.from_queryset_single(User.get(id=user_id))


@router.put("/user/{user_id}", response_model=UserPydantic)
async def update_user(user_id: int, user: UserInPydantic):
    await User.filter(id=user_id).update(**user.model_dump(exclude_unset=True))
    return await UserPydantic.from_queryset_single(User.get(id=user_id))


@router.delete("/user/{user_id}", response_model=Status)
async def delete_user(user_id: int):
    deleted_count = await User.filter(id=user_id).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")
    return Status(message=f"Deleted user {user_id}")


class GroupItem(BaseModel):
    id: int
    name: str


@router.get("/groups", response_model=list[GroupItem])
async def group_list():
    group_objs = await Group.all()
    return [{"id": i.pk, "name": i.name} for i in group_objs]


@router.post("/groups", response_model=GroupItem)
async def create_group(group: GroupInPydantic):
    group_obj = await Group.create(**group.model_dump(exclude_unset=True))
    return {"id": group_obj.pk, "name": group_obj.name}
