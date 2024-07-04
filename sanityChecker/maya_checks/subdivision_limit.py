# ----------------------------------------------------------------------------------------
# check for geometry max arnold subdivision
# ----------------------------------------------------------------------------------------
import maya.cmds as cmds

from sanityChecker.libs.check import Check
from sanityChecker.maya.helpers import get_scene_mesh_transform_nodes
from sanityChecker.libs.enums import CategoryGroups, SeverityLevels
from sanityChecker.resources.logger import sanity_stream_logger

log = sanity_stream_logger('SanityChecker')

LIMIT = 3
name = f'Arnold Max Subdivisions Iterations'
group = CategoryGroups.MESHES
description = f'Shape exceeds the recommended subdivision limit of {LIMIT}'
level = SeverityLevels.MODERATE
autofix = False
hint = f'Set the arnold subdivisions on shapes less than the limit of {LIMIT}.'


class Check(Check):
    def __init__(self):  # noqa: D107
        super().__init__(name, group, description, level, autofix, hint)

    def run(self):
        """Performs scan of this check on maya scene/nodes."""
        self.reset()

        for node in get_scene_mesh_transform_nodes():
            try:
                cmds.getAttr(f'{node}.aiSubdivType') > 0
            except ValueError:
                continue

            if cmds.getAttr(f'{node}.aiSubdivIterations') > LIMIT:
                self.add_failed_node(node)
