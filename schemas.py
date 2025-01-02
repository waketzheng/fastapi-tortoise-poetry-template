from typing import TYPE_CHECKING

from pydantic import BaseModel
from tortoise import Tortoise
from tortoise.contrib.pydantic import PydanticModel, pydantic_model_creator

from models.users import User
from settings import load_models

if TYPE_CHECKING:  # pragma: nocoverage

    class UserPydantic(User, PydanticModel):  # type:ignore[misc]
        pass

    class UserInPydantic(UserPydantic):  # type:ignore[misc]
        pass

else:
    Tortoise.init_models(load_models(), "models")
    UserPydantic = pydantic_model_creator(User, name="User")
    UserInPydantic = pydantic_model_creator(User, name="UserIn", exclude_readonly=True)


class Status(BaseModel):
    message: str
