import pytest
from httpx import AsyncClient

from models.users import Group


class TestCR:
    model = Group

    @pytest.mark.anyio
    async def test_create(self, client: AsyncClient) -> None:
        for idx in range(2, 20):
            name = f"group{idx}"
            if not await self.model.filter(name=name).exists():
                break
        response = await client.post("/users/groups", json={"name": name})
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["name"] == name
        assert "id" in data
        object_id = data["id"]
        obj = await self.model.get(id=object_id)
        assert obj.pk == object_id

    @pytest.mark.anyio
    async def test_list(self, client: AsyncClient) -> None:
        obj, _ = await self.model.get_or_create(name="group1")
        response = await client.get("/users/groups")
        assert response.status_code == 200, response.text
        data = response.json()
        assert isinstance(data, list)
        item = {"id": obj.pk, "name": obj.name}
        assert item in data
