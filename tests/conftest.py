import os
from pathlib import Path

import pytest
from asynctor.utils import AsyncTestClient
from fastapi_cdn_host.utils import TestClientType
from tortoise.contrib.test import MEMORY_SQLITE

os.environ["DB_URL"] = MEMORY_SQLITE
try:
    from app import app
except ImportError:
    if (cwd := Path.cwd()) == (root := Path(__file__).parent.parent):
        dirpath = "."
    else:
        dirpath = str(root.relative_to(cwd))
    print(
        f"You may need to explicitly declare python path:\n\nexport PYTHONPATH={dirpath}\n"
    )
    raise


@pytest.fixture(scope="module")
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture(scope="module")
async def client() -> TestClientType:
    async with AsyncTestClient(app) as c:
        yield c
