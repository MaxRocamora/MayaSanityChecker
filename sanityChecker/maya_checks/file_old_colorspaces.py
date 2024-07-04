# ----------------------------------------------------------------------------------------
# check for old pre ACES colorspaces on colorspace attribute
# the fix converts the old value to the equivalent new one
# ----------------------------------------------------------------------------------------
import maya.cmds as cmds

from sanityChecker.libs.check import Check
from sanityChecker.libs.enums import CategoryGroups, SeverityLevels
from sanityChecker.resources.logger import sanity_stream_logger

log = sanity_stream_logger('SanityChecker')

COLORSPACES = {
    'raw': 'Utility - Raw',
    'out_srgb': 'Utility - sRGB - Texture',
    'srgb_texture': 'Utility - sRGB - Texture',
    'Output - sRGB': 'Utility - sRGB - Texture',
}

ATTRIBUTE = 'colorSpace'

name = 'Texture File with old colorspace'
group = CategoryGroups.MAPS
description = 'Old colorspace found in file node.'
level = SeverityLevels.CRITICAL
autofix = True
hint = f'FileNodes must have updated colorspace attribute {COLORSPACES}'


class Check(Check):
    def __init__(self):  # noqa: D107
        super().__init__(name, group, description, level, autofix, hint)

    def run(self):
        """Performs scan of this check on maya scene/nodes."""
        self.reset()

        for node in cmds.ls(type='file', long=True):
            if cmds.getAttr(f'{node}.{ATTRIBUTE}') in COLORSPACES.keys():
                self.add_failed_node(node)

    def fix(self):
        """Perform technical fix on this check."""
        for node in self.nodes():
            attr_name = cmds.getAttr(f'{node}.{ATTRIBUTE}')
            cmds.setAttr(f'{node}.{ATTRIBUTE}', COLORSPACES[attr_name], type='string')
