# ----------------------------------------------------------------------------------------
# check for unconnected nodes in scene
# ----------------------------------------------------------------------------------------
import maya.cmds as cmds

from sanityChecker.libs.check import Check
from sanityChecker.libs.enums import CategoryGroups, SeverityLevels
from sanityChecker.resources.logger import sanity_stream_logger

log = sanity_stream_logger('SanityChecker')

NODES = ['animCurveTU', 'animCurveTA', 'animCurveTL', 'renderSetupLayer']

name = 'Unconnected Nodes'
group = CategoryGroups.NODES
description = 'Unconnected Nodes in the scene'
level = SeverityLevels.HIGH
autofix = True
hint = 'Remove the orphan nodes'


class Check(Check):
    def __init__(self):  # noqa: D107
        super().__init__(name, group, description, level, autofix, hint)

    def run(self):
        """Performs scan of this check on maya scene/nodes."""
        self.reset()

        for node in self.get_unconnected_nodes():
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

    def get_unconnected_nodes(self):
        """Collect nodes to scan from maya scene."""
        nodes = [cmds.ls(type=name) for name in NODES]
        nodes = [item for sublist in nodes for item in sublist]
        nodes = [n for n in nodes if cmds.listConnections(n) is None]
        return nodes
