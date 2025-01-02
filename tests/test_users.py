import pytest
from httpx import AsyncClient
from tortoise.fields.data import JSON_LOADS

from models.users import Group, User
from schemas import UserPydantic


class TestUser:
    @pytest.mark.anyio
    async def test_create_user(self, client: AsyncClient) -> None:
        group, _ = await Group.get_or_create(name="group1")
        response = await client.post(
            "/users/",
            json={"name": "admin", "group_id": group.pk},
        )
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["name"] == "admin"
        assert "id" in data
        user_id = data["id"]
        user_obj = await User.get(id=user_id)
        assert user_obj.pk == user_id

    @pytest.mark.anyio
    async def test_user_list(self, client: AsyncClient) -> None:
        group, _ = await Group.get_or_create(name="group1")
        user_obj = await User.create(name="test", group=group)
        response = await client.get("/users/")
        assert response.status_code == 200, response.text
        data = response.json()
        assert isinstance(data, list)
        item = await UserPydantic.from_tortoise_orm(user_obj)
        assert JSON_LOADS(item.model_dump_json()) in data
