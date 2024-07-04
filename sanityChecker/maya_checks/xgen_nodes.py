# ----------------------------------------------------------------------------------------
# check for xgen nodes in scene
# ----------------------------------------------------------------------------------------
import maya.cmds as cmds

from sanityChecker.libs.check import Check
from sanityChecker.libs.enums import CategoryGroups, SeverityLevels
from sanityChecker.resources.logger import sanity_stream_logger

log = sanity_stream_logger('SanityChecker')

xgen = [('expression', 'xgmRefreshPreview'), ('script', 'xgenGlobals')]

name = 'XGen Nodes'
group = CategoryGroups.NODES
description = 'Xgen Nodes in the scene'
level = SeverityLevels.HIGH
autofix = True
hint = f'Remove the Xgen nodes: {xgen}'


class Check(Check):
    def __init__(self):  # noqa: D107
        super().__init__(name, group, description, level, autofix, hint)

    def run(self):
        """Performs scan of this check on maya scene/nodes."""
        self.reset()

        for node in self.get_xgen_nodes():
            self.add_failed_node(node)

    def fix(self):
        """Performs technical fix on this check."""
        for node in self.nodes():
            cmds.delete(node)

    def get_xgen_nodes(self):
        """Collect nodes to scan from maya scene."""
        nodes = []
        for node_type, name in xgen:
            for node in cmds.ls(type=node_type):
                if name in node:
                    nodes.append(node)

        return nodes
