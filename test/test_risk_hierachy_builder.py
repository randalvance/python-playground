import json
from pydantic import TypeAdapter
import pytest
from pytest_mock import MockFixture

from cerebro_domain.reference.inst_group_lc_repo_interface import InstGroupLcMap, InstGroupLcRepoInterface
from cerebro_domain.reference.lc_rcp_rc_map_repo_interface import LcRcpRcMapRepoInterface
from cerebro_domain.reference.risk_hierarchy_builder import RiskHierarchyBuilder

@pytest.fixture
def inst_group_lc_repo(mocker: MockFixture):
    return mocker.create_autospec(InstGroupLcRepoInterface)

@pytest.fixture
def lc_rcp_rc_map_repo(mocker: MockFixture):
    return mocker.create_autospec(LcRcpRcMapRepoInterface)


@pytest.fixture
def sut(mocker: MockFixture, inst_group_lc_repo: InstGroupLcRepoInterface, lc_rcp_rc_map_repo: LcRcpRcMapRepoInterface):
    return RiskHierarchyBuilder(inst_group_lc_repo, lc_rcp_rc_map_repo)


@pytest.mark.asyncio
async def test_should_do_something(sut: RiskHierarchyBuilder, inst_group_lc_repo: InstGroupLcRepoInterface, lc_rcp_rc_map_repo: LcRcpRcMapRepoInterface):
    with open("test/test_data/instgrp_lc_maps.json") as f:
        json = f.read()
        result = TypeAdapter(list[InstGroupLcMap]).validate_json(json)
        print(result)
    inst_group_lc_repo.get_mappings.return_value = []
    lc_rcp_rc_map_repo.get_mappings.return_value = []
    result = await sut.get_hierarchy(["CASHBOND"])

    assert result == True