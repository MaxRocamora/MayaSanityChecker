# ----------------------------------------------------------------------------------------
# check for missing tx files from files on file node
# ----------------------------------------------------------------------------------------
import os
import maya.cmds as cmds

from sanityChecker.libs.check import Check
from sanityChecker.libs.enums import CategoryGroups, SeverityLevels
from sanityChecker.resources.logger import sanity_stream_logger

log = sanity_stream_logger('SanityChecker')

name = 'Missing TX Filemaps'
group = CategoryGroups.MAPS
description = 'TX version of filemaps are missing.'
level = SeverityLevels.CRITICAL
autofix = False
hint = 'Generate your missing tx files'


class Check(Check):
    def __init__(self):  # noqa: D107
        super().__init__(name, group, description, level, autofix, hint)

    def run(self):
        """Performs scan of this check on maya scene/nodes."""
        self.reset()

        for node in self.get_non_tx_filenodes():
            filename = cmds.getAttr(f'{node}.fileTextureName')
            filepath_no_extension = os.path.splitext(filename)[0]
            tx_filename = f'{filepath_no_extension}.tx'

            if not os.path.exists(tx_filename):
                self.add_failed_node(node)

    def get_non_tx_filenodes(self) -> list:
        """Collect nodes to scan from maya scene."""
        _non_tx_filenodes = []

        for n in cmds.ls(type='file', long=True):
            filename = cmds.getAttr(f'{n}.fileTextureName')
            if os.path.splitext(filename)[1] != '.tx':
                _non_tx_filenodes.append(n)

        return _non_tx_filenodes
