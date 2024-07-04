# ----------------------------------------------------------------------------------------
# checks for animation curves
# ----------------------------------------------------------------------------------------
import maya.cmds as cmds

from sanityChecker.libs.check import Check
from sanityChecker.maya.helpers import get_scene_mesh_transform_nodes
from sanityChecker.libs.enums import CategoryGroups, SeverityLevels
from sanityChecker.resources.logger import sanity_stream_logger

log = sanity_stream_logger('SanityChecker')

name = 'Animation Curves on meshes'
group = CategoryGroups.MESHES
description = 'Animation Curves on nodes'
level = SeverityLevels.CRITICAL
autofix = False
hint = 'Remove animation curves from the meshes by using break connection on the control'


class Check(Check):
    def __init__(self):  # noqa: D107
        super().__init__(name, group, description, level, autofix, hint)

    def run(self):
        """Performs scan of this check on maya scene/nodes."""
        self.reset()

        # Get meshes with keyframes
        for node in get_scene_mesh_transform_nodes():
            if cmds.nodeType(node) != 'transform':
                continue

            if cmds.keyframe(node, time=(':',), query=True, keyframeCount=True):
                self.add_failed_node(node)
