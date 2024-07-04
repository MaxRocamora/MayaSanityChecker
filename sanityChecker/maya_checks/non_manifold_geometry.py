# ----------------------------------------------------------------------------------------
# check for manifold geometry
# ----------------------------------------------------------------------------------------
import maya.cmds as cmds

from sanityChecker.libs.check import Check
from sanityChecker.maya.helpers import get_scene_mesh_transform_nodes
from sanityChecker.libs.enums import CategoryGroups, SeverityLevels
from sanityChecker.resources.logger import sanity_stream_logger

log = sanity_stream_logger('SanityChecker')

name = 'Non Manifold Geometry'
group = CategoryGroups.MESHES
description = 'NonManifold geometry found in mesh'
level = SeverityLevels.MODERATE
autofix = False
hint = 'Rework your model topology to avoid polygons with 5 or more sides'


class Check(Check):
    def __init__(self):  # noqa: D107
        super().__init__(name, group, description, level, autofix, hint)

    def run(self):
        """Performs scan of this check on maya scene/nodes."""
        self.reset()

        for node in get_scene_mesh_transform_nodes(True):
            edges = cmds.polyInfo(node, nonManifoldEdges=True)
            vertex = cmds.polyInfo(node, nonManifoldVertices=True)

            if edges or vertex:
                self.add_failed_node(node)
