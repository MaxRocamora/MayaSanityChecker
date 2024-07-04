# ----------------------------------------------------------------------------------------
# check for atmosphere nodes in scene
# ----------------------------------------------------------------------------------------
import maya.cmds as cmds

from sanityChecker.libs.check import Check
from sanityChecker.libs.enums import CategoryGroups, SeverityLevels
from sanityChecker.resources.logger import sanity_stream_logger

log = sanity_stream_logger('SanityChecker')

atmosphere_nodes = ['aiAtmosphereVolume', 'aiFog']

name = 'Atmosphere Nodes'
group = CategoryGroups.SCENE
description = 'Atmosphere Nodes in the scene'
level = SeverityLevels.MODERATE
autofix = True
hint = 'Remove the Atmosphere nodes'


class Check(Check):
    def __init__(self):  # noqa: D107
        super().__init__(name, group, description, level, autofix, hint)

    def run(self):
        """Performs scan of this check on maya scene/nodes."""
        self.reset()

        for node in self.collect_nodes():
            self.add_failed_node(node)

    def fix(self):
        """Perform technical fix on this check."""
        for node in self.collect_nodes():
            cmds.delete(node)

    def collect_nodes(self):
        """Collect nodes to scan from maya scene."""
        nodes = [cmds.ls(type=name) for name in atmosphere_nodes]
        return [item for sublist in nodes for item in sublist]
