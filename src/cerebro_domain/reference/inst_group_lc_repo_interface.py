from datetime import date
from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel
from abc import ABC, abstractmethod

__all__ = ["InstGroupLcRepoInterface"]

class InstGroupLcMap(BaseModel):
    inst_group: str
    limit_category: str
    start_date: date
    end_date: date
    model_config=ConfigDict(
        alias_generator=to_camel
    )


class InstGroupLcRepoInterface(ABC):
    @abstractmethod
    async def get_mappings(self, inst_groups: list[str]) -> list[InstGroupLcMap]:
        pass