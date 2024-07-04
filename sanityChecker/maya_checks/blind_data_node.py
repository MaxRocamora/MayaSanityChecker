# ----------------------------------------------------------------------------------------
# check for maya blind data nodes
# ----------------------------------------------------------------------------------------
import maya.cmds as cmds

from sanityChecker.libs.check import Check
from sanityChecker.libs.enums import CategoryGroups, SeverityLevels
from sanityChecker.resources.logger import sanity_stream_logger

log = sanity_stream_logger('SanityChecker')

name = 'blindDataTemplate Node'
group = CategoryGroups.NODES
description = 'blindDataTemplate nodes found on scene'
level = SeverityLevels.LOW
autofix = True
hint = 'Remove any blindDataTemplate node found in scene.'


class Check(Check):
    def __init__(self):  # noqa: D107
        super().__init__(name, group, description, level, autofix, hint)

    def run(self):
        """Performs scan of this check on maya scene/nodes."""
        self.reset()

        for node in cmds.ls(type='blindDataTemplate'):
            self.add_failed_node(node)

    def fix(self):
        """Perform technical fix on this check."""
        for node in self.nodes():
            cmds.delete(node)
