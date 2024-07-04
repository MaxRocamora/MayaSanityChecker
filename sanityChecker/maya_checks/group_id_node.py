# ----------------------------------------------------------------------------------------
# check for maya group_id nodes
# ----------------------------------------------------------------------------------------
import maya.cmds as cmds

from sanityChecker.libs.check import Check
from sanityChecker.libs.enums import CategoryGroups, SeverityLevels
from sanityChecker.resources.logger import sanity_stream_logger

log = sanity_stream_logger('SanityChecker')

ATTRIBUTE = 'groupId'

name = 'GroupID Nodes'
group = CategoryGroups.NODES
description = 'GroupID nodes in your mesh'
level = SeverityLevels.LOW
autofix = True
hint = 'Delete the groupID node using the node editor'


class Check(Check):
    def __init__(self):  # noqa: D107
        super().__init__(name, group, description, level, autofix, hint)

    def run(self):
        """Performs scan of this check on maya scene/nodes."""
        self.reset()

        for node in cmds.ls(type='shape'):
            if cmds.listConnections(node) is None:
                continue

            for conn in cmds.listConnections(node):
                if cmds.nodeType(conn) == ATTRIBUTE:
                    self.add_failed_node(node)

    def fix(self):
        """Perform technical fix on this check."""
        for node in self.nodes():
            cmds.delete(node)