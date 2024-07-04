# ----------------------------------------------------------------------------------------
# check for geometry without shading group
# ----------------------------------------------------------------------------------------
import maya.cmds as cmds

from sanityChecker.libs.check import Check
from sanityChecker.maya.helpers import get_scene_mesh_transform_nodes
from sanityChecker.libs.enums import CategoryGroups, SeverityLevels
from sanityChecker.resources.logger import sanity_stream_logger

log = sanity_stream_logger('SanityChecker')

name = 'No Shading Group on mesh'
group = CategoryGroups.MESHES
description = 'Mesh without shading group'
level = SeverityLevels.CRITICAL
autofix = False
hint = 'Assign a shading group to the mesh'


class Check(Check):
    def __init__(self):  # noqa: D107
        super().__init__(name, group, description, level, autofix, hint)

    def run(self):
        """Performs scan of this check on maya scene/nodes.."""
        self.reset()

        for node in self.get_no_sg_nodes():
            self.add_failed_node(node)

    def get_no_sg_nodes(self) -> list:
        """Returns list of meshes without shading group."""
        nodes = []
        for mesh in get_scene_mesh_transform_nodes():
            shape = self.get_shape_name(mesh)
            sg = self.get_shader_connection(shape)
            if not sg:
                nodes.append(mesh)

        return nodes

    def get_shader_connection(self, mesh: str) -> list:
        """Returns shading group connections of given mesh."""
        return cmds.listConnections(mesh, type='shadingEngine')

    def get_shape_name(self, mesh: str) -> str:
        """Returns shape of given mesh transform."""
        try:
            return cmds.listRelatives(mesh, pa=True, type='shape')[0]
        except ValueError:
            return f'{mesh}Shape'
