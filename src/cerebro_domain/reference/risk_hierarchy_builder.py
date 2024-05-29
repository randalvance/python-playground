from pydantic import BaseModel
from typing import Self

from cerebro_domain.reference.lc_rcp_rc_map_repo_interface import LcRcpRcMapRepoInterface
from .inst_group_lc_repo_interface import InstGroupLcRepoInterface

class RiskHierarchyNode(BaseModel):
    type: str
    code: str
    parent: Self | None = None
    children: list[Self] = []


class RiskHierarchyBuilder:
    def __init__(self, inst_group_lc_repo: InstGroupLcRepoInterface, lc_rcp_rc_map_repo: LcRcpRcMapRepoInterface):
        self.inst_group_lc_repo = inst_group_lc_repo
        self.lc_rcp_rc_map_repo = lc_rcp_rc_map_repo

    async def get_hierarchy(self, instrument_groups: list[str] = []):
        ig_lc_maps = await self.inst_group_lc_repo.get_mappings(instrument_groups)
        lc_rcp_rc_maps = await self.lc_rcp_rc_map_repo.get_mappings()
        return True