from typing import Literal, Union
from pydantic import StrictStr

PixKeyType = Union[
    Literal["CPF", "CNPJ", "EMAIL", "PHONE", "EVP"],
    StrictStr,
]
