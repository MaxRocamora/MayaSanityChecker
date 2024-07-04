# ----------------------------------------------------------------------------------------
# check for maya empty uv sets on geos
# ----------------------------------------------------------------------------------------
import maya.cmds as cmds

from sanityChecker.libs.check import Check
from sanityChecker.maya.helpers import get_scene_mesh_transform_nodes
from sanityChecker.libs.enums import CategoryGroups, SeverityLevels
from sanityChecker.resources.logger import sanity_stream_logger

log = sanity_stream_logger('SanityChecker')

name = 'Empty UVSet on Mesh'
group = CategoryGroups.MESHES
description = 'Mesh with no UVSet'
level = SeverityLevels.HIGH
autofix = False
hint = 'Create an uv set into you mesh'


class Check(Check):
    def __init__(self):  # noqa: D107
        super().__init__(name, group, description, level, autofix, hint)

    def run(self):
        """Performs scan of this check on maya scene/nodes."""
        self.reset()

        for node in get_scene_mesh_transform_nodes():
            obj_uv_sets = cmds.polyUVSet(node, query=True, allUVSets=True)

            if obj_uv_sets is None:
                continue

            for uvset in obj_uv_sets:
                if cmds.polyEvaluate(node, uvcoord=True, uvSetName=uvset) == 0:
                    self.add_failed_node(node)
