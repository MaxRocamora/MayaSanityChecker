# ----------------------------------------------------------------------------------------
# check for aiAutoTx attribute set to 0 on filenodes
# ----------------------------------------------------------------------------------------
import maya.cmds as cmds

from sanityChecker.libs.check import Check
from sanityChecker.libs.enums import CategoryGroups, SeverityLevels
from sanityChecker.resources.logger import sanity_stream_logger

log = sanity_stream_logger('SanityChecker')

ATTRIBUTE = 'aiAutoTx'
VALUE = 0

name = 'Auto Generate Tx Attribute'
group = CategoryGroups.MAPS
description = f'Filenode {ATTRIBUTE} attribute set wrong.'
level = SeverityLevels.HIGH
autofix = True
hint = f'FileNodes must have {ATTRIBUTE} set to {VALUE}'


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
