# ----------------------------------------------------------------------------------------
# check for missing files on file node
# ----------------------------------------------------------------------------------------
import os
import maya.cmds as cmds

from sanityChecker.libs.check import Check
from sanityChecker.libs.enums import CategoryGroups, SeverityLevels
from sanityChecker.resources.logger import sanity_stream_logger

log = sanity_stream_logger('SanityChecker')

name = 'Missing Filemaps'
group = CategoryGroups.MAPS
description = 'Filemaps from scene are missing on disk.'
level = SeverityLevels.CRITICAL
autofix = False
hint = 'Set your missing filemaps to the proper path.'


class Check(Check):
    def __init__(self):  # noqa: D107
        super().__init__(name, group, description, level, autofix, hint)

    def run(self):
        """Performs scan of this check on maya scene/nodes."""
        self.reset()

        for node in cmds.ls(type='file', long=True):
            if not os.path.exists(cmds.getAttr(f'{node}.fileTextureName')):
                self.add_failed_node(node)
