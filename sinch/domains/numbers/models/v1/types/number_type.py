from typing import Union, Literal
from pydantic import StrictStr


NumberType = Union[Literal["MOBILE", "LOCAL", "TOLL_FREE"], StrictStr]
