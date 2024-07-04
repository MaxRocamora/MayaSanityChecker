# ----------------------------------------------------------------------------------------
# check for attribute alphaisluminance set to 1 on filenodes
# ----------------------------------------------------------------------------------------
import maya.cmds as cmds

from sanityChecker.libs.check import Check
from sanityChecker.libs.enums import CategoryGroups, SeverityLevels
from sanityChecker.resources.logger import sanity_stream_logger

log = sanity_stream_logger('SanityChecker')


ALPHA_LUMINANCE_ATTRIBUTE = 'alphaIsLuminance'
COLORSPACE_ATTRIBUTE = 'colorSpace'

VALUES = {'Utility - Raw': 1, 'Utility - sRGB - Texture': 1, 'acescg': 0}

name = 'Alpha Luminance Attribute'
group = CategoryGroups.MAPS
description = f'Incorrect filenode {ALPHA_LUMINANCE_ATTRIBUTE} attribute.'
level = SeverityLevels.HIGH
autofix = True
hint = 'FileNodes must have alphaIsLuminance set to their respective colorspace value'


class Check(Check):
    def __init__(self):  # noqa: D107
        super().__init__(name, group, description, level, autofix, hint)

    def run(self):
        """Performs scan of this check on maya scene/nodes."""
        self.reset()

        for node in cmds.ls(type='file', long=True):
            colorspace = cmds.getAttr(f'{node}.{COLORSPACE_ATTRIBUTE}')
            alpha_luminance_value = cmds.getAttr(f'{node}.{ALPHA_LUMINANCE_ATTRIBUTE}')

            # skip non valid colorspaces
            if colorspace not in VALUES:
                continue

            if alpha_luminance_value != VALUES[colorspace]:
                self.add_failed_node(node)

    def fix(self):
        """Perform technical fix on this check."""
        for node in self.nodes():
            colorspace = cmds.getAttr(f'{node}.{COLORSPACE_ATTRIBUTE}')
            cmds.setAttr(f'{node}.{ALPHA_LUMINANCE_ATTRIBUTE}', VALUES[colorspace])
