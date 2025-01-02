#!/usr/bin/env python
import os
from contextlib import asynccontextmanager
from typing import AsyncGenerator

import uvicorn
from asynctor import AsyncRedis
from fastapi import FastAPI
from tortoise.contrib.fastapi import RegisterTortoise

from routers.users import router as users_router
from settings import DB_CONFIG


@asynccontextmanager
async def lifespan(application) -> AsyncGenerator:
    generate_schemas = ":memory:" in DB_CONFIG["db_url"]
    async with (
        RegisterTortoise(application, generate_schemas=generate_schemas, **DB_CONFIG),
        AsyncRedis(application),
    ):
        yield


app = FastAPI(lifespan=lifespan)
app.include_router(users_router, prefix="/users")
if os.getenv("FAST_CDN"):
    import fastapi_cdn_host

    fastapi_cdn_host.patch_docs(app)


if __name__ == "__main__":
    uvicorn.run("__main__:app", reload=True)
