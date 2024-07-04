# ----------------------------------------------------------------------------------------
# check for total nodes in scene
# ----------------------------------------------------------------------------------------
import maya.cmds as cmds

from sanityChecker.libs.check import Check
from sanityChecker.libs.enums import CategoryGroups, SeverityLevels
from sanityChecker.resources.logger import sanity_stream_logger

log = sanity_stream_logger('SanityChecker')

LIMIT = 2000
name = f'Scene Total Nodes: Limit of {LIMIT}'
group = CategoryGroups.NODES
description = 'Scene exceeds the node limit'
level = SeverityLevels.LOW
autofix = True
hint = 'Check the amount of nodes on your scene'


class Check(Check):
    def __init__(self):  # noqa: D107
        super().__init__(name, group, description, level, autofix, hint)

    def run(self):
        """Performs scan of this check on maya scene/nodes."""
        self.reset()

        total = len(cmds.ls())
        if total >= LIMIT:
            self.add_failed_node(f'Scene Node Limit exceeded ({total})')
