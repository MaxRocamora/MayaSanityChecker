# ----------------------------------------------------------------------------------------
# check for orphan createColorSet nodes in scene
# ----------------------------------------------------------------------------------------
import maya.cmds as cmds

from sanityChecker.libs.check import Check
from sanityChecker.libs.enums import CategoryGroups, SeverityLevels
from sanityChecker.resources.logger import sanity_stream_logger

log = sanity_stream_logger('SanityChecker')

name = 'Unconnected createColorSet Nodes'
group = CategoryGroups.NODES
description = 'Unconnected createColorSet Nodes in the scene'
level = SeverityLevels.MODERATE
autofix = True
hint = 'Remove the unconnected createColorSet nodes'


class Check(Check):
    def __init__(self):  # noqa: D107
        super().__init__(name, group, description, level, autofix, hint)

    def run(self):
        """Performs scan of this check on maya scene/nodes."""
        self.reset()

        for node in self.get_createColorSet_nodes():
            self.add_failed_node(node)

    def fix(self):
        """Perform technical fix on this check."""
        for node in self.nodes():
            try:
                cmds.lockNode(node, l=0)
                cmds.delete(node)
            except RuntimeError as e:
                log.warning(str(e))
            except ValueError:
                pass

    def get_createColorSet_nodes(self) -> list:
        """Collect nodes to scan from maya scene."""
        nodes = []

        for node in cmds.ls(type='createColorSet'):
            # from connected skincluster
            sc_child = cmds.listConnections(node, c=1, t='skinCluster')
            sc_dest = cmds.listConnections(node, d=1, t='skinCluster')

            # connect to a mesh
            mesh_child = cmds.listConnections(node, c=1, t='mesh')
            mesh_dest = cmds.listConnections(node, d=1, t='mesh')

            if not any([sc_child, sc_dest, mesh_dest, mesh_child]):
                nodes.append(node)

        return nodes
