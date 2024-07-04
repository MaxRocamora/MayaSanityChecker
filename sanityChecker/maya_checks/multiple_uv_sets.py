# ----------------------------------------------------------------------------------------
# check for multiple uv sets on meshes
# ----------------------------------------------------------------------------------------
import maya.cmds as cmds

from sanityChecker.libs.check import Check
from sanityChecker.maya.helpers import get_scene_mesh_transform_nodes
from sanityChecker.libs.enums import CategoryGroups, SeverityLevels
from sanityChecker.resources.logger import sanity_stream_logger

log = sanity_stream_logger('SanityChecker')

name = 'Multiple UV Sets on meshes'
group = CategoryGroups.MESHES
description = 'Mesh with more than one uv set'
level = SeverityLevels.HIGH
autofix = False
hint = 'Remove exceeding uvsets in your meshes'


class Check(Check):
    def __init__(self):  # noqa: D107
        super().__init__(name, group, description, level, autofix, hint)

    def run(self):
        """Performs scan of this check on maya scene/nodes."""
        self.reset()

        for node in get_scene_mesh_transform_nodes(True):
            if len(cmds.polyUVSet(node, query=True, allUVSets=True)) > 1:
                self.add_failed_node(node)
