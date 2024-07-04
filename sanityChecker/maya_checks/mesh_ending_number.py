# ----------------------------------------------------------------------------------------
# check for meshes ending with numbers
# ----------------------------------------------------------------------------------------
import contextlib
import maya.cmds as cmds

from sanityChecker.libs.check import Check
from sanityChecker.maya.helpers import get_scene_mesh_transform_nodes
from sanityChecker.libs.enums import CategoryGroups, SeverityLevels
from sanityChecker.resources.logger import sanity_stream_logger

log = sanity_stream_logger('SanityChecker')

name = 'Meshes Names ending with numbers'
group = CategoryGroups.NAMING
description = 'Mesh name ends with a number'
level = SeverityLevels.HIGH
autofix = False
hint = 'Rename your mesh without the numbers and the end, use a proper naming convention for your meshes.'


class Check(Check):
    def __init__(self):  # noqa: D107
        super().__init__(name, group, description, level, autofix, hint)

    def run(self):
        """Performs scan of this check on maya scene/nodes."""

        self.reset()

        for node in cmds.ls(type='mesh'):
            with contextlib.suppress(ValueError, IndexError):
                transform = cmds.listRelatives(node, p=1)[0]
                int(transform[-1])

                self.add_failed_node(node)
