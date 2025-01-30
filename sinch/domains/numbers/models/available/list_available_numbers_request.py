from typing import Optional, Literal
from pydantic import Field, StrictInt, StrictStr, conlist
from sinch.core.models.base_model import BaseModelConfigRequest


class ListAvailableNumbersRequest(BaseModelConfigRequest):
    region_code: StrictStr = Field(alias="regionCode")
    number_type: Literal["MOBILE", "LOCAL", "TOLL_FREE"] = Field(alias="type")
    page_size: Optional[StrictInt] = Field(default=None, alias="size")
    capabilities: Optional[conlist(StrictStr, min_length=1)] = None
    number_search_pattern: Optional[StrictStr] = Field(default=None, alias="numberPattern.searchPattern")
    number_pattern: Optional[StrictStr] = Field(default=None, alias="numberPattern.pattern")
