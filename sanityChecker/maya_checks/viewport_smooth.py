# ----------------------------------------------------------------------------------------
# check for maya viewport subdivision enabled
# ----------------------------------------------------------------------------------------
import maya.cmds as cmds

from sanityChecker.libs.check import Check
from sanityChecker.maya.helpers import get_scene_mesh_transform_nodes
from sanityChecker.libs.enums import CategoryGroups, SeverityLevels
from sanityChecker.resources.logger import sanity_stream_logger

log = sanity_stream_logger('SanityChecker')

name = 'Display Smoothness Enabled'
group = CategoryGroups.MESHES
description = 'Mesh with maya Viewport smooth (3) enabled'
level = SeverityLevels.CRITICAL
autofix = True
hint = 'Select your meshes and press (1) on you keyboard'


class Check(Check):
    def __init__(self):  # noqa: D107
        super().__init__(name, group, description, level, autofix, hint)

    def run(self):
        """Performs scan of this check on maya scene/nodes."""
        self.reset()

        for node in get_scene_mesh_transform_nodes():
            if cmds.nodeType(node) == 'transform':
                smooth = cmds.displaySmoothness(node, q=True, polygonObject=True)[0]

                if int(smooth) == 3:
                    self.add_failed_node(node)

    def fix(self):
        """Perform technical fix on this check."""
        for key in self.nodes():
            cmds.select(self.flag_nodes[key][3], r=True)
            cmds.displaySmoothness(du=0, dv=0, pw=4, ps=1, polygonObject=1)
