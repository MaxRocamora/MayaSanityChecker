# ----------------------------------------------------------------------------------------
# check for valid ACES colorspaces into colorspace attribute for filenodes
# ----------------------------------------------------------------------------------------
import maya.cmds as cmds

from sanityChecker.libs.check import Check
from sanityChecker.libs.enums import CategoryGroups, SeverityLevels
from sanityChecker.resources.logger import sanity_stream_logger

log = sanity_stream_logger('SanityChecker')

COLORSPACES = ['Utility - Raw', 'Utility - sRGB - Texture', 'acescg']
ATTRIBUTE = 'colorSpace'

name = 'Files Colorspaces'
group = CategoryGroups.MAPS
description = 'Incorrect Colorspace on file nodes.'
level = SeverityLevels.CRITICAL
autofix = False
hint = (
    f'FileNodes colorspace ({ATTRIBUTE}) must set to one of the following {COLORSPACES}'
)


class Check(Check):
    def __init__(self):  # noqa: D107
        super().__init__(name, group, description, level, autofix, hint)

    def run(self):
        """Performs scan of this check on maya scene/nodes."""
        self.reset()

        for node in cmds.ls(type='file', long=True):
            if cmds.getAttr(f'{node}.{ATTRIBUTE}') not in COLORSPACES:
                self.add_failed_node(node)
