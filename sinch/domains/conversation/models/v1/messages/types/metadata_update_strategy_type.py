from typing import Literal, Union
from pydantic import StrictStr

MetadataUpdateStrategyType = Union[
    Literal["REPLACE", "MERGE_PATCH"],
    StrictStr,
]
