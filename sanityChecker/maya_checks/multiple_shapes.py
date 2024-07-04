# ----------------------------------------------------------------------------------------
# check for multiple shapes on meshes
# ----------------------------------------------------------------------------------------
import maya.cmds as cmds

from sanityChecker.libs.check import Check
from sanityChecker.maya.helpers import get_scene_mesh_transform_nodes
from sanityChecker.libs.enums import CategoryGroups, SeverityLevels
from sanityChecker.resources.logger import sanity_stream_logger

log = sanity_stream_logger('SanityChecker')

name = 'Multiple Shapes on the same Transform Node'
group = CategoryGroups.MESHES
description = 'Transform has more than one shape connected'
level = SeverityLevels.CRITICAL
autofix = False
hint = 'Remove exceeding shapes in your transforms'


class Check(Check):
    def __init__(self):  # noqa: D107
        super().__init__(name, group, description, level, autofix, hint)

    def run(self):
        """Performs scan of this check on maya scene/nodes."""
        self.reset()

        for node in get_scene_mesh_transform_nodes():
            shapes = cmds.listRelatives(node, shapes=True, fullPath=True)
            if shapes is not None and len(shapes) > 1:
                self.add_failed_node(node)
