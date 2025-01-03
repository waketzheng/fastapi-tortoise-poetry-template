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

    @pytest.mark.anyio
    async def test_user_detail(self, client: AsyncClient) -> None:
        group, _ = await Group.get_or_create(name="group1")
        user_obj, _ = await User.get_or_create(name="test", group=group)
        response = await client.get(f"/users/user/{user_obj.pk}")
        assert response.status_code == 200, response.text
        data = response.json()
        item = await UserPydantic.from_tortoise_orm(user_obj)
        assert JSON_LOADS(item.model_dump_json()) == data

    @pytest.mark.anyio
    async def test_update_user(self, client: AsyncClient) -> None:
        group, _ = await Group.get_or_create(name="group1")
        user_obj, _ = await User.get_or_create(name="test", group=group)
        for i in range(2, 20):
            new_name = f"test{i}"
            if not await User.filter(name=new_name).exists():
                break
        response = await client.put(
            f"/users/user/{user_obj.pk}", json={"name": new_name, "group_id": group.pk}
        )
        assert response.status_code == 200, response.text
        data = response.json()
        updated_user = await User.get(id=user_obj.pk)
        assert data["name"] == new_name == updated_user.name

    @pytest.mark.anyio
    async def test_delete_user(self, client: AsyncClient) -> None:
        group, _ = await Group.get_or_create(name="group1")
        for i in range(2, 20):
            new_name = f"test{i}"
            if not await User.filter(name=new_name).exists():
                user_obj = await User.create(name=new_name, group=group)
                break
        response = await client.delete(f"/users/user/{user_obj.pk}")
        assert response.status_code == 200, response.text
        data = response.json()
        assert str(user_obj.pk) in data["message"]
        assert not await User.filter(id=user_obj.pk).exists()
        response = await client.delete("/users/user/0")
        assert response.status_code == 404
