# ----------------------------------------------------------------------------------------
# check for maya unknown nodes
# ----------------------------------------------------------------------------------------
import maya.cmds as cmds

from sanityChecker.libs.check import Check
from sanityChecker.libs.enums import CategoryGroups, SeverityLevels
from sanityChecker.resources.logger import sanity_stream_logger

log = sanity_stream_logger('SanityChecker')

name = 'Unknown Nodes'
group = CategoryGroups.NODES
description = 'Unknown Nodes found in scene'
level = SeverityLevels.CRITICAL
autofix = True
hint = 'Use optimize to remove unknown nodes.'


class Check(Check):
    def __init__(self):  # noqa: D107
        super().__init__(name, group, description, level, autofix, hint)

    def run(self):
        """Performs scan of this check on maya scene/nodes."""
        self.reset()

        for node in cmds.ls(type='unknown'):
            self.add_failed_node(node)

    def fix(self):
        """Perform technical fix on this check."""
        for node in self.nodes():
            try:
                log.info(f'Fixing Unknown Node {node}')
                cmds.lockNode(node, lock=False)
                cmds.delete(node)
            except RuntimeError as e:
                log.error(str(e))
