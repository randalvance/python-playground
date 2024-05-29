from datetime import date
from pydantic import BaseModel
from abc import ABC, abstractmethod

__all__ = ["InstGroupLcRepoInterface"]

class InstGroupLcMap(BaseModel):
    inst_group: str
    limit_category: str
    start_date: date
    end_date: date


class InstGroupLcRepoInterface(ABC):
    def get_mappings(self, inst_groups: list[str]):
        pass