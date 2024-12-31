import os
from contextlib import asynccontextmanager
from typing import AsyncGenerator

import uvicorn
from fastapi import FastAPI
from tortoise.contrib.fastapi import RegisterTortoise

from settings import DB_CONFIG


@asynccontextmanager
async def lifespan(application) -> AsyncGenerator:
    async with RegisterTortoise(application, **DB_CONFIG):
        yield


app = FastAPI(lifespan=lifespan)
if os.getenv("FAST_CDN"):
    import fastapi_cdn_host

    fastapi_cdn_host.patch_docs(app)


if __name__ == "__main__":
    uvicorn.run("__main__:app", reload=True)
