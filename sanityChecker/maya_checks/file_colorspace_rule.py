# ----------------------------------------------------------------------------------------
# check for ignore colorspace attribute on filenodes
# ----------------------------------------------------------------------------------------
import maya.cmds as cmds

from sanityChecker.libs.check import Check
from sanityChecker.libs.enums import CategoryGroups, SeverityLevels
from sanityChecker.resources.logger import sanity_stream_logger

log = sanity_stream_logger('SanityChecker')

ATTRIBUTE = 'ignoreColorSpaceFileRules'
VALUE = 1

name = 'ignoreColorSpaceFileRules Attribute Enabled'
group = CategoryGroups.MAPS
description = f'Filenode {ATTRIBUTE} attribute must be set to {VALUE}'
level = SeverityLevels.HIGH
autofix = True
hint = f'File nodes must have {ATTRIBUTE} set to {VALUE}'


class Check(Check):
    def __init__(self):  # noqa: D107
        super().__init__(name, group, description, level, autofix, hint)

    def run(self):
        """Performs scan of this check on maya scene/nodes."""
        self.reset()

        for node in cmds.ls(type='file', long=True):
            if cmds.getAttr(f'{node}.{ATTRIBUTE}') != VALUE:
                self.add_failed_node(node)

    def fix(self):
        """Perform technical fix on this check."""
        for node in self.nodes():
            cmds.setAttr(f'{node}.{ATTRIBUTE}', VALUE)
