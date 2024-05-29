from datetime import date
from pydantic import BaseModel
from abc import ABC, abstractmethod


class LcRcpRcMap(BaseModel):
    limit_category: str
    reporting_category: str
    risk_category: str
    start_date: date
    end_date: date


class LcRcpRcMapRepoInterface(ABC):
    @abstractmethod
    async def get_mappings(self) -> list[LcRcpRcMap]:
        pass