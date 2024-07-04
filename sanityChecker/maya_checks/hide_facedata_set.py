# ----------------------------------------------------------------------------------------
# check for maya defaultHideFaceDataSet node
# ----------------------------------------------------------------------------------------
import maya.cmds as cmds

from sanityChecker.libs.check import Check
from sanityChecker.libs.enums import CategoryGroups, SeverityLevels
from sanityChecker.resources.logger import sanity_stream_logger

log = sanity_stream_logger('SanityChecker')

name = 'Hidden Faces or defaultHideFaceDataSet Node'
group = CategoryGroups.MESHES
description = 'defaultHideFaceDataSet node found on scene'
level = SeverityLevels.CRITICAL
autofix = False
hint = 'Remove any hidden face or remove defaultHideFaceDataSet node.'


class Check(Check):
    def __init__(self):  # noqa: D107
        super().__init__(name, group, description, level, autofix, hint)

    def run(self):
        """Performs scan of this check on maya scene/nodes."""

        self.reset()

        for node in cmds.ls(type='objectSet'):
            if 'defaultHideFaceDataSet' in node:
                self.add_failed_node(node)
