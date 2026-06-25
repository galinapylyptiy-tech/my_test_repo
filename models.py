from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID, uuid4
from enum import Enum


class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"

class Role(str, Enum):
    ADMIN = "admin"
    USER = "user"
    STUDENT = "student"

class User(BaseModel):
    id: Optional[UUID] = uuid4()
    first_name: str
    last_name: str
    middle_name: Optional[str]
    gender: Gender
    roles: List[Role]
