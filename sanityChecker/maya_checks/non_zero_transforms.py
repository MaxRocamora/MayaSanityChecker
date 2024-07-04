# ----------------------------------------------------------------------------------------
# check for non zero transforms
# skips namespaces nodes
# ----------------------------------------------------------------------------------------
import maya.cmds as cmds

from sanityChecker.libs.check import Check
from sanityChecker.maya.helpers import get_scene_mesh_transform_nodes
from sanityChecker.libs.enums import CategoryGroups, SeverityLevels
from sanityChecker.resources.logger import sanity_stream_logger

log = sanity_stream_logger('SanityChecker')

name = 'Non Zero Transforms'
group = CategoryGroups.MESHES
description = 'Meshes has non-zeo transformations'
level = SeverityLevels.HIGH
autofix = False
hint = 'Freeze your mesh transformations'


class Check(Check):
    def __init__(self):  # noqa: D107
        super().__init__(name, group, description, level, autofix, hint)

    def run(self):
        """Performs scan of this check on maya scene/nodes."""
        self.reset()

        for node in get_scene_mesh_transform_nodes():
            t = list(cmds.xform(node, query=True, translation=True, worldSpace=True))
            r = list(cmds.xform(node, query=True, rotation=True, worldSpace=True))
            s = list(cmds.xform(node, query=True, scale=True, worldSpace=True))

            if any(i != 0 for i in t) or any(i != 0 for i in r) or any(i != 1 for i in s):
                self.add_failed_node(node)
