# ----------------------------------------------------------------------------------------
# check for maya viewport display layers
# ----------------------------------------------------------------------------------------
import maya.cmds as cmds

from sanityChecker.libs.check import Check
from sanityChecker.libs.enums import CategoryGroups, SeverityLevels
from sanityChecker.resources.logger import sanity_stream_logger

log = sanity_stream_logger('SanityChecker')

name = 'DisplayLayers'
group = CategoryGroups.SCENE
description = 'Delete all display layers before publishing.'
level = SeverityLevels.LOW
autofix = True
hint = """Right Click on the display layer and click 'Delete Layer' """


class Check(Check):
    def __init__(self):  # noqa: D107
        super().__init__(name, group, description, level, autofix, hint)

    def run(self):
        """Performs scan of this check on maya scene/nodes."""
        self.reset()

        for node in self.get_display_layers():
            self.add_failed_node(node)

    def fix(self):
        """Perform technical fix on this check."""
        for node in self.nodes():
            if cmds.nodeType(node) == 'displayLayer':
                cmds.delete(node)

    def get_display_layers(self):
        """Collect nodes to scan from maya scene."""
        return [
            n
            for n in cmds.ls(type='displayLayer')
            if n != 'defaultLayer' and ':' not in n
        ]
