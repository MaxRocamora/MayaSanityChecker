# ----------------------------------------------------------------------------------------
# check for maya orphan nodes with no connections
# ----------------------------------------------------------------------------------------
import maya.cmds as cmds

from sanityChecker.libs.check import Check
from sanityChecker.maya.helpers import get_orphan_nodes_of_type
from sanityChecker.libs.enums import CategoryGroups, SeverityLevels
from sanityChecker.resources.logger import sanity_stream_logger

log = sanity_stream_logger('SanityChecker')

NODES = ['nodeGraphEditorInfo', 'cameraView']

name = 'Scene Orphan Nodes'
group = CategoryGroups.NODES
description = 'Nodes without connections found on scene.'
level = SeverityLevels.HIGH
autofix = True
hint = f'Check your scene for unconnected nodes of type: {NODES}.'


class Check(Check):
    def __init__(self):  # noqa: D107
        super().__init__(name, group, description, level, autofix, hint)

    def run(self):
        """Performs scan of this check on maya scene/nodes."""
        self.reset()

        nodes = get_orphan_nodes_of_type(NODES)
        no_ref_nodes = [n for n in nodes if ':' not in n]

        for node in no_ref_nodes:
            self.add_failed_node(node)

    def fix(self):
        """Perform technical fix on this check."""
        for node in self.nodes():
            try:
                cmds.delete(node)
            except RuntimeError as e:
                print(e)
