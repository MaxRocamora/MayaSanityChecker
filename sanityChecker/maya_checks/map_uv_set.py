# ----------------------------------------------------------------------------------------
# check for uvmap1 nodes in meshes
# ----------------------------------------------------------------------------------------
import maya.cmds as cmds

from sanityChecker.libs.check import Check
from sanityChecker.libs.enums import CategoryGroups, SeverityLevels
from sanityChecker.resources.logger import sanity_stream_logger

log = sanity_stream_logger('SanityChecker')

name = 'Mesh missing map1 UVSet'
group = CategoryGroups.MESHES
description = 'Mesh Missing Map1 UVSet'
level = SeverityLevels.CRITICAL
autofix = False
hint = 'Make the default uvset on your meshes to map1'


class Check(Check):
    def __init__(self):  # noqa: D107
        super().__init__(name, group, description, level, autofix, hint)

    def run(self):
        """Performs scan of this check on maya scene/nodes."""

        self.reset()

        for node in cmds.ls(type='mesh'):
            uvsets = cmds.polyUVSet(node, query=True, allUVSets=True)

            if 'map1' not in uvsets:
                self.add_failed_node(node)
