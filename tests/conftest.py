import os
from pathlib import Path

import pytest
from asynctor import AsyncClientGenerator, AsyncTestClient
from tortoise.contrib.test import MEMORY_SQLITE

os.environ["DB_URL"] = MEMORY_SQLITE
try:
    from app import app
except ImportError:
    PYTHONPATH = "."
    if (cwd := Path.cwd()) != (root := Path(__file__).parent.parent):
        PYTHONPATH = str(root.relative_to(cwd))
    print(f"You may need to explicitly declare python path:\n\nexport {PYTHONPATH=}\n")
    raise


@pytest.fixture(scope="module")
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture(scope="module")
async def client() -> AsyncClientGenerator:
    async with AsyncTestClient(app) as c:
        yield c
