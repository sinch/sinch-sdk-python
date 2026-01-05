from typing import Literal, Union
from pydantic import StrictStr


AgentType = Union[Literal["UNKNOWN_AGENT_TYPE", "HUMAN", "BOT"], StrictStr]
