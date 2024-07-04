# ----------------------------------------------------------------------------------------
# check for maya custom views (left, bottom, etc)
# ----------------------------------------------------------------------------------------
import maya.cmds as cmds

from sanityChecker.libs.check import Check
from sanityChecker.libs.enums import CategoryGroups, SeverityLevels
from sanityChecker.resources.logger import sanity_stream_logger

log = sanity_stream_logger('SanityChecker')

name = 'Custom User View on scene'
group = CategoryGroups.SCENE
description = 'Custom View on scene found.'
level = SeverityLevels.LOW
autofix = True
hint = 'Delete your custom views'


class Check(Check):
    def __init__(self):  # noqa: D107
        super().__init__(name, group, description, level, autofix, hint)

    def run(self):
        """Performs scan of this check on maya scene/nodes."""
        self.reset()

        cam_nodes = cmds.ls(type='camera', shortNames=True)
        cam_nodes = [i for i in cam_nodes if ':' not in i]

        for node in cam_nodes:
            if cmds.camera(node, q=True, startupCamera=True):
                continue

            self.add_failed_node(node)

    def fix(self):
        """Perform technical fix on this check."""
        for node in self.nodes():
            parent_view = cmds.listRelatives(node.name(), p=1)[0]
            if parent_view:
                cmds.delete(parent_view)
