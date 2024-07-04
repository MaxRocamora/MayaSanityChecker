# ----------------------------------------------------------------------------------------
# check for maya duplicate names on transform nodes
# ----------------------------------------------------------------------------------------
import maya.cmds as cmds

from sanityChecker.libs.check import Check
from sanityChecker.maya.helpers import get_scene_mesh_transform_nodes
from sanityChecker.libs.enums import CategoryGroups, SeverityLevels
from sanityChecker.resources.logger import sanity_stream_logger

log = sanity_stream_logger('SanityChecker')

name = 'Duplicate Names'
group = CategoryGroups.NAMING
description = 'Duplicate Meshes Names in scene'
level = SeverityLevels.HIGH
autofix = False
hint = 'Rename your meshes with different names'


class Check(Check):
    def __init__(self):  # noqa: D107
        super().__init__(name, group, description, level, autofix, hint)

    def run(self):
        """Performs scan of this check on maya scene/nodes."""

        self.reset()

        for node in get_scene_mesh_transform_nodes():
            if '|' in node:
                self.add_failed_node(node)
