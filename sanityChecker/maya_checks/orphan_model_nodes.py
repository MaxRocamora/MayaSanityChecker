# ----------------------------------------------------------------------------------------
# check for orphan model nodes in scene
# ----------------------------------------------------------------------------------------
import maya.cmds as cmds

from sanityChecker.libs.check import Check
from sanityChecker.maya.helpers import get_orphan_nodes_of_type
from sanityChecker.libs.enums import CategoryGroups, SeverityLevels
from sanityChecker.resources.logger import sanity_stream_logger

log = sanity_stream_logger('SanityChecker')

model_nodes = [
    'polyPlanarProj',
    'polyAutoProj',
    'polyMirror',
    'polyBridgeEdge',
    'polyUnite',
    'brush',
]

name = 'Model Orphan Nodes'
group = CategoryGroups.NODES
description = 'Orphan Modeling Nodes in the scene'
level = SeverityLevels.HIGH
autofix = True
hint = f'Remove the unconnected model nodes: {model_nodes}'


class Check(Check):
    def __init__(self):  # noqa: D107
        super().__init__(name, group, description, level, autofix, hint)

    def run(self):
        """Performs scan of this check on maya scene/nodes."""
        self.reset()

        for node in get_orphan_nodes_of_type(model_nodes):
            self.add_failed_node(node)

    def fix(self):
        """Perform technical fix on this check."""
        for node in self.nodes():
            cmds.delete(node)
