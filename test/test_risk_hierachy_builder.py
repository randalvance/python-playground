import pytest
from pytest_mock import MockFixture

from cerebro_domain.reference.inst_group_lc_repo_interface import InstGroupLcRepoInterface
from cerebro_domain.reference.risk_hierarchy_builder import RiskHierarchyBuilder

@pytest.fixture
def inst_group_lc_repo(mocker: MockFixture):
    return mocker.create_autospec(InstGroupLcRepoInterface)


@pytest.fixture
def sut(mocker: MockFixture, inst_group_lc_repo: InstGroupLcRepoInterface):
    return RiskHierarchyBuilder(inst_group_lc_repo)


def test_should_do_something(sut: RiskHierarchyBuilder):
    result = sut.get_hierarchy()
    assert result is False, "It should though shall not."