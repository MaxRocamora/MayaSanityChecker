# ----------------------------------------------------------------------------------------
# check for multiple context nodes in scene
# ----------------------------------------------------------------------------------------
import maya.cmds as cmds

from sanityChecker.libs.check import Check
from sanityChecker.libs.enums import CategoryGroups, SeverityLevels
from sanityChecker.resources.logger import sanity_stream_logger

log = sanity_stream_logger('SanityChecker')

name = 'Multiple Arcane ContextNode'
group = CategoryGroups.SCENE
description = 'You have more than one node of "arcane_context"'
level = SeverityLevels.HIGH
autofix = False
hint = 'Delete the additional context_node nodes with a number at the end of the name'


class Check(Check):
    def __init__(self):  # noqa: D107
        super().__init__(name, group, description, level, autofix, hint)

    def run(self):
        """Performs scan of this check on maya scene/nodes."""
        self.reset()

        nodes = cmds.ls(type='objectSet')
        nodes = [n for n in nodes if n.startswith('arcane_context')]
        extra_nodes = [n for n in nodes if n[-1].isdigit()]

        for node in extra_nodes:
            self.add_failed_node(node)
