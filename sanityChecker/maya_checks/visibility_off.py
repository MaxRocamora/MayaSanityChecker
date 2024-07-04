# ----------------------------------------------------------------------------------------
# check for transforms with visibility off
# ----------------------------------------------------------------------------------------
import maya.cmds as cmds

from sanityChecker.libs.check import Check
from sanityChecker.libs.enums import CategoryGroups, SeverityLevels
from sanityChecker.maya.helpers import get_scene_mesh_transform_nodes
from sanityChecker.resources.logger import sanity_stream_logger

log = sanity_stream_logger('SanityChecker')

name = 'Visibility Off'
group = CategoryGroups.MESHES
description = 'Hidden Meshes'
level = SeverityLevels.LOW
autofix = True
hint = 'Set visible on hidden meshes'


class Check(Check):
    def __init__(self):  # noqa: D107
        super().__init__(name, group, description, level, autofix, hint)

    def run(self):
        """Performs scan of this check on maya scene/nodes."""
        self.reset()

        for node in get_scene_mesh_transform_nodes():
            if cmds.getAttr(f'{node}.visibility') is False:
                self.add_failed_node(node)

    def fix(self):
        """Perform technical fix on this check."""
        for node in self.nodes:
            cmds.setAttr(f'{node}.visibility', 1)
