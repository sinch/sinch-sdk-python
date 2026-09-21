from typing import TypeVar
from pydantic import BaseModel

RM = TypeVar("RM", bound=BaseModel)  # Result model: the server response wrapper
BM = TypeVar("BM", bound=BaseModel)  # Body model: a single item in a page
