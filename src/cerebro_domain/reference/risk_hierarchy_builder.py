from datetime import date
from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel
from typing import Self

from cerebro_domain.reference.lc_rpc_rc_map_repo_interface import LcRpcRcMapRepoInterface
from .inst_group_lc_repo_interface import InstGroupLcRepoInterface


class RiskHierarchyNode(BaseModel):
    type: str
    code: str
    parent: Self | None = None
    children: list[Self] = []
    model_config=ConfigDict(
        alias_generator=to_camel
    )


class RiskHierarchyPeriod(BaseModel):
    start_date: date
    end_date: date
    hierarchy: RiskHierarchyNode
    model_config=ConfigDict(
        alias_generator=to_camel
    )

class RiskHierarchyBuilder:
    def __init__(self, inst_group_lc_repo: InstGroupLcRepoInterface, lc_rcp_rc_map_repo: LcRpcRcMapRepoInterface):
        self.inst_group_lc_repo = inst_group_lc_repo
        self.lc_rcp_rc_map_repo = lc_rcp_rc_map_repo

    async def get_hierarchy(self, instrument_groups: list[str] = []) -> list[RiskHierarchyPeriod]:
        ig_lc_maps = await self.inst_group_lc_repo.get_mappings(instrument_groups)
        lc_rpc_rc_maps = await self.lc_rcp_rc_map_repo.get_mappings()
        first_item = next(iter(lc_rpc_rc_maps), None)
        if first_item is None:
            return [] 
        return [
            RiskHierarchyPeriod(start_date=first_item.start_date,
                                end_date=first_item.end_date,
                                hierarchy=RiskHierarchyNode(type=first_item.limit_category, code=first_item.limit_category))]