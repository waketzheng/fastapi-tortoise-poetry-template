from typing import TYPE_CHECKING

from pydantic import BaseModel
from tortoise.contrib.pydantic import PydanticModel, pydantic_model_creator

from models.users import User

if TYPE_CHECKING:  # pragma: nocoverage

    class UserIn_Pydantic(User, PydanticModel):  # type:ignore[misc]
        pass

    class User_Pydantic(User, PydanticModel):  # type:ignore[misc]
        pass

else:
    User_Pydantic = pydantic_model_creator(User, name="User")
    UserIn_Pydantic = pydantic_model_creator(User, name="UserIn", exclude_readonly=True)


class Status(BaseModel):
    message: str
