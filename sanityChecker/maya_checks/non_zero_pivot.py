# ----------------------------------------------------------------------------------------
# check for non zero pivot on meshes
# skips namespaces nodes
# ----------------------------------------------------------------------------------------
import maya.cmds as cmds

from sanityChecker.libs.check import Check
from sanityChecker.maya.helpers import get_scene_mesh_transform_nodes
from sanityChecker.libs.enums import CategoryGroups, SeverityLevels
from sanityChecker.resources.logger import sanity_stream_logger

log = sanity_stream_logger('SanityChecker')

name = 'Non Zero Pivot on Mesh'
group = CategoryGroups.MESHES
description = 'Mesh with Non Zero Pivot Coordinate'
level = SeverityLevels.LOW
autofix = False
hint = 'Set your mesh pivot to 0'


class Check(Check):
    def __init__(self):  # noqa: D107
        super().__init__(name, group, description, level, autofix, hint)

    def run(self):
        """Performs scan of this check on maya scene/nodes."""
        self.reset()

        for node in get_scene_mesh_transform_nodes():
            pivots = cmds.xform(node, pivots=True, query=True, ws=True)
            for p in pivots:
                if p != 0.0:
                    self.add_failed_node(node)
                    continue
