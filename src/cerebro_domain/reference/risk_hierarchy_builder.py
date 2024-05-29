from .inst_group_lc_repo_interface import InstGroupLcRepoInterface

class RiskHierarchyBuilder:
    def __init__(self, inst_group_lc_repo: InstGroupLcRepoInterface):
        self.inst_group_lc_repo = inst_group_lc_repo

    def get_hierarchy(self):
        return True