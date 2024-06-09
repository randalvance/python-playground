from datetime import date
from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel
from abc import ABC, abstractmethod


class LcRpcRcMap(BaseModel):
    limit_category: str
    reporting_category: str
    risk_category: str
    start_date: date
    end_date: date
    model_config=ConfigDict(
        alias_generator=to_camel
    )


class LcRpcRcMapRepoInterface(ABC):
    @abstractmethod
    async def get_mappings(self) -> list[LcRpcRcMap]:
        pass