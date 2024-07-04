# ----------------------------------------------------------------------------------------
# check for meshes lamina faces
# ----------------------------------------------------------------------------------------
import maya.cmds as cmds

from sanityChecker.libs.check import Check
from sanityChecker.maya.helpers import get_scene_mesh_transform_nodes
from sanityChecker.libs.enums import CategoryGroups, SeverityLevels
from sanityChecker.resources.logger import sanity_stream_logger

log = sanity_stream_logger('SanityChecker')


name = 'LaminaFaces'
group = CategoryGroups.MESHES
description = 'LaminaFaces found in mesh geometry'
level = SeverityLevels.HIGH
autofix = False
hint = 'Use mesh cleanup to fix lamina faces'


class Check(Check):
    def __init__(self):  # noqa: D107
        super().__init__(name, group, description, level, autofix, hint)

    def run(self):
        """Performs scan of this check on maya scene/nodes."""
        self.reset()

        for node in get_scene_mesh_transform_nodes():
            lamina = cmds.polyInfo(node, laminaFaces=True)

            if lamina is not None and len(lamina) >= 1:
                self.add_failed_node(node)
