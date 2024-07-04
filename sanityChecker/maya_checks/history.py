# ----------------------------------------------------------------------------------------
# check for maya node history on meshes
# ----------------------------------------------------------------------------------------
import maya.cmds as cmds

from sanityChecker.libs.check import Check
from sanityChecker.maya.helpers import get_scene_mesh_transform_nodes
from sanityChecker.libs.enums import CategoryGroups, SeverityLevels
from sanityChecker.resources.logger import sanity_stream_logger

log = sanity_stream_logger('SanityChecker')

name = 'History on Mesh'
group = CategoryGroups.MESHES
description = 'Mesh with history nodes'
level = SeverityLevels.HIGH
autofix = True
hint = 'Delete the history of your meshes'


class Check(Check):
    def __init__(self):  # noqa: D107
        super().__init__(name, group, description, level, autofix, hint)

    def run(self):
        """Performs scan of this check on maya scene/nodes."""

        self.reset()

        for node in get_scene_mesh_transform_nodes():
            obj_history = cmds.listHistory(node)

            if obj_history is not None and len(obj_history) > 1:
                self.add_failed_node(node)

    def fix(self):
        """Perform technical fix on this check."""
        for node in self.nodes():
            cmds.delete(node, constructionHistory=True)
