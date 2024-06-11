from datetime import date
from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel
from typing import Self

from cerebro_domain.shared.date_splitter import date_splitter, DateRange, DateRangeId
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
    hierarchies: list[RiskHierarchyNode]
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

        date_ranges = [
            DateRange(
                start=ig_lc_map.start_date,
                end=ig_lc_map.end_date,
                ids=[DateRangeId(type="IGLCMAP", id=str(ig_lc_map.id))]
            ) for ig_lc_map in ig_lc_maps
        ]
        date_ranges += [
            DateRange(
                start=lc_rpc_rc_map.start_date,
                end=lc_rpc_rc_map.end_date,
                ids=[DateRangeId(type="LCRPCRCMAP", id=str(lc_rpc_rc_map.id))]
            )
            for lc_rpc_rc_map in lc_rpc_rc_maps
        ]

        date_splits = date_splitter(date_ranges)

        return []