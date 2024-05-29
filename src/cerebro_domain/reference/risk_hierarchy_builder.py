from pydantic import BaseModel
from typing import Self
from .inst_group_lc_repo_interface import InstGroupLcRepoInterface

class RiskHierarchyNode(BaseModel):
    type: str
    code: str
    parent: Self | None = None
    children: list[Self] = []


class RiskHierarchyBuilder:
    def __init__(self, inst_group_lc_repo: InstGroupLcRepoInterface):
        self.inst_group_lc_repo = inst_group_lc_repo

    def get_hierarchy(self, instrument_groups: list[str] = []):
        self.inst_group_lc_repo = self.inst_group_lc_repo.get_mappings(instrument_groups)
        return True