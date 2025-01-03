import os
from pathlib import Path
from typing import TypedDict

from database_url import EngineEnum, generate


class DbConfigDict(TypedDict):
    db_url: str
    modules: dict


def load_models() -> list[str]:
    model_dir = Path(__file__).parent / "models"
    files = (p for p in model_dir.glob("*.py") if p.name[0] != "_")
    return [f"{model_dir.name}.{p.stem}" for p in files]


DB_URL = os.getenv("DB_URL") or generate(engine=EngineEnum.sqlite)
# DB_URL = generate("db_name", engine=EngineEnum.postgres)
# DB_URL = generate("db_name", engine=EngineEnum.mysql)
DB_CONFIG: DbConfigDict = {
    "db_url": DB_URL,
    "modules": {"models": [*load_models(), "aerich.models"]},
}
TORTOISE_ORM = {
    "connections": {"default": DB_URL},
    "apps": {"models": DB_CONFIG["modules"]},
}
