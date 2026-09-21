from typing import Literal, Union

from pydantic import StrictStr

ValidationType = Union[Literal["NORMAL", "STRICT"], StrictStr]
