# ----------------------------------------------------------------------------------------
# Checks for HDRI files in > utility linear
# This check is only for lighting
# HDRI files must have the hdri token on their filename and have hdri extension.
# Studio_HDRI.hdri, Beach_HDRI.tx
# ----------------------------------------------------------------------------------------
import os
import maya.cmds as cmds

from sanityChecker.libs.check import Check
from sanityChecker.libs.enums import CategoryGroups, SeverityLevels
from sanityChecker.resources.logger import sanity_stream_logger

log = sanity_stream_logger('SanityChecker')


ATTRIBUTE = 'colorSpace'
VALUE = 'Utility - Linear - sRGB'
TOKEN = 'hdri'
EXTENSIONS = ['.hdri', '.tx']

name = 'HDRI ColorSpace'
group = CategoryGroups.MAPS
description = 'HDRI Filenodes incorrect colorspace.'
level = SeverityLevels.CRITICAL
autofix = True
hint = f'Set correct colorspace for HDRI Filenodes: {VALUE}'


class Check(Check):
    def __init__(self):  # noqa: D107
        super().__init__(name, group, description, level, autofix, hint)

    def run(self):
        """Performs scan of this check on maya scene/nodes."""
        self.reset()

        for node in self.get_hdri_nodes():
            if cmds.getAttr(f'{node}.{ATTRIBUTE}') != VALUE:
                self.add_failed_node(node)

    def fix(self):
        """Perform technical fix on this check."""
        for node in self.nodes():
            cmds.setAttr(f'{node}.{ATTRIBUTE}', VALUE, type='string')

    def get_hdri_nodes(self):
        """Collect file nodes with hdri extension only."""
        collection = []

        nodes = cmds.ls(type='file', long=True)
        for n in nodes:
            filepath = cmds.getAttr(f'{n}.fileTextureName')
            head, tail = os.path.splitext(filepath)

            if tail in EXTENSIONS and TOKEN in head:
                collection.append(n)

        return collection
