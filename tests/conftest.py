from pathlib import Path

import pytest
from fastapi_cdn_host.utils import TestClient, TestClientType

try:
    from app import app
except ImportError:
    if (cwd := Path.cwd()) == (parent := Path(__file__).parent):
        dirpath = "."
    else:
        dirpath = str(parent.relative_to(cwd))
    print(
        f"You may need to explicitly declare python path:\n\nexport PYTHONPATH={dirpath}\n"
    )
    raise


@pytest.fixture(scope="module")
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture(scope="module")
async def client() -> TestClientType:
    async with TestClient(app) as c:
        yield c
