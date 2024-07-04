# ----------------------------------------------------------------------------------------
# check for maya visible views
# ----------------------------------------------------------------------------------------
import maya.cmds as cmds

from sanityChecker.libs.check import Check
from sanityChecker.libs.enums import CategoryGroups, SeverityLevels
from sanityChecker.resources.logger import sanity_stream_logger

log = sanity_stream_logger('SanityChecker')

name = 'Visible View Nodes on scene'
group = CategoryGroups.SCENE
description = 'Default Camera View node is visible.'
level = SeverityLevels.LOW
autofix = True
hint = 'Hide your maya default camera views'


class Check(Check):
    def __init__(self):  # noqa: D107
        super().__init__(name, group, description, level, autofix, hint)

    def run(self):
        """Performs scan of this check on maya scene/nodes."""
        self.reset()

        for node in self.get_view_cameras():
            if cmds.getAttr(f'{node}.visibility'):
                self.add_failed_node(node)

    def fix(self):
        """Perform technical fix on this check."""
        for node in self.nodes():
            cmds.setAttr(f'{node}.visibility', 0)

    def get_view_cameras(self):
        """Collect nodes to scan from maya scene."""
        return [
            cam
            for cam in cmds.listRelatives(cmds.ls(cameras=1), parent=1)
            if cam in ['front', 'persp', 'side', 'top']
        ]
