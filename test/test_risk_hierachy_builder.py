import json
from pydantic import TypeAdapter
import pytest
from pytest_mock import MockFixture

from cerebro_domain.reference.inst_group_lc_repo_interface import InstGroupLcMap, InstGroupLcRepoInterface
from cerebro_domain.reference.lc_rpc_rc_map_repo_interface import LcRpcRcMap, LcRpcRcMapRepoInterface
from cerebro_domain.reference.risk_hierarchy_builder import RiskHierarchyBuilder, RiskHierarchyNode, RiskHierarchyPeriod

@pytest.fixture
def inst_group_lc_repo(mocker: MockFixture):
    return mocker.create_autospec(InstGroupLcRepoInterface)

@pytest.fixture
def lc_rcp_rc_map_repo(mocker: MockFixture):
    return mocker.create_autospec(LcRpcRcMapRepoInterface)


@pytest.fixture
def sut(mocker: MockFixture, inst_group_lc_repo: InstGroupLcRepoInterface, lc_rcp_rc_map_repo: LcRpcRcMapRepoInterface):
    return RiskHierarchyBuilder(inst_group_lc_repo, lc_rcp_rc_map_repo)


@pytest.mark.asyncio
async def test_should_do_something(sut: RiskHierarchyBuilder, inst_group_lc_repo: InstGroupLcRepoInterface, lc_rcp_rc_map_repo: LcRpcRcMapRepoInterface):
    json = _get_json("test/test_data/instgrp_lc_maps.json")
    inst_group_lc_maps = TypeAdapter(list[InstGroupLcMap]).validate_json(json)
    json = _get_json("test/test_data/lc_rcp_rc_maps.json")
    lc_rcp_rc_maps = TypeAdapter(list[LcRpcRcMap]).validate_json(json)

    json = _get_json("test/test_data/expected_hierarchy.json")
    expected_result = TypeAdapter(list[RiskHierarchyPeriod]).validate_json(json)

    inst_group_lc_repo.get_mappings.return_value = inst_group_lc_maps
    lc_rcp_rc_map_repo.get_mappings.return_value = lc_rcp_rc_maps
    result = await sut.get_hierarchy(["CASHBOND"])

    assert result == expected_result

def _get_json(file_path: str):
    with open(file_path) as f:
        return f.read()